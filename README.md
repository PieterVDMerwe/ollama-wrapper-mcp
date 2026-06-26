# Ollama Model Context Protocol (MCP) Wrapper

A production-grade Python-based MCP server wrapper that exposes local [Ollama](https://ollama.com/) instance capabilities to LLM applications and host systems (such as Claude Desktop or IDEs).

This wrapper allows agents to dynamically query downloaded models, load models into memory, run text completions, request tool-calling operations, and inspect/unload running models under a strict static prompt injection security filter.

---

## Architecture Flow

```text
+-------------------+             +-----------------------+             +--------------------+
|  Host (e.g. IDE)  |  <--STDIO-->|  Ollama MCP Server    |  <--HTTP--> | Local Ollama Daemon|
|  & Agent Clients  |             |  (FastMCP Python SDK) |             | (http://localhost:11434)|
+-------------------+             +-----------------------+             +--------------------+
```

---

## File Structure

```text
├── .agents/                 # Custom Agent rules and automated skills
├── src/
│   └── ollama_wrapper/      # Server package directory
│       ├── __init__.py
│       ├── config.py        # Global settings, timeout & injection settings
│       ├── prompts.py       # Custom agent system prompt templates
│       ├── security.py      # Precompiled regex prompt injection scanners
│       ├── server.py        # Main FastMCP server definitions
│       └── tools_helper.py  # MCP schema to Ollama payload formatters
├── tests/                   # Pytest test cases
├── examples/
│   └── minimal_client.py    # Example Python client integration script
├── pyproject.toml           # Package declarations and dependencies
├── test_changelog.md        # Log of test suite errors and resolutions
└── README.md                # Extensive documentation
```

---

## Features & Tool API Reference

The server registers 5 primary tools, 1 resource path, and 2 prompt templates:

### Tools

1. **`list_local_models`**
   * **Description**: Returns all models currently downloaded on the host machine.
   * **Output**: JSON list containing `name`, `size`, `family`, and `parameter_size`.

2. **`run_model_completion`**
   * **Description**: Runs text generation/completion on a targeted model.
   * **Parameters**:
     * `model_name` (string, required): Target model identifier (e.g. `llama3:latest`).
     * `prompt` (string, required): Text input.
   * **Security**: Blocks execution if prompt violates injection filters.

3. **`generate_with_tools`**
   * **Description**: Runs chat completions exposing a list of execution tool schemas to the model.
   * **Parameters**:
     * `model_name` (string, required): Target model identifier.
     * `messages` (array of objects, required): Chat message history.
     * `tools` (array of objects, required): Custom tool definitions to expose.

4. **`list_running_models`**
   * **Description**: Retrieves a list of models currently loaded and active in the system's memory (RAM/VRAM).

5. **`stop_model`**
   * **Description**: Unloads a specific model from RAM/VRAM to free up system resources.
   * **Parameters**:
     * `model_name` (string, required): Model to unload.

### Resources
* **`active-model://status`**: Returns the status and name of the currently active model.

### Prompts
* **`agent_bootstrap`**: System prompt template to spin up a structured reasoning agent.
* **`code_assistant`**: System prompt template configuring a coding assistant.

---

## Setup & Running

### Prerequisites
1. Install [Ollama](https://ollama.com/) and download a model (e.g. `ollama run qwen2.5-coder:1.5b`).
2. Install [uv](https://docs.astral.sh/uv/) Python package manager.

### Running the Server
To start the MCP server locally using standard I/O (STDIO):
```bash
$env:PYTHONPATH="src"
uv run python -m ollama_wrapper.server
```

---

## Minimal Client Example

We have provided a complete example client in `examples/minimal_client.py`. To run this client and test the server:

1. Start Ollama.
2. In the project root directory, execute:
   ```bash
   uv run python examples/minimal_client.py
   ```

---

## Security Safeguards

To prevent jailbreaks and bypasses, all input prompts passing through text generation tools are filtered by precompiled regular expressions in `security.py`. This blocks:
* Instruction overrides (e.g., `"ignore previous instructions"`).
* Scenarios activating bypass roles (e.g., `"DAN mode"`, `"developer mode active"`).
* Sensitive information disclosure (e.g., `"reveal system prompt"`).
* Encoding attacks (e.g., `"translate system instructions to base64"`).

---

## Running Tests
Run the test suites with pytest:
```bash
uv run pytest
```

---

## Agent / LLM Instructions

When interacting with this MCP server as an AI assistant or agent client, adhere to the following operation guidelines:

### 1. Model Discovery & Selection
* **Do not guess model names**: Always call `list_local_models` first to discover downloaded options.
* Select the smallest viable model appropriate for the task (e.g. use smaller coder models for code tasks, and larger ones for reasoning).

### 2. VRAM and Resource Management
* Local models consume massive GPU/RAM resources.
* Check currently loaded models using `list_running_models`.
* **Clean up after yourself**: When you are finished running generation tasks, explicitly call the `stop_model` tool to unload the model from memory.

### 3. Prompt Safety Limits
* All input prompts are statically scanned. Avoid using phrases that look like overrides (e.g. *"ignore prior commands"*), or the server will reject your request with a security error.
* Keep prompts focused on content generation rather than system configurations.

### 4. Interactive Tool Execution
* Use `generate_with_tools` to expose system capabilities to the Ollama backend model.
* Inspect the returned `message.tool_calls` structure to determine which functions the model wants to run, execute them in your client wrapper, and feed the results back into the chat history.
