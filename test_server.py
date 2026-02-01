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
                "message": "Image uploaded and processed.",
            },
            {
                "type": "progress",
                "step": "forensics",
                "status": "running",
                "message": "Analyzing forensic evidence...",
            },
            {
                "type": "result",
                "step": "forensics",
                "data": {
                    "Deepfake_Detector": {
                        "tool": "Deepfake_Detector",
                        "fake_prob": 0.8035,
                        "verdict": "Likely AI-Generated",
                    },
                    "Citations": "- [deccanchronicle.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH7rBtl8uXuf_qm09-uu7fPaywNccFa41mrccYquTy22PBBhPAfZBXyDA4VN-SRYQaM4g3LmFaz3OHasMhOT271xnnmL3qnM4SPcePksYWqoNuyXxhW-k380YWu6vSKr6ql4FwE3jhcYB60X2EV7vLIadIJragT4kfUyxvdDQucoICHDpc9FxgQB7w5xlxYnuIkVyRdO64LyBhM1JDUvPo5JcnWRAEJ-wcN84L_bFd5FpGVgA==)\n- [indiatvnews.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG9Ti6dRqlImr81rs9Cy0GVtYaf2z6fkJwv16Bkcib4UimrfVrKcGjQmgFDB8KE5rywlPABFt7mi31A5BPPajGxV1lsI8uL0Ekiqgv9mMIELXKlRqeX1K9YiBwyaMsxg30K80KUDKuKdQQ18O8Wh5SWalcrWmE2MALyQK1744_CzeTBxgETHYa-wP2WsU1xThurIKr8SlwDReYI9jlF7TO3GBU9RjKKl_mLStIaLx-ml9ErFrXl6OV-iBVioGcWCQUOkR62)\n- [gulfnews.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuhzXQnNF4oGyfl3sYVkUB2QOIiMeohIy-6VkGxEB7msu5esdunvjBmtXEtsHjV39rq8AntQ1RJ6BcwpJ040qvmWqwd0qRXrc6TtJxo7WrULgpfuQ-mnfl8V0_q2zLJ-JZt9UII9BWPmyZu4BEyPFJTx8PFWy8erf5cEGyK-_tsdqq4UCaKu-hqOg6e95qEX14huzSwrrxo8r_W8wG1hARJdVsrCA=)\n- [channelnewsasia.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGOOO3w9jsVAa_hhiaMfzECU6HbAD6roUv3Y2BzQMiCmXEV6PW_lIZ8P8ulHLgNsOrSYzFozKSSHFIhXnrBGMu2W5ggWapR_T54EDyiFThTnZYjrhXeUH1YXY5X9bVgv7e9n8iOE7ditprURJoa1GC9vO_-_Yh0_Ks9ErCnA6fkrqPEFN7ppMmR8l8OplpruejCwA==)\n- [ctvnews.ca](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5PTfLeF4xXWaRG6_geY4C-8xaWiGSc-iZks8mP5247MjrsMmXSP2i00MGp1bsHAVys5lmr6ikJmQVPMZGL200EWwoLVLmjO4PgS4VQA5V8QjinBcPDC7vW8-Jwg_VxHSCsBH-gq0yD0u0FdyLvWaVHao0GtSjURR74_LE39ifHIRiPyxj810CXmzibq3IWetsm2sjCkbRyn2cRfgMkw==)\n- [indiatimes.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9Rto3THGNL5acnQTU1CqLlUrtfgufwN0gXDM3bmgiNRiY0LwHzA760px1F4rTYhBFC3oJDf1Q4SZlmMm3lAzCWaVOr8OSC2cc2MBcU4VtxhevkQkLhd6mCm3krXiG_IwHZsInj5nc5LZorlKRtvjU_uqtzpQvSro2rHZSoHMKPi57Fw8XqcghmyyMqHx-1bHumpVB6M2Fptodbo-Ga0FYwvt_jA-z428l5LJYsEtDyY_-qMK62Uqu8AuBoouz5k5FqLOpBEomnmnZEhwUgw==)\n- [scmp.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHgHrrKF8vBWaLI3-hVnetBnamlPN_wKWp4h_gcCc_ByLpfKmkKMvPCU1b3NDW4xnYTAaSKWuber1WnC9zGFRsgN6rmtj8CqnIJ4eRVPFtB8hHLIyOtwrMHMqkajOOpNBM6FRwHXBNAkBmcBZDSaFNWq5Sd_XKVMOTKvSuiz0N64bWcOyxto3X8J6dQEvRpuGMdtx-1NVUJQBXLAtbM88sq4B2m7JrkY9mPmwS4agsJ8qjkCnhhSA==)",
                    "Metadata_Analysis": {
                        "tool": "Metadata_Analyzer",
                        "metadata_found": False,
                        "data": {},
                        "verdict": "No metadata found",
                    },
                    "Gemini_Vision": {
                        "tool": "Gemini_Image_Describer",
                        "description": 'As a Forensic Image Analyst, I have examined the provided image and cross-referenced it with real-time reports and historical databases. Below is the detailed forensic report.\n\n### **Phase 1: Visual Forensics**\n\n**General Composition:**\nThe image depicts a massive, billowing plume of dense, black smoke rising into a hazy, pale sky. The smoke originates from a point on the horizon behind a densely packed urban cityscape.\n\n*   **Smoke/Lighting:** The smoke is opaque and textured, suggesting a high-intensity fire involving hydrocarbons or petrochemicals. The lighting is diffused, consistent with late afternoon or a smoggy day. The primary light source is to the upper right, casting soft shadows on the left side of the smoke column.\n*   **Architecture (Geolocators):** The foreground shows a cityscape with low-to-mid-rise residential or commercial buildings. The structures are primarily flat-roofed, light-colored (white, beige, or light grey), and typical of Middle Eastern or Persian Gulf architectural styles (e.g., Tehran or Bandar Abbas). However, no specific landmark (like the Bandar Abbas Port gantry cranes) is clearly visible to confirm the exact location as the port itself.\n*   **Temporal Indicators:** The resolution is low, obscuring specific car models or signs. However, the lack of modern glass skyscrapers in the immediate vicinity suggests an older or more suburban district. \n*   **Manipulation Check:** While the image does not show obvious signs of AI generation (e.g., warped structures or impossible physics), its "standard" appearance—a generic mushroom cloud of smoke over a generic city—is a common trait of **file photos** used by news outlets to illustrate breaking news before actual footage is available.\n\n---\n\n### **Phase 2: Contextual Search**\n\n**1. Earliest Known Source & Context:**\nMy search confirms that this specific image is a **file photo** and does not depict the January 31, 2026, explosion in Bandar Abbas. \n*   **Original Context:** Similar images of thick black smoke over Iranian cities have been documented in previous years. For example, a Reuters file photo dated **June 2, 2021**, shows a similar plume from a refinery fire in southern **Tehran**. \n*   **Reused for Current Event:** Several news agencies (e.g., *Asharq Al-Awsat* and *Al-Monitor*) published this or very similar images on **January 31, 2026**, to illustrate live updates regarding Bandar Abbas, explicitly labeling them as **"File Photo"** or **"Symbolic Image."**\n\n**2. The 2026 Bandar Abbas Incident:**\nAn explosion *did* occur in Bandar Abbas on **January 31, 2026**, but the visual provided does not accurately represent it:\n*   **The Reality:** The actual event involved an explosion at an **eight-storey residential building** on Moallem Boulevard. \n*   **Cause:** Local fire officials (including Chief Mohammad Amin Lyaghat) identified the cause as a **gas leak** and buildup within the building.\n*   **Damage:** The blast blew out the building\'s facade and damaged nearby shops and cars. It did *not* produce the massive, sky-filling black smoke plume seen in your image, which would be characteristic of a large-scale fuel or port facility fire.\n\n**3. Debunking Status:**\n*   Fact-checkers and local officials (such as the Governor of Robat Karim) noted that similar images circulating on social media on Jan 31, 2026, were being falsely attributed to "multiple explosions" or "port attacks." \n*   Specifically, a report from the *Daily Express* highlighted that images of smoke rising from **Parand** (near Tehran) were being shared alongside the Bandar Abbas news but were debunked as a localized reed fire or old footage.\n\n### **Final Verdict**\n**MISLEADING.** The claim that an explosion occurred in Bandar Abbas is **true** (Jan 31, 2026), but the **image is unrelated**. It is a file photo of a previous, much larger industrial fire (likely in Tehran) and is being used as a placeholder. The actual Bandar Abbas incident was a residential building gas explosion, not a massive port-wide disaster as the image implies.',
                        "verdict": "Detailed description generated",
                    },
                    "Semantic_Alignment": {
                        "tool": "Semantic_Alignment_CLIP",
                        "similarity_score": 0.2777,
                        "verdict": "High Visual-Text Consistency",
                    },
                    "ELA_Analysis": {
                        "tool": "ELA_Analysis",
                        "max_difference": 2,
                        "mean_error_level": 0.01,
                        "verdict": "No Obvious Manipulation Artifacts (ELA)",
                    },
                    "Text_Forensics": {
                        "tool": "Text_Forensics",
                        "risk_score": 0,
                        "verdict": "Neutral/Objective Tone",
                        "triggers": [],
                        "ai_analysis": {
                            "top_label": "Objective and Factual",
                            "top_confidence": 0.1785,
                            "all_scores": {
                                "Objective and Factual": 0.178,
                                "Politically Biased": 0.145,
                                "Fear-mongering": 0.13,
                                "Clickbait and Sensationalist": 0.044,
                                "Satire": 0.021,
                            },
                        },
                    },
                },
            },
            {
                "type": "progress",
                "step": "council",
                "status": "running",
                "message": "Convening the Council of LLMs...",
            },
            {
                "type": "result",
                "step": "council",
                "data": [
                    {
                        "member_name": "The Critic",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Authenticity Check",
                                    "observation": "Deepfake_Detector flags the image with a score of 0.8035, indicating it is likely AI-generated. This is a significant red flag for synthetic content.",
                                },
                                {
                                    "step": "Content Verification",
                                    "observation": "Gemini_Vision reveals the image is a file photo from a previous event (likely a 2021 Tehran refinery fire), not the January 31, 2026, Bandar Abbas explosion. The actual incident involved a residential building gas explosion, not a massive port fire.",
                                },
                                {
                                    "step": "Contextual Mismatch",
                                    "observation": "Semantic_Alignment shows high visual-text consistency (0.2777), but Gemini_Vision confirms the image does not depict the claimed event. This is a clear case of out-of-context media reuse.",
                                },
                                {
                                    "step": "Intent Analysis",
                                    "observation": "Text_Forensics shows a neutral tone with no emotional manipulation triggers, suggesting the misleading use of the image may not be intentional but rather a placeholder error by news agencies.",
                                },
                            ],
                            "conclusion": "The image is AI-generated and unrelated to the claimed event. It is a file photo from a previous incident, being used out of context to illustrate the Bandar Abbas explosion. The claim itself is partially true (an explosion occurred), but the visual evidence is misleading.",
                            "verdict": "Misinformation",
                            "confidence_score": 95,
                            "category": "Out-of-Context Media Reuse with Synthetic Content",
                        },
                    },
                    {
                        "member_name": "The Analyst",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Authenticity Check",
                                    "observation": "Deepfake Detector suggests high probability of AI-generation (0.8035), but ELA shows no manipulation artifacts. Gemini Vision confirms this is a real file photo from a previous event (2021 Tehran refinery fire), not current AI generation.",
                                },
                                {
                                    "step": "Content Match Analysis",
                                    "observation": "Semantic Alignment shows high consistency (0.2777) between the image (massive black smoke plume) and claim text (explosion at port). However, Gemini Vision reveals this is misleading visual match - actual Bandar Abbas incident was a residential gas explosion without massive smoke.",
                                },
                                {
                                    "step": "Context Verification",
                                    "observation": "Critical mismatch: Image shows industrial-scale fire (historical file photo), while actual event was residential gas explosion (verified by local officials). Gemini confirms this image is being reused as placeholder with false implication.",
                                },
                                {
                                    "step": "Intent Analysis",
                                    "observation": "Text Forensics shows neutral tone (risk score 0), but image choice creates sensationalism through visual exaggeration of event scale. Citations show multiple outlets used similar file photos, creating false narrative amplification.",
                                },
                            ],
                            "conclusion": "The image is authentic but historically miscontextualized - it depicts a different, larger-scale industrial fire from 2021 being reused to exaggerate a 2026 residential gas explosion. This creates false implication of port attack/major disaster.",
                            "verdict": "Misinformation",
                            "confidence_score": 90,
                            "category": "Out-of-Context Media Reuse with Visual Exaggeration",
                        },
                    },
                    {
                        "member_name": "The Optimist",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Authenticity Check",
                                    "observation": "Deepfake_Detector flags potential AI-generation (Score: 0.8035), but ELA_Analysis shows no manipulation artifacts. Gemini_Vision confirms this is a REAL file photo from 2021, indicating a possible false positive in deepfake detection.",
                                },
                                {
                                    "step": "Content Match",
                                    "observation": "Semantic_Alignment (0.2777) confirms the image shows an explosion in an Iranian city, visually aligning with the claim's text description.",
                                },
                                {
                                    "step": "Context Verification",
                                    "observation": "CRITICAL: Gemini_Vision reveals this image is a 2021 file photo of a Tehran refinery fire. The actual Jan 2026 Bandar Abbas incident involved a residential gas leak explosion without massive smoke plumes.",
                                },
                                {
                                    "step": "Intent Analysis",
                                    "observation": "Text_Forensics shows neutral/objective tone (Risk Score: 0), suggesting no deliberate emotional manipulation in the text itself.",
                                },
                                {
                                    "step": "Source Verification",
                                    "observation": "Citations point to legitimate news outlets, but Gemini_Vision notes they typically label this image as 'file photo' when used in current coverage.",
                                },
                            ],
                            "conclusion": "The image authentically shows an explosion but predates the claimed event by 5 years and misrepresents the scale/nature of the actual incident (residential gas leak vs. industrial-scale fire). While the text claim about an explosion is factually true, the image creates false context about severity and location.",
                            "verdict": "Misinformation",
                            "confidence_score": 90,
                            "category": "Out-of-Context Media Reuse (File Photo Misapplication)",
                        },
                    },
                ],
            },
            {
                "type": "progress",
                "step": "judge",
                "status": "running",
                "message": "The Adjudicator is deliberating...",
            },
            {
                "type": "result",
                "step": "judge",
                "data": {
                    "member_name": "Judge Agent",
                    "output": {
                        "model_evaluations": [
                            {
                                "model": "The Critic",
                                "status": "DISCARD",
                                "reason": "Incorrectly claims image is AI-generated despite Gemini_Vision identifying it as a real file photo. Violates guideline to ignore Deepfake_Detector for non-face images.",
                            },
                            {
                                "model": "The Analyst",
                                "status": "KEEP",
                                "reason": "Correctly references ELA_Analysis and Gemini_Vision findings about historical authenticity. Properly contextualizes forensic evidence without hallucinations.",
                            },
                            {
                                "model": "The Optimist",
                                "status": "KEEP",
                                "reason": "Accurately identifies Deepfake_Detector false positive for non-face image. Cites Semantic_Alignment and Gemini_Vision evidence appropriately.",
                            },
                        ],
                        "final_verdict": "Misinformation",
                        "aggregated_confidence": 90,
                        "explanation": "## Verdict: **Misattributed Media**\n\nThe media is **real/authentic**, but the caption/context is false.\n\n### Forensic Breakdown\n\n* **True Origin:** This image shows a **2021 refinery fire in Tehran** ([gulfnews.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuhzXQnNF4oGyfl3sYVkUB2QOIiMeohIy-6VkGxEB7msu5esdunvjBmtXEtsHjV39rq8AntQ1RJ6BcwpJ040qvmWqwd0qRXrc6TtJxo7WrULgpfuQ-mnfl8V0_q2zLJ-JZt9UII9BWPmyZu4BEyPFJTx8PFWy8erf5cEGyK-_tsdqq4UCaKu-hqOg6e95qEX14huzSwrrxo8r_W8wG1hARJdVsrCA=)), as verified by:\n  - Architectural analysis of Middle Eastern buildings\n  - News agency records labeling this as a file photo\n\n* **False Claim:** Presented as showing the **January 31, 2026, Bandar Abbas explosion** which was:\n  - A **gas leak** in an 8-story residential building ([ctvnews.ca](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5PTfLeF4xXWaRG6_geY4C-8xaWiGSc-iZks8mP5247MjrsMmXSP2i00MGp1bsHAVys5lmr6ikJmQVPMZGL200EWwoLVLmjO4PgS4VQA5V8QjinBcPDC7vW8-Jwg_VxHSCsBH-gq0yD0u0FdyLvWaVHao0GtSjURR74_LE39ifHIRiPyxj810CXmzibq3IWetsm2sjCkbRyn2cRfgMkw==))\n  - Produced localized damage **without massive smoke plumes**\n\n### Why This Matters\n\nThis **out-of-context reuse** exaggerates a real incident (Bandar Abbas gas explosion) by implying:\n1. Industrial-scale destruction\n2. Port facility involvement\n3. Terrorism/national security implications\n\n_Confidence: 90% (based on 2 valid models)_",
                    },
                },
            },
            {"type": "complete", "message": "Analysis complete."},
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
