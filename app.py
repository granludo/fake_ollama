from flask import Flask, request, jsonify
import json

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
