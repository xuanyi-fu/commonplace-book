#!/usr/bin/env python3
"""Check internal wiki links for one or more markdown pages.

Usage:

    uv run python scripts/check_links.py concepts/agent-harness.md
    uv run python scripts/check_links.py concepts/agent-harness.md syntheses/*.md

The checker validates:

- Obsidian wikilinks and embeds: [[...]] and ![[...]]
- optional aliases: [[target|alias]]
- optional fragments:
  - block ids: [[page#^block-id]]
  - headings: [[page#some-heading]]

It resolves link targets relative to the current page first, then relative to
the repository root. External markdown links (http/https/mailto) are ignored.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WIKILINK_RE = re.compile(r"!?(\[\[([^\]]+)\]\])")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BLOCK_ID_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9][A-Za-z0-9_-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


@dataclass(frozen=True)
class LinkIssue:
    page: str
    line: int
    link_text: str
    issue: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slugify_heading(text: str) -> str:
    lowered = text.strip().lower()
    lowered = re.sub(r"[`*_~[\](){}.!?,:;\"'\\/]+", "", lowered)
    lowered = re.sub(r"\s+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered)
    return lowered.strip("-")


def collect_block_ids(path: Path) -> set[str]:
    block_ids: set[str] = set()
    for line in read_text(path).splitlines():
        match = BLOCK_ID_RE.search(line)
        if match:
            block_ids.add(match.group(1))
    return block_ids


def collect_heading_slugs(path: Path) -> set[str]:
    slugs: set[str] = set()
    for line in read_text(path).splitlines():
        match = HEADING_RE.match(line)
        if match:
            slug = slugify_heading(match.group(2))
            if slug:
                slugs.add(slug)
    return slugs


def parse_wikilink_target(raw_inner: str) -> tuple[str, str | None]:
    target_part = raw_inner.split("|", 1)[0].strip()
    if "#" in target_part:
        path_part, fragment = target_part.split("#", 1)
        return path_part.strip(), fragment.strip() or None
    return target_part.strip(), None


def is_external_markdown_target(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "file://"))


def resolve_target_path(current_page: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target:
        return current_page

    candidates: list[Path] = []
    path_obj = Path(target)
    if path_obj.suffix:
        candidates.extend(
            [
                (current_page.parent / path_obj).resolve(),
                (REPO_ROOT / path_obj).resolve(),
            ]
        )
    else:
        with_md = Path(f"{target}.md")
        candidates.extend(
            [
                (current_page.parent / with_md).resolve(),
                (REPO_ROOT / with_md).resolve(),
                (current_page.parent / path_obj).resolve(),
                (REPO_ROOT / path_obj).resolve(),
            ]
        )

    seen: set[Path] = set()
    deduped: list[Path] = []
    for candidate in candidates:
        if candidate not in seen:
            deduped.append(candidate)
            seen.add(candidate)

    for candidate in deduped:
        try:
            candidate.relative_to(REPO_ROOT)
        except ValueError:
            continue
        if candidate.exists():
            return candidate
    return None


def validate_fragment(target_path: Path, fragment: str | None) -> str | None:
    if not fragment:
        return None
    if fragment.startswith("^"):
        block_id = fragment[1:]
        if block_id not in collect_block_ids(target_path):
            return f"missing block id `^{block_id}` in `{target_path.relative_to(REPO_ROOT)}`"
        return None

    slug = slugify_heading(fragment)
    if slug not in collect_heading_slugs(target_path):
        return f"missing heading anchor `#{fragment}` in `{target_path.relative_to(REPO_ROOT)}`"
    return None


def iter_internal_links(page: Path):
    for line_number, line in enumerate(read_text(page).splitlines(), start=1):
        for match in WIKILINK_RE.finditer(line):
            full_link = match.group(1)
            inner = match.group(2).strip()
            yield line_number, full_link, inner

        for match in MARKDOWN_LINK_RE.finditer(line):
            target = match.group(1).strip().strip("<>")
            if is_external_markdown_target(target):
                continue
            yield line_number, target, target


def check_page(page: Path) -> list[LinkIssue]:
    issues: list[LinkIssue] = []

    for line_number, display_text, raw_target in iter_internal_links(page):
        path_part, fragment = parse_wikilink_target(raw_target)
        target_path = resolve_target_path(page, path_part)
        if target_path is None:
            issues.append(
                LinkIssue(
                    page=str(page.relative_to(REPO_ROOT)),
                    line=line_number,
                    link_text=display_text,
                    issue=f"missing target for `{raw_target}`",
                )
            )
            continue

        fragment_issue = validate_fragment(target_path, fragment)
        if fragment_issue:
            issues.append(
                LinkIssue(
                    page=str(page.relative_to(REPO_ROOT)),
                    line=line_number,
                    link_text=display_text,
                    issue=fragment_issue,
                )
            )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check internal wiki links for one or more markdown pages.")
    parser.add_argument("pages", nargs="+", help="One or more markdown page paths, relative to repo root or absolute.")
    args = parser.parse_args()

    all_issues: list[LinkIssue] = []
    checked_pages = 0

    for raw_page in args.pages:
        page = Path(raw_page)
        if not page.is_absolute():
            page = (REPO_ROOT / page).resolve()
        if not page.exists():
            print(f"ERROR: page does not exist: {raw_page}")
            return 2
        if not page.is_file():
            print(f"ERROR: page is not a file: {raw_page}")
            return 2

        checked_pages += 1
        all_issues.extend(check_page(page))

    if all_issues:
        for issue in all_issues:
            print(f"{issue.page}:{issue.line}: {issue.issue} [{issue.link_text}]")
        print()
        print(f"Checked {checked_pages} page(s). Found {len(all_issues)} link issue(s).")
        return 1

    print(f"Checked {checked_pages} page(s). Found 0 link issues.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
