from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)
load_dotenv()
# Replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = os.getenv("API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def ask_question():
    try:
        user_input = request.json['message']

        # Craft a prompt for GPT-3
        prompt = f"Please provide information on the following health-related question: {user_input}\n"

        # Call GPT-3 API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,  # Adjust as needed
            temperature=0.7  # Adjust for creativity vs. accuracy
        )

        gpt_response = response.choices[0].text.strip()

        # Check if the response contains health-related content
        if is_health_related(gpt_response):
            return jsonify({'message': gpt_response})
        else:
            return jsonify({'message': "Sorry, I don't have information about it."})

    except Exception as e:
        return jsonify({'error': str(e)})

def is_health_related(response):
    # Implement your logic to check if the response is health-related
    # For simplicity, this example checks if the response contains the word 'health'
    return 'health' in response.lower()

if __name__ == '__main__':
    app.run(debug=True)
