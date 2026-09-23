FROM python:3.10-slim
WORKDIR /app
COPY . /app

ENV PIP_NO_CACHE_DIR=1

RUN pip install uv
RUN uv pip install --system --no-cache torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN uv pip install --system --no-cache -r requirements.txt

CMD ["python", "main.py"]
