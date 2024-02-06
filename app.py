from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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
