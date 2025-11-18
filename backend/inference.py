import os
import torch
from model import MutationNet
from preprocessing import encode_mutation

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model.pt")

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_model = MutationNet(num_classes=2).to(_device)

if os.path.exists(MODEL_PATH):
    _model.load_state_dict(torch.load(MODEL_PATH, map_location=_device))
    print(f"Loaded model weights from {MODEL_PATH}")
else:
    print("No trained model found at models/model.pt – using randomly initialized weights.")

_model.eval()


def predict_mutation(gene: str, mutation: str):
    """Run model prediction for (gene, mutation)."""
    x = encode_mutation(gene, mutation)  # (1, 4, L)
    x = x.to(_device)

    with torch.no_grad():
        logits = _model(x)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    idx = int(probs.argmax())
    label = "benign" if idx == 0 else "pathogenic"
    confidence = float(probs[idx])
    return {
        "prediction": label,
        "confidence": confidence,
        "probs": {
            "benign": float(probs[0]),
            "pathogenic": float(probs[1]),
        },
    }
