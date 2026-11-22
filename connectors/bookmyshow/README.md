# BookMyShow

A Muse connector for BookMyShow. Search movies and live events, read showtimes, prices and venue details.

- Display name: **BookMyShow**
- Internal Muse slug: `custom.bookmyshow`
- No login, no API key needed. It reads public BookMyShow pages.

## Tools

`bms_get_cities`, `bms_get_movies`, `bms_get_events`, `bms_get_movie_details`, `bms_get_showtimes`, `bms_get_venue_details`, `bms_search`

See [CONNECTOR.md](CONNECTOR.md) for the full connector documentation.

## Install from GitHub

```bash
git clone https://github.com/heyNag/muse-connectors.git
cd muse-connectors/connectors/bookmyshow
python3 -m venv .venv
.venv/bin/pip install -r server/requirements.txt
python3 bin/client.py list-tools
```

The MCP server source in `server/` is the public `m0han-r/bookmyshow-mcp-webscraper` repo, pinned at commit `848707a12c2679d9414fb6184b64bd9f5df57c7d` (MIT).

## Limitation

The server scrapes BookMyShow website pages (it is not an official API) and reads the data embedded in those pages. BookMyShow's Cloudflare protection can return HTTP 403 to the scraper from some machines, in which case tools return well-formed empty results even for known-live shows. An empty result is therefore not proof that an event does not exist. The browser route on BookMyShow passes Cloudflare and is the fallback for live searches and for booking. This connector cannot book tickets, select seats, or pay.
