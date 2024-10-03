FROM python:3.9-alpine
WORKDIR /app
COPY . .

RUN pip3 install requests

EXPOSE 8000

CMD ["python3", "wsgiMyApp.py"]
