import type { StepsResponse } from '../../types/lagrange';
import { formatNum } from '../../utils/format';

interface Props {
  result: StepsResponse | null;
}

export default function StepByStepView({ result }: Props) {
  if (!result) return null;

  return (
    <section className="section">
      <h2 className="section-title">Derivación Paso a Paso</h2>

      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>Datos de entrada</h3>
        <table>
          <thead>
            <tr>
              <th>i</th>
              <th>x_i</th>
              <th>f(x_i)</th>
            </tr>
          </thead>
          <tbody>
            {result.points.map((p, i) => (
              <tr key={i}>
                <td>{i}</td>
                <td>{p.x}</td>
                <td>{p.y}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
          Paso 1: Bases de Lagrange L_i(x)
        </h3>
        {result.steps.map((step) => (
          <div
            key={step.i}
            style={{
              background: '#f7fafc',
              padding: '0.75rem',
              borderRadius: '6px',
              marginBottom: '0.5rem',
              fontFamily: 'monospace',
              fontSize: '0.9rem',
            }}
          >
            <div><strong>{step.basis_term}</strong></div>
            <div style={{ color: '#718096', marginTop: '0.25rem' }}>
              Simplificado: {step.basis_simplified}
            </div>
            <div style={{ color: '#2b6cb0', marginTop: '0.25rem' }}>
              {step.contribution}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
          Paso 2: Polinomio Interpolante
        </h3>
        <div
          style={{
            background: '#ebf8ff',
            padding: '0.75rem',
            borderRadius: '6px',
            fontFamily: 'monospace',
            fontSize: '1rem',
            fontWeight: 600,
          }}
        >
          {result.polynomial}
        </div>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
          Paso 3: Derivada del Polinomio
        </h3>
        <div
          style={{
            background: '#fff5f5',
            padding: '0.75rem',
            borderRadius: '6px',
            fontFamily: 'monospace',
            fontSize: '1rem',
            fontWeight: 600,
          }}
        >
          {result.derivative}
        </div>
      </div>

      <div>
        <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>
          Resultado
        </h3>
        <div
          style={{
            background: '#f0fff4',
            padding: '0.75rem',
            borderRadius: '6px',
            fontFamily: 'monospace',
            fontSize: '1.1rem',
            fontWeight: 700,
            color: '#276749',
          }}
        >
          f'({result.x_eval}) ≈ P'({result.x_eval}) = {formatNum(result.evaluated)}
        </div>
      </div>
    </section>
  );
}
