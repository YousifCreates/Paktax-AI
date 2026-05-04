FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Remove deprecated pinecone plugin that causes conflict
RUN pip uninstall -y pinecone-plugin-inference

# Download embedding model during build
RUN python3 -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('intfloat/multilingual-e5-large')"

COPY app.py .
COPY rag/ ./rag/
COPY chain/ ./chain/
COPY templates/ ./templates/
COPY static/ ./static/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_OFFLINE=1
ENV HF_HUB_OFFLINE=1

EXPOSE 7860

CMD ["python", "app.py"]