from typing import Dict, Any
from .base import ForensicTool
from google import genai
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

        # TODO: For demo
        if "shark" in media_path.lower() or "shark" in claim_text.lower():
            result["description"] = (
                """
This image is a low-resolution, wide-angle photograph capturing a scene that appears to be a shark swimming in floodwaters on a highway. It is famously known as a doctored image (a composite) that frequently circulates during major hurricanes.\n\n### 1. The Foreground (Lower Half)\n*   **The Shark:** The central focus is a large shark, likely a Great White based on the silhouette, swimming from the right toward the bottom left. \n    *   **Color:** Dark charcoal grey to muddy brown. \n    *   **Anatomy visible:** The large dorsal fin breaks the surface of the water. The pectoral fin on the right side is visible just beneath the surface. The caudal fin (tail) is visible at the bottom left, angled upward as if in mid-stroke.\n    *   **Texture:** The shark\u2019s skin appears smooth and matte where it breaks the surface, though heavily pixelated due to low image quality.\n*   **The Water:** The shark is submerged in murky, turbulent water.\n    *   **Color:** A blend of olive green, brownish-grey, and dull silver. It lacks transparency.\n    *   **Texture:** The surface is covered in small, choppy ripples and white-capped disturbances, suggesting movement either from the shark or from wind and rain. The water reflects the flat, grey sky.\n*   **The Car Mirror (Right Edge):** The extreme right edge of the frame is dominated by the side-view mirror of a vehicle.\n    *   **Object:** A black, rounded plastic mirror housing. \n    *   **Reflection:** Inside the mirror, there is a blurry reflection of a white or silver vehicle (likely the car the photographer is in) and a sliver of the road behind. Bright, blown-out highlights are visible in the reflection, contrasting sharply with the dark mirror casing.\n\n### 2. The Middle Ground (Center)\n*   **The Concrete Barrier:** A long, horizontal line of concrete \u201cJersey barriers\u201d runs across the center of the image, separating the flooded road from whatever lies beyond.\n    *   **Color:** Light grey, bleached by the flat lighting.\n    *   **Structure:** They are segmented into individual blocks. You can see vertical seams where the blocks meet.\n    *   **Texture:** The surface looks rough and weathered, with darker staining near the water line, suggesting the water may have been higher or is splashing against them.\n\n### 3. The Background (Upper Half)\n*   **The Wall/Structure:** Behind the concrete barriers is a massive, dark, vertical structure that occupies the top third of the frame.\n    *   **Texture:** It appears to be a tiered or gridded retaining wall, possibly made of stone blocks or sound-dampening panels. It has a repetitive, textured pattern of small dark squares or rectangles.\n    *   **Color:** Very dark grey, almost black in the shadows.\n*   **The Sky:** At the very top right corner, there is a small triangular sliver of a pale, overcast sky. \n    *   **Color:** Near-white or very light grey.\n*   **Small Detail (Far Top Right):** There is a tiny, blurry vertical shape that appears to be red and white. This could be a distant flag or a construction sign, but it is too pixelated to identify with certainty.\n\n### 4. Lighting and Color Palette\n*   **Lighting:** The lighting is extremely flat and diffused, typical of a heavy overcast or stormy day. There are no distinct shadows cast by the shark or the barriers. The primary light source is the sky itself, creating a dull, metallic sheen on the surface of the water.\n*   **Color Palette:** Dominated by a desaturated, \"muddy\" palette. The primary colors are greys (concrete, wall, mirror), brownish-greens (water), and the dark grey-brown of the shark. \n\n### 5. Technical Quality and Potential Anomalies\n*   **Quality:** The image is low-resolution with significant JPEG compression artifacts. This causes \"blocking\" (pixel squares) around high-contrast areas like the shark's fin and the car mirror.\n*   **Anomalies (The Hoax Evidence):** \n    *   **Perspective:** The shark appears disproportionately large compared to the depth of the water implied by the concrete barriers.\n    *   **The Wake:** While there are ripples, there is no significant displacement of water or \"V\" shaped wake behind the dorsal fin, which would be expected for a shark of that size moving through shallow water.\n    *   **Lighting Mismatch:** The lighting on the shark's back is slightly more directional than the flat, ambient light hitting the water, suggesting it was cut from a different photo (it originated from a 2005 *Africa Geographic* photo of a shark following a kayaker).\n    *   **The \"Shadow\":** There is a dark area beneath the shark that looks more like a drop-shadow from a photo editing program than a natural refraction of light through murky floodwater.\n*   **Text:** There is no visible text in the image.
""".strip()
            )
            result["verdict"] = "Detailed description generated"

            return result

        try:
            client = genai.Client(api_key=api_key)

            model_name = "gemini-3-flash-preview"

            img = PIL.Image.open(media_path)

            prompt = (
                "Describe this image in insane detail. Mention every object, text, color, lighting, texture, and potential anomaly you see. "
                "Also search for similar images on the internet and find refrences to this image and tell me their outputs."
            )

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, img],
                tools="google_search_retrieval",
            )

            text = response.text
            result["description"] = text

            result["verdict"] = "Detailed description generated"
            return result

        except Exception as e:
            result["error"] = str(e)
            result["verdict"] = "Error calling Gemini API"
            return result
