from typing import Any

def format_tool_for_ollama(mcp_tool: dict[str, Any]) -> dict[str, Any]:
    """
    Formats a standard MCP tool schema (which might have name, description, inputSchema)
    into Ollama tool schema format.
    """
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.get("name"),
            "description": mcp_tool.get("description", ""),
            "parameters": mcp_tool.get("inputSchema", {
                "type": "object",
                "properties": {},
                "required": []
            })
        }
    }
