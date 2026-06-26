# Ollama MCP Wrapper

A Python-based Model Context Protocol (MCP) server wrapping local Ollama capabilities. This allows AI agents to interface with local language models, query tags, generate text, and execute tool-calling sequences under strict prompt injection static sanitization.

## File Structure

```text
├── .agents/             # Agent rules & skills
├── src/
│   └── ollama_wrapper/  # Package source
│       ├── __init__.py
│       ├── config.py    # Configuration defaults
│       ├── security.py  # Prompt injection scanner
│       └── server.py    # FastMCP server
├── tests/               # Pytest testing suites
└── pyproject.toml       # Python dependencies
```

## Setup & Running

### Requirements
* [uv](https://docs.astral.sh/uv/) for Python environment management.
* [Ollama](https://ollama.com/) running locally (defaults to `http://localhost:11434`).

### Running the Server
To run the server locally via standard I/O (STDIO):
```bash
$env:PYTHONPATH="src"
uv run python -m ollama_wrapper.server
```

### Running Tests
To run the unit tests:
```bash
uv run pytest
```
