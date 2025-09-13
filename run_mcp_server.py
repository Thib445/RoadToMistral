#!/usr/bin/env python3
"""
MCP Server - Run this file to start the MCP server
"""

from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
