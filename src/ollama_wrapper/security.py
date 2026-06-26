from .config import settings

def scan_prompt(prompt: str) -> bool:
    """
    Statically scans the prompt for common prompt injection patterns.
    Returns True if an injection pattern is detected, otherwise False.
    """
    normalized = prompt.lower()
    for keyword in settings.injection_keywords:
        if keyword in normalized:
            return True
    return False
