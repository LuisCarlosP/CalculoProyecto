import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  type TooltipItem,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import type { FunctionPlotPoint, PointDTO } from '../../../types/lagrange';
import { formatNum } from '../../../utils/format';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

interface Props {
  data: FunctionPlotPoint[];
  interpolationPoints: PointDTO[];
  a: number;
  b: number;
}

export default function FunctionPlot({ data, interpolationPoints, a, b }: Props) {
  const labels = data.map((d) => formatNum(d.x));

  const interpValues = data.map((d) => {
    const match = interpolationPoints.find((p) => Math.abs(p.x - d.x) < 1e-10);
    return match ? match.y : null;
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: 'f(x)',
        data: data.map((d) => d.f_x),
        borderColor: '#3182ce',
        backgroundColor: 'rgba(49, 130, 206, 0.1)',
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3,
      },
      {
        label: 'P(x)',
        data: data.map((d) => d.p_x),
        borderColor: '#e53e3e',
        backgroundColor: 'rgba(229, 62, 62, 0.05)',
        borderWidth: 2,
        borderDash: [6, 3],
        pointRadius: 0,
        tension: 0.3,
      },
      {
        label: 'Puntos de interpolación',
        data: interpValues,
        borderColor: '#38a169',
        backgroundColor: '#38a169',
        pointRadius: 5,
        pointStyle: 'triangle',
        showLine: false,
        pointHitRadius: 10,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: `f(x) vs P(x) en [${formatNum(a)}, ${formatNum(b)}]`,
        font: { size: 14 },
      },
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: (ctx: TooltipItem<'line'>) => {
            const val = ctx.parsed.y;
            if (val === null) return '';
            return `${ctx.dataset.label}: ${formatNum(val)}`;
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'x' },
        ticks: { maxRotation: 0 },
      },
      y: {
        title: { display: true, text: 'f(x), P(x)' },
      },
    },
  };

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
}
