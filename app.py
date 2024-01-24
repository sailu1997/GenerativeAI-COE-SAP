from flask import Flask, render_template, request, jsonify, session
import openai
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("API_KEY")

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'vbaesldzsc2308hfewocnaslXZkwcpdsx'

data_files = [data_file for data_file in os.listdir('./Data') if data_file.endswith('.json')]
data = []

for data_file in data_files:
    with open('./Data/' + data_file) as f:
        file_data = json.load(f)
    data.append(file_data)

app.config['DATA'] = data

@app.route('/', methods=['GET', 'POST'])
def chat():
    entry_message = "Hello SAP😄! I am Niha.. How can I help you today ?"

    if 'chatHistory' not in session:
        print("Chat history not found. Creating new chat history.")
        session['chatHistory'] = [{"sender":'Niha', "message":entry_message}]
        session.modified = True
    else:
        print("Chat history found: ", session['chatHistory'])

    if request.method == 'POST':
        user_question = request.form['question']
        
        data = app.config['DATA']

        if api_key:
            openai.api_key = api_key
        else:
            print("API Key not found. Please check your .env file.")
        
        
        messages = [
            {"role": "system", "content": f"Please respond as if you are Sai Niharika Naidu Gandham.{json.dumps(data, indent=2)}."},
            {"role": "user", "content": user_question}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",  
            messages=messages,
            max_tokens=150,
        )

        generated_text = response['choices'][0]['message']['content']

        session['chatHistory'].append({"sender":'User', "message":user_question})
        session['chatHistory'].append({"sender":'Niha', "message":generated_text})
        session.modified = True
        
        print("Chat history found: ", session['chatHistory'])
        return render_template('chat.html', chatHistory=session['chatHistory'])

    return render_template('chat.html', entry_message=entry_message, chatHistory=session['chatHistory'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)