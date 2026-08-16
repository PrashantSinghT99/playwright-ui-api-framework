# Migration Record

## Source repositories

- `git@github.com:PrashantSinghT99/playwright-python.git`
- `git@github.com:PrashantSinghT99/api-playwright-python.git`

The repositories had unrelated Git roots. The modernization branch starts from
`playwright-python/master` and contains a merge commit whose second parent is
`api-playwright-python/master`. This preserves all 27 source commits in one graph without copying
old API files into the new architecture.

Useful history commands:

```bash
git log --graph --oneline --all
git log api-origin/master
git show api-origin/master:src/tests/test_get_products.py
git log ui-origin/master
```

## What changed

| Legacy pattern | Modern replacement |
| --- | --- |
| Standalone scripts launching browsers | pytest-playwright lifecycle fixtures |
| Hard-coded URLs and headed/slow execution | validated environment settings, headless default |
| Selectors and assertions mixed in scripts | behavior-focused page objects plus tests |
| API calls repeated in tests | domain API client and typed contracts |
| Shared mutable dictionaries/test order | unique data and cleanup registries |
| Committed videos, screenshots, HTML, cache | ignored run artifacts published by CI only |
| Separate UI and API resume projects | one risk-layered quality engineering framework |

## Legacy archive policy

`legacy/playwright-python/` is a temporary, read-only review snapshot of the former working tree.
It is excluded from tools and is not part of the new test suite. The API learning files remain in
the preserved API parent history and do not need a second snapshot.

After the modern suite is reviewed, remove `legacy/` in a dedicated cleanup commit. That action is
safe for source history because every old file remains available through `ui-origin/master` and the
pre-modernization commits.

## Recommended remote decision

Keep `playwright-python` as the surviving GitHub repository, update its description/topics, and
archive or delete `api-playwright-python` only after the modernization branch is merged and visible
remotely. A repository redirect is preferable to immediate deletion if existing resume links may
still be in circulation.
