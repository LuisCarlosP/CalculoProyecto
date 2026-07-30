import type { EvaluateResponse, ExperimentResponse } from '../../types/lagrange';
import { formatNum } from '../../utils/format';
import ExperimentTable from './ExperimentTable';
import FunctionPlot from './Charts/FunctionPlot';

interface Props {
  evaluateResult: EvaluateResponse | null;
  experimentResult: ExperimentResponse | null;
}

export default function LagrangeResults({ evaluateResult, experimentResult }: Props) {
  if (!evaluateResult && !experimentResult) {
    return null;
  }

  return (
    <>
      {evaluateResult && (
        <section className="section">
          <h2 className="section-title">Resultados de Evaluación</h2>
          <div className="result-card">
            <div className="result-item">
              <div className="label">f'(x) Aproximado</div>
              <div className="value">{formatNum(evaluateResult.derivative_approx)}</div>
            </div>
            <div className="result-item">
              <div className="label">f'(x) Exacto</div>
              <div className="value">{formatNum(evaluateResult.derivative_exact)}</div>
            </div>
            <div className="result-item">
              <div className="label">Error Absoluto</div>
              <div className="value error">{formatNum(evaluateResult.absolute_error)}</div>
            </div>
            <div className="result-item">
              <div className="label">Error Relativo</div>
              <div className="value error">{formatNum(evaluateResult.relative_error)}</div>
            </div>
            <div className="result-item">
              <div className="label">Tiempo</div>
              <div className="value">{formatNum(evaluateResult.execution_time * 1000)} ms</div>
            </div>
            <div className="result-item">
              <div className="label">Puntos usados</div>
              <div className="value">{evaluateResult.num_points}</div>
            </div>
          </div>
        </section>
      )}

      {experimentResult && (
        <>
          <section className="section">
            <h2 className="section-title">
              Experimentación — {experimentResult.function_name.replace('_', ' ')}
            </h2>
            <p style={{ marginBottom: '1rem', color: '#718096', fontSize: '0.9rem' }}>
              a = {experimentResult.a}, b = {experimentResult.b}, x₀ = {experimentResult.x_eval}
            </p>
            <ExperimentTable results={experimentResult.results} />
          </section>

          <section className="section">
            <h2 className="section-title">Gráfica de la Función vs Polinomio Interpolante</h2>
            <FunctionPlot
              data={experimentResult.function_plot_data}
              interpolationPoints={experimentResult.interpolation_points}
              a={experimentResult.a}
              b={experimentResult.b}
            />
          </section>
        </>
      )}
    </>
  );
}
