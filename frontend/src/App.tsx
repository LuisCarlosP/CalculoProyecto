import { useState, useCallback } from 'react';
import type { EvaluateResponse, ExperimentResponse, StepsResponse } from './types/lagrange';
import Header from './components/Header';
import Footer from './components/Footer';
import LagrangeForm from './components/Lagrange/LagrangeForm';
import LagrangeResults from './components/Lagrange/LagrangeResults';
import StepByStepView from './components/Lagrange/StepByStepView';
import './App.css';

export default function App() {
  const [evaluateResult, setEvaluateResult] = useState<EvaluateResponse | null>(null);
  const [experimentResult, setExperimentResult] = useState<ExperimentResponse | null>(null);
  const [stepsResult, setStepsResult] = useState<StepsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleError = useCallback((msg: string) => setError(msg), []);

  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <LagrangeForm
          onEvaluateResult={setEvaluateResult}
          onExperimentResult={setExperimentResult}
          onStepsResult={setStepsResult}
          onLoading={setLoading}
          onError={handleError}
        />

        {error && <div className="error-message">{error}</div>}

        {loading && <div className="loading">Procesando...</div>}

        <LagrangeResults
          evaluateResult={evaluateResult}
          experimentResult={experimentResult}
        />

        <StepByStepView result={stepsResult} />
      </main>
      <Footer />
    </div>
  );
}
