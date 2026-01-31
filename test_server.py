import asyncio
import websockets
import json
import time

async def handler(websocket):
    print("Client connected")
    try:
        # Wait for initial message
        message = await websocket.recv()
        print(f"Received: {message}")

        # Sequence of messages to send
        messages = [
            {
                "type": "progress",
                "step": "upload",
                "status": "complete",
                "message": "Image uploaded and processed."
            },
            {
                "type": "progress",
                "step": "forensics",
                "status": "running",
                "message": "Analyzing forensic evidence..."
            },
            {
                "type": "result",
                "step": "forensics",
                "data": {
                    "Deepfake_Detector": {
                        "tool": "Deepfake_Detector",
                        "fake_prob": 0.1,
                        "verdict": "Likely Real Camera Image"
                    },
                    "Metadata_Analysis": {
                        "tool": "Metadata_Analyzer",
                        "metadata_found": False,
                        "data": {},
                        "verdict": "No metadata found"
                    },
                    "Gemini_Vision": {
                        "tool": "Gemini_Image_Describer",
                        "description": "This image is a low-resolution, wide-angle photograph capturing a scene that appears to be a shark swimming in floodwaters on a highway. It is famously known as a doctored image (a composite) that frequently circulates during major hurricanes.\n\n### 1. The Foreground (Lower Half)\n*   **The Shark:** The central focus is a large shark, likely a Great White based on the silhouette, swimming from the right toward the bottom left. \n    *   **Color:** Dark charcoal grey to muddy brown. \n    *   **Anatomy visible:** The large dorsal fin breaks the surface of the water. The pectoral fin on the right side is visible just beneath the surface. The caudal fin (tail) is visible at the bottom left, angled upward as if in mid-stroke.\n    *   **Texture:** The shark’s skin appears smooth and matte where it breaks the surface, though heavily pixelated due to low image quality.\n*   **The Water:** The shark is submerged in murky, turbulent water.\n    *   **Color:** A blend of olive green, brownish-grey, and dull silver. It lacks transparency.\n    *   **Texture:** The surface is covered in small, choppy ripples and white-capped disturbances, suggesting movement either from the shark or from wind and rain. The water reflects the flat, grey sky.\n*   **The Car Mirror (Right Edge):** The extreme right edge of the frame is dominated by the side-view mirror of a vehicle.\n    *   **Object:** A black, rounded plastic mirror housing. \n    *   **Reflection:** Inside the mirror, there is a blurry reflection of a white or silver vehicle (likely the car the photographer is in) and a sliver of the road behind. Bright, blown-out highlights are visible in the reflection, contrasting sharply with the dark mirror casing.\n\n### 2. The Middle Ground (Center)\n*   **The Concrete Barrier:** A long, horizontal line of concrete “Jersey barriers” runs across the center of the image, separating the flooded road from whatever lies beyond.\n    *   **Color:** Light grey, bleached by the flat lighting.\n    *   **Structure:** They are segmented into individual blocks. You can see vertical seams where the blocks meet.\n    *   **Texture:** The surface looks rough and weathered, with darker staining near the water line, suggesting the water may have been higher or is splashing against them.\n\n### 3. The Background (Upper Half)\n*   **The Wall/Structure:** Behind the concrete barriers is a massive, dark, vertical structure that occupies the top third of the frame.\n    *   **Texture:** It appears to be a tiered or gridded retaining wall, possibly made of stone blocks or sound-dampening panels. It has a repetitive, textured pattern of small dark squares or rectangles.\n    *   **Color:** Very dark grey, almost black in the shadows.\n*   **The Sky:** At the very top right corner, there is a small triangular sliver of a pale, overcast sky. \n    *   **Color:** Near-white or very light grey.\n*   **Small Detail (Far Top Right):** There is a tiny, blurry vertical shape that appears to be red and white. This could be a distant flag or a construction sign, but it is too pixelated to identify with certainty.\n\n### 4. Lighting and Color Palette\n*   **Lighting:** The lighting is extremely flat and diffused, typical of a heavy overcast or stormy day. There are no distinct shadows cast by the shark or the barriers. The primary light source is the sky itself, creating a dull, metallic sheen on the surface of the water.\n*   **Color Palette:** Dominated by a desaturated, \"muddy\" palette. The primary colors are greys (concrete, wall, mirror), brownish-greens (water), and the dark grey-brown of the shark. \n\n### 5. Technical Quality and Potential Anomalies\n*   **Quality:** The image is low-resolution with significant JPEG compression artifacts. This causes \"blocking\" (pixel squares) around high-contrast areas like the shark's fin and the car mirror.\n*   **Anomalies (The Hoax Evidence):** \n    *   **Perspective:** The shark appears disproportionately large compared to the depth of the water implied by the concrete barriers.\n    *   **The Wake:** While there are ripples, there is no significant displacement of water or \"V\" shaped wake behind the dorsal fin, which would be expected for a shark of that size moving through shallow water.\n    *   **Lighting Mismatch:** The lighting on the shark's back is slightly more directional than the flat, ambient light hitting the water, suggesting it was cut from a different photo (it originated from a 2005 *Africa Geographic* photo of a shark following a kayaker).\n    *   **The \"Shadow\":** There is a dark area beneath the shark that looks more like a drop-shadow from a photo editing program than a natural refraction of light through murky floodwater.\n*   **Text:** There is no visible text in the image.",
                        "verdict": "Detailed description generated"
                    },
                    "Semantic_Alignment": {
                        "tool": "Semantic_Alignment_CLIP",
                        "similarity_score": 0.3405,
                        "verdict": "High Visual-Text Consistency"
                    },
                    "ELA_Analysis": {
                        "tool": "ELA_Analysis",
                        "max_difference": 7,
                        "mean_error_level": 0.42,
                        "verdict": "No Obvious Manipulation Artifacts (ELA)"
                    },
                    "Frequency_Analysis": {
                        "tool": "Frequency_Analysis",
                        "anomaly_score": 1,
                        "details": [
                            "High-Freq Energy Ratio: 0.94",
                            "Max HF Anomaly (Z-score): 3.38",
                            "Unusually high high-frequency energy"
                        ],
                        "verdict": "Noisy/High-Texture Image",
                        "hf_ratio": 0.9381
                    },
                    "Text_Forensics": {
                        "tool": "Text_Forensics",
                        "risk_score": 2,
                        "verdict": "Slightly Emotive/Subjective",
                        "triggers": [
                            "Imitates 'Breaking News' format"
                        ],
                        "ai_analysis": {
                            "top_label": "Fear-mongering",
                            "top_confidence": 0.1903,
                            "all_scores": {
                                "Fear-mongering": 0.19,
                                "Objective and Factual": 0.068,
                                "Satire": 0.065,
                                "Clickbait and Sensationalist": 0.01,
                                "Politically Biased": 0.001
                            }
                        }
                    }
                }
            },
            {
                "type": "progress",
                "step": "council",
                "status": "running",
                "message": "Convening the Council of LLMs..."
            },
            {
                "type": "result",
                "step": "council",
                "data": [
                    {
                        "member_name": "Model A",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Authenticity Check",
                                    "observation": "Deepfake_Detector (0.1) and Frequency_Analysis indicate the image is likely a composite of real photographic elements rather than a purely synthetic Generative AI (GAN/Diffusion) creation."
                                },
                                {
                                    "step": "Visual Content Verification",
                                    "observation": "Gemini_Vision identifies the image as a famous 'hoax' composite. While Semantic_Alignment (0.34) confirms the image contains a shark in water, the visual evidence (Jersey barriers, car mirror) indicates a highway, not a 'subway station' as claimed."
                                },
                                {
                                    "step": "Anomaly Detection",
                                    "observation": "Gemini_Vision notes a lighting mismatch on the shark's back and the lack of a 'wake' or water displacement, confirming the shark was digitally spliced into the floodwater (Cheapfake)."
                                },
                                {
                                    "step": "Historical Context",
                                    "observation": "Forensic analysis confirms this is the 'Street Shark' hoax, which originated from a 2005 Africa Geographic photo of a shark following a kayaker, repurposed for various storms since 2011."
                                }
                            ],
                            "conclusion": "The claim is misinformation. While the image is not a Deepfake (AI-generated), it is a digitally manipulated 'Cheapfake' composite. Furthermore, the claim incorrectly identifies the location as a subway station when visual cues confirm it is a flooded road. This specific image is a known recurring internet hoax.",
                            "verdict": "Misinformation",
                            "confidence_score": 99,
                            "category": "Digitally Manipulated / Composite Media"
                        }
                    },
                    {
                        "member_name": "Model C",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "AI Generative Analysis",
                                    "observation": "Deepfake_Detector (0.1) and Frequency_Analysis indicate the image is not an AI-generated (GAN or Diffusion) piece, but rather a traditional digital photograph."
                                },
                                {
                                    "step": "Detailed Visual Forensic Analysis",
                                    "observation": "Gemini_Vision identifies the image as a known historical hoax. Key anomalies include a 'drop-shadow' under the shark inconsistent with water refraction and a lighting mismatch between the shark and the environment. It identifies the shark source as a 2005 'Africa Geographic' photograph."
                                },
                                {
                                    "step": "Semantic & Contextual Verification",
                                    "observation": "The claim states the location is a 'subway station'. However, Gemini_Vision identifies highway-specific elements such as 'Jersey barriers' and a car side-view mirror, proving the setting is a flooded road, not a subway."
                                },
                                {
                                    "step": "Technical Tool Limitations",
                                    "observation": "ELA_Analysis shows no results due to high JPEG compression/low resolution, which often masks splicing artifacts in older 'Cheapfakes'. Semantic Alignment is high because the image does contain a shark and water, though the context is false."
                                },
                                {
                                    "step": "Intent and History",
                                    "observation": "The claim uses 'Breaking' (Text_Forensics) to create urgency. This image is a persistent internet urban legend used during almost every major flooding event (e.g., Hurricane Irene, Harvey, Ian)."
                                }
                            ],
                            "conclusion": "The claim is false. The image is a 'Cheapfake'—a manual digital composite created by splicing a 2005 photograph of a Great White shark onto a photo of a flooded highway. Furthermore, the claim incorrectly identifies the location as a subway station when visual cues (car mirrors, highway barriers) confirm it is a road.",
                            "verdict": "Misinformation",
                            "confidence_score": 99,
                            "category": "Doctored Media / Cheapfake"
                        }
                    },
                    {
                        "member_name": "Model B",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Authenticity Check",
                                    "observation": "Deepfake_Detector indicates the image is likely real (score 0.1). Frequency_Analysis shows high-frequency energy but does not flag synthetic artifacts. Gemini_Vision explicitly identifies this as a known composite image from past hurricane hoaxes."
                                },
                                {
                                    "step": "Content Verification",
                                    "observation": "Gemini_Vision provides detailed analysis showing the shark image is a doctored composite. It notes perspective issues, lack of natural wake, lighting mismatch, and a drop-shadow effect - all classic signs of digital manipulation. The shark was originally from a 2005 Africa Geographic photo."
                                },
                                {
                                    "step": "Context Analysis",
                                    "observation": "Semantic_Alignment shows high visual-text consistency (0.3405), meaning the image does show a shark in water. However, Gemini_Vision reveals this is a known fake that has been debunked repeatedly during hurricane events."
                                },
                                "step ",
                                "Intent Analysis",
                                "observation ",
                                "Text_Forensics shows low risk score (2) but identifies 'Breaking News' format imitation, suggesting attempt to create urgency."
                            ]
                        }
                    }
                ]
            },
            {
                "type": "progress",
                "step": "judge",
                "status": "running",
                "message": "The Adjudicator is deliberating..."
            },
            {
                "type": "result",
                "step": "judge",
                "data": {
                    "member_name": "Judge Agent",
                    "output": {
                        "model_evaluations": [
                            {
                                "model": "Model A",
                                "status": "KEEP",
                                "reason": "Accurately utilized the Gemini_Vision data to identify the specific 'Street Shark' hoax. Correctly interpreted the Deepfake_Detector score (0.1) to conclude it is a composite/cheapfake rather than a Generative AI creation. Properly identified the contradiction between the claim (subway) and visual evidence (highway)."
                            },
                            {
                                "model": "Model C",
                                "status": "KEEP",
                                "reason": "Provided a highly detailed synthesis of all tools. Correctly identified the historical source of the shark (2005 Africa Geographic) and explained why ELA analysis was inconclusive due to JPEG artifacts. Correctly identified the 'Breaking News' tactic from the Text_Forensics tool."
                            },
                            {
                                "model": "Model B",
                                "status": "DISCARD",
                                "reason": "The output is structurally malformed and incomplete. It failed to provide a final conclusion, verdict, or confidence score, and the reasoning steps broke into disconnected strings at the end."
                            }
                        ],
                        "final_verdict": "Misinformation",
                        "aggregated_confidence": 99,
                        "explanation": "The claim that a shark is swimming in a flooded subway station is false. Forensic analysis and visual verification confirm this is the 'Street Shark' hoax, a famous digital composite ('Cheapfake') that has circulated since at least 2011. While the Deepfake_Detector confirms the image is not purely AI-generated (GAN/Diffusion), Gemini_Vision identifying the 2005 'Africa Geographic' source photograph proves the shark was spliced in. Furthermore, the visual evidence—specifically the 'Jersey barriers' and car side-view mirror—proves the setting is a flooded highway, directly contradicting the claim that the location is a subway station. Technical anomalies such as lighting mismatches on the shark's dorsal fin and a lack of a physical wake further confirm the manipulation."
                    }
                }
            },
            {
                "type": "complete",
                "message": "Analysis complete."
            }
        ]

        for msg in messages:
            await websocket.send(json.dumps(msg))
            await asyncio.sleep(2)  # Delay between messages

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handler, "localhost", 8000):
        print("Server started on ws://localhost:8000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
