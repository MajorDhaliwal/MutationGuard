export default function PredictionCard({ result }) {
  if (!result) {
    return (
      <div className="card placeholder">
        <p>Submit a mutation to see the prediction here.</p>
      </div>
    );
  }

  const { prediction, confidence, probs } = result;

  return (
    <div className="card prediction">
      <h2>Prediction</h2>
      <p>
        <strong>Result:</strong>{" "}
        <span className={prediction === "pathogenic" ? "pill pill-danger" : "pill pill-safe"}>
          {prediction.toUpperCase()}
        </span>
      </p>
      <p>
        <strong>Confidence:</strong> {(confidence * 100).toFixed(1)}%
      </p>
      {probs && (
        <div className="probs">
          <p>Benign: {(probs.benign * 100).toFixed(1)}%</p>
          <p>Pathogenic: {(probs.pathogenic * 100).toFixed(1)}%</p>
        </div>
      )}
      <p className="note">
        Note: This is a demo model and <strong>not for clinical use</strong>. This is to demonstrate the architecture only.
      </p>
    </div>
  );
}
