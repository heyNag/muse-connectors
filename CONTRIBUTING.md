# Contributing

This repo is a collection of Muse connectors. Each connector lives in its
own folder under `connectors/` and they share
the versioning scheme below. Releases and tags are repo-wide: one version
line for the whole repo at a time.

## Adding a new connector

Create a folder `connectors/<name>/` with:

- `README.md` — what the connector does, plus Install, Update, Uninstall,
  Example usage and Troubleshooting sections.
- `CONNECTOR.md` — the full connector documentation: how it connects, its
  tools, credentials, limits and generic verification notes only — no
  personal test cases, dates, shows, prices, or event codes.
- `connector.yaml` — `id: "custom.<name>"`, `title`, `description`,
  `icon: icon.png`, `aliases`, `include_in_prompt: true`,
  `require_auth: true` or `false`.
- `bin/client.py` — the helper that exposes the server's tools as
  `list-tools` and `call-tool` commands.
- `server/` — the MCP server source, if the connector is MCP-backed, with
  its upstream repo and pinned commit noted in the README.
- `icon.png` — the connector's icon.

The folder name, the `connector.yaml` `id`, and the installed folder name
`~/workspace/custom-connectors/custom.<name>/` must all match.

## Versioning

Versions are date-based CalVer, YYYY.MM.DD, with `.1`, `.2`, `.3` appended
for extra releases on the same day (for example `2026.11.22`, then
`2026.11.22.1`). The Manual release workflow computes the next version
and bumps it in `connector.yaml` and in the version lines in
`CONNECTOR.md` and `README.md`, commits the bump, and tags the release
on GitHub — do not bump versions by hand. Do not renumber `server/`;
it is vendored upstream at its own version.

## Releases

Releases are created only through the Manual release workflow: GitHub
repo → Actions → "Manual release" → Run workflow, and enter notes
(leave the version empty and the workflow computes the next one
automatically, or enter a version to override it). Do not create a release directly from the GitHub web UI, the
`gh` command line, or the API — that bypasses the workflow's version,
tag, and version-file checks. This is a convention, not an enforcement —
GitHub cannot block direct release creation; the workflow is the path we
use. The release workflow runs the keep-latest-2 cleanup itself at the
end, because a release it creates does not trigger other workflows —
so the cleanup that keeps only the latest 2 releases still happens.

Only the latest 2 releases are kept. Older releases are deleted automatically
when a new one is published (see
`.github/workflows/keep-latest-releases.yml`), so always install the latest.
Releases and their tags are deleted, only the latest 2 remain.

## License

This collection is MIT licensed (see `LICENSE`). Only add connectors whose
upstream source allows redistribution, and note the upstream repo, pinned
commit and license in the connector's README.
