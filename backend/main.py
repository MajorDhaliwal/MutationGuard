from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from inference import predict_mutation


class MutationRequest(BaseModel):
    gene: str
    mutation: str


app = FastAPI(title="MutationGuard API", version="0.1.0")

# Allow local dev for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "MutationGuard API running"}


@app.post("/predict")
def predict(req: MutationRequest):
    """Predict whether the given mutation is benign or pathogenic.

    Note: Currently uses placeholder sequence encoding.
    """
    result = predict_mutation(req.gene, req.mutation)
    return result
