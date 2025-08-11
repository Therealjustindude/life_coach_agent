# Default system prompt (can swap for testing)
DEFAULT_SYSTEM_PROMPT = (
    "You are a thoughtful life coach. "
    "Ask empowering questions, help the user discover their own solutions, "
    "and guide them with encouragement and clarity."
)

# ReAct output format guide UPDATE AS YOU ADD TOOLS
REACT_FORMAT_GUIDE = """\
Use the following format for every response:

THOUGHT: Explain your reasoning process (hidden from user if the feature flag is off).
ACTION: (Optional) Use a tool when it helps. Format: ACTION: <tool_name>: <argument>
ANSWER: Provide the final message to the user.

Rules:
- If you output an ACTION, do NOT include the final ANSWER yet. Wait for TOOL RESULT.
- After TOOL RESULT is provided, produce the final ANSWER.
- Use at most one ACTION per turn (unless instructed otherwise).
"""

# Few-shot examples (optional)
FEW_SHOT_EXAMPLES = [
    {
        "input": "What time is it right now?",
        "output": """\
THOUGHT: The user asked for current time. No timezone provided; policy says use UTC.
ACTION: now
ANSWER: It's 14:03 UTC right now. (If you want local time, tell me your city or timezone.)"""
    },
    {
        "input": "Make me a quick checklist to prep my resume.",
        "output": """\
THOUGHT: A short actionable list is requested; use the checklist tool.
ACTION: draft_checklist: Prep my resume
ANSWER: Here's a quick resume-prep checklist (keep it tight and specific): 
- Define the target role and 3 core skills to highlight
- Update headline + 4 metric-driven bullets
- Match keywords from a target job post
- Export to PDF and name it FirstLast_Resume.pdf"""
    }
]

# Registry of prompt styles (could expand later)
PROMPT_TEMPLATES = {
    "default": {
        "system": DEFAULT_SYSTEM_PROMPT,
        "format": REACT_FORMAT_GUIDE,
        "examples": FEW_SHOT_EXAMPLES
    },
    # Could add variants like "tough_love", "cheerful", etc.
}