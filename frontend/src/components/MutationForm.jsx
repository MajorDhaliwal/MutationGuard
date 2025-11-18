import { useState } from "react";
import { api } from "../api";

export default function MutationForm({ onResult }) {
  const [gene, setGene] = useState("");
  const [mutation, setMutation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    onResult(null);

    try {
      const { data } = await api.post("/predict", { gene, mutation });
      onResult(data);
    } catch (err) {
      console.error(err);
      setError("Request failed. Is the backend running on port 8000?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h2>Enter Mutation</h2>
      <label>
        Gene
        <input
          type="text"
          placeholder="e.g., BRCA1"
          value={gene}
          onChange={(e) => setGene(e.target.value)}
          required
        />
      </label>

      <label>
        Mutation
        <input
          type="text"
          placeholder="e.g., c.5266dupC"
          value={mutation}
          onChange={(e) => setMutation(e.target.value)}
          required
        />
      </label>

      <button type="submit" disabled={loading}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {error && <p className="error">{error}</p>}
    </form>
  );
}
