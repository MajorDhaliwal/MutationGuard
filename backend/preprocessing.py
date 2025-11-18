import torch
import numpy as np

BASE_TO_INDEX = {
    "A": 0,
    "C": 1,
    "G": 2,
    "T": 3,
}

def one_hot_encode_sequence(seq: str, window_size: int = 201) -> torch.Tensor:
    """Encode a DNA sequence (A/C/G/T) into a one-hot tensor of shape (1, 4, window_size).

    - If seq is shorter than window_size, it's padded with 'A'.
    - If longer, it's truncated.
    """
    seq = seq.upper().replace("N", "A")
    if len(seq) < window_size:
        seq = seq + "A" * (window_size - len(seq))
    elif len(seq) > window_size:
        seq = seq[:window_size]

    arr = np.zeros((4, window_size), dtype=np.float32)
    for i, base in enumerate(seq):
        idx = BASE_TO_INDEX.get(base)
        if idx is not None:
            arr[idx, i] = 1.0
    tensor = torch.from_numpy(arr).unsqueeze(0)  # (1, 4, window_size)
    return tensor


def encode_mutation(gene: str, mutation: str, window_size: int = 201) -> torch.Tensor:
    """Placeholder: map (gene, mutation) → one-hot encoded DNA window.

    For now, this just generates a dummy sequence that depends on the
    hash of the input so it's deterministic but not biologically real.

    TODO: Replace this with real logic that:
      - looks up the genomic coordinate of (gene, mutation)
      - extracts the local sequence from a reference FASTA
    """
    key = f"{gene}:{mutation}".upper()
    bases = ["A", "C", "G", "T"]
    seq_chars = []
    for i in range(window_size):
        idx = (hash(key + str(i)) % 4 + 4) % 4
        seq_chars.append(bases[idx])
    seq = "".join(seq_chars)
    return one_hot_encode_sequence(seq, window_size=window_size)
