import httpx
import json

LLM_URL = "http://127.0.0.1:8080/v1/chat/completions"

async def stream_llm_response(messages):
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            LLM_URL,
            json={
                "model": "local",
                "messages": messages,
                "stream": True,
                "temperature": 0.8
            }
        ) as response:
            async for line in response.aiter_lines():
                if not line:
                    continue
                if line.startswith("data: "):
                    data = line.replace("data: ", "")
                    if data == "[DONE]":
                        break
                    try:
                        token = json.loads(data)["choices"][0]["delta"].get("content")
                        if token:
                            yield token
                    except Exception:
                        pass
