---
name: mcp-protocol-specs
description: Specifications, messages, architecture, connection lifecycles, and error codes for the Model Context Protocol (MCP).
---

# MCP Protocol Specs Skill

Use this skill when designing, debugging, or analyzing lower-level Model Context Protocol (MCP) integrations, JSON-RPC communication, or transport layers.

## Core Protocol Architecture

MCP establishes a 1:1 client-server connection within a host application (such as Claude Desktop or an IDE).

```
Host (e.g. IDE) <--> Client <== Transport (JSON-RPC 2.0) ==> Server
```

### Transports
1. **Stdio Transport**: Communicates via standard input/output streams. Ideal for local server processes.
2. **Streamable HTTP Transport (Recommended for Web)**: Exposes endpoints for HTTP POST (client-to-server) and Server-Sent Events (SSE) (server-to-client).
3. **SSE Transport**: The traditional Server-Sent Events transport.

## Connection Lifecycle

1. **Initialization**:
   - Client sends `initialize` request containing protocol version and client capabilities.
   - Server returns `initialize` response containing protocol version, server capabilities, and server information.
   - Client sends `initialized` notification as acknowledgment.
2. **Message Exchange**: Normal request-response or notification flows (e.g., `tools/list`, `tools/call`, `resources/list`, etc.).
3. **Termination**:
   - Clean shutdown via client/server connection close.
   - Sudden transport disconnect or protocol-level errors.

## Message Types (JSON-RPC 2.0)

- **Requests**:
  ```json
  {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "add",
      "arguments": { "a": 1, "b": 2 }
    }
  }
  ```
- **Responses (Success)**:
  ```json
  {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
      "content": [
        { "type": "text", "text": "3" }
      ]
    }
  }
  ```
- **Responses (Error)**:
  ```json
  {
    "jsonrpc": "2.0",
    "id": 1,
    "error": {
      "code": -32601,
      "message": "Method not found"
    }
  }
  ```

## Standard Error Codes

MCP reserves the standard JSON-RPC 2.0 error codes and allows custom codes above `-32000`:
- `ParseError = -32700`
- `InvalidRequest = -32600`
- `MethodNotFound = -32601`
- `InvalidParams = -32602`
- `InternalError = -32603`
