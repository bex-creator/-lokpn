from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# Enable CORS so your HTML frontend can communicate with this Python server
CORS(app)

# Pull the API key from the environment. NEVER hardcode this in a file you upload to the cloud!
API_KEY = os.environ.get("POLLINATIONS_API_KEY")

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get the messages and model from the frontend request
    user_data = request.json
    
    # Forward the request to Pollinations.ai, injecting the secret API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    try:
        # Call the Pollinations API
        pollinations_response = requests.post(
            'https://gen.pollinations.ai/v1/chat/completions',
            headers=headers,
            json=user_data
        )
        
        # Return the AI's response back to the frontend
        return jsonify(pollinations_response.json()), pollinations_response.status_code
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to communicate with AI server"}), 500

if __name__ == '__main__':
    # Cloud providers like Render, Heroku, or Railway assign a PORT dynamically
    port = int(os.environ.get("PORT", 3000))
    print(f"🌸 Python backend starting on port {port}")
    # host='0.0.0.0' allows external connections
    app.run(host='0.0.0.0', port=port)
