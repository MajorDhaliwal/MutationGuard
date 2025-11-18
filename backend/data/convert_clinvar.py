import pandas as pd
from pathlib import Path
from preprocessing import encode_mutation  # since convert is inside backend/data/

INPUT = Path("data/variant_summary.txt")
OUTPUT = Path("data/mutations.csv")

def map_label(sig: str):
    """Map ClinVar significance → 0/1."""
    if not isinstance(sig, str):
        return None
    sig = sig.lower()
    if "pathogenic" in sig:
        return 1
    if "benign" in sig:
        return 0
    return None

def main():
    print("Loading ClinVar file...")
    df = pd.read_csv(INPUT, sep="\t", low_memory=False)

    # Keep only relevant columns if available
    needed_cols = ["GeneSymbol", "Name", "ClinicalSignificance"]
    df = df[[c for c in needed_cols if c in df.columns]]
    df = df.dropna(subset=["GeneSymbol", "Name", "ClinicalSignificance"])

    print("Mapping labels...")
    df["label"] = df["ClinicalSignificance"].map(map_label)
    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    print(f"Remaining rows after filtering: {len(df)}")

    sequences = []
    labels = []

    print("Encoding sequences (this may take a while)...")
    for _, row in df.iterrows():
        gene = row["GeneSymbol"]
        mutation = row["Name"]

        # Use fake deterministic DNA generator
        tensor = encode_mutation(gene, mutation, window_size=201)

        # Convert one-hot tensor → string sequence (ACGT)
        seq_vector = tensor.squeeze(0).argmax(dim=0).tolist()
        seq = "".join("ACGT"[b] for b in seq_vector)

        sequences.append(seq)
        labels.append(int(row["label"]))

    out = pd.DataFrame({
        "sequence": sequences,
        "label": labels
    })

    print(f"Saving {len(out)} rows → {OUTPUT}")
    out.to_csv(OUTPUT, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
