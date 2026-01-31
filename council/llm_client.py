import requests
import json
import os
import sys
from google import genai

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
            "max_tokens": 8000,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=360,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"\033[91mError calling OpenRouter API for model {model}: {e}\033[0m")
            return self.call_gemini_fallback(messages)

    def call_gemini_fallback(self, messages: list) -> dict:
        """
        Fallback to Gemini API when OpenRouter fails.
        Mimics the OpenAI/OpenRouter response structure.
        """
        print("\033[93m[Fallback] Attempting Gemini API Backup...\033[0m")

        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            print("No GEMINI_API_KEY found in environment.")
            return None

        try:
            client = genai.Client(api_key=gemini_key)

            # Construct a prompt from the messages list
            # Messages are usually [{"role": "system",...}, {"role": "user",...}]
            full_prompt = ""
            for msg in messages:
                role = msg.get("role", "user").upper()
                content = msg.get("content", "")
                full_prompt += f"--- {role} ---\n{content}\n\n"

            response = client.models.generate_content(
                # model="gemini-2.5-flash",
                model="gemini-3-flash-preview",
                contents=full_prompt,
                config={"response_mime_type": "application/json"},
            )

            if not response.text:
                print("Gemini returned empty response.")
                return None

            # Mimic OpenAI structure for compatibility
            return {"choices": [{"message": {"content": response.text}}]}

        except ImportError:
            print("google-genai library not installed.")
            return None
        except Exception as e:
            print(f"Gemini Fallback Error: {e}")
            return None
