#!/usr/bin/env python3
"""Validate catalog metadata and both human-readable indexes."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "resources" / "github-repositories.yml"
READMES = [ROOT / "README.md", ROOT / "README.zh-CN.md"]
MINIMUM_CATALOG_SIZE = 50
ALLOWED_CATEGORIES = {
    "getting-started",
    "best-practices",
    "case-studies",
    "tools",
}
SECTION_HEADINGS = {
    "README.md": {
        "getting-started": "Getting started",
        "best-practices": "Best practices",
        "case-studies": "Cases and reference implementations",
        "tools": "Tools",
    },
    "README.zh-CN.md": {
        "getting-started": "入门与系统学习",
        "best-practices": "最佳实践",
        "case-studies": "案例与参考实现",
        "tools": "工具",
    },
}
GITHUB_URL = re.compile(r"https://github\.com/[^\s)]+")


def section_urls(readme: str, heading: str) -> list[str]:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        readme,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"missing section: {heading}"
    return GITHUB_URL.findall(match.group("body"))


def validate_date(value: object, field: str, repository: str) -> None:
    assert isinstance(value, str) and value, f"{repository}: missing {field}"
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise AssertionError(f"{repository}: invalid {field}: {value}") from error


def validate_timestamp(value: object, repository: str) -> None:
    assert isinstance(value, str) and value, f"{repository}: missing updated_at"
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise AssertionError(f"{repository}: invalid updated_at: {value}") from error


def main() -> None:
    payload = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    repositories = payload["repositories"]
    urls = [repo["url"] for repo in repositories]
    names = [repo["name"].lower() for repo in repositories]
    counts = Counter(repo["category"] for repo in repositories)
    direct_count = sum(bool(repo["direct_fde"]) for repo in repositories)

    assert payload["repository_count"] == len(repositories), "repository_count does not match catalog"
    assert payload["repository_count"] >= MINIMUM_CATALOG_SIZE, (
        f"the curated catalog must retain at least {MINIMUM_CATALOG_SIZE} repositories"
    )
    assert payload["minimum_stars"] == 50, "minimum star policy must be 50"
    assert len(urls) == len(set(urls)), "duplicate repository URL"
    assert len(names) == len(set(names)), "duplicate repository name"
    assert all(url.startswith("https://github.com/") for url in urls), "non-GitHub URL in repository catalog"
    assert set(counts) == ALLOWED_CATEGORIES, "missing or unknown category"
    assert counts == Counter(payload["category_counts"]), "category counts do not match catalog"
    assert sum(payload["category_counts"].values()) == len(repositories), "category count total mismatch"
    assert payload["direct_fde_count"] == direct_count, "direct FDE count does not match catalog"
    assert payload["supporting_repository_count"] == len(repositories) - direct_count, "supporting count mismatch"
    assert all(repo["editorial_state"] in {"reviewed", "featured"} for repo in repositories), (
        "published repositories must be reviewed or featured"
    )
    assert all(repo.get("description", "").strip() for repo in repositories), "empty description"
    assert all(repo["stars_snapshot"] >= payload["minimum_stars"] for repo in repositories), "repository below star threshold"

    required_fields = {
        "name",
        "url",
        "description",
        "category",
        "direct_fde",
        "tags",
        "primary_language",
        "license",
        "stars_snapshot",
        "updated_at",
        "why_it_matters",
        "editorial_state",
        "reviewed_on",
    }
    for repo in repositories:
        name = repo.get("name", "<unnamed>")
        missing = required_fields - set(repo)
        assert not missing, f"{name}: missing fields: {sorted(missing)}"
        assert isinstance(repo["direct_fde"], bool), f"{name}: direct_fde must be boolean"
        assert isinstance(repo["stars_snapshot"], int), f"{name}: stars_snapshot must be integer"
        assert isinstance(repo["tags"], list) and repo["tags"], f"{name}: tags must be a non-empty list"
        assert len(repo["tags"]) == len(set(repo["tags"])), f"{name}: duplicate tags"
        assert repo["why_it_matters"].strip(), f"{name}: empty why_it_matters"
        validate_timestamp(repo["updated_at"], name)
        validate_date(repo["reviewed_on"], "reviewed_on", name)

    for readme_path in READMES:
        readme = readme_path.read_text(encoding="utf-8")
        headings = SECTION_HEADINGS[readme_path.name]
        for category, heading in headings.items():
            expected = [repo["url"] for repo in repositories if repo["category"] == category]
            actual = section_urls(readme, heading)
            assert actual == expected, (
                f"{readme_path.name}: {category} links differ from catalog or are out of order"
            )
            count_pattern = rf"\[{re.escape(heading)}\]\([^)]*\)\s*[-—]\s*{len(expected)}\b"
            assert re.search(count_pattern, readme), (
                f"{readme_path.name}: contents count for {heading} must be {len(expected)}"
            )

        listed_urls = [url for heading in headings.values() for url in section_urls(readme, heading)]
        assert len(listed_urls) == len(repositories), f"{readme_path.name}: repository total mismatch"

    print(f"Catalog OK: {len(repositories)} curated repositories")


if __name__ == "__main__":
    main()
