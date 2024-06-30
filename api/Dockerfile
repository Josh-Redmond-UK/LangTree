FROM --platform=linux/amd64 python:3


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]