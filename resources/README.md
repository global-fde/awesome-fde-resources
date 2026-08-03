# Resource data

[`github-repositories.yml`](github-repositories.yml) is the machine-readable source for the 50 repositories listed in both language versions of the README.

Publication rules:

- manual editorial selection;
- demonstrated relevance, maintenance, adoption, or field evidence;
- direct value to FDE or production AI delivery;
- one of `getting-started`, `best-practices`, `case-studies`, or `tools`;
- no archived, disabled, duplicate, or description-less repositories.

Search candidates are produced by [`discover_github_repos.py`](../scripts/discover_github_repos.py). Only repositories explicitly added to `CURATED_REPOSITORIES` in [`select_github_repos.py`](../scripts/select_github_repos.py) are published.

External resources remain under their owners' licenses.
