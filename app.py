from flask import Flask, render_template, request, jsonify, session, g
import openai
import json
import os
from dotenv import load_dotenv
import requests
import uuid
import nltk
nltk.download('punkt')

 

load_dotenv()
api_key = os.environ.get("API_KEY")

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SECRET_KEY")

BACK4APP_ENDPOINT = "https://parseapi.back4app.com/classes/GenerativeAI"

headers = {
    'X-Parse-Application-Id': "J8rQAd6J92xVUdl0fBNaaLu1RCq2HJgEJAS9QnrD",
    'X-Parse-REST-API-Key': "xTGZGqglFx1jI1JRzT147o6Jam6Zkh33y3hHKjeU",
    'Content-Type': 'application/json'
}


data_files = [data_file for data_file in os.listdir('./Data') if data_file.endswith('.json')]
data = []

for data_file in data_files:
    with open('./Data/' + data_file) as f:
        file_data = json.load(f)
    data.append(file_data)

app.config['DATA'] = data


#Function to remove sentence that ends abruptly
def remove_abruptly_ended_sentence(text):
    sentences = nltk.sent_tokenize(text)
    valid_sentences = []
    
    for sentence in sentences:
        if sentence.strip().endswith("."):
            valid_sentences.append(sentence)
            
    cleaned_text = " ".join(valid_sentences)
    
    return cleaned_text.strip()


#Funtion to generate continued response when abrupt response is obervserved
def continue_response(messages, original_response, max_additional_tokens=300):
    continued_response = original_response
    current_length = len(original_response.split())

    while current_length < max_additional_tokens:
        continuation = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=messages + [{"role": "system", "content": continued_response}],
            max_tokens=max_additional_tokens - current_length,
            top_p=1,
            temperature = 0.7,
            frequency_penalty=0.4,
            presence_penalty=0.4,
        )

        part_response = continuation['choices'][0]['message']['content']
        continued_response += part_response
        current_length += len(part_response.split())

        if continuation['choices'][0].get('finish_reason') != 'length':
            break

    return continued_response

#Route to submit the feedback
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback = data['feedback']
    
    session['last_feedback'] = feedback

    return jsonify({"message": "Feedback received successfully"})


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

        if 'last_feedback' not in session:
            session['last_feedback'] = None
        
        data = app.config['DATA']

        if api_key:
            openai.api_key = api_key
        else:
            print("API Key not found. Please check your .env file.")
        
        try:
            messages = [
                {"role": "system", "content": f"You are Sai Niharika Naidu Gandham . Please provide brief and rephrased answers to the user's questions based on your knowledge and understanding of this data about you here:{json.dumps(data, indent=2)}."},
                {"role": "user", "content": user_question}
            ]
    
            response = openai.ChatCompletion.create(
                model="gpt-4-1106-preview",  
                messages=messages,
                max_tokens=150,
                top_p=1,
                temperature = 0.7,
                frequency_penalty=0.4,
                presence_penalty=0.4,
            )

            generated_text = response['choices'][0]['message']['content']
            generated_text = remove_abruptly_ended_sentence(generated_text)
        
        except openai.error.RateLimitError as e:
            print("Hit rate limit:", str(e))
            generated_text = "I'm a bit overwhelmed at the moment. Please try again later."
    
        except openai.error.InvalidRequestError as e:
            print("Invalid request:", str(e))
            generated_text = "I didn't understand that. Could you rephrase it?"
        
        except openai.error.OpenAIError as e:
            print("OpenAI error:", str(e))
            generated_text = "I encountered an error. Please try again later."

        session['chatHistory'].append({"sender":'User', "message":user_question})
        session['chatHistory'].append({"sender":'Niha', "message":generated_text})
        session.modified = True

        messages.append({"role": "user", "content": user_question})
        messages.append({"role": "assistant", "content": generated_text})
        print('Last feedback is',session['last_feedback'])
        chat_data = {
            "user": user_question,
            "Niha": generated_text,
            "feedback": session['last_feedback'],
        }
        session['last_feedback'] = None
        
        response = requests.post(BACK4APP_ENDPOINT, headers=headers, data=json.dumps(chat_data))

        if response.status_code == 201:
            print("Data saved to Back4App database")
        else:
            print("Failed to save data to Back4App database:", response.status_code)

        print("Chat history found: ", session['chatHistory'])
        return render_template('chat.html', chatHistory=session['chatHistory'])

    return render_template('chat.html', entry_message=entry_message, chatHistory=session['chatHistory'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)