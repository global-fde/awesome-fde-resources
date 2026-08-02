#!/usr/bin/env python3
"""Select 200 high-signal repositories from the GitHub discovery pool."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "resources" / "github-candidates.json"
YAML_OUTPUT = ROOT / "resources" / "github-repositories.yml"
MARKDOWN_OUTPUT = ROOT / "GITHUB_REPOSITORIES.md"
TARGET = 200
QUOTAS = {
    "getting-started": 85,
    "best-practices": 25,
    "case-studies": 15,
    "tools": 75,
}

OVERRIDE_CATEGORY = {
    "evidentlyai/evidently": "tools",
    "mlflow/mlflow": "tools",
    "huggingface/agents-course": "getting-started",
    "microsoft/mcp-for-beginners": "getting-started",
    "rdmgator12/awesome-claude-connectors": "tools",
    "patchy631/ai-engineering-hub": "case-studies",
    "nirdiamant/genai_agents": "case-studies",
    "googlecloudplatform/generative-ai": "case-studies",
    "pathwaycom/llm-app": "case-studies",
    "gurpreetkaurjethra/end-to-end-generative-ai-projects": "case-studies",
    "mollyretter/forward-deployed-engineer-toolkit": "tools",
    "dan-cleary/fdestack": "tools",
    "zhongzhuoran/fde-copilot": "tools",
    "objectstack-ai/objectstack": "tools",
    "icecreamlun/understudy": "tools",
    "cephos-ai/deploykit": "tools",
    "memovai/openfde": "tools",
    "sumitoza/hephaestus": "tools",
    "raghu-007/zero-trust-ai-proxy": "best-practices",
    "hamzamissewi/fde-framework": "case-studies",
    "bhardwaj-saurabh/aurora_hotel_concierge_voice_based_agent": "case-studies",
    "flamingtonforai/fdeagent": "tools",
    "agents-to-go/opencode-forward-deployed-engineer": "tools",
    "jakeb440/microsoft-fde-teardown": "case-studies",
}

CATEGORY_META = {
    "getting-started": {
        "title": "入门与系统学习 / Getting Started",
        "intro": "FDE 角色认知、书籍、指南、路线图、课程和系统学习资料。",
        "why": "Provides structured knowledge that helps practitioners build FDE foundations.",
    },
    "best-practices": {
        "title": "最佳实践与方法 / Best Practices",
        "intro": "现场发现、交付、生产 AI、Agent、RAG、评估、安全和运维方法。",
        "why": "Provides reusable practices for designing, deploying, evaluating, or operating production AI.",
    },
    "case-studies": {
        "title": "案例、实验与参考实现 / Cases",
        "intro": "真实案例、工作坊、示例工程、行业项目和可复现参考实现。",
        "why": "Provides an implementation, example, or case that can be studied and adapted in field delivery.",
    },
    "tools": {
        "title": "FDE 工具与基础设施 / Tools",
        "intro": "Agent 平台、评估与可观测性、安全沙箱、MCP、上下文和部署工具。",
        "why": "Provides infrastructure useful for building or operating production AI and agent deployments.",
    },
}

FORCE_INCLUDE = {
    "xdash/fde-the-guidance-book-of-forward-deployed-engineer",
    "pierpaolo28/awesome-fde-roadmap",
    "libaice/awesome-fde",
    "yeasy/forward_deployed_engineering_guide",
    "thecoder8890/forward-deployed-engineer-roadmap",
    "openfdeai/openfde",
    "dawei008/fde-book",
    "liuhuanyong/fdegreenbook",
    "goday-org/fde-handbook",
    "wwwweeia/palantir-aip-study",
    "bicced/ai-engineer-interview-handbook",
    "cma0232/fde-interview-prep",
    "leading-ai-io/the-forward-deployed-shift",
    "suboss87/fdeops",
    "mollyretter/forward-deployed-engineer-toolkit",
    "kalyvask/fde-simulation",
    "aifde/fde-practice-cases",
    "dan-cleary/fdestack",
    "bittush8789/ai-forward-deployed-engineer-zero-to-hero",
    "chenshuai9101/fde-cli",
    "tatendaz/langchain-fde-curriculum",
    "zhongzhuoran/fde-copilot",
    "chiphuyen/aie-book",
    "mlabonne/llm-course",
    "huggingface/agents-course",
    "nirdiamant/agents-towards-production",
    "nirdiamant/genai_agents",
    "patchy631/ai-engineering-hub",
    "ethicalml/awesome-production-machine-learning",
    "googlecloudplatform/agent-starter-pack",
    "langfuse/langfuse",
    "arize-ai/phoenix",
    "vibrantlabsai/ragas",
    "evidentlyai/evidently",
    "promptfoo/promptfoo",
    "confident-ai/deepeval",
    "modelcontextprotocol/servers",
    "punkpeye/awesome-mcp-servers",
    "e2b-dev/awesome-ai-agents",
}

BLOCKLIST = {
    "ripienaar/free-for-dev",
    "rust-unofficial/awesome-rust",
    "akullpp/awesome-java",
    "fffaraz/awesome-cpp",
    "avelino/awesome-go",
    "vuejs/awesome-vue",
    "awesome-selfhosted/awesome-selfhosted",
    "public-apis/public-apis",
    "sindresorhus/awesome",
    "dkhamsing/open-source-ios-apps",
    "wilsonfreitas/awesome-quant",
    "academic/awesome-datascience",
    "josephmisiti/awesome-machine-learning",
    "munGell/awesome-for-beginners".lower(),
}

NOISE_TERMS = {
    "internship",
    "new grad",
    "new-grad",
    "job list",
    "job board",
    "positions for 202",
    "trading",
    "quantitative finance",
    "computer vision",
    "opencv",
    "pytorch",
    "design system",
    "image generation",
    "image editing",
    "prompt collection",
    "chatgpt clone",
    "ios apps",
    "free tiers",
    "game development",
    "job search",
    "job aggregator",
    "career operating system",
    "money making",
    "intern positions",
    "daily news",
    "weekly news",
    "pytorch papers",
    "fine-tuning large language models",
    "image prompt",
    "design intelligence",
    "ui/ux",
}

AI_RELEVANCE_TERMS = {
    "ai agent",
    "ai agents",
    "agentic",
    "llm",
    "large language model",
    "generative ai",
    "enterprise ai",
    "production ai",
    "production-grade ai",
    "rag",
    "model context protocol",
    "mcp",
    "mlops",
    "llmops",
    "context engineering",
}

PRODUCTION_TERMS = {
    "production",
    "enterprise",
    "deployment",
    "deploy",
    "evaluation",
    "evals",
    "observability",
    "monitor",
    "security",
    "guardrail",
    "sandbox",
    "gateway",
    "orchestration",
    "reliability",
    "operations",
    "best practice",
    "pattern",
}

DOC_TERMS = {
    "book": 5,
    "handbook": 5,
    "guidance": 5,
    "guide": 4,
    "roadmap": 4,
    "course": 4,
    "curriculum": 4,
    "best practice": 4,
    "playbook": 4,
    "awesome": 3,
    "learn": 3,
    "tutorial": 3,
    "cookbook": 3,
    "reference": 2,
    "resources": 2,
    "material": 2,
    "interview": 2,
    "notes": 2,
    "patterns": 2,
}

CASE_TERMS = {
    "case study": 5,
    "case studies": 5,
    "case": 3,
    "example": 3,
    "demo": 3,
    "workshop": 3,
    "lab": 2,
    "simulation": 4,
    "portfolio": 2,
    "real-world": 2,
    "project": 1,
}

TOOL_TERMS = {
    "platform",
    "framework",
    "toolkit",
    "sdk",
    "server",
    "cli",
    "observability",
    "evaluation",
    "evals",
    "sandbox",
    "security",
    "gateway",
    "orchestration",
    "deployment",
    "monitor",
    "tracing",
    "mcp",
}


def text(repo: dict) -> str:
    return " ".join([
        repo["full_name"],
        repo.get("description", ""),
        " ".join(repo.get("topics", [])),
    ]).lower()


def has_explicit_fde(repo: dict) -> bool:
    value = text(repo)
    return (
        "forward deployed" in value
        or "forward-deployed" in value
        or "forward deployment" in value
        or "forward_deployed" in value
        or re.search(r"(^|[^a-z])fde([^a-z]|$)", value) is not None
    )


def weighted_terms(value: str, terms: dict[str, int]) -> int:
    return sum(weight for term, weight in terms.items() if term in value)


def is_eligible(repo: dict) -> bool:
    value = text(repo)
    name = repo["full_name"].lower()
    if name in FORCE_INCLUDE:
        return True
    if name in BLOCKLIST or repo.get("archived") or not repo.get("description"):
        return False
    if any(term in value for term in NOISE_TERMS):
        return False
    if has_explicit_fde(repo):
        return True
    minimum_stars = 50 if repo["category"] == "case-studies" else 100
    if repo.get("stars", 0) < minimum_stars or not any(term in value for term in AI_RELEVANCE_TERMS):
        return False
    source = repo["category"]
    doc_score = weighted_terms(value, DOC_TERMS)
    case_score = weighted_terms(value, CASE_TERMS)
    tool_score = sum(1 for term in TOOL_TERMS if term in value)
    production_score = sum(1 for term in PRODUCTION_TERMS if term in value)
    if source == "learning-guides":
        return doc_score >= 3
    if source == "case-studies":
        return case_score >= 3
    if source == "best-practices":
        return doc_score >= 2 and production_score >= 1
    return tool_score >= 1 and production_score >= 1


def classify(repo: dict) -> str:
    value = text(repo)
    override = OVERRIDE_CATEGORY.get(repo["full_name"].lower())
    if override:
        return override
    direct = has_explicit_fde(repo)
    doc_score = weighted_terms(value, DOC_TERMS)
    case_score = weighted_terms(value, CASE_TERMS)
    tool_score = sum(1 for term in TOOL_TERMS if term in value)
    production_score = sum(1 for term in PRODUCTION_TERMS if term in value)
    source_category = repo["category"]
    if direct:
        if case_score >= 3:
            return "case-studies"
        if tool_score >= 2 and doc_score < 3:
            return "tools"
        if any(term in value for term in {"best practice", "playbook", "protocol", "operations", "ethics"}):
            return "best-practices"
        return "getting-started"
    if source_category == "case-studies" or case_score >= 5:
        return "case-studies"
    if source_category == "learning-guides":
        if doc_score >= 2 and production_score >= 2:
            return "best-practices"
        return "getting-started"
    if doc_score >= 7:
        return "getting-started"
    if source_category == "best-practices" or (doc_score >= 2 and production_score >= 1):
        return "best-practices"
    return "tools"


def score(repo: dict, category: str) -> tuple:
    value = text(repo)
    direct = has_explicit_fde(repo)
    forced = repo["full_name"].lower() in FORCE_INCLUDE
    doc_score = weighted_terms(value, DOC_TERMS)
    case_score = weighted_terms(value, CASE_TERMS)
    tool_score = sum(1 for term in TOOL_TERMS if term in value)
    quality = {
        "getting-started": doc_score,
        "best-practices": doc_score + tool_score,
        "case-studies": case_score + doc_score // 2,
        "tools": tool_score,
    }[category]
    return (
        forced,
        direct,
        quality,
        len(repo.get("matched_queries", [])),
        min(repo.get("stars", 0), 100000),
        repo.get("updated_at") or "",
    )


def tags(repo: dict, category: str) -> list[str]:
    value = text(repo)
    found = []
    mapping = [
        ("fde", {"forward deployed", "forward-deployed", "forward deployment", " fde"}),
        ("agents", {"agent", "agentic"}),
        ("enterprise-ai", {"enterprise ai", "enterprise-grade"}),
        ("evaluation", {"evaluation", "evals", "benchmark"}),
        ("observability", {"observability", "tracing", "monitor"}),
        ("security", {"security", "red team", "guardrail"}),
        ("sandbox", {"sandbox", "code execution"}),
        ("mcp", {"model context protocol", " mcp"}),
        ("rag", {" rag", "retrieval-augmented", "retrieval augmented"}),
        ("mlops", {"mlops", "llmops"}),
        ("learning", {"book", "guide", "course", "tutorial", "roadmap", "handbook"}),
        ("cases", {"case", "example", "demo", "workshop", "simulation"}),
    ]
    for tag, needles in mapping:
        if any(needle in value for needle in needles):
            found.append(tag)
    if not found:
        found.append(category)
    return found[:6]


def select(repositories: list[dict]) -> list[dict]:
    buckets = {category: [] for category in QUOTAS}
    for repo in repositories:
        if not is_eligible(repo) or repo["full_name"].lower() == "global-fde/awesome-global-fde":
            continue
        category = classify(repo)
        buckets[category].append(repo)
    selected = []
    for category, quota in QUOTAS.items():
        ranked = sorted(buckets[category], key=lambda repo: score(repo, category), reverse=True)
        chosen = ranked[:quota]
        if len(chosen) < quota:
            raise RuntimeError(f"Not enough eligible repositories for {category}: {len(chosen)}/{quota}")
        for repo in chosen:
            record = {
                "name": repo["full_name"],
                "url": repo["html_url"],
                "description": repo["description"].strip(),
                "category": category,
                "direct_fde": has_explicit_fde(repo),
                "tags": tags(repo, category),
                "primary_language": repo.get("language"),
                "license": repo.get("license"),
                "stars_snapshot": repo.get("stars", 0),
                "updated_at": repo.get("updated_at"),
                "why_it_matters": CATEGORY_META[category]["why"],
                "editorial_state": "candidate",
                "reviewed_on": str(date.today()),
            }
            selected.append(record)
    return selected


def markdown(selected: list[dict]) -> str:
    direct_count = sum(repo["direct_fde"] for repo in selected)
    supporting_count = len(selected) - direct_count
    lines = [
        "# FDE GitHub Repository Collection",
        "",
        "> 200 repositories for Forward Deployed Engineers, organized around learning, best practices, cases, and tools.",
        "",
        "This collection prioritizes documentation, books, handbooks, roadmaps, courses, field methods, case material, and practical production tooling. It excludes repositories where `FDE` refers to unrelated concepts such as finite-difference equations or full-disk encryption.",
        "",
        f"The current snapshot contains **{direct_count} direct FDE repositories** and **{supporting_count} supporting production-AI repositories**. Direct FDE entries are labeled below; supporting entries cover the engineering stack an FDE commonly needs in the field.",
        "",
        "Repository metadata is a snapshot and does not imply endorsement. Always review the source, license, security posture, and maintenance status before use.",
        "",
        "## Contents",
        "",
    ]
    for category, meta in CATEGORY_META.items():
        anchor = meta["title"].lower().replace(" / ", "-").replace(" ", "-")
        lines.append(f"- [{meta['title']}](#{anchor}) — {QUOTAS[category]} repositories")
    lines.extend(["", "## Selection method", "", "- Direct FDE relevance receives the highest priority.", "- Documentation, books, guides, courses, cases, and reusable practices are preferred.", "- Supporting tools must be relevant to production agents, evaluation, observability, security, MCP, RAG, context, or deployment.", "- Stars are a discovery signal, not proof of quality.", "- Metadata is maintained in [`resources/github-repositories.yml`](resources/github-repositories.yml).", ""])
    for category, meta in CATEGORY_META.items():
        repos = [repo for repo in selected if repo["category"] == category]
        lines.extend([f"## {meta['title']}", "", meta["intro"], ""])
        for repo in repos:
            stars = f" · ★ {repo['stars_snapshot']:,}" if repo["stars_snapshot"] else ""
            language = f" · {repo['primary_language']}" if repo["primary_language"] else ""
            scope = "**Direct FDE** · " if repo["direct_fde"] else ""
            lines.append(f"- {scope}[{repo['name']}]({repo['url']}){stars}{language} — {repo['description']}")
        lines.append("")
    lines.extend([
        "## Contributing",
        "",
        "To add or improve a repository, follow the [contribution guide](CONTRIBUTING.md), update the structured metadata, and open a focused pull request. Explain the concrete value to FDE practice and disclose any relationship to the project.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    raw = json.loads(INPUT.read_text(encoding="utf-8"))
    selected = select(raw["repositories"])
    counts = Counter(repo["category"] for repo in selected)
    if len(selected) != TARGET or counts != Counter(QUOTAS):
        raise RuntimeError(f"Selection invariant failed: total={len(selected)}, counts={counts}")
    payload = {
        "schema_version": 1,
        "generated_on": str(date.today()),
        "repository_count": len(selected),
        "direct_fde_count": sum(repo["direct_fde"] for repo in selected),
        "supporting_repository_count": sum(not repo["direct_fde"] for repo in selected),
        "category_counts": dict(counts),
        "selection_note": "Curated from GitHub search; prefer documentation, learning, cases, and FDE-relevant production tools.",
        "repositories": selected,
    }
    YAML_OUTPUT.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    MARKDOWN_OUTPUT.write_text(markdown(selected), encoding="utf-8")
    print(f"Selected {len(selected)} repositories: {dict(counts)}")
    print(YAML_OUTPUT)
    print(MARKDOWN_OUTPUT)


if __name__ == "__main__":
    main()
