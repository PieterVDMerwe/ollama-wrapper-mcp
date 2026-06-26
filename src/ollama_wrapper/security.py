import re
from ollama_wrapper.config import settings

# Pre-compiled regex patterns for common injection and jailbreak structures
INJECTION_PATTERNS = [
    # Override keywords
    re.compile(r"ignore\s+(?:the\s+)?(?:above|previous)\s+instructions?", re.IGNORECASE),
    re.compile(r"system\s+(?:prompt\s+)?override", re.IGNORECASE),
    re.compile(r"disregard\s+(?:all\s+)?guidelines?", re.IGNORECASE),
    # Jailbreak / Roleplay modes
    re.compile(r"(?:acting|playing)\s+as\s+a\s+.*without\s+(?:any\s+)?restrictions?", re.IGNORECASE),
    re.compile(r"(?:dan|jailbreak)\s+mode", re.IGNORECASE),
    # Information disclosure
    re.compile(r"(?:reveal|leak|show|print)\s+(?:your\s+)?system\s+(?:prompt|instructions?)", re.IGNORECASE),
    # Command styling / encoding tricks to bypass filters
    re.compile(r"translate\s+system\s+prompt\s+to\s+(?:base64|hex|rot13)", re.IGNORECASE),
]

def scan_prompt(prompt: str) -> bool:
    """
    Statically scans the prompt for common prompt injection and jailbreak patterns.
    Returns True if an injection pattern is detected, otherwise False.
    """
    # 1. Check keyword-based matches
    normalized = prompt.lower()
    for keyword in settings.injection_keywords:
        if keyword in normalized:
            return True
            
    # 2. Check regex-based structural matches
    for pattern in INJECTION_PATTERNS:
        if pattern.search(prompt):
            return True
            
    return False
