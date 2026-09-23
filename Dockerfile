FROM python:3.10-slim
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
