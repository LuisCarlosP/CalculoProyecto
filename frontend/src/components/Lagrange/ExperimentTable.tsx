import type { ExperimentResultDTO } from '../../types/lagrange';
import { formatNum } from '../../utils/format';

interface Props {
  results: ExperimentResultDTO[];
}

export default function ExperimentTable({ results }: Props) {
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>n</th>
            <th>Resultado</th>
            <th>Valor Exacto</th>
            <th>Error Absoluto</th>
            <th>Error Relativo</th>
            <th>Tiempo (ms)</th>
            <th>Iteraciones</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r) => (
            <tr key={r.n}>
              <td>{r.n}</td>
              <td>{formatNum(r.result)}</td>
              <td>{formatNum(r.exact_value)}</td>
              <td>{formatNum(r.absolute_error)}</td>
              <td>{formatNum(r.relative_error)}</td>
              <td>{formatNum(r.execution_time * 1000)}</td>
              <td>{r.iterations}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
