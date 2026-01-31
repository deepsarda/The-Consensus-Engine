from typing import Dict, Any
from .deepfake import DeepfakeDetector
from .clip import SemanticAlignment
from .reverse_image import ContextRetriever
from .metadata import MetadataAnalyzer
from .gemini_vision import GeminiAnalyzer
from .ela import ELAanalyzer
from .text_forensics import TextForensics


class ForensicAnalyzer:

    def __init__(self):
        self.deepfake_tool = DeepfakeDetector()
        self.clip_tool = SemanticAlignment()
        self.reverse_image = ContextRetriever()
        self.metadata_tool = MetadataAnalyzer()
        self.gemini_tool = GeminiAnalyzer()
        self.ela_tool = ELAanalyzer()
        self.text_tool = TextForensics()

    def run_all(self, media_path: str, claim_text: str) -> Dict[str, Any]:
        """
        Runs all tools and returns a dictionary ready for the LLM Council.
        """
        deepfake_res = self.deepfake_tool.analyze(media_path, claim_text)
        metadata_res = self.metadata_tool.analyze(media_path, claim_text)
        gemini_res = self.gemini_tool.analyze(media_path, claim_text)
        clip_res = self.clip_tool.analyze(media_path, claim_text)
        ela_res = self.ela_tool.analyze(media_path, claim_text)
        text_res = self.text_tool.analyze(media_path, claim_text)

        # search_res = self.reverse_image.analyze(media_path, claim_text)

        return {
            "Deepfake_Detector": deepfake_res,
            # "Reverse_Image_Search": search_res,
            "Metadata_Analysis": metadata_res,
            "Gemini_Vision": gemini_res,
            "Semantic_Alignment": clip_res,
            "ELA_Analysis": ela_res,
            "Text_Forensics": text_res,
        }
