FROM python:3.12.8-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE ${WEBSOCKET_PORT}
CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "8001"]
