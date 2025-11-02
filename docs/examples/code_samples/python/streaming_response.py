"""
Example: Streaming AI Response with FastAPI and Server-Sent Events
Technique Reference: Python Backend #40-41
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

async def generate_ai_stream(prompt: str):
    """Simulate streaming AI response"""
    response = "This is a simulated AI response that streams token by token."
    
    for token in response.split():
        await asyncio.sleep(0.1)  # Simulate processing
        yield f"data: {json.dumps({'token': token})}\n\n"
    
    yield "data: [DONE]\n\n"

@app.post("/api/chat/stream")
async def stream_chat(prompt: str):
    """Streaming chat endpoint"""
    return StreamingResponse(
        generate_ai_stream(prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

# Run with: uvicorn streaming_response:app --reload
