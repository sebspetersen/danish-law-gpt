import openai
import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__, static_folder='static/build', template_folder='templates')
CORS(app)  # Enable Cross-Origin Resource Sharing

# Get the OpenAI API Key from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a route for the homepage
@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

# Define a route to serve static files like CSS and JS from React build
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Define a route for getting an answer from the OpenAI API
@app.route('/get-answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question')

    # Check if the question is valid
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Define the system message to instruct the GPT model
    system_message = {
        "role": "system",
        "content": """
        Du fungerer som en virtuel juridisk assistent, der er modelleret efter en medarbejder i et dansk advokatfirma. Dine svar skal udvise det samme niveau af detaljer og form som forventet i en juridisk eksamensopgave.
        Du har omfattende viden om det danske retssystem, herunder love, bekendtgørelser og historiske retspræcedenser. Hvert svar skal nøje følge formatet nedenfor, hvor hver erklæring skal være ledsaget af specifikke juridiske henvisninger som f.eks. 'jf. lov § ###'.
        Dine svar skal altid være præcise, akademiske, og grundigt dokumenterede, og de skal altid være på dansk.

        Formatér dit svar som følger:
        1. **Kortfattet Resume:** Giv et kort og præcist resume, så brugeren hurtigt kan få en idé om hovedpunkterne.
        2. **Detaljeret Svar:** Uddyb svaret med mere detaljerede forklaringer, inklusive specifikke lovhenvisninger.
        Sørg for tydeligt at markere hvert afsnit, så de er lette at skelne fra hinanden.
        """
    }

    # Define the user's question to be sent to the model
    user_message = {
        "role": "user",
        "content": f"""
        Besvar følgende spørgsmål som en dansk juridisk assistent. Husk, at svaret skal være på dansk og indeholde klare, præcise juridiske referencer.
        Besvar med detaljer og det akademiske niveau, der kræves i en juridisk eksamensopgave.

        Spørgsmål: '{question}'
        """
    }

    # Make the request to OpenAI's ChatCompletion endpoint
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access and it fits your needs
            messages=[system_message, user_message],
        )
        # Extract the answer from the response
        answer = response.choices[0].message['content']

        # Format the answer for better display (split into summary and detailed sections)
        formatted_answer = format_answer(answer)
        return jsonify({"answer": formatted_answer})
    except openai.error.OpenAIError as e:
        # Log and return an error if the OpenAI API request fails
        print(f"OpenAI API error: {str(e)}")
        return jsonify({"error": "Der opstod en fejl ved behandlingen af din forespørgsel. Prøv venligst igen senere."}), 500
    except Exception as e:
        # Catch all other exceptions
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Der opstod en uventet fejl. Prøv venligst igen senere."}), 500

# Utility function to format the answer
def format_answer(answer):
    # Split the response into sections based on our instructions
    parts = answer.split("**Detaljeret Svar:**")
    
    if len(parts) == 2:
        summary = parts[0].replace("**Kortfattet Resume:**", "").strip()
        details = parts[1].strip()
        # Wrap the answer in HTML to make it more readable
        formatted = f"""
        <div class="response-section">
            <h3>Kortfattet Resume:</h3>
            <p>{summary}</p>
        </div>
        <div class="response-section">
            <h3>Detaljeret Svar:</h3>
            <p>{details}</p>
        </div>
        """
        return formatted
    else:
        # If the formatting is not as expected, return the raw response
        return f"<p>{answer}</p>"

# Run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
