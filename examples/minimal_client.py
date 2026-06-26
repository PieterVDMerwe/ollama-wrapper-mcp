import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define the server connection parameters
# We use 'uv' to run our server inside the virtual environment
server_params = StdioServerParameters(
    command="uv",
    args=["run", "python", "-m", "ollama_wrapper.server"],
    env={
        "PYTHONPATH": "src",
        "PATH": os.environ.get("PATH", "")
    }
)

async def run():
    print("Connecting to Ollama MCP server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()
            print("Connected successfully!\n")

            # 1. List available local models
            print("Calling 'list_local_models'...")
            models = await session.call_tool("list_local_models", arguments={})
            print(f"Available Models: {models.content[0].text}\n")

            # 2. Check running models
            print("Calling 'list_running_models'...")
            running_models = await session.call_tool("list_running_models", arguments={})
            print(f"Running Models: {running_models.content[0].text}\n")

            # 3. Request a text completion
            # Replace 'qwen2.5-coder:1.5b' with a model you have downloaded
            target_model = "qwen2.5-coder:1.5b"
            prompt = "Why is the sky blue? Answer in 1 sentence."
            
            print(f"Calling 'run_model_completion' with model '{target_model}'...")
            result = await session.call_tool(
                "run_model_completion", 
                arguments={"model_name": target_model, "prompt": prompt}
            )
            print(f"Result: {result.content[0].text}\n")

if __name__ == "__main__":
    asyncio.run(run())
