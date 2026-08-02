# Contributing to Awesome Global FDE

Thank you for helping build a useful knowledge base for Forward Deployed
Engineers. We value a small number of well-explained resources more than a
large directory of links.

## What belongs here

A resource should satisfy most of the following criteria:

- **Direct FDE relevance** — it changes how practitioners discover, scope,
  build, deploy, secure, operate, evaluate, or scale real systems.
- **Field evidence** — it contains original experience, architecture,
  constraints, outcomes, data, or a clearly explained method.
- **Practitioner utility** — another FDE can reuse the lesson or decision.
- **Credible source** — prefer first-party documentation, original research,
  named practitioners, standards bodies, and primary case studies.
- **Durable access** — the canonical link is public and likely to remain
  available.
- **Honest framing** — limitations, uncertainty, and commercial relationships
  are clear.

## What does not belong here

- affiliate or referral links;
- SEO pages assembled from other sources;
- generic AI news without a deployment lesson;
- title-only uses of “FDE” that do not involve hands-on delivery;
- vendor landing pages without technical or field substance;
- unverified claims, scraped personal data, or confidential customer material;
- duplicate resources or links without an explanation of their value.

## Before submitting

1. Search the README and existing pull requests for duplicates.
2. Read the resource in full.
3. Link to the canonical source, not a repost or search-result page.
4. Write one concise sentence explaining why it matters to an FDE.
5. Disclose any relationship to the author, employer, product, or organization.
6. Place the entry in the most specific section and preserve alphabetical order
   where practical.

## Entry format

```markdown
- [Resource title](https://canonical.example/resource) — What an FDE will learn
  or be able to do differently after reading it.
```

Descriptions should be factual, specific, and free of promotional adjectives.

## Choose a contribution type

### A. Curated external link

Use this route when the source already has a canonical public home.

1. Add the resource to the appropriate README section.
2. Add its structured record to [`resources/links.yml`](resources/links.yml).
3. Link to the original author, repository, publisher, company, or standards body.
4. Do not copy the resource into this repository unless its license explicitly
   permits it and hosting creates clear community value.

For a GitHub repository, also check
[`resources/github-repositories.yml`](resources/github-repositories.yml) for
duplicates. A submission should identify one of these categories:

- `getting-started`
- `best-practices`
- `case-studies`
- `tools`

State whether the project is directly about FDE or supports a specific part of
the production-AI delivery stack. Generic AI lists and projects with only a
title-level connection to FDE will not be accepted.

### B. Hosted Global FDE resource

Use this route for an original or explicitly authorized guide, report,
template, checklist, field note, transcript, or anonymized case.

1. Read the [`library` policy](library/README.md).
2. Put the content in the appropriate `library/` category.
3. Include a source record using [`library/SOURCE_TEMPLATE.yml`](library/SOURCE_TEMPLATE.yml).
4. Remove customer secrets, personal information, credentials, and unapproved
   commercial details.
5. Confirm that the submitter owns the content or has documented permission to
   release it under a compatible license.

Public access is not the same as permission to republish. If rights are unclear,
submit an external link instead.

## Pull request scope

Prefer one resource or one tightly related group per pull request. A focused
pull request makes verification, discussion, and attribution easier.

Your pull request should include:

- the resource category;
- why it matters to FDE practice;
- evidence type: first-party documentation, research, case study, field note,
  tool, course, book, or role description;
- language and geographic or regulatory context where relevant;
- conflict-of-interest disclosure, including “none.”

## Books, reports, and paid resources

Paid resources may be listed when they are unusually useful and clearly
identified as paid. Link to the author's or publisher's canonical page. Do not
upload or link to unauthorized copies.

## Jobs and opportunities

The main list may link to durable organization career pages or role families.
Short-lived individual openings should use a future dedicated opportunity
channel rather than accumulating as dead links in the README.

## Review process

Maintainers assess submissions for relevance, evidence quality, utility,
source quality, durability, and undisclosed promotion. Inclusion is editorial,
not automatic, and does not imply endorsement by Global FDE.

By contributing, you agree that your contribution may be released under the
repository's [Apache License 2.0](LICENSE).
