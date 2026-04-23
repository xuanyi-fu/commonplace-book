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
Only wiki-layer markdown pages are checked:

- index.md
- notes/*.md
- concepts/*.md
- entities/*.md
- summaries/*.md
- syntheses/*.md
- sources/*/summary.md
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCOPED_DIRS = {"summaries", "notes", "entities", "concepts", "syntheses"}
WIKILINK_RE = re.compile(r"!?(\[\[([^\]]+)\]\])")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BLOCK_ID_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9][A-Za-z0-9_-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


@dataclass(frozen=True)
class LinkIssue:
    rule_id: str
    page: str
    line: int
    link_text: str
    rule: str
    found: str
    expected: str
    why_it_matters: str
    next_step: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relpath(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def is_supported_page(path: Path) -> bool:
    try:
        relative = path.relative_to(REPO_ROOT)
    except ValueError:
        return False

    if path.suffix != ".md":
        return False
    if relative == Path("index.md"):
        return True
    if relative.parts and relative.parts[0] in SCOPED_DIRS:
        return True
    return len(relative.parts) == 3 and relative.parts[0] == "sources" and relative.parts[2] == "summary.md"


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


def parse_link_target(raw_inner: str) -> tuple[str, str | None]:
    target_part = raw_inner.split("|", 1)[0].strip()
    if "#" in target_part:
        path_part, fragment = target_part.split("#", 1)
        return path_part.strip(), fragment.strip() or None
    return target_part.strip(), None


def is_external_markdown_target(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith(("http://", "https://", "mailto:", "file://"))


def resolve_exact_or_extensionless(base_candidate: Path) -> Path | None:
    if base_candidate.exists() and base_candidate.is_file():
        return base_candidate

    if not base_candidate.suffix:
        markdown_candidate = base_candidate.with_suffix(".md")
        if markdown_candidate.exists() and markdown_candidate.is_file():
            return markdown_candidate

    matches = sorted(
        candidate
        for candidate in base_candidate.parent.glob(f"{base_candidate.name}.*")
        if candidate.is_file()
    )
    if len(matches) == 1:
        return matches[0]
    return None


def resolve_repo_basename(raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or "/" in target or "\\" in target:
        return None

    exact_markdown = sorted(candidate for candidate in REPO_ROOT.rglob(f"{target}.md") if candidate.is_file())
    if len(exact_markdown) == 1:
        return exact_markdown[0]

    scoped_markdown = [candidate for candidate in exact_markdown if is_supported_page(candidate)]
    if len(scoped_markdown) == 1:
        return scoped_markdown[0]

    exact_any = sorted(candidate for candidate in REPO_ROOT.rglob(f"{target}.*") if candidate.is_file())
    if len(exact_any) == 1:
        return exact_any[0]

    return None


def resolve_target_path(current_page: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target:
        return current_page

    path_obj = Path(target)
    candidates = [
        (current_page.parent / path_obj).resolve(),
        (REPO_ROOT / path_obj).resolve(),
    ]

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            candidate.relative_to(REPO_ROOT)
        except ValueError:
            continue
        resolved = resolve_exact_or_extensionless(candidate)
        if resolved is not None:
            return resolved

    return resolve_repo_basename(target)


def make_missing_target_issue(page: Path, line: int, link_text: str, raw_target: str) -> LinkIssue:
    return LinkIssue(
        rule_id="links.missing_target",
        page=relpath(page),
        line=line,
        link_text=link_text,
        rule="Internal wiki links must resolve to an existing repository file.",
        found=f"Link target `{raw_target}` did not resolve to an existing file.",
        expected="The target page or source artifact must exist and be reachable from the current page.",
        why_it_matters="Broken internal links make the wiki harder to navigate and can break source-backed citations.",
        next_step=f"Create the missing target, or update `{link_text}` so it points to the correct existing file.",
    )


def make_missing_block_issue(page: Path, line: int, link_text: str, target_path: Path, block_id: str) -> LinkIssue:
    return LinkIssue(
        rule_id="links.missing_block_id",
        page=relpath(page),
        line=line,
        link_text=link_text,
        rule="Block-id citations must resolve to a real block id in the target page.",
        found=f"Block id `^{block_id}` was not found in `{relpath(target_path)}`.",
        expected=f"The target page must define block id `^{block_id}`.",
        why_it_matters="Broken block-id citations make precise source-backed claims unverifiable.",
        next_step=f"Add `^{block_id}` to the supporting passage in `{relpath(target_path)}`, or update `{link_text}` to an existing block id.",
    )


def make_missing_heading_issue(page: Path, line: int, link_text: str, target_path: Path, fragment: str) -> LinkIssue:
    return LinkIssue(
        rule_id="links.missing_heading_anchor",
        page=relpath(page),
        line=line,
        link_text=link_text,
        rule="Heading anchors must resolve to an existing heading in the target markdown page.",
        found=f"Heading anchor `#{fragment}` was not found in `{relpath(target_path)}`.",
        expected=f"The target page must contain a heading that slugifies to `#{fragment}`.",
        why_it_matters="Broken heading anchors send readers to the wrong place and weaken reusable citations.",
        next_step=f"Add or rename the target heading in `{relpath(target_path)}`, or update `{link_text}` to an existing heading anchor.",
    )


def validate_fragment(page: Path, line: int, link_text: str, target_path: Path, fragment: str | None) -> LinkIssue | None:
    if not fragment:
        return None

    if fragment.startswith("^"):
        block_id = fragment[1:]
        if block_id not in collect_block_ids(target_path):
            return make_missing_block_issue(page, line, link_text, target_path, block_id)
        return None

    slug = slugify_heading(fragment)
    if slug not in collect_heading_slugs(target_path):
        return make_missing_heading_issue(page, line, link_text, target_path, fragment)
    return None


def iter_internal_links(page: Path):
    for line_number, line in enumerate(read_text(page).splitlines(), start=1):
        for match in WIKILINK_RE.finditer(line):
            yield line_number, match.group(1), match.group(2).strip()

        for match in MARKDOWN_LINK_RE.finditer(line):
            target = match.group(1).strip().strip("<>")
            if is_external_markdown_target(target):
                continue
            yield line_number, target, target


def check_page(page: Path) -> list[LinkIssue]:
    issues: list[LinkIssue] = []

    for line_number, display_text, raw_target in iter_internal_links(page):
        path_part, fragment = parse_link_target(raw_target)
        target_path = resolve_target_path(page, path_part)
        if target_path is None:
            issues.append(make_missing_target_issue(page, line_number, display_text, raw_target))
            continue

        fragment_issue = validate_fragment(page, line_number, display_text, target_path, fragment)
        if fragment_issue is not None:
            issues.append(fragment_issue)

    return issues


def format_issue(issue: LinkIssue) -> str:
    return "\n".join(
        [
            f"ERROR [{issue.rule_id}]",
            f"path: {issue.page}",
            f"line: {issue.line}",
            f"rule: {issue.rule}",
            f"link: {issue.link_text}",
            f"found: {issue.found}",
            f"expected: {issue.expected}",
            f"why_it_matters: {issue.why_it_matters}",
            f"next_step: {issue.next_step}",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check internal wiki links for one or more markdown pages.")
    parser.add_argument("pages", nargs="*", help="Markdown page paths, relative to repo root or absolute.")
    args = parser.parse_args()

    if not args.pages:
        print("Checked 0 eligible page(s). Found 0 link issues. No markdown pages were provided.")
        return 0

    eligible_pages: list[Path] = []
    skipped_pages: list[str] = []

    for raw_page in args.pages:
        page = Path(raw_page)
        if not page.is_absolute():
            page = (REPO_ROOT / page).resolve()

        if not page.exists():
            print(f"ERROR [links.invalid_input]")
            print(f"path: {raw_page}")
            print("rule: Link checking can only run on existing repository files.")
            print(f"found: `{raw_page}` does not exist.")
            print("expected: Pass an existing wiki-layer markdown page path.")
            print("why_it_matters: Missing input files usually mean the hook was pointed at the wrong staged path.")
            print(f"next_step: Re-run the checker with an existing page path, or remove `{raw_page}` from the hook invocation.")
            return 2

        if not page.is_file():
            print(f"ERROR [links.invalid_input]")
            print(f"path: {raw_page}")
            print("rule: Link checking can only run on files, not directories.")
            print(f"found: `{raw_page}` is not a file.")
            print("expected: Pass an existing wiki-layer markdown page path.")
            print("why_it_matters: Directory inputs cannot be checked line-by-line for link correctness.")
            print(f"next_step: Re-run the checker with one or more markdown file paths instead of `{raw_page}`.")
            return 2

        if is_supported_page(page):
            eligible_pages.append(page)
        else:
            skipped_pages.append(raw_page)

    if not eligible_pages:
        if skipped_pages:
            print(
                "Checked 0 eligible page(s). Found 0 link issues. "
                f"Skipped {len(skipped_pages)} non-wiki or out-of-scope file(s)."
            )
        else:
            print("Checked 0 eligible page(s). Found 0 link issues.")
        return 0

    all_issues: list[LinkIssue] = []
    for page in eligible_pages:
        all_issues.extend(check_page(page))

    if all_issues:
        for index, issue in enumerate(all_issues):
            if index:
                print()
            print(format_issue(issue))
        print()
        print(f"Checked {len(eligible_pages)} eligible page(s). Found {len(all_issues)} link issue(s).")
        return 1

    summary = f"Checked {len(eligible_pages)} eligible page(s). Found 0 link issues."
    if skipped_pages:
        summary += f" Skipped {len(skipped_pages)} non-wiki or out-of-scope file(s)."
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
