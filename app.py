from flask import Flask, render_template, request
import openai
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("API_KEY")

app = Flask(__name__)
data_files = [data_file for data_file in os.listdir('./Data') if data_file.endswith('.json')]
data = []

@app.route('/', methods=['GET', 'POST'])
def chat():
    entry_message = "Hello SAP😄! I am Kushi AI Virtual Assistant"
    if request.method == 'POST':
        user_question = request.form['question']
        
        for data_file in data_files:
            with open('./Data/' + data_file) as f:
                file_data = json.load(f)
            data.append(file_data)

        if api_key:
            openai.api_key = api_key
        else:
            print("API Key not found. Please check your .env file.")
        #openai.api_key =   # Replace with your API key

        messages = [
            {"role": "system", "content": f"The assistant is a virtual representation of a person named Niharika. Here is some information about her: {json.dumps(data, indent=2)}"},
            {"role": "user", "content": user_question}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  
            messages=messages,
        )

        generated_text = response['choices'][0]['message']['content']
        #generated_text = ' '.join(responses)
        return render_template('chat.html', question=user_question, answer=generated_text)

    return render_template('chat.html', entry_message=entry_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)