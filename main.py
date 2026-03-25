#!/usr/bin/env python3
# upgoerfivemcp Source Code
# word_checker_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import re

import words
WORDS = words.WORDS
app = Server("word-checker")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="check_words",
            description="returns words to be reworded according to the upgoer five word list",
            inputSchema={
                "type": "object",
                "properties": {
                    "sentence": {"type": "string", "description": "word to check"}
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

    def mark_word(match):
        word = match.group(0)
        if word.lower() not in WORDS:
            return word + "❌"
        return word

    result = re.sub(r"[a-zA-Z']+", mark_word, sentence)
    return [TextContent(type="text", text=f'"{result}"')]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    print("Starting word checker server...")
    asyncio.run(main())