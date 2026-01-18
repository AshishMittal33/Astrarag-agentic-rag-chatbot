FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Upgrade build tools (NO gcc needed)
RUN pip install --upgrade pip setuptools wheel

# 🔥 CRITICAL: install torch CPU wheel FIRST
RUN pip install torch==2.2.2+cpu torchvision==0.17.2+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Copy requirements
COPY requirements.txt .

# Install remaining dependencies (fast, no compile)
RUN pip install --progress-bar off \
    --timeout 100 \
    --retries 5 \
    -r requirements.txt

# Copy application code
COPY src/ src/
COPY doc_dir/ doc_dir/
COPY start.sh .

RUN chmod +x start.sh

EXPOSE 8000 8501

ENV GROQ_API_KEY="your_groq_api_key_here"
ENV DOCUMENTS_DIR="/app/doc_dir"
ENV VECTOR_STORE_DIR="/app/doc_vector_store"
ENV COLLECTION_NAME="document_collection"
ENV MODEL_NAME="llama-3.3-70b-versatile"
ENV MODEL_TEMPERATURE=0.0
ENV CHAT_ENDPOINT_URL="http://localhost:8000/chat/answer"

CMD ["/app/start.sh"]
