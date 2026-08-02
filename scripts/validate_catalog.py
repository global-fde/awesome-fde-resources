#!/usr/bin/env python3
"""Validate the generated Global FDE GitHub repository catalog."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "resources" / "github-repositories.yml"
INDEX = ROOT / "GITHUB_REPOSITORIES.md"
ALLOWED_CATEGORIES = {
    "getting-started",
    "best-practices",
    "case-studies",
    "tools",
}


def main() -> None:
    payload = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    repositories = payload["repositories"]
    urls = [repo["url"] for repo in repositories]
    names = [repo["name"].lower() for repo in repositories]
    counts = Counter(repo["category"] for repo in repositories)
    direct_count = sum(bool(repo["direct_fde"]) for repo in repositories)

    assert payload["repository_count"] == len(repositories), "repository_count does not match catalog"
    assert len(urls) == len(set(urls)), "duplicate repository URL"
    assert len(names) == len(set(names)), "duplicate repository name"
    assert all(url.startswith("https://github.com/") for url in urls), "non-GitHub URL in repository catalog"
    assert set(counts) <= ALLOWED_CATEGORIES, "unknown category"
    assert counts == Counter(payload["category_counts"]), "category counts do not match catalog"
    assert payload["direct_fde_count"] == direct_count, "direct FDE count does not match catalog"
    assert payload["supporting_repository_count"] == len(repositories) - direct_count, "supporting count mismatch"
    assert all(repo["editorial_state"] in {"candidate", "reviewed", "featured", "archived"} for repo in repositories), "unknown editorial state"
    assert all(repo.get("description", "").strip() for repo in repositories), "empty description"

    index = INDEX.read_text(encoding="utf-8")
    assert f"> {len(repositories)} repositories" in index, "Markdown index count is stale"
    assert index.count("https://github.com/") == len(repositories), "Markdown index URL count is stale"

    print(
        f"Catalog OK: {len(repositories)} repositories, "
        f"{direct_count} direct FDE, {len(repositories) - direct_count} supporting"
    )


if __name__ == "__main__":
    main()
