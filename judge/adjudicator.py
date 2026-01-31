import json
from typing import List, Dict, Any
from council.llm_client import LLMClient
import config
from utils.reply_processing import process_content_return_ouput_json
import datetime

JUDGE_PROMPT = """
### Role: The Adjudicator Agent

**Date: ** {curent_date}
You are the final Judge in a misinformation consensus system.
You have received analysis from 3 different AI models (The Council) regarding a claim and forensic evidence.

**Your Goal:**
1.  **Evaluate Reasoning:** Critique the reasoning of each model.
2.  **Filter Models:**
    *   **DISCARD** models that hallucinate evidence, use subjective logic (e.g., "it looks cool"), or ignore clear forensic data.
    *   **KEEP** models that correctly cite the provided Forensic Evidence (Deepfake scores, Search results, CLIP scores).
    *   *Note: Ignore Deepfake_Detector outputs for non-face images.*
3.  **Aggregate Confidence:** Calculate the average confidence of only the VALID models.
4.  **Synthesize Explanation:** Write a final user-facing verdict following the specific guidelines below.

**Explanation Generation Guidelines:**
*   **Nuance is Critical:** You must distinguish between "Fake Media" (AI/Photoshop) and "Misattributed Media" (Real photo, wrong caption).
*   **If Misattributed:** Explicitly state: "The media is real/authentic, but the caption/context is false." Explain the true origin versus the claimed origin.
*   **If Accurate:** Provide an in-depth verification. Don't just say "It's true"—explain the specific date, location, and event confirming the caption.
*   **Context:** Always provide broader background context about the image and the claim.
*   **Formatting:** Use Markdown (bolding, lists) to structure the text for readability.

**Forensic Evidence Provided:**
{forensic_evidence}

**Council Opinions:**
{council_outputs}

**Output strictly in JSON:**
(Ensure all Markdown in the 'explanation' field is properly escaped for JSON, e.g., use \n for newlines)

{{
  "model_evaluations": [
    {{
      "model": "Model A",
      "status": "KEEP/DISCARD",
      "reason": "Cited search evidence correctly regarding the original date of the image."
    }}
  ],
  "final_verdict": "Real/Misinformation/Inconclusive/Mislabeled",
  "aggregated_confidence": 98.5,
  "explanation": "## Verdict: Mislabeled\n\n### Analysis\nAlthough the image is **authentic** and has not been digitally altered, it is being shared with a false narrative.\n\n* **True Context:** The image was actually taken in [Year] at [Location].\n* **Claimed Context:** The caption incorrectly claims this shows [False Event].\n\n### Conclusion\nThe media is real, but the attribution is false."
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

        today = datetime.date.today()
        prompt = JUDGE_PROMPT.format(
            forensic_evidence=formatted_forensics,
            council_outputs=formatted_council,
            curent_date=today.strftime("%B %d, %Y"),
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
