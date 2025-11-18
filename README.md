MutationGuard
AI-Powered DNA Mutation Classifier

MutationGuard is a full-stack machine learning project that predicts whether a given genetic mutation is benign or pathogenic.

It includes:
- A PyTorch model trained on mutation data
- A FastAPI backend for inference
- A React frontend for entering gene/mutation info
- Dockerized deployment with docker-compose

This project is built as a portfolio showcase to demonstrate ML engineering, model training, APIs, and frontend integration.

Features:
- Train a simple neural network on synthetic mutation sequences
- FastAPI endpoint /predict for model inference
- React UI to input gene + mutation
- Dockerized backend + frontend
- Clean architecture: backend/, frontend/, training/
- Easily extendable to real biological datasets


Requirements
- Docker
- Docker Compose
- (Optional) Python 3.11 if running backend locally

Running the environment:
```docker compose up --build```

This will start:

- FastAPI backend at: ```http://localhost:8000```
- React frontend at: ```http://localhost:3000```

Training a model

```docker compose exec backend bash```

```python training/train.py```

