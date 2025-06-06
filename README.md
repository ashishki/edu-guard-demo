# 🛡️ Edu-Guard Demo

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Poetry](https://img.shields.io/badge/Poetry-Managed-orange.svg)](https://python-poetry.org)

> **A sophisticated RAG (Retrieval-Augmented Generation) service with built-in content moderation and multi-LLM support**

## 🎯 Overview

Edu-Guard Demo is a production-ready Python service that demonstrates advanced AI safety patterns by combining:

- **🔍 Semantic Search**: Intelligent document retrieval using LlamaIndex + ChromaDB
- **🛡️ Content Moderation**: OpenAI-powered guardrails for safe AI interactions  
- **🤖 Multi-LLM Support**: Parallel querying of OpenAI GPT-3.5 and TogetherAI Mixtral
- **🏗️ Enterprise Architecture**: Clean OOP design with comprehensive testing

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Semantic Indexing** | Builds vector embeddings from `.txt` files for intelligent context retrieval |
| **Content Moderation** | Blocks harmful prompts using OpenAI Moderation API |
| **Parallel LLM Queries** | Simultaneous requests to multiple AI models for diverse responses |
| **Persistent Storage** | ChromaDB maintains your index across restarts |
| **RESTful API** | Clean FastAPI endpoints with automatic documentation |
| **Test Coverage** | Comprehensive pytest suite for reliability |

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   EduChain       │    │  DocumentIndexer│
│   /ask endpoint │───▶│   Pipeline       │───▶│  LlamaIndex +   │
│   Pydantic      │    │   Orchestrator   │    │  ChromaDB       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Guardrails     │
                       │   OpenAI Mod API │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   LLM Clients    │
                       │   OpenAI + Together│
                       └──────────────────┘
```

### 📁 Project Structure

```
edu-guard-demo/
├── 📁 app/
│   ├── 🛡️ guardrails.py      # Content moderation logic
│   ├── 🤖 llm_client.py      # Multi-LLM wrapper
│   ├── 📚 vector_index.py    # Document indexing
│   ├── ⚙️ educhain.py        # Core pipeline
│   └── 🚀 main.py           # FastAPI application
├── 📁 data/                  # Your .txt documents
├── 📁 chroma_db/            # Persistent vector store
├── 📁 tests/                # Unit test suite
├── 🐳 Dockerfile            # Container definition
├── 🐳 docker-compose.yml    # Orchestration config
├── 📝 pyproject.toml        # Poetry dependencies
└── 🔒 .env                  # API keys (create this)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Poetry** (for dependency management)
- **Docker & Docker Compose** (optional)
- **OpenAI API Key** (required)
- **TogetherAI API Key** (optional)

### 🔧 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashishki/edu-guard-demo.git
   cd edu-guard-demo
   ```

2. **Configure environment**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=sk-your-openai-key-here
   # TOGETHER_API_KEY=your-together-key-here  # Optional
   ```

3. **Install dependencies**
   ```bash
   poetry install
   poetry shell
   ```

4. **Run tests**
   ```bash
   pytest
   ```

5. **Start the service**
   ```bash
   uvicorn app.main:app --reload
   ```

### 🎯 Usage

#### Interactive API Documentation
Visit `http://127.0.0.1:8000/docs` for the auto-generated Swagger UI.

#### Example API Calls

**✅ Safe Query**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python programming?"}'
```

**Response:**
```json
{
  "context": "Python is a high-level programming language...",
  "answers": {
    "openai": "Python is a versatile, high-level programming language..."
  }
}
```

**🚫 Blocked Query**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "How to harm someone"}'
```

**Response:**
```json
{
  "detail": "Blocked by guardrails: violence"
}
```

---

## 🐳 Docker Deployment

### Quick Deploy
```bash
# Build and start services
docker-compose up --build

# Access at http://localhost:8000
```

### Production Deployment
```bash
# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🧪 Testing

Our comprehensive test suite covers all major components:

### Test Categories

| Test File | Coverage |
|-----------|----------|
| `test_vector_index.py` | Document indexing and retrieval |
| `test_guardrails.py` | Content moderation logic |

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_vector_index.py -v
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for GPT models |
| `TOGETHER_API_KEY` | ❌ Optional | TogetherAI key for Mixtral model |

### Customization Options

- **Document Sources**: Place your `.txt` files in the `data/` directory
- **Vector Store**: ChromaDB persists in `chroma_db/` directory
- **LLM Models**: Easily add new providers in `llm_client.py`
- **Moderation Rules**: Customize guardrails in `guardrails.py`

---

## 🛠️ Troubleshooting

### Common Issues

<details>
<summary><strong>🔑 "No API key found for OpenAI"</strong></summary>

**Cause**: Missing or incorrectly loaded environment variables.

**Solution**: 
- Ensure `.env` file exists in project root
- Verify `OPENAI_API_KEY` is set correctly
- Check that `load_dotenv()` is called in `app/main.py`
</details>

<details>
<summary><strong>🔄 "Invalid input type" errors</strong></summary>

**Cause**: Passing dict instead of string to LLM client.

**Solution**: 
- Ensure `LangChainLLMClient` receives string prompts
- Check that response extraction uses `.content` or `.text`
</details>

<details>
<summary><strong>📊 "Number of requested results greater than elements"</strong></summary>

**Cause**: Vector index has fewer chunks than requested.

**Solution**: 
- This is just a warning, not an error
- The system automatically adjusts to available chunks
</details>

<details>
<summary><strong>🚫 Unexpected moderation blocks</strong></summary>

**Cause**: OpenAI Moderation API flagged benign content.

**Solution**: 
- Rephrase your prompt
- Review moderation thresholds in `guardrails.py`
- Use test mocks for development
</details>

---

## 🚀 Future Enhancements

### Planned Features

- [ ] **Advanced Guardrails**: Integration with Guardrails-AI library
- [ ] **Web Interface**: React/Vue frontend for interactive queries  
- [ ] **Metrics Dashboard**: Request/response analytics and monitoring
- [ ] **Caching Layer**: Redis-based response caching
- [ ] **Multi-format Support**: PDF, DOCX, and markdown document indexing
- [ ] **Fine-tuning Pipeline**: Custom model training workflows

### Extension Ideas

- **Multi-tenant Support**: Isolated indexes per user/organization
- **Streaming Responses**: Real-time answer generation
- **Advanced RAG**: Hybrid search combining semantic and keyword matching
- **Model Comparison**: Side-by-side LLM response analysis

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LlamaIndex** for powerful document indexing capabilities
- **FastAPI** for the excellent web framework
- **ChromaDB** for efficient vector storage
- **OpenAI** for moderation and language model APIs
- **TogetherAI** for additional LLM options

---

<div align="center">

**⭐ If you find this project helpful, please give it a star! ⭐**

[![GitHub Stars](https://img.shields.io/github/stars/ashishki/edu-guard-demo?style=social)](https://github.com/ashishki/edu-guard-demo)

</div>