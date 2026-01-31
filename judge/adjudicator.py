import json
from typing import List, Dict, Any
from council.llm_client import LLMClient
import config
from utils.reply_processing import process_content_return_ouput_json

JUDGE_PROMPT = """
### Role: The Adjudicator Agent
You are the final Judge in a misinformation consensus system.
You have received analysis from 3 different AI models (The Council) regarding a claim and forensic evidence.

**Your Goal:**
1. Evaluate the reasoning of each model.
2. Discard models that hallucinate evidence or use subjective logic (e.g., "it looks cool").
3. Keep models that cite the provided Forensic Evidence (Deepfake scores, Search results, CLIP scores).
4. Aggregate the confidence of the VALID models.
5. Write a final explanation based ONLY on valid reasoning.

**Forensic Evidence Provided:**
{forensic_evidence}

**Council Opinions:**
{council_outputs}

**Output strictly in JSON:**
{{
  "model_evaluations": [
    {{
      "model": "Model A",
      "status": "KEEP/DISCARD",
      "reason": "Cited search evidence correctly."
    }},
    ...
  ],
  "final_verdict": "Real/Misinformation/Inconclusive",
  "aggregated_confidence": 98.5,
  "explanation": "Final user-facing text..."
}}
"""


class JudgeAgent:
    def __init__(self):
        self.client = LLMClient()
        self.model = config.MODEL_JUDGE_NAME

    def adjudicate(
        self, forensic_data: Dict[str, Any], council_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        # Filter out errors first
        valid_inputs = [
            res for res in council_results if "error" not in res and "output" in res
        ]

        if not valid_inputs:
            return {"error": "All council members failed."}

        # Prepare prompt
        formatted_forensics = json.dumps(forensic_data, indent=2)
        formatted_council = json.dumps(valid_inputs, indent=2)

        prompt = JUDGE_PROMPT.format(
            forensic_evidence=formatted_forensics, council_outputs=formatted_council
        )

        messages = [
            {
                "role": "system",
                "content": "You are the Chief Adjudicator. Be critical and objective.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat_completion(self.model, messages)

        if not response or "choices" not in response:
            return {"error": "Judge failed to adjudicate."}

        try:
            content = response["choices"][0]["message"]["content"]
            print("Judge Unedited Content: ", content)

            return process_content_return_ouput_json(content, "Judge Agent")
        except Exception as e:
            return {"error": f"Judge processing error: {str(e)}"}
