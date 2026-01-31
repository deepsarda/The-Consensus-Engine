from typing import Dict, Any
from .base import ForensicTool

import tensorflow as tf
from huggingface_hub import hf_hub_download
import numpy as np
from PIL import Image


class DeepfakeDetector(ForensicTool):

    def __init__(self):
        model_path = hf_hub_download(
            repo_id="Dnyanesh-Gavali07/XCEPTIONNET-DeepFake-Detector",
            filename="xception_deepfake_model.keras"
        )

        self.model = tf.keras.models.load_model(model_path)

        # Image input size for Xception
        self.img_size = (299, 299)


    def preprocess(self, image_path: str):
        img = Image.open(image_path).convert("RGB")
        img = img.resize(self.img_size)

        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)

        return arr

    def analyze(self, media_path: str, claim_text: str = "") -> Dict[str, Any]:
        try:
            img = self.preprocess(media_path)

            # Model prediction
            pred = self.model.predict(img, verbose=0)[0][0]

            fake_prob = float(pred)

            return {
                "tool": "Deepfake_Detector",
                "fake_prob": round(fake_prob, 4),
                "verdict": (
                    "Likely AI-Generated"
                    if fake_prob > 0.5
                    else "Likely Real Camera Image"
                ),
            }

        except Exception as e:
            return {
                "tool": "Deepfake_Detector",
                "error": str(e),
                "fake_prob": None,
                "verdict": "Analysis Failed",
            }
