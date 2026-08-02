# Resource Model

Awesome Global FDE maintains two complementary kinds of knowledge.

## 1. Curated external links

Use an external link when a resource already has a trustworthy canonical home.
The original author keeps ownership and updates; Global FDE provides curation,
context, classification, and discovery.

Each selected resource should have:

- a canonical URL;
- title and author or organization;
- language and publication or last-reviewed date;
- evidence type and topic tags;
- a concise explanation of FDE relevance;
- access and license notes where known;
- conflict-of-interest disclosure.

Structured records live in [`links.yml`](links.yml). The human-readable list in
the main README remains the public editorial surface.

### GitHub repository catalog

The larger discovery index is published as
[`GITHUB_REPOSITORIES.md`](../GITHUB_REPOSITORIES.md), backed by
[`github-repositories.yml`](github-repositories.yml). It currently contains 200
repositories classified as getting started, best practices, cases, or tools.
Each record declares whether it is directly about FDE or a supporting part of
the production-AI stack.

The catalog is generated from a GitHub API snapshot by
[`discover_github_repos.py`](../scripts/discover_github_repos.py) and
[`select_github_repos.py`](../scripts/select_github_repos.py). Generated
metadata is marked `candidate` until a maintainer performs a deeper editorial
review. A GitHub search match, star count, or catalog entry does not constitute
endorsement.

## 2. Hosted resources

Use the hosted library for original, community-authored, or explicitly licensed
material that benefits from version control and collaborative improvement.

Examples include:

- discovery and scoping templates;
- evaluation plans and deployment checklists;
- original field notes and anonymized postmortems;
- reusable diagrams and workshop materials;
- Global FDE research and translations published with permission.

See the [`library` policy](../library/README.md) before submitting files.

## Editorial states

| State | Meaning |
| --- | --- |
| `candidate` | Suggested but not fully reviewed |
| `reviewed` | Source, relevance, and description verified by a maintainer |
| `featured` | Strong starting point with unusual practitioner value |
| `archived` | Retained for history but no longer current or maintained |

## Core tags

- `role-and-career`
- `field-discovery`
- `delivery`
- `production-ai`
- `agents`
- `evaluation`
- `observability`
- `security`
- `governance`
- `adoption`
- `case-study`
- `china`

Add a new tag only when existing tags cannot express a durable distinction.
