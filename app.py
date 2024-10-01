import openai
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question')
    
    prompt = f"As a Danish legal expert, answer the following question: '{question}'. Your answer should be supported by references to Danish law, providing accurate citations."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Danish law expert. Answer every question like a lawyer would, always citing relevant Danish law."},
                {"role": "user", "content": prompt},
            ],
        )
        answer = response.choices[0].message['content']
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
