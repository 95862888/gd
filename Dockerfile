FROM ultralytics/ultralytics
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
EXPOSE 5000
CMD ["python3", "main.py"]
