# GenerativeAI-COE-SAP
1. Please go through the documentation to get insights into my work.

#For Docker :
1. I have run my code on docker setup. Hence providing you with the docker image to run.
2. Follow the steps below :
   - docker pull sai21111997/docker_ai:v2
   - docker run -d -p 3000:3000 -e SECRET_KEY="your_random_secret_key" -e API_KEY="your_open_ai_key" sai21111997/docker_ai:v2
   - To access the application go to: http://localhost:3000
   - Enter the question you wanted to ask , and it responds with answers

#Without Docker:
- git clone "repository_url"
- Create .env file and add the following lines :
   API_KEY = "your_Open_ai_api_key"
   SECRET_KEY = "anyrandomsecrectkey" #example: rbuisdv834y9hgqfwaondscklmxzopfrkeads2934r
- pip install nltk
- pip install -r requirements.txt
- python3 app.py
- To access the application go to: http://localhost:3000
