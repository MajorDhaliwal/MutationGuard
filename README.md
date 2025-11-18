# MutationGuard – DNA Mutation Pathogenicity Demo (PyTorch + FastAPI + React)

This is a **portfolio-ready scaffold** for a small ML/AI project that predicts whether a DNA mutation is **benign or pathogenic**.

Tech stack:
- **Backend**: Python, FastAPI, PyTorch
- **Frontend**: React (Vite)
- **ML**: Simple CNN + BiLSTM over one-hot encoded DNA sequences

> ⚠️ This is a scaffold: you still need to plug in **real genomic data** (e.g., ClinVar) and implement a real `encode_mutation` using gene coordinates. Right now it uses a dummy sequence so everything runs out-of-the-box.

---

## 1. Backend (FastAPI + PyTorch)

### Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run API

```bash
cd backend
uvicorn main:app --reload
```

This starts FastAPI at `http://localhost:8000`.

### Training (placeholder)

The `training/` folder contains a minimal training pipeline that expects a CSV file:

- `data/mutations.csv` with columns:
  - `sequence` – DNA string (A/C/G/T) of fixed length, e.g. 201bp
  - `label` – 0 (benign) or 1 (pathogenic)

You can start from **ClinVar** or another dataset, preprocess it into this format, and then run:

```bash
cd backend
python -m training.train
```

This will train a model and save weights to `models/model.pt`.

---

## 2. Frontend (React + Vite)

### Setup

```bash
cd frontend
npm install
```

### Run Dev Server

```bash
npm run dev
```

Vite will show you a local URL, usually `http://localhost:5173`.

Make sure the backend is running on `http://localhost:8000` or update `src/api.js`.

---

## 3. API Contract

**POST** `http://localhost:8000/predict`

Request JSON:

```json
{
  "gene": "BRCA1",
  "mutation": "c.5266dupC"
}
```

Response JSON (demo):

```json
{
  "prediction": "pathogenic",
  "confidence": 0.92
}
```

Again, currently this is using dummy encoding logic so you can focus on the architecture first, then plug in real biology.

---

## 4. Suggested Next Steps for You

1. Replace `encode_mutation` in `backend/preprocessing.py` with real logic that:
   - Maps (gene, mutation) → genomic coordinate
   - Extracts a window around the mutation from a reference FASTA
2. Build a proper training dataset from ClinVar/dbSNP/COSMIC.
3. Improve the model (more layers, class weighting, etc.).
4. Add sequence visualization to the React UI.
5. Deploy backend (Railway/Render) + frontend (Vercel/Netlify).

This project structure is already good enough to show employers you can:
- Design an ML system end-to-end
- Implement a PyTorch model and API
- Hook up a modern React front-end
