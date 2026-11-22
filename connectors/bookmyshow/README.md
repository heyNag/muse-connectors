# BookMyShow

A Muse connector for BookMyShow. Search movies and live events, read showtimes, prices and venue details.

- Display name: **BookMyShow**
- Internal Muse slug: `custom.bookmyshow`
- Version: **2026.11.22.1** (2026-11-22, second release of the day; date-based CalVer YYYY.MM.DD, with .1/.2/.3 for extra releases the same day; supersedes 2026.11.22 and the briefly-published 2026.11.0)
- No login, no API key needed. It reads public BookMyShow pages.

## Tools

`bms_get_cities`, `bms_get_movies`, `bms_get_events`, `bms_get_movie_details`, `bms_get_showtimes`, `bms_get_venue_details`, `bms_search`

See [CONNECTOR.md](CONNECTOR.md) for the full connector documentation.

## Install

There is no one-click install for Muse custom connectors yet — installing is copying the connector folder into Muse's custom-connectors folder.

```bash
# 1. Clone the repo
git clone https://github.com/heyNag/muse-connectors.git

# 2. Copy the connector into Muse's custom-connectors folder.
#    This is the install step. The folder name must be custom.bookmyshow
#    to match the id in connector.yaml.
cp -r muse-connectors/connectors/bookmyshow ~/workspace/custom-connectors/custom.bookmyshow

# 3. Set up its dependencies
cd ~/workspace/custom-connectors/custom.bookmyshow
python3 -m venv .venv
.venv/bin/pip install -r server/requirements.txt

# 4. Verify it works — this should list the 7 tools
python3 bin/client.py list-tools
```

After that, Muse discovers it as **BookMyShow** (id `custom.bookmyshow`). No login or API key is needed.

## Update

To get a new version, pull the latest from the repo and copy the connector over again:

```bash
# 1. Pull the latest version
cd muse-connectors
git pull

# 2. Copy the updated connector over the installed one
cp -r connectors/bookmyshow ~/workspace/custom-connectors/custom.bookmyshow

# 3. Re-install dependencies in case requirements changed
cd ~/workspace/custom-connectors/custom.bookmyshow
.venv/bin/pip install -r server/requirements.txt

# 4. Verify it works
python3 bin/client.py list-tools
```

Check which version you have in `connector.yaml` (`version:`) or on the [releases page](https://github.com/heyNag/muse-connectors/releases) — for example, `2026.11.22.1` is the second release of 2026-11-22.

## Uninstall

Delete the installed connector folder — that removes it from Muse:

```bash
rm -rf ~/workspace/custom-connectors/custom.bookmyshow
```

You can also delete the cloned `muse-connectors` repo if you no longer need it. There is no credential to revoke, since this connector uses no login or API key.

The MCP server source in `server/` is the public `m0han-r/bookmyshow-mcp-webscraper` repo, pinned at commit `848707a12c2679d9414fb6184b64bd9f5df57c7d` (MIT).

## Limitation

The server scrapes BookMyShow website pages (it is not an official API) and reads the data embedded in those pages. BookMyShow's Cloudflare protection can return HTTP 403 to the scraper from some machines, in which case tools return well-formed empty results even for known-live shows. An empty result is therefore not proof that an event does not exist. The browser route on BookMyShow passes Cloudflare and is the fallback for live searches and for booking. This connector cannot book tickets, select seats, or pay.
