FROM --platform=linux/amd64 python:3


WORKDIR /app

COPY api/requirements.txt .

RUN pip install -r api/requirements.txt

COPY api . 

EXPOSE 8080

CMD ["fastapi", "run", "main.py", "--port", "8080"]