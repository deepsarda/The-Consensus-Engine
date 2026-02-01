from typing import Dict, Any
from .base import ForensicTool
from google import genai
from google.genai import types
import os
import PIL.Image


class GeminiAnalyzer(ForensicTool):
    def analyze(self, media_path: str, claim_text: str = "") -> Dict[str, Any]:
        result = {
            "tool": "Gemini_Image_Describer",
            "description": None,
            "verdict": "Processed",
        }

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            result["verdict"] = "Skipped: No GEMINI_API_KEY found"
            result["error"] = "Missing API Key"
            return result

        try:
            client = genai.Client(api_key=api_key)

            model_name = (
                "gemini-3-flash-preview"  # "gemini-2.5-flash"  # gemini-3-flash-preview
            )

            img = PIL.Image.open(media_path)

            """prompt = (
                "Describe this image in insane detail. Mention every object, text, color, lighting, texture, and potential anomaly you see. "
                "Also search for similar images on the internet and find references to this image and tell me their outputs. The caption for this image is: "
                + claim_text
            )"""

            prompt = (
                "Act as a Forensic Image Analyst. Your goal is to look for issues in the image.\n\n"
                f'CLAIM: "{claim_text}"\n\n'
                "## Phase 1: Visual Forensics\n"
                "Describe the image with extreme precision and insane amount of details (mention every object, text, color, lighting, texture, and potential anomaly you see):\n"
                "- **Text/Language:** Extract any visible text (signs, badges, license plates) and translate if necessary.\n"
                "- **Geolocators:** Identify landmarks, architecture, street signs, or vegetation that indicate location.\n"
                "- **Temporal Indicators:** Look for car models, technology, or weather that suggest a specific time period.\n"
                "- **Manipulation Check:** Scrutinize shadows, reflections, and hands/faces for signs of AI generation or Photoshop.\n\n"
                "## Phase 2: Contextual Search\n"
                "Use your browsing tools to perform a reverse image search or search for the visual details you identified.\n"
                "- Find the **earliest known source** of this image.\n"
                "- Identify the original context (who took it, when, and where, and other information).\n"
                "- Check if this image has been debunked by fact-checkers previously.\n\n"
            )

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, img],
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                ),
            )

            chunks = response.candidates[0].grounding_metadata.grounding_chunks

            citation_links = []
            if chunks:
                for chunk in chunks:
                    if chunk.web and chunk.web.uri and chunk.web.title:
                        citation_links.append(f"- [{chunk.web.title}]({chunk.web.uri})")

            if citation_links:
                result["citations"] = "\n".join(citation_links)
            else:
                result["citations"] = "No citations found"
            text = response.text
            result["description"] = text

            result["verdict"] = "Detailed description generated"
            return result

        except Exception as e:
            print(e)
            result["error"] = str(e)
            result["verdict"] = "Error calling Gemini API"
            return result
