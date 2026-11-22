# BookMyShow

A Muse connector for BookMyShow. Search movies and live events, read showtimes, prices and venue details.

- Display name: **BookMyShow**
- Internal Muse slug: `custom.bookmyshow`
- Version: **2026.11.22.7** (date-based CalVer YYYY.MM.DD, with .1/.2/.3 for extra releases the same day)
- No login, no API key needed. It reads public BookMyShow pages.

## Tools

`bms_get_cities`, `bms_get_movies`, `bms_get_events`, `bms_get_movie_details`, `bms_get_showtimes`, `bms_get_venue_details`, `bms_search`

See [CONNECTOR.md](CONNECTOR.md) for the full connector documentation.

## Example usage

Once installed, ask Muse things like:

- "Search BookMyShow for a comedy show in Hyderabad"
- "What movies are playing in Hyderabad?"
- "What comedy shows are on in Bengaluru this weekend?"

To call a tool directly, write the arguments as a JSON file and pass it with `--arguments-file`:

```bash
cd ~/workspace/custom-connectors/custom.bookmyshow
echo '{"query": "standup comedy", "city": "hyderabad"}' > search.json
python3 bin/client.py call-tool --name bms_search --arguments-file search.json
```

## Install

There is no one-click install for Muse custom connectors yet — installing is copying the connector folder into Muse's custom-connectors folder.

Python 3.10+ required (tested with Python 3.12.3); dependencies are listed in `server/requirements.txt`. Note: upstream claims Python 3.9+, but that is untested for this connector.

```bash
# 1. Clone the repo (if the folder already exists, skip cloning)
cd ~ && git clone https://github.com/heyNag/muse-connectors.git

# 2. Copy the connector into Muse's custom-connectors folder.
#    This is the install step. The folder name must be custom.bookmyshow
#    to match the id in connector.yaml. Remove any previous copy first,
#    so a re-install does not copy the folder inside itself.
mkdir -p ~/workspace/custom-connectors
rm -rf ~/workspace/custom-connectors/custom.bookmyshow
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
cd ~/muse-connectors
git pull

# 2. Copy the updated connector over the installed one. Remove the
#    previous copy first, so the copy does not land inside itself.
#    This also removes the old .venv, so step 3 recreates it.
mkdir -p ~/workspace/custom-connectors
rm -rf ~/workspace/custom-connectors/custom.bookmyshow
cp -r connectors/bookmyshow ~/workspace/custom-connectors/custom.bookmyshow

# 3. Re-install dependencies in case requirements changed
cd ~/workspace/custom-connectors/custom.bookmyshow
python3 -m venv .venv
.venv/bin/pip install -r server/requirements.txt

# 4. Verify it works
python3 bin/client.py list-tools
```

Check which version you have in `connector.yaml` (`version:`) or on the [releases page](https://github.com/heyNag/muse-connectors/releases).

## Uninstall

Delete the installed connector folder — that removes it from Muse:

```bash
rm -rf ~/workspace/custom-connectors/custom.bookmyshow
```

You can also delete the cloned `muse-connectors` repo if you no longer need it. There is no credential to revoke, since this connector uses no login or API key.

The MCP server source in `server/` is the public `m0han-r/bookmyshow-mcp-webscraper` repo, pinned at commit `848707a12c2679d9414fb6184b64bd9f5df57c7d` (MIT). Note: `server/` is vendored upstream at its own version 1.0.0; the connector's version is the CalVer one in `connector.yaml`. Its badges refer to the upstream repo. Upstream has no LICENSE file in its repo at the pinned commit; attribution is to Mohan R (`m0han-r/bookmyshow-mcp-webscraper`), MIT as stated in its `pyproject.toml` and README. `server/` is vendored upstream and its install instructions are upstream's own, not this connector's install path — follow this README instead.

## Troubleshooting

- **`list-tools` fails with `RuntimeError: connector venv python not found: …`** — the venv was never created. This happens when `mcp` is installed system-wide but `.venv` was never created in the installed folder, so the client cannot re-exec into it. From the installed connector folder, run `python3 -m venv .venv`, then `.venv/bin/pip install -r server/requirements.txt`, then try `python3 bin/client.py list-tools` again.
- **`list-tools` fails with `ModuleNotFoundError`** — the dependencies are not installed in the venv. From the installed connector folder, re-run `.venv/bin/pip install -r server/requirements.txt`, then try `python3 bin/client.py list-tools` again.
- **Tools return empty lists** — most likely BookMyShow's Cloudflare protection returned HTTP 403 to the scraper from your machine. An empty result is not proof that an event does not exist. Use the browser route on BookMyShow for live searches instead.
- **Muse does not discover the connector** — check that the installed folder is exactly `~/workspace/custom-connectors/custom.bookmyshow`, matching the `id: "custom.bookmyshow"` in `connector.yaml`, and that `connector.yaml` is present in that folder.

## Limitation

The server scrapes BookMyShow website pages (it is not an official API) and reads the data embedded in those pages. BookMyShow's Cloudflare protection can return HTTP 403 to the scraper from some machines, in which case tools return well-formed empty results even for known-live shows. An empty result is therefore not proof that an event does not exist. The browser route on BookMyShow passes Cloudflare and is the fallback for live searches and for booking. This connector cannot book tickets, select seats, or pay. The bundled FastAPI server and web dashboard are not used by this connector; if you run them, review their CORS settings first. The dashboard loads Google Fonts and FontAwesome from CDNs, uses via.placeholder.com fallback images, and builds cards with innerHTML from scraped titles.
