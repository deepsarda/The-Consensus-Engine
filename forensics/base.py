from abc import ABC, abstractmethod
from typing import Dict, Any

class ForensicTool(ABC):
    """Abstract base class for all forensic tools."""
    
    @abstractmethod
    def analyze(self, media_path: str, claim_text: str = "") -> Dict[str, Any]:
        """
        Analyze the media and/or claim.
        
        Args:
            media_path: Path to the image or video file.
            claim_text: The associated text claim (optional, for tools that need it).
            
        Returns:
            A dictionary containing the analysis results.
        """
        pass
