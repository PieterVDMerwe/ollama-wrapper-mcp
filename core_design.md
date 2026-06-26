# Core Design Document: Ollama MCP Wrapper (`ollama-wrapper-mcp`)

This document governs the design, architecture, features, and security rules for the Ollama MCP Wrapper.

## 1. Intention & Scope
The primary goal is to expose local Ollama instance functionalities to the Antigravity IDE harness, enabling agent systems to use local Ollama models as backends.
* **Scope Limits**: The wrapper does not aim to expose the entire Ollama API. It is restricted to inspecting, loading, and running already downloaded models. It will not autonomously download or pull new models.

## 2. Key Features & Primitives

### 2.1 Tools
* `list_models`: Returns the list of already downloaded Ollama models on the system.
* `run_model`: Initializes or targets an active model for completion/chat.
* `generate_completion`: Requests text generation or chat completions from the active model.
* `generate_with_tools`: Exposes tool schemas to the model and processes tool execution loops for models with native tool-calling capabilities.

### 2.2 Resources
* `active_model/status`: Exposes current active model state and metadata.
* `models/list`: Lists available local models as a resource.

### 2.3 Prompts
* Custom template prompts that developers can use to bootstrap agents using this MCP server (e.g., configuring system prompts, template formats).

## 3. Architecture
* **Language**: Python (utilizing FastMCP SDK).
* **Transport**: Local STDIO (default) for integration with developer environments.
* **Backend Interaction**: Interacts directly with Ollama's local REST API (typically `http://localhost:11434`).

## 4. Security & Compliance
* **Static Scanner**: A built-in scanner to inspect incoming prompts for common prompt injection patterns (e.g., instruction override commands, system-role spoofing) before sending them to the backend model. If matched, requests must be rejected or sanitized.
* **No Uncontrolled Downloads**: No APIs or tools are exposed to pull new models from the registry.

## 5. Development Compliance
All code changes and commits must conform to these architectural boundaries. The system must not expand the API footprint beyond local Ollama integration and prompt security.
