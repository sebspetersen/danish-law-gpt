import openai
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Get the OpenAI API Key from the environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

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
        Du har omfattende viden om det danske retssystem, herunder love, bekendtgørelser og historiske retspræcedenser. Hvert svar skal nøje følge den format, der kræves i juridiske eksamener, hvor enhver erklæring skal være ledsaget af specifikke juridiske henvisninger som f.eks. 'jf. lov § ###'.
        Dine svar skal altid være præcise, akademiske, og grundigt dokumenterede, og de skal altid være på dansk.
        
        Eksempel:
        Spørgsmål: "Hvad er reglerne for forældremyndighed i Danmark?"
        Svar: "Reglerne om forældremyndighed findes i Forældreansvarsloven, jf. lovbekendtgørelse nr. 1085 af 2021. Ifølge § 4 har begge forældre som udgangspunkt fælles forældremyndighed, medmindre andet er aftalt eller bestemt af retten, jf. Forældreansvarsloven § 11. Dette betyder, at begge forældre har lige rettigheder og ansvar i forhold til barnets opvækst og trivsel."
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
        return jsonify({"answer": answer})
    except openai.error.OpenAIError as e:
        # Log and return an error if the OpenAI API request fails
        print(f"OpenAI API error: {str(e)}")
        return jsonify({"error": "Der opstod en fejl ved behandlingen af din forespørgsel. Prøv venligst igen senere."}), 500
    except Exception as e:
        # Catch all other exceptions
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Der opstod en uventet fejl. Prøv venligst igen senere."}), 500

# Run the application
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
