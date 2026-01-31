from typing import Dict, List, Any
import json
import concurrent.futures
from .llm_client import LLMClient
from .prompts import MASTER_PROMPT
from utils.reply_processing import process_content_return_ouput_json
import sys
import os
import re
import config
from datetime import date

# Thinking regex
thinking_regex = re.compile(r"<think>.*?</think>", re.DOTALL)


class CouncilMember:
    def __init__(self, name: str, model_id: str, client: LLMClient):
        self.name = name
        self.model_id = model_id
        self.client = client

    def evaluate(
        self, claim: str, media_type: str, forensic_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sends the claim and forensic data to this specific LLM member.
        """
        today = date.today()
        formatted_forensics = json.dumps(forensic_data, indent=2)
        prompt = MASTER_PROMPT.format(
            name=self.name,
            current_date=today.strftime("%B %d, %Y"),
            actual_user_claim=claim,
            media_type=media_type,
            actual_forensic_data_dump=formatted_forensics,
        )

        messages = [
            {
                "role": "system",
                "content": "You are a member of a misinformation forensic council. Output strictly in JSON.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat_completion(self.model_id, messages)

        if not response or "choices" not in response:
            return {"error": f"Model {self.name} failed to respond."}

        content = response["choices"][0]["message"]["content"]
        print(f"Unedited Content for {self.name}: ", content)

        return process_content_return_ouput_json(content, self.name)


class Council:
    def __init__(self):
        self.client = LLMClient()
        self.members = [
            CouncilMember("The Analyst", config.MODEL_A_NAME, self.client),
            CouncilMember("The Critic", config.MODEL_B_NAME, self.client),
            CouncilMember("The Optimist", config.MODEL_C_NAME, self.client),
        ]

    def convene(
        self, claim: str, media_type: str, forensic_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Runs all council members in parallel.
        """
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_member = {
                executor.submit(
                    member.evaluate, claim, media_type, forensic_data
                ): member
                for member in self.members
            }

            for future in concurrent.futures.as_completed(future_to_member):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"error": str(e)})

        return results
