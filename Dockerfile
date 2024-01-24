
FROM Python:3.10.9

WORKDIR /home/yt_clone/

RUN npm install

COPY . .

EXPOSE 3000

CMD ["python3", "app.py"]
