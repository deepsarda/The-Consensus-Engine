import os

import json
import asyncio
import base64
import random
import string
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from termcolor import colored

from forensics import ForensicAnalyzer
from council import Council
from judge import JudgeAgent

# Directory to save uploaded images temporarily
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    print(colored("Loading models... This may take a moment.", "yellow"))
    app.state.analyzer = ForensicAnalyzer()
    app.state.council = Council()
    app.state.judge = JudgeAgent()
    print(colored("All models loaded successfully!", "yellow"))
    yield
    # Clean up on shutdown if needed
    print(colored("Shutting down...", "red"))


app = FastAPI(title="The Consensus Engine", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_filename(extension: str = ".jpg") -> str:
    """Generates a random filename."""
    chars = string.ascii_letters + string.digits
    name = "".join(random.choice(chars) for _ in range(12))
    return f"{name}{extension}"


@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    await websocket.accept()
    try:
        # Await initial message with claim and image
        data = await websocket.receive_json()
        claim = data.get("claim")
        image_data_b64 = data.get("image")  # Base64 string

        if not claim or not image_data_b64:
            await websocket.send_json(
                {"type": "error", "message": "Missing claim or image."}
            )
            return

        # Decode and save image
        try:
            # Handle data:image/jpeg;base64, prefix if present
            if "," in image_data_b64:
                header, encoded = image_data_b64.split(",", 1)
                # Simple extension detection
                ext = ".jpg"
                if "png" in header:
                    ext = ".png"
                elif "jpeg" in header:
                    ext = ".jpg"
                elif "webp" in header:
                    ext = ".webp"
            else:
                encoded = image_data_b64
                ext = ".jpg"

            image_bytes = base64.b64decode(encoded)
            filename = generate_filename(ext)
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                f.write(image_bytes)

            await websocket.send_json(
                {
                    "type": "progress",
                    "step": "upload",
                    "status": "complete",
                    "message": "Image uploaded and processed.",
                }
            )

        except Exception as e:
            await websocket.send_json(
                {"type": "error", "message": f"Failed to save image: {str(e)}"}
            )
            return

        # Forensics
        await websocket.send_json(
            {
                "type": "progress",
                "step": "forensics",
                "status": "running",
                "message": "Analyzing forensic evidence...",
            }
        )

        # Run in executor to avoid blocking event loop
        loop = asyncio.get_event_loop()

        forensics = await loop.run_in_executor(
            None, app.state.analyzer.run_all, file_path, claim
        )

        await websocket.send_json(
            {"type": "result", "step": "forensics", "data": forensics}
        )

        # Council
        await websocket.send_json(
            {
                "type": "progress",
                "step": "council",
                "status": "running",
                "message": "Convening the Council of LLMs...",
            }
        )

        council_results = await loop.run_in_executor(
            None, app.state.council.convene, claim, "Image", forensics
        )

        await websocket.send_json(
            {"type": "result", "step": "council", "data": council_results}
        )

        # Judge
        await websocket.send_json(
            {
                "type": "progress",
                "step": "judge",
                "status": "running",
                "message": "The Adjudicator is deliberating...",
            }
        )

        final_verdict = await loop.run_in_executor(
            None, app.state.judge.adjudicate, forensics, council_results
        )

        await websocket.send_json(
            {"type": "result", "step": "judge", "data": final_verdict}
        )

        await websocket.send_json({"type": "complete", "message": "Analysis complete."})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass
    finally:
        pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
