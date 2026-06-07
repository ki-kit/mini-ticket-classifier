from src.config import ALLOWED_PRIORITIES

SYSTEM_PROMPT = f"""You are an advanced IT support and incident ticket classification assistant. 
Your task is to analyze the provided support ticket and extract structured information.

You MUST respond strictly with a valid JSON object matching this schema:
{{
  "category": "string",
  "priority": "low | medium | high | critical",
  "summary": "string",
  "recommended_action": "string"
}}

Rules:
1. The JSON must be clean and valid. Do not wrap it in markdown codeblocks (e.g., do not use ```json).
2. The 'priority' property MUST be exactly one of these values: {', '.join(ALLOWED_PRIORITIES)}.
3. Rely only on the provided text. Keep summaries and actions concise.
"""

def get_user_prompt(ticket_text: str) -> str:
    return f"Analyze the following support ticket:\n\n\"\"\"\n{ticket_text}\n\"\"\""