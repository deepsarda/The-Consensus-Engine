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
                    "Citations": "- [hindustantimes.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpT4QwJ8qYTOdMdjlOZEsRfJmPysXoaN8-bBIWpmY6T71gAyOj0NgSqx4eLaIGybjG8-XHwQC-Fn35MItXgkDFjvdXRZBLWoVNXRNzdcIQ7lPsGi2fonhLEwnegb2gpejFmmo2rlqtYcH178guc0-WoQjg6ZJTJRQSbtDo3HyLsb_4ND14k7pcefrgsJLtiHYbhpYTXpkiNnnw4cM3VO7HBCML7977c2SfD32dawNG3EtYzSBKeysGtpOvXEAyjbCazs0ctu7G)\n- [ncr-iran.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEfFf2yI5fLHjO-opDUgfnuZfYTCyMfyHN2Qxtxazy7Y2VMDHaHV7sSEerWonVprWsrL8Nk8QwODxjHPAyv-3rz6P90Ya5LrreFmcb979iBjzqluJPIAMbFaMN--I0a-8vRh5_BqynbJGjlYPg8pMffkl1B3xV51_mtL582GsJ3LpvQ4aCYhOUg6I_n-_jk2kc3VXymKNHprnHTTf3JItcFYJ9AoF60i20yIMcSTylasUovCV2fYkz9iw-XYoQ71rqhcO4a3nNr7tM=)\n- [cbsnews.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFYy1PRhdWZV0e4WWRL8IAiuUvcB_SZ2hJrCa0nUvOB_fr1oXLMYYa3CNWHMjNmWmPuu5cQ_qkMwCvN9HKb021X8On7vV0JnbqRw5cklB3cioPQSXARK_mX9ON86zXqYjGd2ee0sbI09OWoJDQjKdYdF_AlS7i21xUfK9Ks1LAODflki3eSY6c=)\n- [wikipedia.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF7i8n0E7TcpSbdfj8gbxMhLIplDdp3G70wC0RfT0qHVMlVYU8iplcskdfcG91fHpG1tex1g5XxoNs0SaK0dlK4uEkmzRC6njLo1g86v7P152WBwU1W8sJILCaXTv551jFGt2D32pS7nTrz_Iz0T9sGyRaoBxYoBYU=)\n- [mines.edu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE8oIWEctGnwsyJlVU0adphVOOk5usRd-Wi7sB083TsAppLNCS6GM51VvhVptOjFjDOpdWzFe3nHUg99RDe3BK58y0g8ALtKjAsE-scvWh3u5CBnEag-f3YxSLXvZ9BzHN_rbSOBuUXAZa9qOtpRR2JPpF8XGhJviT4S8gU0lxaLePU)\n- [ground.news](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnq48KX0QX9nl15idyVN-lnCK7sGC2SZI0LsAC7DFhM6IDU6E4JYX3LHnmsijSoKi751QMICPLtEAEhiRrLwcy--F-5UZ3KKjhC2n_buS0GXo6mVrWcfCcQQBsVMZA2saIGduwxkQWCfPvQDUevXtbQlgxjvS23ibllUVnMRCzaWxLvHAYn2Ugr4RIHsqAdDJpPq2jLDEz79zh5gSD0OnVi-SQQhdafQJfktMszC0QaC7RAkeMhg==)\n- [iranintl.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHcsibWfF8ybFvWIgXgWANDp91InnwfV8NAcQN7-u70Fe6gK96BVIKJG8lAiCXrt6-dNbe_D0vDpTfo_-KmBaVLkinO_gd2BCPzLmfPFT_aBbe-TtXDd-wnJgbt7VzfTQ8oYng=)",
                    "Metadata_Analysis": {
                        "tool": "Metadata_Analyzer",
                        "metadata_found": False,
                        "data": {},
                        "verdict": "No metadata found",
                    },
                    "Gemini_Vision": {
                        "tool": "Gemini_Image_Describer",
                        "description": 'As a Forensic Image Analyst, I have conducted a visual and contextual investigation of the provided image. Here are the findings:\n\n### **Phase 1: Visual Forensics**\n*   **Subject Matter:** The image depicts a massive, towering column of dense black smoke rising from a coastal or industrial area into a hazy sky. \n*   **Foreground:** A dense residential or commercial area featuring multi-story, light-colored (white/tan) rectangular buildings typical of Persian Gulf architecture.\n*   **Background:** A distinct, long mountain ridge is visible through the haze, which is characteristic of the geography surrounding **Bandar Abbas** (specifically the Geno/Hormozgan mountain ranges).\n*   **Temporal & Environmental Indicators:** The lighting suggests early morning or late afternoon. The sheer volume and density of the smoke indicate a large-scale industrial or fuel-related fire, rather than a localized building fire.\n*   **Manipulation Check:** The image appears to be a low-resolution screengrab from a video. While no obvious AI artifacts (like warped hands or floating objects) are present, the image quality is intentionally degraded, a common trait of "viral" recycled media.\n\n---\n\n### **Phase 2: Contextual Search & Verification**\nMy investigation confirms that while the **text of the claim** refers to a real event from January 31, 2026, the **image itself is recycled** and misleadingly used.\n\n*   **Original Event:** This image was first documented on **April 26, 2025**. It depicts a catastrophic explosion at the **Shahid Rajaee Port** (Iran\'s largest container terminal), located southwest of Bandar Abbas. That incident involved the explosion of chemical containers (purportedly ammonium perchlorate) and resulted in over 70 deaths and a plume of smoke visible by satellite.\n*   **Current Event (Jan 31, 2026):** On January 31, 2026, a separate explosion occurred in Bandar Abbas at an **eight-story residential/commercial building** on Moallem Boulevard. Official reports (and confirmed footage) show the building’s facade blown out and structural damage to two floors. Authorities attributed this 2026 blast to a **gas leak**.\n*   **Discrepancy:** The massive industrial smoke plume in your image is physically inconsistent with a gas leak in a single apartment building. The 2026 incident produced debris and localized smoke, but not the kilometer-high column of black smoke shown in the 2025 port disaster photo.\n\n### **Conclusion**\n**STATUS: MISLEADING / RECYCLED IMAGE**\n\nThe claim about an explosion in Bandar Abbas on January 31, 2026, is **TRUE** (it was a fatal gas leak in a residential building). However, the image provided is **FALSELY LINKED** to that event. It is a **file photo from the April 2025 Shahid Rajaee port explosion**. \n\nNews outlets like *Hindustan Times* and social media accounts are currently using this 2025 photo as a "representational image," which can lead viewers to believe the current "Iran-US tension" situation involves a much larger strategic or industrial attack than the localized accident reported.',
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
                                    "observation": "Deepfake_Detector indicates the image is likely AI-generated with a score of 0.8035. However, Gemini_Vision suggests the image is a low-resolution screengrab from a video, not a synthetic image. This discrepancy needs careful consideration.",
                                },
                                {
                                    "step": "Content Match",
                                    "observation": "Semantic_Alignment shows high visual-text consistency with a score of 0.2777, indicating the image does depict a large explosion with smoke, which aligns with the claim of an explosion at Bandar Abbas.",
                                },
                                {
                                    "step": "Context Verification",
                                    "observation": "Gemini_Vision provides critical context: the image is actually from the April 26, 2025 Shahid Rajaee Port explosion, not the January 31, 2026 incident described in the claim. The claim is about a gas leak in a residential building, but the image shows a massive industrial fire.",
                                },
                                {
                                    "step": "Intent Analysis",
                                    "observation": "Text_Forensics shows a neutral and objective tone with a risk score of 0, suggesting the text itself is not emotionally manipulative. However, the use of a recycled image to represent a different event is misleading.",
                                },
                            ],
                            "conclusion": "The image is real but is being used in a falsified context (Out-of-Context Media). While the Deepfake_Detector suggests the image might be AI-generated, Gemini_Vision clarifies it is a real image from a different event. The claim about an explosion in Bandar Abbas on January 31, 2026, is true, but the image provided is from the April 2025 Shahid Rajaee port explosion. This is a case of recycled media being used to mislead viewers about the scale and nature of the current event.",
                            "verdict": "Misinformation",
                            "confidence_score": 90,
                            "category": "Out-of-Context Media Reuse",
                        },
                    },
                    {
                        "member_name": "The Analyst",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Authenticity Check",
                                    "observation": "Deepfake_Detector indicates potential AI-generation (score 0.8035), but tool is IGNORED per guidelines since image contains no faces. ELA_Analysis shows no manipulation artifacts (max difference 2), confirming the image is likely real.",
                                },
                                {
                                    "step": "Content Match",
                                    "observation": "Semantic_Alignment score 0.2777 (High Consistency) confirms the image shows an explosion in a coastal/residential area consistent with Bandar Abbas.",
                                },
                                {
                                    "step": "Context Verification",
                                    "observation": "CRITICAL: Gemini_Vision analysis identifies this as a recycled image from the April 2025 Shahid Rajaee Port explosion, not the January 2026 residential gas leak. The industrial-scale plume contradicts official reports of a localized building incident.",
                                },
                                {
                                    "step": "Intent Analysis",
                                    "observation": "Text_Forensics shows neutral/objective tone (risk score 0), but pairing with a dramatic recycled image creates misleading scale perception despite factual claim.",
                                },
                            ],
                            "conclusion": "The claim describes a real event (January 2026 gas leak), but uses an unrelated image from a 2025 industrial explosion to falsely amplify the severity. This constitutes out-of-context media reuse.",
                            "verdict": "Misinformation",
                            "confidence_score": 90,
                            "category": "Out-of-Context Media Reuse (Temporal Mismatch)",
                        },
                    },
                    {
                        "member_name": "The Optimist",
                        "output": {
                            "reasoning_steps": [
                                {
                                    "step": "Synthetic Media Check",
                                    "observation": "Deepfake_Detector flags high AI probability (0.8035), but Gemini_Vision identifies this as a low-resolution screengrab from real 2025 footage. Prioritizing contextual analysis over potential false-positive from image degradation.",
                                },
                                {
                                    "step": "Content Verification",
                                    "observation": "Semantic_Alignment confirms image shows massive explosion (Score 0.2777 > 0.25 threshold), visually matching claim about 'explosion damaging residential building'.",
                                },
                                {
                                    "step": "Temporal Context Analysis",
                                    "observation": "CRITICAL DISCREPANCY: Gemini_Vision confirms image is from 2025 Shahid Rajaee Port explosion, not the 2026 residential gas leak event described in claim. Smoke plume scale inconsistent with residential gas explosion.",
                                },
                                {
                                    "step": "Manipulation Check",
                                    "observation": "ELA_Analysis finds no splicing artifacts (Max Difference 2), confirming the image is intact but recycled rather than digitally altered.",
                                },
                                {
                                    "step": "Intent Analysis",
                                    "observation": "Text_Forensics shows neutral tone (Risk Score 0), indicating the misinformation likely stems from careless sourcing rather than deliberate fear-mongering.",
                                },
                            ],
                            "conclusion": "While the claim describes a real event (2026 residential gas explosion), the image is deceptively reused from a larger 2025 industrial disaster. This creates false perception of event scale and implied geopolitical escalation.",
                            "verdict": "Misinformation",
                            "confidence_score": 90,
                            "category": "Out-of-Context Media Reuse (Temporal Mismatch)",
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
                                "status": "KEEP",
                                "reason": "Correctly cited Gemini_Vision and Semantic_Alignment evidence but incorrectly considered Deepfake_Detector (non-face image). Minor deduction for guideline oversight.",
                            },
                            {
                                "model": "The Analyst",
                                "status": "KEEP",
                                "reason": "Properly ignored Deepfake_Detector (non-face), accurately cited Semantic_Alignment and Gemini_Vision forensic evidence.",
                            },
                            {
                                "model": "The Optimist",
                                "status": "KEEP",
                                "reason": "Correctly dismissed Deepfake_Detector (per guidelines), thoroughly integrated Gemini_Vision timeline analysis and ELA forensics.",
                            },
                        ],
                        "final_verdict": "Misinformation",
                        "aggregated_confidence": 90,
                        "explanation": "## Verdict: Misinformation \n\n### Analysis\n\nThe **media is authentic**, but the **caption/context is false**. This is a **misattributed media** case.\n\n* **True Context:** This image depicts the **April 26, 2025 explosion at Shahid Rajaee Port** (Bandar Abbas, Iran). Official reports confirm this was an industrial chemical container blast killing 70+ people, visible by satellite.\n* **Claimed Context:** The image is falsely presented as showing a **January 31, 2026 residential gas leak explosion** on Moallem Boulevard in Bandar Abbas. This real 2026 event caused facade damage to one building, not a massive industrial smoke plume.\n\n### Forensic Validation  \n- **Semantic Alignment (0.2777):** High visual consistency with “explosion” descriptions but mismatched to the 2026 claim.  \n- **ELA Analysis:** No manipulation artifacts found, confirming image authenticity.  \n- **Gemini_Vision:** Geolocated mountains match Bandar Abbas but date-stamped to 2025 port disaster.  \n\n### Why This Matters  \nRecycling dramatic imagery from past disasters to represent unrelated events exaggerates severity and implies geopolitical escalation (e.g., Iran-US tensions). News outlets using this as “representational” imagery mislead audiences about the actual residential accident.",
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
