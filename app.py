import openai
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes lets try again

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

    # Add some error checking for the question input
    if not question:
        return jsonify({"error": "No question provided"}), 400

    prompt = f"As a Danish legal expert, answer the following question: '{question}'. Your answer should be supported by references to Danish law, providing accurate citations."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Danish law expert. Answer every question like a lawyer would, always citing relevant Danish law."},
                {"role": "user", "content": prompt},
            ],
        )
        answer = response.choices[0].message['content']
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error for debugging
        return jsonify({"error": "There was an error processing your request"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
