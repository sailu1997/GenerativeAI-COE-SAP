
FROM Python:3.10.9
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["python3", "app.py"]
