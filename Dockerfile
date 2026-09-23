FROM python:3.10-slim
WORKDIR /app
COPY . /app

ENV PIP_NO_CACHE_DIR=1

RUN pip install --upgrade pip
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
