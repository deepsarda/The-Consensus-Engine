import os
import load_env # This unused is fine, it loads .env variables into os.environ

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

MODEL_A_NAME = "tngtech/deepseek-r1t2-chimera:free"
MODEL_B_NAME = "arcee-ai/trinity-large-preview:free"
MODEL_C_NAME = "deepseek/deepseek-r1-0528:free"
MODEL_JUDGE_NAME = "tngtech/deepseek-r1t2-chimera:free"
# Fallback model if specific ones aren't available/working or for testing
FALLBACK_MODEL = "deepseek/deepseek-r1-0528:free"