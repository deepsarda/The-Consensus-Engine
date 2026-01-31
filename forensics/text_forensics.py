from typing import Dict, Any
from .base import ForensicTool
import re
from transformers import pipeline, logging


class TextForensics(ForensicTool):
    def __init__(self):
        self.classifier = None

        logging.set_verbosity_error()

        try:
            print("Loading Text Forensics AI Model (DistilBART)...")
            # Using a distilled model for speed/memory efficiency while maintaining accuracy
            self.classifier = pipeline(
                "zero-shot-classification", model="valhalla/distilbart-mnli-12-1"
            )
            print("Text Forensics Model loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load TextForensics AI model: {e}")

    def analyze(self, media_path: str = None, claim_text: str = "") -> Dict[str, Any]:
        """
        Analyzes text using hybrid method: Heuristics + AI Zero-Shot Classification.
        """
        if not claim_text:
            return {
                "tool": "Text_Forensics",
                "verdict": "No text provided",
            }

        # Heuristic Analysis
        heuristic_score = 0
        reasons = []

        lower_text = claim_text.lower()
        words = claim_text.split()

        # Check for All Caps (shouting)
        if len(words) > 3:
            cap_words = [w for w in words if w.isupper() and len(w) > 1]
            if len(cap_words) / len(words) > 0.3:
                heuristic_score += 2
                reasons.append("Excessive capitalization (Shouting)")

        # Sensationalist Keywords
        keyword_categories = {
            "Clickbait/Hype": [
                "shocking",
                "unbelievable",
                "exposed",
                "OMG",
                "mind-blowing",
                "viral",
                "epic",
                "won't believe",
                "what happens next",
            ],
            "Conspiracy/Secrecy": [
                "secret",
                "they don't want you to know",
                "censored",
                "covered up",
                "mainstream media",
                "truth about",
                "hidden agenda",
                "deep state",
            ],
            "Fear/Urgency": [
                "danger",
                "warning",
                "be careful",
                "crisis",
                "collapse",
                "panic",
                "deadly",
                "threat",
                "destroy",
                "before it's deleted",
                "share now",
            ],
            "Certainty/Absolutism": [
                "proof",
                "proven",
                "100%",
                "undeniable",
                "guaranteed",
                "fact",
                "miracle",
                "cure",
                "scam",
                "hoax",
            ],
        }

        for category, kws in keyword_categories.items():
            found = [kw for kw in kws if kw in lower_text]
            if found:
                heuristic_score += len(found)
                reasons.append(f"{category} terms: {', '.join(found[:3])}")

        # Excessive Punctuation
        if "!!" in claim_text:
            heuristic_score += 1
            reasons.append("Excessive exclamation marks")
        if "??" in claim_text:
            heuristic_score += 1
            reasons.append("Excessive question marks")

        # Pattern Matching
        if claim_text.strip().upper().startswith("BREAKING") or "ALERT:" in claim_text:
            heuristic_score += 2
            reasons.append("Imitates 'Breaking News' format")

        weasel_phrases = [
            "experts say",
            "studies show",
            "sources tell",
            "everyone knows",
            "it is said",
        ]
        if any(p in lower_text for p in weasel_phrases):
            heuristic_score += 1
            reasons.append("Vague sourcing/Weasel words")

        # AI Analysis (Zero-Shot)
        ai_data = {}
        if self.classifier:
            try:
                candidate_labels = [
                    "Objective and Factual",
                    "Clickbait and Sensationalist",
                    "Fear-mongering",
                    "Politically Biased",
                    "Satire",
                ]

                # Multi-label=True allows it to dependently score each
                results = self.classifier(
                    claim_text, candidate_labels, multi_label=True
                )

                # Format results
                scores = dict(zip(results["labels"], results["scores"]))
                ai_data = {
                    "top_label": results["labels"][0],
                    "top_confidence": round(results["scores"][0], 4),
                    "all_scores": {k: round(v, 3) for k, v in scores.items()},
                }

                # Integrate AI into reasons for clarity
                if scores["Clickbait and Sensationalist"] > 0.6:
                    reasons.append(
                        f"AI Detected High Sensationalism ({scores['Clickbait and Sensationalist']:.2f})"
                    )
                    heuristic_score += 2
                if scores["Fear-mongering"] > 0.6:
                    reasons.append(
                        f"AI Detected Fear-mongering ({scores['Fear-mongering']:.2f})"
                    )
                    heuristic_score += 2
                if scores["Objective and Factual"] > 0.7:
                    heuristic_score -= 2  # Reduce panic score if AI thinks it's factual

            except Exception as e:
                ai_data = {"error": str(e)}

        # Verdict Logic
        # Normalize score
        heuristic_score = max(0, heuristic_score)

        if heuristic_score == 0:
            verdict = "Neutral/Objective Tone"
        elif heuristic_score < 4:
            verdict = "Slightly Emotive/Subjective"
        elif heuristic_score < 7:
            verdict = "Highly Sensationalist/Clickbait"
        else:
            verdict = "Potential Disinformation/Propaganda"

        return {
            "tool": "Text_Forensics",
            "risk_score": heuristic_score,
            "verdict": verdict,
            "triggers": reasons,
            "ai_analysis": ai_data,
        }
