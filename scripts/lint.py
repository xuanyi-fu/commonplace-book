#!/usr/bin/env python3
"""Deterministic repository lint for the LLM wiki.

This script implements the current deterministic subset of AGENTS.md.
Run it with:

    uv run python scripts/lint.py

List the implemented rule catalog with:

    uv run python scripts/lint.py --list-rules
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "\n".join(
            [
                "ERROR [setup.python_dependency]",
                "path: scripts/lint.py",
                "agents_section: setup",
                "agents_rule: PyYAML must be installed so scripts/lint.py can parse frontmatter.",
                "rule: The linter requires PyYAML at runtime.",
                "found: PyYAML is not available in the current Python environment.",
                "expected: Run the linter with `uv run python scripts/lint.py` so the project dependency is installed automatically.",
                "why_it_matters: Without PyYAML, the linter cannot validate frontmatter deterministically.",
                "next_step: Run `uv lock` once if needed, then rerun `uv run python scripts/lint.py`.",
            ]
        )
    )
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = REPO_ROOT / "sources"
ROOT_INDEX = REPO_ROOT / "index.md"
GITATTR_FILE = REPO_ROOT / ".gitattributes"
EXPECTED_GITATTR_RULE = "sources/**/source/** filter=lfs diff=lfs merge=lfs -text"
FRONTMATTER_KEYS = ["type", "status", "created", "updated"]
ALLOWED_TYPES = {"source", "summary", "note", "entity", "concept", "synthesis", "index"}
ALLOWED_STATUS = {"draft", "stable"}
OPTIONAL_SCOPED_DIRS = ("summaries", "notes", "entities", "concepts", "syntheses")
REQUIRED_SOURCE_SUMMARY_HEADINGS = [
    "## Structure",
    "## How To Use",
    "## Summary",
    "## Sources",
]
KEBAB_CASE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
READING_NOTE_STEM_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-reading-note$")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


@dataclass(frozen=True)
class RuleSpec:
    rule_id: str
    title: str
    agents_section: str
    agents_rule: str
    check_description: str
    why_it_matters: str
    default_next_step: str


@dataclass(frozen=True)
class Finding:
    rule_id: str
    path: str
    line: int | None
    found: str
    expected: str
    why_it_matters: str | None = None
    next_step: str | None = None


RULE_SPECS = [
    RuleSpec(
        rule_id="repo.git_worktree",
        title="Repository must be a git worktree",
        agents_section="Git History",
        agents_rule="Git history is the only change history. Do not use `log.md`.",
        check_description="The linter must run inside a valid git worktree rooted at this repository.",
        why_it_matters="The linter relies on git metadata for repo validation and LFS checks.",
        default_next_step="Run the linter from inside the knowledge-base git repository.",
    ),
    RuleSpec(
        rule_id="repo.required_paths",
        title="Required repository paths must exist",
        agents_section="Scope / Git History",
        agents_rule="These rules apply to wiki-layer pages in specific paths, and the repo uses `sources/`, `index.md`, and `.gitattributes` as part of that structure.",
        check_description="The repo root must contain `AGENTS.md`, `index.md`, `.gitattributes`, and `sources/`.",
        why_it_matters="Without the required root paths, the repository cannot satisfy the current wiki contract.",
        default_next_step="Restore the missing root path or fix its type so the repository shape matches AGENTS.md.",
    ),
    RuleSpec(
        rule_id="repo.git_lfs_available",
        title="Git LFS must be installed",
        agents_section="sources/ rules",
        agents_rule="Git LFS tracks every file under `sources/<collection>/source/**`.",
        check_description="`git lfs` must be callable in the current environment.",
        why_it_matters="The repository explicitly requires Git LFS for raw source files.",
        default_next_step="Install Git LFS and rerun the linter.",
    ),
    RuleSpec(
        rule_id="sources.direct_children_are_folders",
        title="`sources/` direct children must be folders",
        agents_section="sources/ rules",
        agents_rule="Everything directly under `sources/` must be a folder.",
        check_description="Every direct child of `sources/` must be a directory.",
        why_it_matters="A flat file under `sources/` breaks the collection-oriented source layout.",
        default_next_step="Move the file into a `sources/<collection>/source/` directory or remove it.",
    ),
    RuleSpec(
        rule_id="sources.collection_kebab_case",
        title="Source collection folders must use kebab-case",
        agents_section="sources/ rules",
        agents_rule="Each `sources/<collection>/` folder must use `kebab-case`.",
        check_description="Each collection directory name under `sources/` must match kebab-case.",
        why_it_matters="Collection names are used in links, summaries, and deterministic path rules.",
        default_next_step="Rename the collection folder to kebab-case using lowercase letters, numbers, and `-` only.",
    ),
    RuleSpec(
        rule_id="sources.collection_root_shape",
        title="Source collection root shape is fixed",
        agents_section="sources/ rules",
        agents_rule="Each `sources/<collection>/` folder must contain exactly: `summary.md`, `source/`.",
        check_description="Each collection root must contain exactly `summary.md` and `source/`.",
        why_it_matters="The repo relies on a single summary entrypoint plus a single raw-source subtree.",
        default_next_step="Reduce the collection root to only `summary.md` and `source/`.",
    ),
    RuleSpec(
        rule_id="sources.no_raw_files_at_collection_root",
        title="Raw source files cannot live at collection root",
        agents_section="sources/ rules",
        agents_rule="No raw source file may live directly under `sources/<collection>/`.",
        check_description="No file except `summary.md` may exist directly under a collection root.",
        why_it_matters="Root-level raw files bypass the required `source/` subtree and break the LFS rule.",
        default_next_step="Move the raw file into `sources/<collection>/source/`.",
    ),
    RuleSpec(
        rule_id="sources.raw_files_under_source_dir",
        title="Raw source files must live under `source/`",
        agents_section="sources/ rules",
        agents_rule="Every raw source file must live under `sources/<collection>/source/**`.",
        check_description="Every non-summary file in a source collection must live below the `source/` directory.",
        why_it_matters="The repo uses the `source/` subtree as the canonical location for raw materials and LFS tracking.",
        default_next_step="Move the file into the collection's `source/` subtree or delete it.",
    ),
    RuleSpec(
        rule_id="sources.summary_required_sections",
        title="Source summaries must contain required sections",
        agents_section="sources/ rules",
        agents_rule="Each `sources/<collection>/summary.md` must include: `## Structure`, `## How To Use`, `## Summary`, `## Sources`.",
        check_description="Every source summary must include the required section headings.",
        why_it_matters="Agents rely on a fixed summary structure to understand the source collection consistently.",
        default_next_step="Add the missing required headings to the source summary.",
    ),
    RuleSpec(
        rule_id="frontmatter.required_block",
        title="Scoped wiki pages must start with frontmatter",
        agents_section="Frontmatter",
        agents_rule="Every wiki page must start with this exact four-field frontmatter, in this exact order.",
        check_description="Each scoped wiki page must begin with a frontmatter block.",
        why_it_matters="The deterministic metadata contract starts at the first line of every scoped wiki page.",
        default_next_step="Add the required four-field frontmatter block to the top of the file.",
    ),
    RuleSpec(
        rule_id="frontmatter.exact_keys_and_order",
        title="Frontmatter keys and order are fixed",
        agents_section="Frontmatter",
        agents_rule="Only `type`, `status`, `created`, `updated` are allowed.",
        check_description="Frontmatter keys must be exactly `type`, `status`, `created`, `updated` in that order.",
        why_it_matters="Stable key order and key set are required for deterministic automation.",
        default_next_step="Rewrite the frontmatter so it contains only `type`, `status`, `created`, and `updated` in that order.",
    ),
    RuleSpec(
        rule_id="frontmatter.allowed_type",
        title="`type` must be an allowed enum",
        agents_section="Frontmatter",
        agents_rule="Allowed `type` values: `source`, `summary`, `entity`, `concept`, `synthesis`, `index`.",
        check_description="The `type` field must use one of the allowed enum values.",
        why_it_matters="Type drives deterministic page classification in the wiki layer.",
        default_next_step="Replace the `type` value with one of the allowed values from AGENTS.md.",
    ),
    RuleSpec(
        rule_id="frontmatter.allowed_status",
        title="`status` must be an allowed enum",
        agents_section="Frontmatter",
        agents_rule="Allowed `status` values: `draft`, `stable`.",
        check_description="The `status` field must use one of the allowed enum values.",
        why_it_matters="Status is constrained so agents can reason about page maturity consistently.",
        default_next_step="Replace the `status` value with `draft` or `stable`.",
    ),
    RuleSpec(
        rule_id="frontmatter.valid_dates",
        title="Frontmatter dates must be valid ISO dates",
        agents_section="Frontmatter",
        agents_rule="Dates must use `YYYY-MM-DD`.",
        check_description="`created` and `updated` must be valid dates in `YYYY-MM-DD` format.",
        why_it_matters="Invalid dates break deterministic sorting and freshness checks.",
        default_next_step="Rewrite the date value using a valid `YYYY-MM-DD` string.",
    ),
    RuleSpec(
        rule_id="frontmatter.updated_not_earlier_than_created",
        title="`updated` cannot be earlier than `created`",
        agents_section="Frontmatter",
        agents_rule="`updated` must not be earlier than `created`.",
        check_description="The `updated` date must be the same as or later than `created`.",
        why_it_matters="A reversed date range makes page history internally inconsistent.",
        default_next_step="Set `updated` to the same day as or a later day than `created`.",
    ),
    RuleSpec(
        rule_id="naming.scoped_markdown_kebab_case",
        title="Scoped markdown filenames must use kebab-case",
        agents_section="File Naming",
        agents_rule="Use `kebab-case` only. Source collection summary pages are always named `summary.md`.",
        check_description="Scoped markdown filenames must use kebab-case, except for `sources/<collection>/summary.md`.",
        why_it_matters="Stable filenames make links and deterministic path rules predictable.",
        default_next_step="Rename the markdown file to kebab-case or use the allowed `summary.md` exception.",
    ),
    RuleSpec(
        rule_id="naming.canonical_reading_note_filename",
        title="Canonical reading note filenames must end with `-reading-note.md`",
        agents_section="notes/ rules",
        agents_rule="Canonical source reading notes use the path shape `notes/<collection>-reading-note.md`.",
        check_description="Markdown pages under `notes/` must use the canonical `notes/<collection>-reading-note.md` naming pattern.",
        why_it_matters="Stable reading-note filenames make note lookup, resumption, and indexing deterministic.",
        default_next_step="Rename the note to `notes/<collection>-reading-note.md` using the source collection slug.",
    ),
    RuleSpec(
        rule_id="index.no_raw_source_links",
        title="Root index cannot link to raw source files",
        agents_section="Index",
        agents_rule="Root `index.md` must not index raw source files under `sources/**/source/**` directly.",
        check_description="`index.md` must not contain a link target that points into `sources/**/source/**`.",
        why_it_matters="The root index should expose source collections through summary pages, not raw materials.",
        default_next_step="Replace the raw source link with a link to the collection summary page.",
    ),
    RuleSpec(
        rule_id="lfs.required_gitattributes_rule",
        title="`.gitattributes` must declare the raw-source LFS rule",
        agents_section="sources/ rules",
        agents_rule="Git LFS tracks every file under `sources/<collection>/source/**`.",
        check_description="`.gitattributes` must contain the exact LFS tracking rule for `sources/**/source/**`.",
        why_it_matters="Without the gitattributes rule, raw source files will not be tracked by Git LFS consistently.",
        default_next_step="Add the required LFS rule to `.gitattributes`.",
    ),
    RuleSpec(
        rule_id="lfs.source_files_tracked",
        title="Raw source files must resolve to LFS attributes",
        agents_section="sources/ rules",
        agents_rule="Git LFS tracks every file under `sources/<collection>/source/**`.",
        check_description="Every file under `sources/**/source/**` must resolve to `filter=lfs`, `diff=lfs`, and `merge=lfs` via git.",
        why_it_matters="Attribute resolution is the actual enforcement mechanism behind the repo's LFS rule.",
        default_next_step="Fix `.gitattributes` or move the file so git resolves LFS attributes for it.",
    ),
]
RULES = {rule.rule_id: rule for rule in RULE_SPECS}


def relpath(path: Path | str) -> str:
    if isinstance(path, Path):
        try:
            return path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return path.as_posix()
    return path


def is_kebab_case(value: str) -> bool:
    return bool(KEBAB_CASE_RE.fullmatch(value))


def is_source_collection_summary(path: Path) -> bool:
    try:
        parts = path.relative_to(REPO_ROOT).parts
    except ValueError:
        return False
    return len(parts) == 3 and parts[0] == "sources" and parts[2] == "summary.md"


def is_canonical_reading_note(path: Path) -> bool:
    try:
        parts = path.relative_to(REPO_ROOT).parts
    except ValueError:
        return False
    return len(parts) == 2 and parts[0] == "notes" and bool(READING_NOTE_STEM_RE.fullmatch(path.stem))


def add_finding(
    findings: list[Finding],
    rule_id: str,
    path: Path | str,
    *,
    line: int | None = None,
    found: str,
    expected: str,
    why_it_matters: str | None = None,
    next_step: str | None = None,
) -> None:
    findings.append(
        Finding(
            rule_id=rule_id,
            path=relpath(path),
            line=line,
            found=found,
            expected=expected,
            why_it_matters=why_it_matters,
            next_step=next_step,
        )
    )


def format_finding(finding: Finding) -> str:
    rule = RULES.get(finding.rule_id)
    if rule is None:
        agents_section = "setup"
        agents_rule = "n/a"
        description = finding.rule_id
        why_it_matters = finding.why_it_matters or "The linter cannot continue until this setup issue is resolved."
        next_step = finding.next_step or "Fix the setup issue and rerun the linter."
    else:
        agents_section = rule.agents_section
        agents_rule = rule.agents_rule
        description = rule.check_description
        why_it_matters = finding.why_it_matters or rule.why_it_matters
        next_step = finding.next_step or rule.default_next_step

    lines = [
        f"ERROR [{finding.rule_id}]",
        f"path: {finding.path}",
    ]
    if finding.line is not None:
        lines.append(f"line: {finding.line}")
    lines.extend(
        [
            f"agents_section: {agents_section}",
            f"agents_rule: {agents_rule}",
            f"rule: {description}",
            f"found: {finding.found}",
            f"expected: {finding.expected}",
            f"why_it_matters: {why_it_matters}",
            f"next_step: {next_step}",
        ]
    )
    return "\n".join(lines)


def print_rule_catalog() -> None:
    print("Implemented deterministic AGENTS.md rules in scripts/lint.py:")
    print()
    for rule in RULE_SPECS:
        print(f"- {rule.rule_id}: {rule.title}")
        print(f"  agents_section: {rule.agents_section}")
        print(f"  agents_rule: {rule.agents_rule}")
        print(f"  checks: {rule.check_description}")
        print(f"  next_step: {rule.default_next_step}")
        print()


def run_git_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def setup_error(rule_id: str, found: str, expected: str, next_step: str) -> None:
    print(
        format_finding(
            Finding(
                rule_id=rule_id,
                path=".",
                line=None,
                found=found,
                expected=expected,
                next_step=next_step,
            )
        )
    )


def ensure_git_setup() -> int | None:
    try:
        result = run_git_command(["git", "rev-parse", "--is-inside-work-tree"])
    except FileNotFoundError:
        setup_error(
            "repo.git_worktree",
            "The `git` executable is not available in PATH.",
            "`git rev-parse --is-inside-work-tree` should succeed inside this repository.",
            "Install git or fix PATH, then rerun the linter from the repository root.",
        )
        return 2

    if result.returncode != 0 or result.stdout.strip() != "true":
        setup_error(
            "repo.git_worktree",
            f"`git rev-parse --is-inside-work-tree` returned code {result.returncode} with output: {result.stdout.strip() or result.stderr.strip() or '(no output)'}",
            "The repository must be a valid git worktree before lint can run.",
            "Run the linter from inside the knowledge-base git repository.",
        )
        return 2

    try:
        lfs_result = run_git_command(["git", "lfs", "version"])
    except FileNotFoundError:
        setup_error(
            "repo.git_lfs_available",
            "The `git` executable is not available in PATH.",
            "`git lfs version` should succeed.",
            "Install git and Git LFS, then rerun the linter.",
        )
        return 2

    if lfs_result.returncode != 0:
        setup_error(
            "repo.git_lfs_available",
            lfs_result.stderr.strip() or lfs_result.stdout.strip() or "`git lfs version` failed.",
            "`git lfs version` must succeed because raw source files are tracked with Git LFS.",
            "Install Git LFS and rerun the linter.",
        )
        return 2

    return None


def collect_collection_dirs() -> list[Path]:
    if not SOURCES_DIR.exists() or not SOURCES_DIR.is_dir():
        return []
    return sorted([child for child in SOURCES_DIR.iterdir() if child.is_dir()], key=lambda path: path.name)


def collect_scoped_markdown_paths() -> list[Path]:
    paths: list[Path] = []
    if ROOT_INDEX.exists():
        paths.append(ROOT_INDEX)

    for collection in collect_collection_dirs():
        summary_path = collection / "summary.md"
        if summary_path.exists():
            paths.append(summary_path)

    for directory_name in OPTIONAL_SCOPED_DIRS:
        directory = REPO_ROOT / directory_name
        if directory.is_dir():
            paths.extend(sorted(directory.rglob("*.md")))

    unique_paths = sorted({path.resolve() for path in paths})
    return [Path(path) for path in unique_paths]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path, findings: list[Finding]) -> tuple[dict[str, str], dict[str, int]] | None:
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        add_finding(
            findings,
            "frontmatter.required_block",
            path,
            line=1,
            found="The file does not start with a valid frontmatter block.",
            expected="The file must begin with the required four-field frontmatter block.",
        )
        return None

    frontmatter_body = match.group(1)
    try:
        parsed = yaml.load(frontmatter_body, Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        add_finding(
            findings,
            "frontmatter.exact_keys_and_order",
            path,
            line=2,
            found=f"Frontmatter could not be parsed as YAML: {exc}",
            expected="A valid YAML mapping with only `type`, `status`, `created`, `updated` in that order.",
            next_step="Rewrite the frontmatter as a simple YAML mapping with the required four keys.",
        )
        return None

    if not isinstance(parsed, dict):
        add_finding(
            findings,
            "frontmatter.exact_keys_and_order",
            path,
            line=2,
            found=f"Parsed frontmatter type was `{type(parsed).__name__}` instead of a mapping.",
            expected="A YAML mapping with exactly `type`, `status`, `created`, `updated` in that order.",
            next_step="Rewrite the frontmatter so it is a simple key/value mapping.",
        )
        return None

    line_numbers: dict[str, int] = {}
    for line_number, raw_line in enumerate(frontmatter_body.splitlines(), start=2):
        match_line = re.match(r"^([A-Za-z0-9_-]+)\s*:", raw_line)
        if match_line and match_line.group(1) not in line_numbers:
            line_numbers[match_line.group(1)] = line_number

    return {str(key): str(value) for key, value in parsed.items()}, line_numbers


def validate_frontmatter(path: Path, findings: list[Finding]) -> None:
    parsed = parse_frontmatter(path, findings)
    if parsed is None:
        return

    values, line_numbers = parsed
    keys = list(values.keys())
    if keys != FRONTMATTER_KEYS:
        add_finding(
            findings,
            "frontmatter.exact_keys_and_order",
            path,
            line=2,
            found=f"Frontmatter keys were {keys}.",
            expected=f"Frontmatter keys must be exactly {FRONTMATTER_KEYS} in that order.",
        )

    page_type = values.get("type")
    if page_type is None or page_type not in ALLOWED_TYPES:
        add_finding(
            findings,
            "frontmatter.allowed_type",
            path,
            line=line_numbers.get("type", 2),
            found=f"type: {page_type!r}",
            expected=f"`type` must be one of {sorted(ALLOWED_TYPES)}.",
        )

    status = values.get("status")
    if status is None or status not in ALLOWED_STATUS:
        add_finding(
            findings,
            "frontmatter.allowed_status",
            path,
            line=line_numbers.get("status", 3),
            found=f"status: {status!r}",
            expected=f"`status` must be one of {sorted(ALLOWED_STATUS)}.",
        )

    created_raw = values.get("created")
    updated_raw = values.get("updated")
    created_date = validate_date_field(path, findings, "created", created_raw, line_numbers.get("created", 4))
    updated_date = validate_date_field(path, findings, "updated", updated_raw, line_numbers.get("updated", 5))

    if created_date is not None and updated_date is not None and updated_date < created_date:
        add_finding(
            findings,
            "frontmatter.updated_not_earlier_than_created",
            path,
            line=line_numbers.get("updated", 5),
            found=f"`created` is {created_raw} but `updated` is {updated_raw}.",
            expected="`updated` must be the same as or later than `created`.",
        )


def validate_date_field(
    path: Path,
    findings: list[Finding],
    key: str,
    raw_value: str | None,
    line_number: int,
) -> date | None:
    if raw_value is None or not DATE_RE.fullmatch(raw_value):
        add_finding(
            findings,
            "frontmatter.valid_dates",
            path,
            line=line_number,
            found=f"{key}: {raw_value!r}",
            expected=f"`{key}` must use a valid `YYYY-MM-DD` date string.",
        )
        return None

    try:
        return date.fromisoformat(raw_value)
    except ValueError:
        add_finding(
            findings,
            "frontmatter.valid_dates",
            path,
            line=line_number,
            found=f"{key}: {raw_value!r}",
            expected=f"`{key}` must be a valid calendar date in `YYYY-MM-DD` format.",
        )
        return None


def validate_required_paths(findings: list[Finding]) -> None:
    requirements = {
        REPO_ROOT / "AGENTS.md": "file",
        ROOT_INDEX: "file",
        GITATTR_FILE: "file",
        SOURCES_DIR: "directory",
    }

    for path, expected_type in requirements.items():
        if expected_type == "file":
            if not path.exists():
                add_finding(
                    findings,
                    "repo.required_paths",
                    path,
                    found="Path does not exist.",
                    expected=f"A {expected_type} must exist at this path.",
                )
            elif not path.is_file():
                add_finding(
                    findings,
                    "repo.required_paths",
                    path,
                    found=f"Path exists as a non-file (`{path.stat().st_mode}` / not a regular file).",
                    expected=f"A regular {expected_type} must exist at this path.",
                )
        else:
            if not path.exists():
                add_finding(
                    findings,
                    "repo.required_paths",
                    path,
                    found="Path does not exist.",
                    expected=f"A {expected_type} must exist at this path.",
                )
            elif not path.is_dir():
                add_finding(
                    findings,
                    "repo.required_paths",
                    path,
                    found="Path exists but is not a directory.",
                    expected="A directory must exist at this path.",
                )


def validate_sources_layout(findings: list[Finding]) -> None:
    if not SOURCES_DIR.is_dir():
        return

    for child in sorted(SOURCES_DIR.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            add_finding(
                findings,
                "sources.direct_children_are_folders",
                child,
                found="Direct child under `sources/` is not a directory.",
                expected="Every direct child under `sources/` must be a collection folder.",
            )
            continue

        if not is_kebab_case(child.name):
            add_finding(
                findings,
                "sources.collection_kebab_case",
                child,
                found=f"Collection folder name was `{child.name}`.",
                expected="Collection folder names must use kebab-case.",
            )

        children = sorted(path.name for path in child.iterdir())
        if children != ["source", "summary.md"]:
            add_finding(
                findings,
                "sources.collection_root_shape",
                child,
                found=f"Collection root children were {children}.",
                expected="Collection root must contain exactly `summary.md` and `source/`.",
            )

        for direct_file in sorted(path for path in child.iterdir() if path.is_file() and path.name != "summary.md"):
            add_finding(
                findings,
                "sources.no_raw_files_at_collection_root",
                direct_file,
                found="A non-summary file exists directly under the collection root.",
                expected="Only `summary.md` may exist directly under a collection root.",
            )

        source_dir = child / "source"
        if not source_dir.exists() or not source_dir.is_dir():
            continue

        for file_path in sorted(path for path in child.rglob("*") if path.is_file()):
            relative = file_path.relative_to(child)
            if relative == Path("summary.md"):
                continue
            if relative.parts[0] != "source":
                add_finding(
                    findings,
                    "sources.raw_files_under_source_dir",
                    file_path,
                    found=f"File exists outside `source/`: `{relative.as_posix()}`.",
                    expected="All non-summary files in a source collection must live under `source/`.",
                )


def validate_source_summary_sections(findings: list[Finding]) -> None:
    for collection in collect_collection_dirs():
        summary_path = collection / "summary.md"
        if not summary_path.exists():
            continue
        text = read_text(summary_path)
        headings = {line.strip() for line in text.splitlines() if line.startswith("## ")}
        missing = [heading for heading in REQUIRED_SOURCE_SUMMARY_HEADINGS if heading not in headings]
        if missing:
            add_finding(
                findings,
                "sources.summary_required_sections",
                summary_path,
                found=f"Missing required headings: {missing}. Present headings were {sorted(headings)}.",
                expected=f"The source summary must include {REQUIRED_SOURCE_SUMMARY_HEADINGS}.",
                next_step=f"Add these missing headings to the summary: {', '.join(missing)}.",
            )


def validate_scoped_markdown(findings: list[Finding]) -> None:
    for path in collect_scoped_markdown_paths():
        validate_frontmatter(path, findings)

        if is_source_collection_summary(path):
            continue

        if path.relative_to(REPO_ROOT).parts[0] == "notes" and not is_canonical_reading_note(path):
            add_finding(
                findings,
                "naming.canonical_reading_note_filename",
                path,
                found=f"Filename was `{path.name}`.",
                expected="Reading notes under `notes/` must be named `notes/<collection>-reading-note.md`.",
            )

        if not is_kebab_case(path.stem):
            add_finding(
                findings,
                "naming.scoped_markdown_kebab_case",
                path,
                found=f"Filename stem was `{path.stem}`.",
                expected="Scoped markdown filenames must use kebab-case.",
            )


def extract_link_targets(line: str) -> list[str]:
    targets: list[str] = []
    for match in WIKILINK_RE.finditer(line):
        inner = match.group(1).strip()
        target = inner.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            targets.append(target)
    for match in MARKDOWN_LINK_RE.finditer(line):
        inner = match.group(1).strip().strip("<>").split("#", 1)[0].strip()
        if inner:
            targets.append(inner)
    return targets


def validate_index_links(findings: list[Finding]) -> None:
    if not ROOT_INDEX.exists():
        return

    in_code_fence = False
    for line_number, raw_line in enumerate(read_text(ROOT_INDEX).splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        for target in extract_link_targets(raw_line):
            normalized = target.replace("\\", "/")
            if normalized.startswith("sources/") and "/source/" in normalized:
                add_finding(
                    findings,
                    "index.no_raw_source_links",
                    ROOT_INDEX,
                    line=line_number,
                    found=f"`index.md` links to raw source target `{target}`.",
                    expected="Root `index.md` must link to source collection summaries, not raw source files.",
                )


def validate_gitattributes(findings: list[Finding]) -> None:
    if not GITATTR_FILE.exists():
        return

    lines = [line.strip() for line in read_text(GITATTR_FILE).splitlines() if line.strip() and not line.strip().startswith("#")]
    if EXPECTED_GITATTR_RULE not in lines:
        add_finding(
            findings,
            "lfs.required_gitattributes_rule",
            GITATTR_FILE,
            found=f"Active `.gitattributes` rules were {lines}.",
            expected=f"`.gitattributes` must include `{EXPECTED_GITATTR_RULE}`.",
        )


def collect_raw_source_files() -> list[Path]:
    if not SOURCES_DIR.is_dir():
        return []
    return sorted(path for path in SOURCES_DIR.rglob("*") if path.is_file() and "/source/" in path.as_posix())


def validate_lfs_attributes(findings: list[Finding]) -> int | None:
    raw_files = collect_raw_source_files()
    if not raw_files:
        return None

    relative_paths = [relpath(path) for path in raw_files]
    result = run_git_command(["git", "check-attr", "filter", "diff", "merge", "--", *relative_paths])
    if result.returncode != 0:
        setup_error(
            "lfs.source_files_tracked",
            result.stderr.strip() or result.stdout.strip() or "`git check-attr` failed.",
            "`git check-attr filter diff merge -- <raw-source-files>` must succeed.",
            "Fix the git repository state and rerun the linter.",
        )
        return 2

    attributes: dict[str, dict[str, str]] = {}
    for line in result.stdout.splitlines():
        parts = line.split(": ", 2)
        if len(parts) != 3:
            continue
        path_text, attr_name, value = parts
        attributes.setdefault(path_text, {})[attr_name] = value

    for raw_path in relative_paths:
        attr_map = attributes.get(raw_path, {})
        expected = {"filter": "lfs", "diff": "lfs", "merge": "lfs"}
        if any(attr_map.get(name) != value for name, value in expected.items()):
            add_finding(
                findings,
                "lfs.source_files_tracked",
                raw_path,
                found=f"`git check-attr` returned {attr_map or '(no attributes)'}.",
                expected="Each raw source file must resolve to `filter=lfs`, `diff=lfs`, and `merge=lfs`.",
            )
    return None


def run_lint() -> int:
    setup_status = ensure_git_setup()
    if setup_status is not None:
        return setup_status

    findings: list[Finding] = []
    validate_required_paths(findings)
    validate_sources_layout(findings)
    validate_source_summary_sections(findings)
    validate_scoped_markdown(findings)
    validate_index_links(findings)
    validate_gitattributes(findings)
    lfs_status = validate_lfs_attributes(findings)
    if lfs_status is not None:
        return lfs_status

    if findings:
        for index, finding in enumerate(findings):
            if index:
                print()
            print(format_finding(finding))
        print()
        print(f"Summary: found {len(findings)} lint error(s).")
        return 1

    print("Lint passed. Summary: found 0 lint errors.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the deterministic subset of AGENTS.md for this LLM wiki.")
    parser.add_argument(
        "--list-rules",
        action="store_true",
        help="Print the deterministic AGENTS.md rules implemented by this linter and exit.",
    )
    args = parser.parse_args()

    if args.list_rules:
        print_rule_catalog()
        return 0
    return run_lint()


if __name__ == "__main__":
    raise SystemExit(main())
