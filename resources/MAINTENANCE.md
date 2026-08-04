# Catalog maintenance

This repository uses editorial review rather than automatic publication.
GitHub search discovers candidates; a maintainer reads and verifies every
resource before it enters the public catalog.

## Weekly discovery

The `Candidate discovery` workflow runs weekly and can also be started
manually. It uploads a workflow artifact containing the latest search snapshot.
It never commits candidates or changes the public README.

Review the artifact for:

- direct relevance to FDE or a production-AI delivery decision;
- first-party evidence, reusable field practice, or a working implementation;
- recent maintenance and durable access;
- security, license, and commercial-interest context;
- overlap with an existing entry.

Stars are a discovery signal, not a substitute for editorial judgment.

## Add a GitHub repository

1. Add the repository to `EDITORIAL_SEEDS` when broad search does not reliably
   discover it.
2. Add its canonical `owner/repository` name to the appropriate list in
   `CURATED_REPOSITORIES`.
3. Increase the matching value in `QUOTAS`.
4. Run discovery to refresh `resources/github-candidates.json`.
5. Run selection to refresh `resources/github-repositories.yml`.
6. Add one factual English description to `README.md` and one factual Chinese
   description to `README.zh-CN.md`, in the same catalog order.
7. Run the checks below before opening a pull request.

```bash
python scripts/validate_catalog.py
npx --yes awesome-lint
```

## Remove or archive an entry

Remove an entry when its canonical source disappears, the repository becomes
archived without durable reference value, its scope changes materially, or
new evidence invalidates the original reason for inclusion.

Update the curated list, quota, structured catalog, and both README sections in
one pull request. Explain the reason in the pull request; do not silently swap
one project for another to preserve a fixed count.

## Review record

For each published repository, retain:

- canonical URL and repository name;
- star and update snapshots;
- category and direct-FDE status;
- tags and practical relevance;
- editorial state and review date.

The structured catalog is an auditable snapshot, not a live ranking.
