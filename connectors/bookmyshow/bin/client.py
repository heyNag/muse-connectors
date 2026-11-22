#!/usr/bin/env python3
"""BookMyShow stdio MCP client.

Spawns the local BookMyShow MCP server over stdio; no auth.

Usage:
    python3 bin/client.py list-tools
    python3 bin/client.py call-tool --name bms_search --arguments-file /path/to/args.json

The client runs with the connector venv python so the server's
dependencies are the isolated ones installed under .venv.
"""

import argparse
import asyncio
import importlib.util
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
VENV_PYTHON = BASE / ".venv" / "bin" / "python"
SERVER = BASE / "server" / "mcp_server.py"

# The MCP SDK lives in the connector venv, not the system python. Re-exec
# under the venv python when it is missing, so `python3 bin/client.py`
# works from any interpreter. Compare paths without resolving symlinks,
# because the venv python is a symlink to the system python. The env var
# stops a re-exec loop.
if importlib.util.find_spec("mcp") is None and VENV_PYTHON.exists():
    if os.environ.get("BMS_CLIENT_REEXEC") != "1":
        env = dict(os.environ)
        env["BMS_CLIENT_REEXEC"] = "1"
        os.execve(str(VENV_PYTHON), [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]], env)

ALLOWED_TOOLS = {
    "bms_get_cities",
    "bms_get_movies",
    "bms_get_events",
    "bms_get_movie_details",
    "bms_get_showtimes",
    "bms_get_venue_details",
    "bms_search",
}


def _dump(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "__dict__"):
        return value.__dict__
    return value


async def _run(command, name=None, arguments=None):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    if not VENV_PYTHON.exists():
        raise RuntimeError(f"connector venv python not found: {VENV_PYTHON}")
    if not SERVER.exists():
        raise RuntimeError(f"MCP server not found: {SERVER}")

    params = StdioServerParameters(
        command=str(VENV_PYTHON),
        args=[str(SERVER)],
        cwd=str(SERVER.parent),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if command == "list-tools":
                result = await session.list_tools()
                tools = [_dump(t) for t in result.tools]
                print(json.dumps({"tools": tools}, ensure_ascii=False))
                return 0
            result = await session.call_tool(name, arguments or {})
            is_error = bool(getattr(result, "is_error", False))
            payload = {
                "isError": is_error,
                "content": [_dump(c) for c in result.content],
            }
            structured = getattr(result, "structured_content", None)
            if structured is not None:
                payload["structuredContent"] = structured
            print(json.dumps(payload, ensure_ascii=False))
            return 1 if is_error else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list-tools")
    calling = subparsers.add_parser("call-tool")
    calling.add_argument("--name", required=True)
    calling.add_argument("--arguments-file", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "call-tool":
        if args.name not in ALLOWED_TOOLS:
            parser.error(
                "Inspect this operation's schema and add its exact name to ALLOWED_TOOLS"
            )
        arguments = json.loads(args.arguments_file.read_bytes())
        if not isinstance(arguments, dict):
            parser.error("arguments must be a JSON object")
    else:
        arguments = None
    try:
        return asyncio.run(_run(args.command, getattr(args, "name", None), arguments))
    except Exception as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
