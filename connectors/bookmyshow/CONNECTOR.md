# BookMyShow

- `custom.bookmyshow` connects Muse to BookMyShow through a local stdio MCP server that scrapes the public BookMyShow website. It needs no login and no API key.

- The server source lives in `connectors/bookmyshow/server/` at pinned commit `848707a12c2679d9414fb6184b64bd9f5df57c7d` of the public repo at `https://github.com/m0han-r/bookmyshow-mcp-webscraper.git`. The repo is MIT licensed.

- Helpers live in `connectors/bookmyshow/bin/`. The helper is `client.py` and it spawns the MCP server as a child process and exposes its tools as `list-tools` and `call-tool` commands.

- The display name is BookMyShow and the icon is `icon.png` in this folder. The icon is the BookMyShow "my" ticket logo — a white ticket with red "my" on a red background, 400x400 PNG.

## Version

- Current version: **2026.11.22.4**
- Versions are date-based CalVer, YYYY.MM.DD, with .1, .2, .3 appended for extra releases on the same day.

## Connect

- There is no credential to connect. The scraper only reads public pages on `https://in.bookmyshow.com` and sends no login or payment details.

- Create a venv and install `server/requirements.txt` (see README Install); tested with Python 3.12.3.

- Verify the connector works with a harmless read:

Run these commands from the installed folder:

```text
cd ~/workspace/custom-connectors/custom.bookmyshow
python3 bin/client.py list-tools
```

- The client re-execs itself under the venv python when the MCP SDK is missing from the system python. Run it with plain `python3` as shown above.

## Credentials

- This connector uses no credential. This connector uses no key, token, password or cookie.

- This connector never asks for a BookMyShow password or one-time code; booking and sign-in stay in the browser.

## List tools

- Use `list-tools` to see the tools the server offers, with each tool's input schema.

```text
python3 bin/client.py list-tools
```

- The server offers exactly these 7 tools.

```text
bms_get_cities
bms_get_movies
bms_get_events
bms_get_movie_details
bms_get_showtimes
bms_get_venue_details
bms_search
```

- Write each call's arguments as one JSON object in a file and pass that file with `--arguments-file`. Keep credentials out of that file because this connector uses none. Every call needs an arguments file, even a call with no arguments — use a file containing `{}`.

## Get cities

- Get supported cities and regions with their codes and URL slugs. This is a read.

```text
python3 bin/client.py call-tool --name bms_get_cities --arguments-file cities.json
```

- The arguments file holds one object with an optional `popular_only` boolean. With `popular_only` set to true the tool returns only the 10 popular cities. Example:

```json
{"popular_only": true}
```

- Returns the popular cities (e.g. Hyderabad, HYD / hyderabad). The scraper falls back to a hardcoded popular cities list when its page fetch fails, so a working cities result does not prove live scraping works.

## Get movies in a city

- Get active movie listings in a city with optional language and genre filters. This is a read.

```text
python3 bin/client.py call-tool --name bms_get_movies --arguments-file movies-hyd.json
```

- The arguments file holds one object with `city` as a slug such as hyderabad or bengaluru or mumbai (optional, defaults to `mumbai`) and optional `language` and `genre` strings. Example:

```json
{"city": "hyderabad", "language": "Hindi", "genre": "Comedy"}
```

- The result is a list of movie summaries with title and code and languages and genres and a price range when the page supplies one.

## Get events in a city

- Get live events in a city with an optional category filter. This is a read and it is the tool to use for comedy shows and concerts.

```text
python3 bin/client.py call-tool --name bms_get_events --arguments-file events-hyd-comedy.json
```

- The arguments file holds one object with `city` as a slug (optional, defaults to `mumbai`) and optional `category` as one of events or comedy-shows or music-shows or sports. Example:

```json
{"city": "hyderabad", "category": "comedy-shows"}
```

- The result is a list of event summaries with title and code and date and venue name when the page supplies them.

## Search movies and events

- Search active movie titles and live event listings in one city for a query string. This is a read.

```text
python3 bin/client.py call-tool --name bms_search --arguments-file search-hyd.json
```

- The arguments file holds one object with a required `query` string and `city` as a slug (optional, defaults to `mumbai`). The tool searches only the movies and events lists the scraper fetched for that city, so it finds nothing when those lists come back empty. Example:

```json
{"query": "standup comedy", "city": "hyderabad"}
```

- The result holds two lists named `movies` and `events` with matching titles and codes.

## Get movie details

- Get synopsis and metadata for one movie by its BookMyShow code or its full page URL. This is a read.

```text
python3 bin/client.py call-tool --name bms_get_movie_details --arguments-file details-bng.json
```

- The arguments file holds one object with a required `movie_code` string (the code shown on the event page, or a full BookMyShow movie page URL) and `city` as a slug (optional, defaults to `mumbai`). Example:

```json
{"movie_code": "ET00378770", "city": "mumbai"}
```

- The result holds title and code and synopsis and duration and censor rating and rating score and languages and genres and poster and banner URLs and trailers and cast and crew when the page supplies them.

## Get showtimes

- Get cinema venues and showtimes for one movie code in a city on a date. This is a read.

```text
python3 bin/client.py call-tool --name bms_get_showtimes --arguments-file showtimes-bng.json
```

- The arguments file holds one object with a required `movie_code` string (or a full BookMyShow buy-tickets URL) and `city` as a slug (optional, defaults to `mumbai`) and optional `date` in YYYYMMDD or YYYY-MM-DD form and optional `language` and `format` strings. The language value `all` aggregates all languages. Example:

```json
{"movie_code": "ET00378770", "city": "chennai", "date": "20260827", "language": "tamil", "format": "2D"}
```

- The result is a list of venues with venue code and name and showtimes and screen formats and price ranges and seat availability when the page supplies them.

## Get venue details

- Get address and location details for one cinema venue by its BookMyShow venue code or its full page URL. This is a read.

```text
python3 bin/client.py call-tool --name bms_get_venue_details --arguments-file venue.json
```

- The arguments file holds one object with a required `venue_code` string such as PCAN (or a full BookMyShow venue page URL) and `city` as a slug (optional, defaults to `mumbai`). Example:

```json
{"venue_code": "PCAN", "city": "chennai"}
```

- The result holds venue name and street address and postal code and latitude and longitude and facilities such as parking and food court and M-Ticket when the page supplies them.

## Recover from errors

- A call that returns `isError` true means the tool itself failed. The client exits with status 1 and prints the tool error. Read the error before retrying the call.

- A call that returns an empty list or an empty object with `isError` false means the scraper fetched nothing usable. Check whether the live site is reachable from your machine before you treat an empty result as proof that no event exists.

- A 403 from BookMyShow means Cloudflare blocked the scraper request. Retrying the same call will not help and trying to bypass the block is out of scope for this connector. Use the browser route on BookMyShow instead, because a real browser passes the check.

## Limits

- BookMyShow's Cloudflare protection can return HTTP 403 to the scraper from some machines. The tools still run and return well-formed empty results instead of erroring, so an empty result from this connector does not prove that an event does not exist.

- The connector cannot book tickets and cannot select seats and cannot add to a cart and cannot pay. Booking stays with the browser route on BookMyShow.

- The connector cannot sign in to BookMyShow and cannot read a signed in account or past bookings.

- Each client call spawns a fresh MCP server process, so the scraper's in-memory cache of 300 seconds does not persist across calls. The scraper timeout is 12 seconds per page fetch.

- Only the stdio MCP server is supported by this connector; the bundled REST server/CLI are untested.
