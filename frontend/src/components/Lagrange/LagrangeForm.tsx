import { useState, useEffect } from 'react';
import type {
  EvaluateResponse,
  ExperimentResponse,
  FunctionInfo,
  StepsResponse,
} from '../../types/lagrange';
import {
  fetchFunctions,
  evaluateDerivative,
  runExperiment,
  computeSteps,
} from '../../services/api';

interface Props {
  onEvaluateResult: (r: EvaluateResponse | null) => void;
  onExperimentResult: (r: ExperimentResponse | null) => void;
  onStepsResult: (r: StepsResponse | null) => void;
  onLoading: (v: boolean) => void;
  onError: (msg: string) => void;
}

export default function LagrangeForm({
  onEvaluateResult,
  onExperimentResult,
  onStepsResult,
  onLoading,
  onError,
}: Props) {
  const [functions, setFunctions] = useState<FunctionInfo[]>([]);
  const [func, setFunc] = useState('x3');
  const [pointsType, setPointsType] = useState<'equispaced' | 'custom'>('equispaced');
  const [a, setA] = useState('0');
  const [b, setB] = useState('1');
  const [n, setN] = useState('10');
  const [xEval, setXEval] = useState('0.5');
  const [customText, setCustomText] = useState('1\t2\n2\t3');

  const restrictedFuncs = ['ln', 'sqrt'];

  useEffect(() => {
    fetchFunctions()
      .then((res) => {
        setFunctions(res.functions);
        if (res.functions.length > 0) setFunc(res.functions[0].name);
      })
      .catch(() => onError('No se pudieron cargar las funciones'));
  }, [onError]);

  const parseCustomPoints = (): { x: number; y: number }[] | string => {
    const lines = customText.trim().split('\n');
    const points: { x: number; y: number }[] = [];
    for (const line of lines) {
      const parts = line.trim().split(/\s+/);
      if (parts.length < 2) return `Linea invalida: "${line}"`;
      const x = parseFloat(parts[0]);
      const y = parseFloat(parts[1]);
      if (isNaN(x) || isNaN(y)) return `Valor numerico invalido en: "${line}"`;
      points.push({ x, y });
    }
    if (points.length < 2) return 'Se requieren al menos 2 puntos';
    return points;
  };

  const handleEvaluate = async () => {
    onError('');
    onEvaluateResult(null);
    onExperimentResult(null);
    onStepsResult(null);
    onLoading(true);
    try {
      if (pointsType === 'custom') {
        const parsed = parseCustomPoints();
        if (typeof parsed === 'string') { onError(parsed); onLoading(false); return; }
        const result = await evaluateDerivative({
          func, x_eval: parseFloat(xEval),
          points_type: 'custom', custom_points: parsed,
          a: 0, b: 0, n: 2,
        });
        onEvaluateResult(result);
      } else {
        const result = await evaluateDerivative({
          func, x_eval: parseFloat(xEval),
          points_type: 'equispaced',
          a: parseFloat(a), b: parseFloat(b), n: parseInt(n, 10),
        });
        onEvaluateResult(result);
      }
    } catch (err: any) {
      onError(err?.response?.data?.detail || err.message || 'Error al evaluar');
    } finally {
      onLoading(false);
    }
  };

  const handleExperiment = async () => {
    onError('');
    onEvaluateResult(null);
    onExperimentResult(null);
    onStepsResult(null);
    onLoading(true);
    try {
      const nValues = [2, 3, 4, 5, 10, 15, 20, 30, 50, 100];
      const result = await runExperiment({
        func,
        a: parseFloat(a),
        b: parseFloat(b),
        x_eval: parseFloat(xEval),
        n_values: nValues,
        plot_n: parseInt(n, 10),
      });
      onExperimentResult(result);
    } catch (err: any) {
      onError(err?.response?.data?.detail || err.message || 'Error en experimento');
    } finally {
      onLoading(false);
    }
  };

  const handleSteps = async () => {
    onError('');
    onEvaluateResult(null);
    onExperimentResult(null);
    onStepsResult(null);
    onLoading(true);
    try {
      const parsed = parseCustomPoints();
      if (typeof parsed === 'string') {
        onError(parsed);
        return;
      }
      const result = await computeSteps({
        points: parsed,
        x_eval: parseFloat(xEval),
      });
      onStepsResult(result);
    } catch (err: any) {
      onError(err?.response?.data?.detail || err.message || 'Error al calcular pasos');
    } finally {
      onLoading(false);
    }
  };

  const isRestricted = restrictedFuncs.includes(func);

  return (
    <section className="section">
      <h2 className="section-title">Parametros de Entrada</h2>
      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="func">Funcion</label>
          <select id="func" value={func} onChange={(e) => setFunc(e.target.value)}>
            {functions.map((f) => (
              <option key={f.name} value={f.name}>
                {f.expression}
              </option>
            ))}
          </select>
          {isRestricted && (
            <small style={{ color: '#e53e3e', marginTop: '0.25rem' }}>
              Dominio restringido — verifica los limites
            </small>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="pointsType">Tipo de puntos</label>
          <select
            id="pointsType"
            value={pointsType}
            onChange={(e) => setPointsType(e.target.value as 'equispaced' | 'custom')}
          >
            <option value="equispaced">Equiespaciados</option>
            <option value="custom">Personalizados</option>
          </select>
        </div>

        {pointsType === 'equispaced' ? (
          <>
            <div className="form-group">
              <label htmlFor="a">Limite inferior (a)</label>
              <input id="a" type="number" step="any" value={a} onChange={(e) => setA(e.target.value)} />
            </div>
            <div className="form-group">
              <label htmlFor="b">Limite superior (b)</label>
              <input id="b" type="number" step="any" value={b} onChange={(e) => setB(e.target.value)} />
            </div>
            <div className="form-group">
              <label htmlFor="n">Particiones (n)</label>
              <input id="n" type="number" min="2" max="200" value={n} onChange={(e) => setN(e.target.value)} />
            </div>
          </>
        ) : (
          <div className="form-group" style={{ gridColumn: 'span 2' }}>
            <label htmlFor="customPoints">Puntos (x  f(x) por linea)</label>
            <textarea
              id="customPoints"
              rows={4}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #e2e8f0',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '0.9rem',
              }}
              value={customText}
              onChange={(e) => setCustomText(e.target.value)}
            />
            <small style={{ color: '#718096' }}>
              Ejemplo: "1  2" (x=1, f(x)=2). Un par por linea.
            </small>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="xEval">Punto de evaluacion (x₀)</label>
          <input id="xEval" type="number" step="any" value={xEval} onChange={(e) => setXEval(e.target.value)} />
        </div>
      </div>

      <div className="btn-group" style={{ marginTop: '1rem' }}>
        <button className="btn btn-primary" onClick={handleEvaluate}>
          Evaluar Derivada
        </button>
        <button className="btn btn-success" onClick={handleExperiment}>
          Ejecutar Experimento
        </button>
        {pointsType === 'custom' && (
          <button
            className="btn"
            style={{ backgroundColor: '#805ad5', color: 'white' }}
            onClick={handleSteps}
          >
            Mostrar Pasos
          </button>
        )}
      </div>
    </section>
  );
}
