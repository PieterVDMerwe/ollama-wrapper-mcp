from mcp.server.fastmcp.prompts import base

def get_prompts_list() -> list[dict]:
    """
    Returns list of custom prompts/templates exposed by this server.
    """
    return [
        {
            "name": "agent-bootstrap",
            "description": "System prompt blueprint for setting up an autonomous reasoning agent.",
            "arguments": [
                {
                    "name": "role",
                    "description": "Specific persona or job role (e.g. Developer, Analyst).",
                    "required": True
                }
            ]
        },
        {
            "name": "code-assistant",
            "description": "Configure Ollama model specifically for robust programming assistance.",
            "arguments": [
                {
                    "name": "language",
                    "description": "Target programming language (e.g., python, javascript).",
                    "required": False
                }
            ]
        }
    ]

def get_prompt_value(name: str, arguments: dict[str, str] | None = None) -> list[base.Message]:
    """
    Generate prompt messages based on prompt templates and user arguments.
    """
    args = arguments or {}
    if name == "agent-bootstrap":
        role = args.get("role", "General Assistant")
        system_instructions = (
            f"You are an AI agent acting as a {role}.\n"
            "Your decisions must be logical, step-by-step, and comply with strict safety rules."
        )
        return [
            base.UserMessage(content=system_instructions)
        ]
    elif name == "code-assistant":
        lang = args.get("language", "any programming language")
        system_instructions = (
            f"You are a Senior Software Engineer specializing in {lang}.\n"
            "Provide clean, well-commented code, adhere to industry standards, and write unit tests."
        )
        return [
            base.UserMessage(content=system_instructions)
        ]
    else:
        raise ValueError(f"Prompt template {name} not found.")
