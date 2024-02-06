from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
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


@app.get('/api/version')
async def get_version():
    return {"version": "0.1.23"}

@app.get('/api/tags')
async def get_models():
    models = list_local_models()
    return models




async def generate_stream_response(model_name: str, full_message: str):
    start_time = datetime.utcnow()
    # Split the full message into parts to stream them one by one
    message_parts = list(full_message)  # Splitting the message into individual characters for fine-grained streaming
    total_parts = len(message_parts)

    for i, part in enumerate(message_parts, start=1):
        await asyncio.sleep(0.03)  # Simulate a slight delay between parts
        
        created_at = datetime.utcnow().isoformat() + "Z"
        content = part if part.strip() else "." if i < total_parts else ""  # Replace empty spaces with '.' for demonstration, except the last part
        part_response = {
            "model": model_name,
            "created_at": created_at,
            "message": {"role": "assistant", "content": content},
            "done": False
        }

        if i == total_parts:
            part_response["done"] = True
            end_time = datetime.utcnow()
            # Include statistics in the final part
            part_response.update({
                "total_duration": int((end_time - start_time).total_seconds() * 1e9),
                "load_duration": 38404189875,  # Example fixed value
                "prompt_eval_count": 29,
                "prompt_eval_duration": 533928000,
                "eval_count": 198,
                "eval_duration": 5711725000
            })

        yield f"data: {json.dumps(part_response)}\n"

@app.post("/api/chat")
async def generate_chat_completion(request: Request):
    body = await request.json()
    model_name = body.get('model', 'mixtral:latest')
    # For demonstration, concatenate all messages into a single string
    full_message = " ".join([msg["content"] for msg in body.get('messages', [])])
    
    return StreamingResponse(generate_stream_response(model_name, full_message), media_type='text/event-stream')



@app.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
async def catch_all(path: str, request: Request):
    await log_request(request)
    return JSONResponse({"error": "Endpoint not found or not implemented yet."}, status_code=404)


