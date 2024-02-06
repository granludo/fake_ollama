from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.responses import Response
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import asyncio




app = FastAPI()

# Helper function to simulate your original list_local_models
def list_local_models():
    return {
        "models": [
            {
                "name": "mixtral:latest",
                "modified_at": "2023-11-04T14:56:49.277302595-07:00",
                "size": 7365960935,
                "digest": "9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
                "details": {
                    "format": "gguf",
                    "family": "llama",
                    "parameter_size": "13B",
                    "quantization_level": "Q4_0"
                }
            },
            {
                "name": "Pet.artdo",
                "modified_at": "2023-12-07T09:32:18.757212583-08:00",
                "size": 3825819519,
                "digest": "fe938a131f40e6f6d40083c9f0f430a515233eb2edaa6d72eb85c50d64f2300e",
                "details": {
                    "format": "gguf",
                    "family": "llama",
                    "parameter_size": "7B",
                    "quantization_level": "Q4_0"
                }
            }
        ]
    }

async def log_request(request: Request):
    body = await request.body()
    print(f"Access to: {request.method} {request.url.path}")
    print(f"Full URL: {request.url}")
    print(f"Headers: {json.dumps({key: value for key, value in request.headers.items()}, indent=2)}")
    if body:
        try:
            print(f"Body: {body.decode('utf-8')}")
        except Exception as e:
            print(f"Error reading body: {e}")


class NDJSONResponse(Response):
    media_type = "application/x-ndjson"

    def __init__(self, content, *args, **kwargs):
        super().__init__(content=content, *args, **kwargs)

    async def body_iterator(self, data):
        async for item in data:
            yield json.dumps(item).encode('utf-8') + b'\n'

async def generate_stream_data():
    parts = ["How", "cool", "is", "that?"]
    for part in parts:
        await asyncio.sleep(0.1)
        yield {"message": part}

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    return NDJSONResponse(generate_stream_data())


@app.post('/api/generate')
async def generate_completion(data: Dict[str, Any]):
    await log_request(Request)
    # Your logic here...
    response = {
        "model": data.get('model'),
        "created_at": "2023-08-04T19:22:45.499127Z",
        # Rest of your response...
    }
    return JSONResponse(response)


@app.post('/api/chat')
async def generate_chat_completion(request: Request):
    await log_request(request)
    body = await request.body()
    
    try:
        data = json.loads(body.decode('utf-8'))
    except json.JSONDecodeError as e:
        return JSONResponse(content={"error": f"Error parsing JSON: {e}"}, status_code=400)

    stream = data.get('stream', True)
    
    if stream:
        return StreamingResponse(generate_stream_response(data), media_type='application/x-ndjson')
    else:
        response = {
            "model": data.get('model', 'default:model'),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "message": {
                "role": "assistant",
                "content": "This is a complete simulated chat response, not streamed."
            },
            "done": True,
            "total_duration": 1234567,
            "load_duration": 12345,
            "prompt_eval_count": 50,
            "prompt_eval_duration": 54321,
            "eval_count": 150,
            "eval_duration": 98765
        }
        return JSONResponse(response)

@app.get('/api/version')
async def get_version():
    return {"version": "0.1.23"}

@app.get('/api/tags')
async def get_models():
    models = list_local_models()
    return models

@app.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def catch_all(path: str, request: Request):
    await log_request(request)
    return JSONResponse({"error": "Endpoint not found or not implemented yet."}, status_code=404)

