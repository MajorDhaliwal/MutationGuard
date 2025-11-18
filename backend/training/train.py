import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))   # <-- MUST come before imports

import torch
from torch.utils.data import DataLoader, random_split
import torch.nn as nn
import torch.optim as optim

from model import MutationNet
from training.dataset import MutationDataset


DATA_CSV = ROOT / "data" / "mutations.csv"
MODEL_PATH = ROOT / "models" / "model.pt"

def train(
    epochs: int = 5,
    batch_size: int = 32,
    lr: float = 1e-3,
):
    dataset = MutationDataset(str(DATA_CSV))

    # Train/val split
    val_size = max(1, len(dataset) // 10)
    train_size = len(dataset) - val_size
    train_ds, val_ds = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MutationNet(num_classes=2).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for x, y in train_loader:
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * x.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)

        train_loss = total_loss / total
        train_acc = correct / total

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for x, y in val_loader:
                x, y = x.to(device), y.to(device)
                logits = model(x)
                preds = logits.argmax(dim=1)
                val_correct += (preds == y).sum().item()
                val_total += y.size(0)
        val_acc = val_correct / val_total if val_total > 0 else 0.0

        print(f"Epoch {epoch}/{epochs} - loss={train_loss:.4f} acc={train_acc:.3f} val_acc={val_acc:.3f}")

    os.makedirs(MODEL_PATH.parent, exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    if not DATA_CSV.exists():
        raise SystemExit(f"Dataset CSV not found at {DATA_CSV}. Please create data/mutations.csv first.")
    train()
