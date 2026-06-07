import os

# Ollama configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")

# Validation Constraints
ALLOWED_PRIORITIES = ["low", "medium", "high", "critical"]