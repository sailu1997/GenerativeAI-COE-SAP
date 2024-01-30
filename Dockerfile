FROM Python:3.10.9

WORKDIR /home/yt_clone/

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["python3", "app.py"]
