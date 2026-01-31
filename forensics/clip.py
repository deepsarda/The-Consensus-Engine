from typing import Dict, Any
from .base import ForensicTool
import os
from transformers import CLIPProcessor, CLIPModel, logging
import torch
import PIL.Image


class SemanticAlignment(ForensicTool):
    def __init__(self):
        self.model = None
        self.processor = None

        try:
            print("Loading CLIP Model (approx 800MB)... first run may be slow.")

            # Suppress generic transformers warnings for cleaner output
            logging.set_verbosity_error()

            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.processor = CLIPProcessor.from_pretrained(
                "openai/clip-vit-base-patch32"
            )
            print("CLIP Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load CLIP model: {e}")

    def analyze(self, media_path: str, claim_text: str = "") -> Dict[str, Any]:

        if not self.model or not self.processor:
            return {
                "tool": "Semantic_Alignment_CLIP",
                "error": "CLIP model not loaded.",
                "verdict": "Skipped",
            }

        if not claim_text:
            return {
                "tool": "Semantic_Alignment_CLIP",
                "error": "No claim text provided for alignment check.",
                "verdict": "Skipped",
            }

        try:
            image = PIL.Image.open(media_path)
            # Truncate text if too long, though CLIP processor handles truncation usually
            inputs = self.processor(
                text=[claim_text[:77]], images=image, return_tensors="pt", padding=True
            )

            with torch.no_grad():
                outputs = self.model(**inputs)

            # Calculate cosine similarity
            image_embeds = outputs.image_embeds
            text_embeds = outputs.text_embeds

            # Normalize
            image_embeds = image_embeds / image_embeds.norm(p=2, dim=-1, keepdim=True)
            text_embeds = text_embeds / text_embeds.norm(p=2, dim=-1, keepdim=True)

            # Cosine similarity
            similarity = (text_embeds @ image_embeds.T).item()

            # Heuristics for verdict
            # 0.2 is typically a threshold for relevance in CLIP base.
            verdict = "Consistency Indeterminate"
            if similarity > 0.25:
                verdict = "High Visual-Text Consistency"
            elif similarity < 0.15:
                verdict = "Low Consistency / Potential Out-of-Context"

            return {
                "tool": "Semantic_Alignment_CLIP",
                "similarity_score": round(similarity, 4),
                "verdict": verdict,
            }

        except Exception as e:
            return {
                "tool": "Semantic_Alignment_CLIP",
                "error": str(e),
                "verdict": "Error",
            }
