import asyncio
import json
import os
import time
import uuid
from typing import List, Optional

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import StreamingResponse

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model_config = {
    "temperature": 0.1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

app = FastAPI(title="OpenAI-compatible API")


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.3
    model: Optional[str] = "gemini-1.5-flash"
    messages: List[Message]
    stream: Optional[bool] = False


async def _async_resp_generator(text_resp: str, request: ChatCompletionRequest):
    model = genai.GenerativeModel(
        model_name=request.model,
        generation_config={
            **model_config,
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        },
    )

    for chunk in model.generate_content(text_resp, stream=True):
        for i, token in enumerate(chunk.text.split(" ")):
            chunk = {
                "id": i,
                "object": "chat.completion.chunk",
                "created": time.time(),
                "model": request.model,
                "choices": [{"delta": {"content": f"{token} "}}],
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.01)
    yield "data: [DONE]\n\n"


@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided.")

    last_message = request.messages[-1].content
    model = genai.GenerativeModel(
        model_name=request.model,
        generation_config={
            **model_config,
            "temperature": request.temperature,
            "max_output_tokens": request.max_tokens,
        },
    )
    resp_content = model.generate_content(last_message).text

    if request.stream:
        return StreamingResponse(
            _async_resp_generator(resp_content, request),
            media_type="application/x-ndjson",
        )

    return {
        "id": uuid.uuid4(),
        "object": "chat.completion",
        "created": time.time(),
        "model": request.model,
        "choices": [{"message": Message(role="assistant", content=resp_content)}],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
