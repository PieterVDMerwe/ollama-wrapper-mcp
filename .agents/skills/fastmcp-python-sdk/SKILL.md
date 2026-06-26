---
name: fastmcp-python-sdk
description: Guidelines, best practices, and code examples for building Model Context Protocol (MCP) servers using the FastMCP Python SDK.
---

# FastMCP Python SDK Skill

Use this skill when developing or debugging MCP servers using FastMCP in Python.

## Core Concepts & Implementation Patterns

### 1. Initialization
Create a FastMCP server instance:
```python
from mcp.server.fastmcp import FastMCP

# recommended: json_response=True and stateless_http=True for web deployments
mcp = FastMCP("My Server Name", stateless_http=True, json_response=True)
```

### 2. Tools (`@mcp.tool()`)
Tools allow the model to take actions (side-effects or computations).
- **Type Annotations**: Return type and parameter types must be annotated. They generate the JSON Schema.
- **Context Injection**: Annotate a parameter with `Context` (e.g. `ctx: Context`) to access logging, progress, etc.
- **Structured Output**: Can return Pydantic models (`BaseModel`), `TypedDict`, `dict[str, T]`, or dataclasses.

Example:
```python
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context

class WeatherResponse(BaseModel):
    temp: float = Field(description="Temperature in Celsius")
    condition: str

@mcp.tool()
async def get_weather(city: str, ctx: Context) -> WeatherResponse:
    """Get the current weather for a city."""
    await ctx.info(f"Fetching weather for {city}")
    # Return structured output
    return WeatherResponse(temp=22.5, condition="Sunny")
```

### 3. Resources (`@mcp.resource()`)
Resources expose data/content to the model as context (read-only, no side effects).
```python
@mcp.resource("config://settings")
def get_settings() -> str:
    """Get application configuration settings."""
    return '{"theme": "dark"}'
```

### 4. Prompts (`@mcp.prompt()`)
Prompts provide reusable prompt templates that are user-controlled.
```python
@mcp.prompt()
def review_code(code: str) -> str:
    """Generate a prompt template for code review."""
    return f"Please review this code:\n\n{code}"
```

### 5. Lifespans
Manage startup and shutdown (e.g., database connections) cleanly using async context managers.
```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    # Startup: connect to db
    db = await Database.connect()
    try:
        yield {"db": db}
    finally:
        # Shutdown: cleanup
        await db.disconnect()

mcp = FastMCP("DB Server", lifespan=app_lifespan)

@mcp.tool()
def query_db(ctx: Context) -> str:
    db = ctx.request_context.lifespan_context["db"]
    return db.query()
```

### 6. Running / Transport
- **Stdio**: `mcp.run()` (default, great for local/CLI processes like Claude Desktop)
- **Streamable HTTP**: `mcp.run(transport="streamable-http")` (recommended for production/web)
- **Mounting in ASGI/Starlette**:
  ```python
  from starlette.applications import Starlette
  from starlette.routing import Mount
  
  app = Starlette(
      routes=[Mount("/mcp", app=mcp.streamable_http_app())],
      lifespan=lifespan
  )
  ```
