from flask import Flask, render_template, request
import openai
import json
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_question = request.form['question']

        with open("./Data/resume_data.json", "r") as json_file:
            json_data = json.load(json_file)

        openai.api_key = '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'  # Replace with your API key

        messages = [
            {"role": "system", "content": f"The assistant is a virtual representation of a person named Niharika. Here is some information about her: {json.dumps(json_data, indent=2)}"},
            {"role": "user", "content": user_question}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=messages,
        )

        generated_text = response['choices'][0]['message']['content']
        return render_template('chat.html', question=user_question, answer=generated_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)