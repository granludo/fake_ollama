from flask import Flask, request, jsonify, Response
import json
import time
from datetime import datetime


app = Flask(__name__)


@app.route('/api/generate', methods=['POST'])
def generate_completion():
    # Parse the JSON data from the request
    data = request.get_json()

    # Required parameters
    model = data.get('model')
    prompt = data.get('prompt')

    # Optional parameters with defaults
    images = data.get('images', [])  # Assuming images are not processed in this example
    format = data.get('format', 'json')  # Default to 'json' if not specified
    options = data.get('options', {})
    system = data.get('system', '')
    template = data.get('template', '')
    context = data.get('context', [])
    stream = data.get('stream', False)  # Always false in this implementation
    raw = data.get('raw', False)

    # Here, you would add logic to generate a response using the provided model and prompt.
    # This is a simplified example response.
    response = {
        "model": model,
        "created_at": "2023-08-04T19:22:45.499127Z",  # Example timestamp
        "response": "Ese pecadorrrr! Fistro de la pradera!.",
        "done": True,
        "context": context,  # Echo back the provided context for continuity
        "total_duration": 123456789,  # Simulated timing data
        "load_duration": 123456,
        "prompt_eval_count": len(prompt.split()),  # Simulated evaluation count
        "prompt_eval_duration": 654321,
        "eval_count": 100,  # Simulated response token count
        "eval_duration": 987654
    }

    return jsonify(response)



def log_request(request):
    print(f"Access to: {request.method} {request.path}")

    # Logging the full URL
    print(f"Full URL: {request.url}")

    # Logging the raw query string for all request types
    if request.query_string:
        print(f"Raw Query String: {request.query_string.decode('utf-8')}")

    # Handling GET requests by logging URL query parameters
    if request.method == 'GET':
        query_params = {key: request.args[key] for key in request.args}
        if query_params:
            print(f"Query Parameters: {json.dumps(query_params, indent=2)}")
        else:
            print("No Query Parameters.")

    # Logging the headers
    headers = {key: value for key, value in request.headers}
    print(f"Headers: {json.dumps(headers, indent=2)}")

    # Attempt to log JSON body data for POST requests
    if request.method == 'POST' and request.data:
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            try:
                data = request.get_json()
                if data is not None:
                    print(f"JSON Request Data: {json.dumps(data, indent=2)}")
                else:
                    print("No JSON Request Data or invalid JSON.")
            except Exception as e:
                print(f"Error reading JSON body: {e}")
        else:
            # For non-JSON body content, log as raw data
            try:
                data = request.get_data(as_text=True)
                if data:
                    print(f"Raw Request Data: {data}")
                else:
                    print("No Raw Request Data.")
            except Exception as e:
                print(f"Error reading raw body: {e}")



@app.route('/api/chat', methods=['POST'])
def generate_chat_completion():
    log_request(request)
    
    # Manually read the raw data and parse as JSON
    try:
        raw_data = request.get_data(as_text=True)
        data = json.loads(raw_data)
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {e}", 400  # Bad Request for JSON parsing errors
    
    # Handle streaming and non-streaming based on 'stream' flag in the data
    stream = data.get('stream', True)  # Assume streaming by default
    
    if stream:
        # Return a streaming response
        return Response(generate_stream_response(data), content_type='text/event-stream')
    else:
        # Non-streaming response
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
        return jsonify(response)



def generate_stream_response(data):
    message = "I need information on a specific topic, feel free to ask!"
    parts = message.split()  # Example: Splitting a predefined message into parts
    
    for i, part in enumerate(parts, 1):
        time.sleep(0.1)  # Simulate processing delay
        
        part_response = {
            "model": data.get('model', 'default:model'),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "message": {
                "role": "assistant",
                "content": part
            },
            "done": False  # Keep false until the last part
        }
        
        # Add additional metadata on the last part
        if i == len(parts):
            part_response["done"] = True
            part_response.update({
                "total_duration": 1234567,
                "load_duration": 12345,
                "prompt_eval_count": 50,
                "prompt_eval_duration": 54321,
                "eval_count": 150,
                "eval_duration": 98765
            })
        
        yield f"data: {json.dumps(part_response)}\n\n"


@app.route('/api/version', methods=['GET'])
def get_version():
    # Define your version information or fetch it from somewhere if dynamic
    version_info = {"version": "0.1.23"}
    return jsonify(version_info), 200

@app.route('/api/tags', methods=['GET'])
def get_models():
    models = list_local_models()  # Fetch the list of models
    return jsonify(models), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    # Logging the method and path
    print(f"Unhandled access to: {request.method} {request.path}")
    
    # Logging the full URL
    print(f"Full URL: {request.url}")
    
    # Logging the headers
    headers = {key: value for key, value in request.headers}
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    # Logging query parameters
    query_params = {key: request.args[key] for key in request.args}
    print(f"Query Parameters: {json.dumps(query_params, indent=2)}")
    
    # Logging the body of the request, if any
    try:
        body = request.json if request.is_json else request.data.decode()
    except Exception as e:
        body = f"Error reading body: {e}"
    print(f"Body: {json.dumps(body, indent=2) if isinstance(body, dict) else body}")
    
    return jsonify({"error": "Endpoint not found or not implemented yet."}), 404

def list_local_models():
    # This is a placeholder for how you might list your models
    return {
        "models": [
            {
                "name": "Pepino:del.norte",
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

if __name__ == '__main__':
    app.run(debug=True, port=11434)
