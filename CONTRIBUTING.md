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
`2026.11.22.1`). Bump the version in `connector.yaml` and in the version
lines in `CONNECTOR.md` and `README.md` for every release, and tag the
release on GitHub with the same version number. Do not renumber `server/`;
it is vendored upstream at its own version.

## Releases

Only the latest 2 releases are kept. Older releases are deleted automatically
when a new one is published (see
`.github/workflows/keep-latest-releases.yml`), so always install the latest.
Releases and their tags are deleted, only the latest 2 remain.

## License

This collection is MIT licensed (see `LICENSE`). Only add connectors whose
upstream source allows redistribution, and note the upstream repo, pinned
commit and license in the connector's README.
