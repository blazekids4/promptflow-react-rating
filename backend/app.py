from flask import Flask, request, jsonify
from main import handle_prompt  # Assuming you have a function `handle_prompt` in your `main.py` that takes a prompt and returns a response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    chat_history = data.get('chat_history', [])
    if prompt:
        response = handle_prompt(prompt, chat_history)
        return jsonify({'response': response})
    else:
        return jsonify({'error': 'No prompt provided'}), 400


if __name__ == '__main__':
    app.run(debug=True)
