#!/usr/bin/env python3
"""
Shared MCP Server - Can be imported by both Python files and Jupyter notebooks
"""

from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Shared Eloan Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def greet(name: str) -> str:
    """Greet someone"""
    return f"Hello, {name}!"

@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool
def get_server_info() -> str:
    """Get server information"""
    return f"Server: {mcp.name}, Tools: {len(mcp.tools)}"

# Function to start the server
def start_server(port: int = 8004):
    """Start the MCP server"""
    print(f"Starting {mcp.name} on port {port}")
    mcp.run(transport="http", port=port)
