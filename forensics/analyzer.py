from typing import Dict, Any
from .deepfake import DeepfakeDetector
from .clip import SemanticAlignment
from .search import ContextRetriever


class ForensicAnalyzer:

    def __init__(self):
        self.deepfake_tool = DeepfakeDetector()
        self.clip_tool = SemanticAlignment()
        self.search_tool = ContextRetriever()

    def run_all(self, media_path: str, claim_text: str) -> Dict[str, Any]:
        """
        Runs all tools and returns a dictionary ready for the LLM Council.
        """
        deepfake_res = self.deepfake_tool.analyze(media_path, claim_text)
        clip_res = self.clip_tool.analyze(media_path, claim_text)
        search_res = self.search_tool.analyze(media_path, claim_text)

        return {
            "Deepfake_Detector": deepfake_res,
            "Cross_Modal_CLIP": clip_res,
            "Reverse_Image_Search": search_res,
            "Text_Forensics": {  # TODO: Placeholder for now, as mentioned in one-shot but not strictly required
                "tool": "Text_Forensics",
                "sentiment": "Neutral/Objective",  # Simple default
            },
        }
