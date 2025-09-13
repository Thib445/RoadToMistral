
import subprocess
from fastmcp import FastMCP

# Clean port 8001 before starting
subprocess.run(['lsof', '-ti', ':8001'], capture_output=True) and subprocess.run(['kill', '-9', subprocess.run(['lsof', '-ti', ':8001'], capture_output=True, text=True).stdout.strip().split('\n')[0]], check=False)
mcp = FastMCP("Eloan Server")

def start_server():
    mcp.run(transport="http", port=8001)
    
import threading
thread = threading.Thread(target=start_server, daemon=True)
thread.start()

from pyngrok import ngrok

# Set your auth token
ngrok.set_auth_token("32duqPnT5eNRSbVwjOu0f1pUaKP_jswV2QbAoaUEfGW4R7n1")

# Open an HTTP tunnel to your local MCP server (port 8001)
public_url = ngrok.connect(8001)
print("Ngrok URL:", public_url)
