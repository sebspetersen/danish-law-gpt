import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the OpenAI API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

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
    app.run()
