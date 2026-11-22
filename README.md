# muse-connectors

A collection of Muse connectors.

## Connectors

| Connector | Description |
| --- | --- |
| [BookMyShow](connectors/bookmyshow/) | Search BookMyShow movies and live events, read showtimes, prices and venue details. |

Each connector lives in its own folder under `connectors/` and has its own README with install, update, uninstall, example usage and troubleshooting instructions.

## How it works

Each connector is a folder with a `connector.yaml` (id, title, icon, version), a `CONNECTOR.md` with the full documentation, a `bin/client.py` helper, and — for MCP-backed connectors — the server source under `server/`. To install one, copy its folder into Muse's custom-connectors folder (`~/workspace/custom-connectors/custom.<name>/`) and set up its dependencies; see the connector's own README.

## Versioning

Versions are date-based CalVer, YYYY.MM.DD, with `.1`, `.2`, `.3` appended for extra releases on the same day (for example `2026.11.22`, then `2026.11.22.1`). Each release is tagged on GitHub — see the [releases page](https://github.com/heyNag/muse-connectors/releases).

## Releases

Only the latest 2 releases are kept. Older releases are deleted automatically when a new one is published, so always install the latest. Releases and their tags are deleted, only the latest 2 remain.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a new connector. This collection is MIT licensed — see [LICENSE](LICENSE).
