#!/usr/bin/env python3
# upgoerfivemcp Source Code
# word_checker_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

WORDS = set("""understandings|understanding|conversations|disappearing|
your|is|a|the|and|or|but|in|on|at|to|for|of|with|it|this|that""".replace("\n","").split("|"))

app = Server("word-checker")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="check_words",
            description="Check which words in a sentence are not in the allowed list",
            inputSchema={
                "type": "object",
                "properties": {
                    "sentence": {"type": "string", "description": "The sentence to check"}
                },
                "required": ["sentence"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name != "check_words":
        raise ValueError(f"Unknown tool: {name}")

    sentence = arguments["sentence"]
    # Strip punctuation and lowercase
    import re
    words = re.findall(r"[a-zA-Z']+", sentence.lower())
    failed = [w for w in words if w not in WORDS]

    result = json.dumps({"failed": failed})
    return [TextContent(type="text", text=result)]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    print("Starting word checker server...")
    asyncio.run(main())