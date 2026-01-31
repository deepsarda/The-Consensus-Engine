from typing import Dict, Any
from PIL import Image, ExifTags
from .base import ForensicTool
import datetime


class MetadataAnalyzer(ForensicTool):

    def analyze(self, media_path: str, claim_text: str) -> Dict[str, Any]:
        """
        Analyze the media for metadata.

        Args:
            media_path: Path to the image file.
            claim_text: (Unused for metadata)

        Returns:
            Dictionary containing extracted metadata.
        """
        result = {
            "tool": "Metadata_Analyzer",
            "metadata_found": False,
            "data": {},
            "verdict": "No metadata found",
        }

        try:
            with Image.open(media_path) as img:
                exif_data = img._getexif()

                if not exif_data:
                    return result

                result["metadata_found"] = True
                extracted_data = {}

                # Map Exif tags to readable names
                # We specifically look for: 'Make', 'Model', 'DateTimeOriginal', 'Software', 'GPSInfo'

                # Helper to convert byte values or other non-serializable types if needed
                def clean_value(val):
                    if isinstance(val, bytes):
                        try:
                            return val.decode()
                        except:
                            return str(val)
                    if isinstance(
                        val, (datetime.datetime, datetime.date, datetime.time)
                    ):
                        return val.isoformat()
                    return val

                # Standard tags
                for tag_id, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag_id, tag_id)

                    if tag_name == "GPSInfo":
                        # GPS info needs special handling to be readable
                        gps_data = {}
                        for t in value:
                            sub_tag = ExifTags.GPSTAGS.get(t, t)
                            gps_data[sub_tag] = clean_value(value[t])
                        extracted_data["GPS"] = gps_data
                    else:
                        extracted_data[tag_name] = clean_value(value)

                result["data"] = extracted_data

                # Formulate a verdict
                verdict_parts = []
                if "Software" in extracted_data:
                    verdict_parts.append(f"Edited with: {extracted_data['Software']}")
                if "DateTimeOriginal" in extracted_data:
                    verdict_parts.append(
                        f"Taken on: {extracted_data['DateTimeOriginal']}"
                    )
                if "GPS" in extracted_data:
                    verdict_parts.append("Contains GPS data")

                if not verdict_parts:
                    result["verdict"] = (
                        "Metadata present but no key forensic tags (Software/Date/GPS)"
                    )
                else:
                    result["verdict"] = " | ".join(verdict_parts)

                return result

        except Exception as e:
            result["error"] = str(e)
            result["verdict"] = "Error extracting metadata"
            return result
