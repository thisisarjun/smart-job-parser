# Text Processing API

A FastAPI-based REST API for testing text splitting and embedding functionality using LangChain and Ollama.

## Features

- **Text Splitting**: Split large texts into smaller chunks with configurable size and overlap
- **Text Embedding**: Generate embeddings using Ollama's mxbai-embed-large model
- **Combined Processing**: Split text and generate embeddings for each chunk in one request
- **Interactive Documentation**: Auto-generated API docs with Swagger UI
- **Health Checks**: Monitor API status

## Quick Start

### 1. Start the API Server

```bash
python start_api.py
```

This will:
- Automatically install required dependencies (FastAPI, Uvicorn, Pydantic)
- Start the server on `http://localhost:8000`
- Enable auto-reload for development

### 2. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 3. Test the API

```bash
python test_api_examples.py
```

## API Endpoints

### 1. Split Text
**POST** `/split-text`

Split text into chunks using RecursiveCharacterTextSplitter.

**Request Body:**
```json
{
  "text": "Your text to split...",
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

**Response:**
```json
{
  "chunks": ["chunk1", "chunk2", "..."],
  "chunk_count": 3,
  "original_length": 1500
}
```

### 2. Embed Text
**POST** `/embed-text`

Generate embeddings for text using Ollama.

**Request Body:**
```json
{
  "text": "Text to embed"
}
```

**Response:**
```json
{
  "embedding": [0.1, 0.2, 0.3, "..."],
  "text_length": 13
}
```

### 3. Process Text (Split + Embed)
**POST** `/process-text`

Split text into chunks AND generate embeddings for each chunk.

**Request Body:**
```json
{
  "text": "Your long text...",
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

**Response:**
```json
{
  "chunks": ["chunk1", "chunk2"],
  "embeddings": [[0.1, 0.2, "..."], [0.3, 0.4, "..."]],
  "chunk_count": 2,
  "original_length": 1500
}
```

### 4. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Text Processing API is running"
}
```

## Testing Examples

### Using curl

#### Test Text Splitting
```bash
curl -X POST "http://localhost:8000/split-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a long text that needs to be split into smaller chunks for processing...",
    "chunk_size": 100,
    "chunk_overlap": 20
  }'
```

#### Test Text Embedding
```bash
curl -X POST "http://localhost:8000/embed-text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Sample text for embedding"
  }'
```

### Using Python requests

```python
import requests

# Split text
response = requests.post("http://localhost:8000/split-text", json={
    "text": "Your text here...",
    "chunk_size": 200,
    "chunk_overlap": 50
})
result = response.json()
print(f"Split into {result['chunk_count']} chunks")

# Embed text
response = requests.post("http://localhost:8000/embed-text", json={
    "text": "Text to embed"
})
embedding = response.json()['embedding']
print(f"Generated {len(embedding)}-dimensional embedding")
```

## Configuration

### Default Parameters
- **chunk_size**: 1000 characters
- **chunk_overlap**: 200 characters
- **embedding_model**: mxbai-embed-large (Ollama)

### Validation Limits
- **chunk_size**: 1 - 10,000 characters
- **chunk_overlap**: 0 - 1,000 characters

## Requirements

The API automatically installs these dependencies:
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `pydantic` - Data validation
- `langchain` - Text processing (from your existing requirements)
- `requests` - For testing scripts

## Development

### Project Structure
```
├── api/
│   └── main.py              # FastAPI application
├── src/
│   └── text_processor/
│       └── text_processor.py # Your text processing functions
├── start_api.py             # Server startup script
├── test_api_examples.py     # API testing script
└── API_README.md           # This file
```

### Running in Development Mode
The server runs with `--reload` flag by default, so it will automatically restart when you make changes to the code.

### Error Handling
The API includes comprehensive error handling:
- Invalid parameters return 422 Unprocessable Entity
- Processing errors return 500 Internal Server Error
- All errors include descriptive messages

## Troubleshooting

### Common Issues

1. **"Cannot connect to API"**
   - Make sure the server is running: `python start_api.py`
   - Check if port 8000 is available

2. **"Ollama connection failed"**
   - Ensure Ollama is running and the model is available
   - Check your Ollama installation and model download

3. **Import errors**
   - Make sure you're in the project root directory
   - Check that your virtual environment is activated

### Logs
Server logs will show in the terminal where you ran `start_api.py`. Look for error messages there if requests are failing.

## Next Steps

1. **Start the server**: `python start_api.py`
2. **Run tests**: `python test_api_examples.py`
3. **Explore the docs**: Visit http://localhost:8000/docs
4. **Try your own text**: Use the interactive test in the test script

Enjoy testing your text processing pipeline! 🚀
