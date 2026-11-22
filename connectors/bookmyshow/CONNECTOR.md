# BookMyShow

- `custom.bookmyshow` connects Muse to BookMyShow through a local stdio MCP server that scrapes the public BookMyShow website. It needs no login and no API key.

- The server source lives in `connectors/bookmyshow/server/` at pinned commit `848707a12c2679d9414fb6184b64bd9f5df57c7d` of the public repo at `https://github.com/m0han-r/bookmyshow-mcp-webscraper.git`. The repo is MIT licensed and was created on 2026-08-26 with 11 commits and 2 stars and no releases at the time it was checked.

- Helpers live in `connectors/bookmyshow/bin/`. The helper is `client.py` and it spawns the MCP server as a child process and exposes its tools as `list-tools` and `call-tool` commands.

- The display name is BookMyShow and the icon is `icon.png` in this folder. The icon is the BookMyShow "my" ticket logo — a white ticket with red "my" on a red background, 400x400 PNG.

## Version

- Current version: **2026.11.0**, released 2026-11-22 — the first release.
- Versions follow Charms' calendar scheme, YEAR.MONTH.RELEASE (for example 2026.11.0, then 2026.11.1 for the next change).

## Connect

- There is no credential to connect. The scraper only reads public pages on `https://in.bookmyshow.com` and sends no login or payment details.

- Dependencies live in an isolated venv at `connectors/bookmyshow/.venv/`. They were installed from `server/requirements.txt` on 2026-11-22 with Python 3.12.3. Installed versions include mcp 2.3.0 and requests 2.34.2 and beautifulsoup4 4.15.0 and fastapi 0.165.0 and pydantic 2.14.4 and pandas 3.1.1 and httpx 0.28.1.

- The scaffold script in the custom connector skill refused to run because no credential is registered for this connector. The connector files were created by hand from the skill templates instead.

- Before the first use in a conversation, prove access with a harmless read:

```text
python3 connectors/bookmyshow/bin/client.py list-tools
```

- The client re-execs itself under the venv python when the MCP SDK is missing from the system python. Run it with plain `python3` as shown above.

## Credentials

- This connector uses no credential. Helpers never put a key or token or password or cookie in this doc or a helper or a command argument or an environment variable or a log.

- Never ask the user to paste a BookMyShow password or one time code in chat for this connector. Booking and sign in stay with the browser route.

## List tools

- List every tool the server offers and read each input schema before calling a tool the task needs.

```text
python3 connectors/bookmyshow/bin/client.py list-tools
```

- Verified on 2026-11-22 that the server offers exactly these 7 tools. Add a new tool to `ALLOWED_TOOLS` in `client.py` only after you have reviewed its name and schema.

```text
bms_get_cities
bms_get_movies
bms_get_events
bms_get_movie_details
bms_get_showtimes
bms_get_venue_details
bms_search
```

- Write each call's arguments as one JSON object in a file and pass that file with `--arguments-file`. Keep credentials out of that file because this connector uses none.

## Get cities

- Get supported cities and regions with their codes and URL slugs. This is a read.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_get_cities --arguments-file /tmp/bms-args/cities.json
```

- The arguments file holds one object with an optional `popular_only` boolean. With `popular_only` set to true the tool returns only the 10 popular cities.

- Verified on 2026-11-22 that this tool returns the 10 popular cities including Hyderabad with code HYD and slug hyderabad. The scraper falls back to a hardcoded popular cities list when its page fetch fails, so a working cities result does not prove live scraping works.

## Get movies in a city

- Get active movie listings in a city with optional language and genre filters. This is a read.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_get_movies --arguments-file /tmp/bms-args/movies-hyd.json
```

- The arguments file holds one object with `city` as a slug such as hyderabad or bengaluru or mumbai and optional `language` and `genre` strings.

- The result is a list of movie summaries with title and code and languages and genres and a price range when the page supplies one.

## Get events in a city

- Get live events in a city with an optional category filter. This is a read and it is the tool to use for comedy shows and concerts.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_get_events --arguments-file /tmp/bms-args/events-hyd-comedy.json
```

- The arguments file holds one object with `city` as a slug and optional `category` as one of events or comedy-shows or music-shows or sports.

- The result is a list of event summaries with title and code and date and venue name when the page supplies them.

## Search movies and events

- Search active movie titles and live event listings in one city for a query string. This is a read.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_search --arguments-file /tmp/bms-args/search-djc-hyd.json
```

- The arguments file holds one object with a required `query` string and `city` as a slug. The tool searches only the movies and events lists the scraper fetched for that city, so it finds nothing when those lists come back empty.

- The result holds two lists named `movies` and `events` with matching titles and codes.

## Get movie details

- Get synopsis and metadata for one movie by its BookMyShow code or its full page URL. This is a read.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_get_movie_details --arguments-file /tmp/bms-args/details-bng.json
```

- The arguments file holds one object with a required `movie_code` string such as ET00519382 and `city` as a slug.

- The result holds title and code and synopsis and duration and censor rating and rating score and languages and genres and poster and banner URLs and trailers and cast and crew when the page supplies them.

## Get showtimes

- Get cinema venues and showtimes for one movie code in a city on a date. This is a read.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_get_showtimes --arguments-file /tmp/bms-args/showtimes-bng.json
```

- The arguments file holds one object with a required `movie_code` string and `city` as a slug and optional `date` in YYYYMMDD or YYYY-MM-DD form and optional `language` and `format` strings. The language value `all` aggregates all languages.

- The result is a list of venues with venue code and name and showtimes and screen formats and price ranges and seat availability when the page supplies them.

## Get venue details

- Get address and location details for one cinema venue by its BookMyShow venue code or its full page URL. This is a read.

```text
python3 connectors/bookmyshow/bin/client.py call-tool --name bms_get_venue_details --arguments-file /tmp/bms-args/venue.json
```

- The arguments file holds one object with a required `venue_code` string such as PCAN and `city` as a slug.

- The result holds venue name and street address and postal code and latitude and longitude and facilities such as parking and food court and M-Ticket when the page supplies them.

## Recover from errors

- A call that returns `isError` true means the tool itself failed. The client exits with status 1 and prints the tool error. Do not replay the call until you have read the error.

- A call that returns an empty list or an empty object with `isError` false means the scraper fetched nothing usable. Check whether the live site is reachable from this machine before you treat an empty result as proof that no event exists.

- A 403 from BookMyShow means Cloudflare blocked the scraper request. Retrying the same call will not help and trying to bypass the block is out of scope for this connector. Use the browser route on BookMyShow instead, because a real browser passes the check.

- After a failed or timed out change, check the current state with a read before trying again, because the first request may have completed. This connector has no write operations, so this rule applies only if a write tool is added later.

## Limits

- Live scraping is currently blocked on this machine. BookMyShow returned HTTP 403 from Cloudflare for every page the scraper fetched on 2026-11-22, including the movies list and the events list and the ET00519382 event page. The tools still run and return well formed empty results instead of erroring, so an empty result from this connector does not prove that an event does not exist.

- The connector cannot book tickets and cannot select seats and cannot add to a cart and cannot pay. Booking stays with the browser route on BookMyShow.

- The connector cannot sign in to BookMyShow and cannot read a signed in account or past bookings.

- Each client call spawns a fresh MCP server process, so the scraper in memory cache of 300 seconds does not persist across calls. The scraper timeout is 12 seconds per page fetch.

- The FastAPI REST server and the web dashboard and the CLI in the source repo were not set up or tested. Only the stdio MCP server through `client.py` is verified.

- The repo unit tests were not run. Label them untested.

## Test results for 29 November 2026

- The test case was Dear Jim Carrey by Rajasekhar Mamidanna in Hyderabad on Sunday 29 November 2026 for 2 adults.

- On 2026-11-22 the connector returned no Hyderabad 29 November Dear Jim Carrey event and no URL and no event code. Search for Dear Jim Carrey in Hyderabad returned empty movies and empty events. Search for Rajasekhar Mamidanna in Hyderabad returned empty movies and empty events. Events in Hyderabad with category comedy-shows returned an empty list.

- The same empty result came back for the Bengaluru control, where a live event is known to exist. Search for Dear Jim Carrey in Bengaluru returned empty. Events in Bengaluru with category comedy-shows returned an empty list. Showtimes for ET00519382 in Bengaluru on 20261122 returned an empty list. Movie details for ET00519382 returned title Unknown with all fields empty. Venue details for PCAN in Chennai returned an empty object.

- The known Bengaluru event is Dear Jim Carrey by Rajasekhar Mamidanna on Sunday 22 November 2026 at 18:00 at The Koramangala Club in Bengaluru at `https://in.bookmyshow.com/events/rajasekhar-mamidanna-live/ET00519382` with Early Bird at 499 rupees sold out and Regular at 699 rupees and Phase 1 at 999 rupees. That event was verified through the browser and through web search, not through this connector.

- Because the connector returns empty even for a known live event, its empty Hyderabad result is not proof that the Hyderabad show does not exist. The reliable evidence that no Hyderabad 29 November link exists yet comes from the browser probe of BookMyShow search and the Hyderabad 29 November listings and from the Instagram bio links, which still show only the 21 November and 22 November Bengaluru shows.

## Related skills

- [Event Tickets](/opt/muse/skills/event-tickets/SKILL.md)

- Use `muse.skill_search` to find other skills and `muse.connector_search` to find other connectors.
