# Global FDE Hosted Library

The hosted library contains original or explicitly authorized material that
the community can review, improve, translate, and preserve in version control.

## Categories

- `guides/` — original methods and learning paths;
- `templates/` — reusable field artifacts and checklists;
- `cases/` — authorized, anonymized deployment cases and postmortems;
- `reports/` — original Global FDE research and reports;
- `translations/` — translations published with the rights holder's permission.

## Current hosted resources

### Reports

- [FDE Deployment in China Whitepaper 2026 (Chinese preview)](reports/fde-deployment-in-china-whitepaper-preview-2026-zh-CN.pdf) — 崔牛会研究院, 15 pages.

### Guides

- [How to Become an FDE Engineer (Chinese key notes)](guides/how-to-become-an-fde-engineer-notes-zh-CN.pdf) — 张子峰 ARK, 5 pages.

Each PDF has a neighboring `.source.yml` record containing attribution, integrity hash, permission basis, and review status.

## Required source record

Every hosted resource must include a neighboring source record based on
[`SOURCE_TEMPLATE.yml`](SOURCE_TEMPLATE.yml). The record documents authorship,
provenance, permission, license, sensitivity review, and maintainer review.

## Rights policy

You may submit material when at least one of the following is true:

1. you own the work and agree to publish it under the repository license;
2. the work already uses a compatible open license and attribution is preserved;
3. the rights holder has given explicit permission for this repository to host
   and modify the material, and that permission is documented.

Do not upload a resource merely because it is downloadable or free to read.
When rights are unclear or restrictive, add a curated external link instead.

## Privacy and field safety

Before submission, remove or authorize:

- customer and employee names;
- personal data and contact details;
- credentials, tokens, internal URLs, and security-sensitive configuration;
- source code, screenshots, contracts, pricing, or metrics covered by an NDA;
- claims that could identify a customer through indirect details.

Anonymization must preserve the technical lesson without exposing the field.

## File formats

Prefer Markdown and source-controlled diagrams. PDF may be included for a
designed report when the editable source or a Markdown equivalent is also
available. Avoid large binary files, video, raw datasets, and proprietary
formats unless the repository maintainers approve a clear preservation need.

## Review

Hosted material receives a higher review bar than an external link. Maintainers
may request evidence of rights, further anonymization, technical review, or an
external-link-only contribution.
