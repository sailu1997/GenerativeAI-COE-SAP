FROM python:3.10

WORKDIR /home/yt_clone/

COPY . .

RUN pip install --upgrade pip

RUN pip install nltk

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python3", "app.py"]
