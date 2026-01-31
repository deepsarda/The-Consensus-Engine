from typing import Dict, Any
from .base import ForensicTool
import PIL.Image
import PIL.ImageChops
import os
import tempfile
import numpy as np


class ELAanalyzer(ForensicTool):
    """
    Error Level Analysis (ELA) to detect manipulation in images.
    It works by re-saving the image at a known quality and differencing it.
    """

    def analyze(self, media_path: str, claim_text: str = "") -> Dict[str, Any]:
        result = {
            "tool": "ELA_Analysis",
            "max_difference": 0,
            "mean_error_level": 0,
            "verdict": "Skipped",
        }
        
        tmp_name = None
        try:
            original = PIL.Image.open(media_path).convert("RGB")

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                tmp_name = tmp.name

            # Resave at 90% quality
            original.save(tmp_name, "JPEG", quality=90)
            resaved = PIL.Image.open(tmp_name)

            ela_image = PIL.ImageChops.difference(original, resaved)
            extrema = ela_image.getextrema()
            max_diff = max([ex[1] for ex in extrema])

            np_ela = np.array(ela_image)
            mean_error = np.mean(np_ela)

            result["max_difference"] = max_diff
            result["mean_error_level"] = round(mean_error, 2)

            # Heuristic: 
            # High mean error might indicate the original was low quality 
            # or highly compressed differently than 90%.
            # Localized high error is suspicious (not captured by global mean easily, but max helps).
            # This is a basic implementation.
            
            if mean_error > 15.0: 
                # If the difference is huge globally, it might just be different compression tables
                result["verdict"] = "Inconclusive (High Global Variance)"
            elif max_diff > 50 and mean_error < 5.0:
                 # High local peak but low global mean -> suspicious
                result["verdict"] = "Potential Local Manipulation"
            else:
                result["verdict"] = "No Obvious Manipulation Artifacts (ELA)"

        except Exception as e:
            result["error"] = str(e)
            result["verdict"] = "Error"
        finally:
            if tmp_name and os.path.exists(tmp_name):
                os.remove(tmp_name)

        return result
