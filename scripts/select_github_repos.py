#!/usr/bin/env python3
"""Publish the manually curated 59-repository Global FDE catalog."""

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
TARGET = 59
MINIMUM_STARS = 50
QUOTAS = {
    "getting-started": 19,
    "best-practices": 15,
    "case-studies": 8,
    "tools": 17,
}

# Explicit editorial selection. Search discovers candidates; it never publishes
# them automatically. Keep this list short and review every addition.
CURATED_REPOSITORIES = {
    "getting-started": [
        "xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer",
        "pierpaolo28/Awesome-FDE-Roadmap",
        "mlabonne/llm-course",
        "chiphuyen/aie-book",
        "huggingface/agents-course",
        "ombharatiya/ai-system-design-guide",
        "PacktPublishing/LLM-Engineers-Handbook",
        "decodingai-magazine/llm-twin-course",
        "MLOps-Courses/mlops-coding-course",
        "paiml/practical-mlops-book",
        "Meirtz/Awesome-Context-Engineering",
        "curiousily/AI-Bootcamp",
        "ashishps1/learn-ai-engineering",
        "microsoft/mcp-for-beginners",
        "anmolksachan/AI-ML-Free-Resources-for-Security-and-Prompt-Injection",
        "dair-ai/MLOPs-Primer",
        "libaice/Awesome-FDE",
        "bryanyzhu/agentic-ai-system-course",
        "alexeygrigorev/ai-engineering-field-guide",
    ],
    "best-practices": [
        "EthicalML/awesome-production-machine-learning",
        "NirDiamant/agents-towards-production",
        "ai-boost/awesome-harness-engineering",
        "benchflow-ai/awesome-evals",
        "Puliczek/awesome-mcp-security",
        "requie/AI-Red-Teaming-Guide",
        "vllm-project/guidellm",
        "visenger/awesome-mlops",
        "lizhe2004/Awesome-LLM-RAG-Application",
        "suboss87/FDEOps",
        "NVIDIA-NeMo/Guardrails",
        "GoogleCloudPlatform/agent-starter-pack",
        "humanlayer/12-factor-agents",
        "databricks/databricks-agent-skills",
        "anthropics/cwc-long-running-agents",
    ],
    "case-studies": [
        "patchy631/ai-engineering-hub",
        "NirDiamant/GenAI_Agents",
        "ikatsov/tensor-house",
        "muratcankoylan/AI-Investigator",
        "GoogleCloudPlatform/generative-ai",
        "GURPREETKAURJETHRA/END-TO-END-GENERATIVE-AI-PROJECTS",
        "pathwaycom/llm-app",
        "Azure-Samples/AI-Gateway",
    ],
    "tools": [
        "langfuse/langfuse",
        "Arize-ai/phoenix",
        "evidentlyai/evidently",
        "promptfoo/promptfoo",
        "confident-ai/deepeval",
        "vibrantlabsai/ragas",
        "mlflow/mlflow",
        "modelcontextprotocol/servers",
        "archestra-ai/archestra",
        "langgenius/dify",
        "daytonaio/daytona",
        "langchain-ai/langgraph",
        "google/agents-cli",
        "opensandbox-group/OpenSandbox",
        "microsoft/PyRIT",
        "langwatch/scenario",
        "snyk/agent-scan",
    ],
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
    "alexeygrigorev/ai-engineering-field-guide",
    "humanlayer/12-factor-agents",
    "databricks/databricks-agent-skills",
    "anthropics/cwc-long-running-agents",
    "google/agents-cli",
    "opensandbox-group/opensandbox",
    "microsoft/pyrit",
    "langwatch/scenario",
    "snyk/agent-scan",
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
    by_name = {repo["full_name"].lower(): repo for repo in repositories}
    selected = []
    for category, names in CURATED_REPOSITORIES.items():
        if len(names) != QUOTAS[category]:
            raise RuntimeError(f"Curated count mismatch for {category}: {len(names)}/{QUOTAS[category]}")
        for name in names:
            repo = by_name.get(name.lower())
            if not repo:
                raise RuntimeError(f"Curated repository missing from discovery snapshot: {name}")
            if repo.get("archived") or repo.get("disabled"):
                raise RuntimeError(f"Curated repository is unavailable: {name}")
            if repo.get("stars", 0) < MINIMUM_STARS:
                raise RuntimeError(
                    f"Curated repository is below {MINIMUM_STARS} stars: {name} ({repo.get('stars', 0)})"
                )
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
                "editorial_state": "reviewed",
                "reviewed_on": str(date.today()),
            }
            selected.append(record)
    return selected


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
        "minimum_stars": MINIMUM_STARS,
        "selection_note": "Manually curated for relevance, maintenance, adoption, field evidence, and practical value.",
        "repositories": selected,
    }
    YAML_OUTPUT.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
    print(f"Selected {len(selected)} repositories: {dict(counts)}")
    print(YAML_OUTPUT)


if __name__ == "__main__":
    main()
