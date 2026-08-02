#!/usr/bin/env python3
"""Discover and rank GitHub repositories relevant to FDE practice.

The script uses GitHub's public repository search API. Set GITHUB_TOKEN for a
higher rate limit; unauthenticated discovery also works and waits for resets.
Raw results are retained so the editorial selection can be audited.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resources" / "github-candidates.json"
API = "https://api.github.com/search/repositories"
TOKEN = os.environ.get("GITHUB_TOKEN")


@dataclass(frozen=True)
class Search:
    category: str
    query: str
    relevance: str


SEARCHES = [
    Search("direct-fde", '"forward deployed engineer" in:name,description,readme', "Explicitly discusses the Forward Deployed Engineer role or discipline."),
    Search("direct-fde", '"forward-deployed engineer" in:name,description,readme', "Explicitly discusses forward-deployed engineering."),
    Search("direct-fde", '"forward deployed engineering" in:name,description,readme', "Explicitly discusses forward-deployed engineering practice."),
    Search("direct-fde", 'palantir FDE in:name,description,readme', "Connects FDE practice to its Palantir origins or implementations."),
    Search("agent-platforms", '"agent platform" deployment in:name,description,readme stars:>20', "Supports building and deploying agent systems in production."),
    Search("evaluation-observability", 'LLM evals observability in:name,description,readme stars:>10', "Supports evaluation and operational visibility for production AI."),
    Search("security-sandbox", 'agent sandbox security in:name,description,readme stars:>10', "Supports safe execution and security boundaries for agent deployments."),
    Search("enterprise-ai", '"enterprise AI" agents in:name,description,readme stars:>10', "Addresses enterprise constraints around AI and agent adoption."),
    Search("context-integration", '"model context protocol" server in:name,description,readme stars:>10', "Connects agents to tools, systems, and enterprise context through MCP."),
    Search("production-rag", 'RAG production evaluation in:name,description,readme stars:>10', "Supports production retrieval, evaluation, and context quality."),
    Search("learning-guides", '"AI engineering" book in:name,description,readme stars:>20', "Provides book-style or structured learning material for applied AI engineering."),
    Search("learning-guides", '"production AI" guide in:name,description,readme stars:>10', "Provides guidance for moving AI systems from prototype to production."),
    Search("learning-guides", '"LLM in production" guide in:name,description,readme stars:>10', "Provides practical guidance for production LLM systems."),
    Search("learning-guides", '"agent engineering" course in:name,description,readme stars:>10', "Provides a structured path for learning production agent engineering."),
    Search("case-studies", '"enterprise AI" "case study" in:name,description,readme stars:>5', "Documents an enterprise AI implementation or deployment case."),
    Search("best-practices", '"AI agents" "best practices" in:name,description,readme stars:>20', "Collects reusable practices for building and operating AI agents."),
    Search("learning-guides", 'MLOps course book in:name,description,readme stars:>100', "Provides structured learning for production machine learning operations."),
    Search("best-practices", 'LLMOps guide in:name,description,readme stars:>20', "Provides reusable practices for deploying and operating LLM systems."),
]

EXCLUDE_TERMS = {
    "finite difference",
    "finite-difference",
    "full disk encryption",
    "full-disk encryption",
    "frequency domain equalization",
    "fractional differential equation",
    "fokker planck",
    "fermi-dirac",
    "feature distribution encoding",
}


def request_json(url: str) -> tuple[dict, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-global-fde-discovery",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    while True:
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data, dict(response.headers.items())
        except HTTPError as error:
            remaining = error.headers.get("X-RateLimit-Remaining")
            reset = error.headers.get("X-RateLimit-Reset")
            if error.code in {403, 429} and remaining == "0" and reset:
                delay = max(1, int(reset) - int(time.time()) + 2)
                print(f"Search rate limit reached; waiting {delay}s", flush=True)
                time.sleep(delay)
                continue
            raise


def normalize(item: dict, search: Search) -> dict:
    license_data = item.get("license") or {}
    return {
        "full_name": item["full_name"],
        "html_url": item["html_url"],
        "description": item.get("description") or "",
        "homepage": item.get("homepage") or "",
        "language": item.get("language"),
        "topics": item.get("topics") or [],
        "stars": item.get("stargazers_count", 0),
        "forks": item.get("forks_count", 0),
        "open_issues": item.get("open_issues_count", 0),
        "license": license_data.get("spdx_id"),
        "archived": bool(item.get("archived")),
        "disabled": bool(item.get("disabled")),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "pushed_at": item.get("pushed_at"),
        "default_branch": item.get("default_branch"),
        "category": search.category,
        "fde_relevance": search.relevance,
        "matched_queries": [search.query],
    }


def is_noise(repo: dict) -> bool:
    haystack = " ".join([
        repo["full_name"],
        repo["description"],
        " ".join(repo["topics"]),
    ]).lower()
    return any(term in haystack for term in EXCLUDE_TERMS) or repo["disabled"]


def main() -> None:
    repositories: dict[str, dict] = {}
    query_stats = []
    for index, search in enumerate(SEARCHES, 1):
        params = urlencode({"q": search.query, "sort": "stars", "order": "desc", "per_page": 100, "page": 1})
        print(f"[{index}/{len(SEARCHES)}] {search.query}", flush=True)
        result, headers = request_json(f"{API}?{params}")
        items = result.get("items", [])
        query_stats.append({
            "category": search.category,
            "query": search.query,
            "total_count": result.get("total_count", 0),
            "returned": len(items),
            "rate_limit_remaining": headers.get("X-RateLimit-Remaining"),
        })
        for item in items:
            candidate = normalize(item, search)
            if is_noise(candidate):
                continue
            existing = repositories.get(candidate["full_name"].lower())
            if existing:
                existing["matched_queries"].append(search.query)
                if existing["category"] != "direct-fde" and search.category == "direct-fde":
                    existing["category"] = "direct-fde"
                    existing["fde_relevance"] = search.relevance
            else:
                repositories[candidate["full_name"].lower()] = candidate
    ranked = sorted(
        repositories.values(),
        key=lambda repo: (
            repo["category"] != "direct-fde",
            repo["archived"],
            -len(repo["matched_queries"]),
            -repo["stars"],
            repo["full_name"].lower(),
        ),
    )
    output = {
        "generated_at": datetime.now(UTC).isoformat(),
        "searches": query_stats,
        "candidate_count": len(ranked),
        "repositories": ranked,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(ranked)} candidates to {OUTPUT}")


if __name__ == "__main__":
    main()
