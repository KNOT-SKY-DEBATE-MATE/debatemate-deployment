FROM python:3.12.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8001
CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8001"]
