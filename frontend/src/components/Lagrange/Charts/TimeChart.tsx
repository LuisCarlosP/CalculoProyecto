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
import { formatNum } from '../../../utils/format';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  data: { n: number; execution_time: number }[];
}

export default function TimeChart({ data }: Props) {
  const labels = data.map((d) => d.n.toString());

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Tiempo de ejecución',
        data: data.map((d) => d.execution_time * 1000),
        borderColor: '#3182ce',
        backgroundColor: 'rgba(49, 130, 206, 0.1)',
        borderWidth: 2,
        pointRadius: 4,
        tension: 0.3,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Tiempo de Ejecución vs Número de Particiones (n)',
        font: { size: 14 },
      },
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: (ctx: TooltipItem<'line'>) => `${formatNum(ctx.parsed.y)} ms`,
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'n (particiones)' },
      },
      y: {
        title: { display: true, text: 'Tiempo (ms)' },
      },
    },
  };

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
}
