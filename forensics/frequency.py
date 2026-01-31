from typing import Dict, Any
from .base import ForensicTool
import numpy as np
import PIL.Image
import PIL.ImageOps


class FrequencyForensics(ForensicTool):
    """
    Analyzes the frequency domain of an image using Fourier Transform (FFT).
    Synthetic images (GANs/Diffusion) often exhibit specific artifacts in the frequency domain,
    such as checkerboard patterns (visible as bright stars/grids in FFT) or abnormal high-frequency energy.
    """

    def analyze(self, media_path: str, claim_text: str = "") -> Dict[str, Any]:
        result = {
            "tool": "Frequency_Analysis",
            "anomaly_score": 0.0,
            "details": [],
            "verdict": "Skipped",
        }

        try:

            img = PIL.Image.open(media_path).convert("L")
            img_array = np.array(img)

            # Compute 2D FFT
            f = np.fft.fft2(img_array)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-6)  # + epsilon

            # Natural images have much higher energy in low frequencies (center)
            # and it falls off rapidly.
            # We define "Low Frequency" as the center circle.
            rows, cols = img_array.shape
            crow, ccol = rows // 2, cols // 2

            # Mask for Low Frequency (Center 15%)
            radius = min(rows, cols) * 0.15
            y, x = np.ogrid[:rows, :cols]
            mask_area = (x - ccol) ** 2 + (y - crow) ** 2 <= radius**2

            # Calculate energy ratio (High Freq / Total)
            total_energy = np.sum(magnitude_spectrum)
            low_freq_energy = np.sum(magnitude_spectrum[mask_area])
            high_freq_energy = total_energy - low_freq_energy

            hf_ratio = high_freq_energy / total_energy

            result["hf_ratio"] = round(hf_ratio, 4)

            # Detect Spikes (Grid artifacts common in GANs)
            # This is a simplified check for outliers in the high-frequency range
            hf_spectrum = magnitude_spectrum.copy()
            hf_spectrum[mask_area] = 0  # zero out center

            mean_hf = np.mean(hf_spectrum[hf_spectrum > 0])
            std_hf = np.std(hf_spectrum[hf_spectrum > 0])
            max_hf = np.max(hf_spectrum)

            z_score_max = (max_hf - mean_hf) / (std_hf + 1e-6)

            result["details"].append(f"High-Freq Energy Ratio: {hf_ratio:.2f}")
            result["details"].append(f"Max HF Anomaly (Z-score): {z_score_max:.2f}")

            # Verdict Heuristics
            # Real images usually have hf_ratio < 0.35 (mostly low freq).
            # Noisy or Synthetic images might have higher ratios or sharp spikes (Z > 10).

            score = 0
            if hf_ratio > 0.45:  # Very noisy or texture-heavy or synthetic noise
                score += 1
                result["details"].append("Unusually high high-frequency energy")

            if z_score_max > 12:  # Significant periodic artifact
                score += 2
                result["details"].append(
                    "Detected periodic artifacts (potential GAN grid)"
                )

            result["anomaly_score"] = score

            if score >= 2:
                result["verdict"] = "Potential Synthetic/GAN Artifacts Detected"
            elif score == 1:
                result["verdict"] = "Noisy/High-Texture Image"
            else:
                result["verdict"] = "Natural Frequency Distribution"

        except Exception as e:
            result["error"] = str(e)
            result["verdict"] = "Error during analysis"

        return result
