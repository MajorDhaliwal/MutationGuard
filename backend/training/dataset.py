import os
import csv
from typing import List, Tuple

import torch
from torch.utils.data import Dataset

from preprocessing import encode_mutation


class MutationDataset(Dataset):
    """
    Dataset for mutation strings + pathogenicity labels.
    Expected CSV columns:
      mutation,label
    where:
      mutation = HGVS string (e.g., 'NM_000546.5:c.215C>G')
      label = 0 or 1
    """

    def __init__(self, csv_path: str):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        self.samples: List[Tuple[str, int]] = []
        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                mutation = row["mutation"].strip()
                label = int(row["label"])
                self.samples.append((mutation, label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        mutation, label = self.samples[idx]

        # Dummy encoding: deterministic pseudo-sequence based on mutation string
        x = encode_mutation("GENE", mutation)  # we ignore real gene name for now
        x = x.squeeze(0)  # shape becomes (4, L)

        y = torch.tensor(label, dtype=torch.long)
        return x, y
