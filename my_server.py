import sys
print(sys.executable)


from fastmcp import FastMCP
mcp = FastMCP("Alex Server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()
