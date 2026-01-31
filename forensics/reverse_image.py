import os
import requests
import json
import http.client
import urllib.parse
import mimetypes
from typing import Dict, Any
from .base import ForensicTool
from libs.reverse_image_search import GoogleReverseImageSearch


class ContextRetriever(ForensicTool):

    def upload_to_tmpfiles(self, file_path: str) -> str:
        """
        Uploads a file to tmpfiles.org and returns the direct download URL.
        """
        url = "https://tmpfiles.org/api/v1/upload"

        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return None

        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                # tmpfiles.org expects the field name 'file'
                files = {"file": (os.path.basename(file_path), f, mime_type)}
                response = requests.post(url, files=files)

            response.raise_for_status()
            data = response.json()

            if data.get("status") == "success":
                # Convert display URL to direct download URL
                # Display: https://tmpfiles.org/12345/image.jpg
                # Direct: https://tmpfiles.org/dl/123445/image.jpg
                display_url = data["data"]["url"]
                direct_url = display_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
                return direct_url
            else:
                print(f"Upload failed: {data}")
                return None
        except Exception as e:
            print(f"Exception during upload: {e}")
            return None

    def analyze(self, media_path: str, claim_text: str = None) -> Dict[str, Any]:
        try:
            print(f"Uploading {media_path} to temporary storage...")
            image_url = self.upload_to_tmpfiles(media_path)

            if not image_url:
                return {"error": "Failed to upload image or file not found."}

            print(f"File uploaded. URL: {image_url}")
            print("Performing reverse image search...")
            request = GoogleReverseImageSearch()

            response = request.response(
                query=claim_text, image_url=image_url, max_results=5
            )

            print(response)

            return response

        except Exception as e:
            return {"error": f"Exception occurred: {str(e)}"}
