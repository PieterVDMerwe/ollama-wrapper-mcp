# Agent Internalization Rules

* **Command Loop Prevention**: If a command or similar commands fail 2 times consecutively without resolving the error, stop execution, report the error to the user, and await instructions.
* **Ultra-Concise Communication**: Respond using the absolute minimum words necessary to convey the required information. (Exception: detailed responses are permitted for /grill-me, design alignment, and complex Q&A).
* **Bulletpoint First**: Format explanations, summaries, and updates using concise bullet points rather than paragraphs (except during interactive sessions where conversational flow is preferred).
* **Targeted File Reading**: Never read full files if specific line ranges suffice. Always specify narrow `StartLine` and `EndLine` parameters when calling file viewing tools.
* **Minimize Search Span**: Filter grep searches by specific file extensions or directories using `Includes` to avoid wide, slow, token-heavy scans.
* **Direct File Edits**: Target exact code segments using small, precise replacement blocks instead of rewriting large sections of files.
