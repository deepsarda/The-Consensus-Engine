import requests
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class LLMClient:

    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.OPENROUTER_API_KEY
        self.base_url = config.OPENROUTER_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://consensus-engine.local",  # Required by OpenRouter
            "X-Title": "The Consensus Engine",
            "Content-Type": "application/json",
        }

    def chat_completion(
        self, model: str, messages: list, temperature: float = 0.7
    ) -> dict:

        if not self.api_key:
            print("WARNING: No OpenRouter API Key provided.")
            return None

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=120,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling OpenRouter API for model {model}: {e}")
            if response is not None:
                print(f"Response content: {response.text}")
            return None