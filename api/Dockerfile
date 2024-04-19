FROM public.ecr.aws/lambda/python:3.10


WORKDIR /app


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]