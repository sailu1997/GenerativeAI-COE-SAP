from flask import Flask, render_template, request
import openai
import json
import os

app = Flask(__name__)
data_files = [data_file for data_file in os.listdir('./Data') if data_file.endswith('.json')]
data = []
@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_question = request.form['question']

        for data_file in data_files:
            with open('./Data/' + data_file) as f:
                file_data = json.load(f)
            data.append(file_data)

        openai.api_key = 'API-KEY'  # Replace with your API key
        
        CHUNK_SIZE = 1
        responses = []
        for i in range(0,len(data),CHUNK_SIZE):
            chunk = data[i:i+CHUNK_SIZE]

            truncated_data = json.dumps(chunk,indent=2)[:10000]
            messages = [
                {"role": "system", "content": f"You are now chatting with Niharika. Here is some information about her: {truncated_data}."},
                {"role": "user", "content": user_question}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  
                messages=messages,
            )
            responses.append(response.choices[0].message['content'])

        #generated_text = response['choices'][0]['message']['content']
        generated_text = ' '.join(responses)
        return render_template('chat.html', question=user_question, answer=generated_text)

    return render_template('chat.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)