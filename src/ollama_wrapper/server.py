import httpx
from mcp.server.fastmcp import FastMCP, Context
from ollama_wrapper.config import settings
from ollama_wrapper.security import scan_prompt
from ollama_wrapper.tools_helper import format_tool_for_ollama
from ollama_wrapper.prompts import get_prompt_value
from mcp.server.fastmcp.prompts import base

# Initialize FastMCP Server
mcp = FastMCP("Ollama-Wrapper", stateless_http=True, json_response=True)

# Store active model state locally in the server session/state
class ServerState:
    active_model: str | None = None

state = ServerState()

@mcp.tool()
async def list_local_models(ctx: Context) -> list[dict]:
    """
    List all local models currently downloaded in the Ollama instance.
    """
    await ctx.info("Fetching local Ollama models...")
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            response = await client.get(f"{settings.ollama_host}/api/tags")
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])
            return [
                {
                    "name": m.get("name"),
                    "size": m.get("size"),
                    "family": m.get("details", {}).get("family"),
                    "parameter_size": m.get("details", {}).get("parameter_size"),
                }
                for m in models
            ]
        except Exception as e:
            await ctx.error(f"Failed to fetch models from Ollama: {str(e)}")
            raise RuntimeError(f"Could not connect to Ollama at {settings.ollama_host}: {e}")

@mcp.tool()
async def run_model_completion(model_name: str, prompt: str, ctx: Context) -> dict:
    """
    Run text generation completion on a specific local model.
    """
    # Security Compliance check
    if scan_prompt(prompt):
        await ctx.error("Prompt injection pattern detected. Request blocked.")
        return {"error": "Prompt blocked by static security scanner."}
    
    await ctx.info(f"Running completion on model: {model_name}...")
    state.active_model = model_name
    
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
            response = await client.post(f"{settings.ollama_host}/api/generate", json=payload)
            response.raise_for_status()
            result = response.json()
            return {
                "model": model_name,
                "response": result.get("response"),
                "done": result.get("done")
            }
        except Exception as e:
            await ctx.error(f"Failed to execute completion on model {model_name}: {str(e)}")
            raise RuntimeError(f"Error communicating with Ollama: {e}")

@mcp.resource("active-model://status")
def get_active_model_status() -> str:
    """
    Get the status of the currently loaded active model.
    """
    if state.active_model:
        return f"Active model: {state.active_model}"
    return "No model has been run yet."

@mcp.tool()
async def generate_with_tools(model_name: str, messages: list[dict], tools: list[dict], ctx: Context) -> dict:
    """
    Execute chat generation with a list of tools exposed to the model.
    """
    # Security Compliance check on all user inputs
    for msg in messages:
        if msg.get("role") == "user" and scan_prompt(msg.get("content", "")):
            await ctx.error("Prompt injection pattern detected in chat messages. Request blocked.")
            return {"error": "Prompt blocked by static security scanner."}

    await ctx.info(f"Running tool-calling completions on model: {model_name}...")
    formatted_tools = [format_tool_for_ollama(t) for t in tools]

    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            payload = {
                "model": model_name,
                "messages": messages,
                "tools": formatted_tools,
                "stream": False
            }
            response = await client.post(f"{settings.ollama_host}/api/chat", json=payload)
            response.raise_for_status()
            result = response.json()
            return {
                "message": result.get("message", {}),
                "done": result.get("done")
            }
        except Exception as e:
            await ctx.error(f"Failed to execute tool-completion on model {model_name}: {str(e)}")
            raise RuntimeError(f"Error communicating with Ollama: {e}")

@mcp.tool()
async def list_running_models(ctx: Context) -> list[dict]:
    """
    List all models currently loaded and running in memory (RAM/VRAM).
    """
    await ctx.info("Checking running Ollama models...")
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            response = await client.get(f"{settings.ollama_host}/api/ps")
            response.raise_for_status()
            data = response.json()
            models = data.get("models", [])
            return [
                {
                    "name": m.get("name"),
                    "size": m.get("size"),
                    "vram": m.get("size_vram"),
                    "expires_at": m.get("expires_at")
                }
                for m in models
            ]
        except Exception as e:
            await ctx.error(f"Failed to check running models: {str(e)}")
            raise RuntimeError(f"Error communicating with Ollama: {e}")

@mcp.tool()
async def stop_model(model_name: str, ctx: Context) -> dict:
    """
    Stop and unload a specific model from memory (RAM/VRAM).
    """
    await ctx.info(f"Unloading model {model_name} from memory...")
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        try:
            payload = {
                "model": model_name,
                "prompt": "",
                "keep_alive": 0
            }
            # Sending an empty prompt with keep_alive=0 unloads the model
            response = await client.post(f"{settings.ollama_host}/api/generate", json=payload)
            response.raise_for_status()
            if state.active_model == model_name:
                state.active_model = None
            return {"status": "success", "message": f"Model {model_name} has been successfully unloaded."}
        except Exception as e:
            await ctx.error(f"Failed to unload model {model_name}: {str(e)}")
            raise RuntimeError(f"Error communicating with Ollama: {e}")

@mcp.prompt()
def agent_bootstrap(role: str) -> list[base.Message]:
    """System prompt blueprint for setting up an autonomous reasoning agent."""
    return get_prompt_value("agent-bootstrap", {"role": role})

@mcp.prompt()
def code_assistant(language: str = "python") -> list[base.Message]:
    """Configure Ollama model specifically for robust programming assistance."""
    return get_prompt_value("code-assistant", {"language": language})

if __name__ == "__main__":
    mcp.run()
