import { useState } from "react";
import MutationForm from "./components/MutationForm.jsx";
import PredictionCard from "./components/PredictionCard.jsx";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app">
      <header className="header">
        <h1>MutationGuard</h1>
        <p>Demo: Predict whether a DNA mutation is benign or pathogenic.</p>
      </header>

      <main className="main">
        <MutationForm onResult={setResult} />
        <PredictionCard result={result} />
      </main>

      <footer className="footer">
        <small>PyTorch + FastAPI + React — portfolio scaffold</small>
      </footer>
    </div>
  );
}

export default App;
