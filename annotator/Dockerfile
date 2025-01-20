FROM python:3.12.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8002
CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8002"]
