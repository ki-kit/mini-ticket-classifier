import json
from pydantic import BaseModel, Field, field_validator
from src.config import ALLOWED_PRIORITIES

class TicketAnalysis(BaseModel):
    category: str = Field(..., min_length=1)
    priority: str
    summary: str = Field(..., min_length=1)
    recommended_action: str = Field(..., min_length=1)

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: str) -> str:
        clean_v = v.strip().lower()
        if clean_v not in ALLOWED_PRIORITIES:
            raise ValueError(f"Priority must be one of {ALLOWED_PRIORITIES}, got '{v}'")
        return clean_v

def validate_and_parse_response(raw_text: str) -> tuple[dict | None, str | None]:
    """
    Validates LLM raw output.
    Returns: (parsed_dict, error_message)
    """
    try:
        # Clean potential markdown wrappers if the LLM ignored instructions
        clean_text = raw_text.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("\n", 1)[1]
        if clean_text.endswith("```"):
            clean_text = clean_text.rsplit("\n", 1)[0]
        clean_text = clean_text.strip()

        # Parse JSON
        data = json.loads(clean_text)
        
        # Validate schema via Pydantic
        validated_data = TicketAnalysis(**data)
        return validated_data.model_dump(), None
        
    except json.JSONDecodeError as je:
        return None, f"LLM output is not valid JSON. Raw output: {raw_text[:100]}... Error: {str(je)}"
    except Exception as ve:
        return None, f"Validation constraints failed: {str(ve)}"