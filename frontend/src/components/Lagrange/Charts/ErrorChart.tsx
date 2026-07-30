import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  LogarithmicScale,
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
  Legend,
  LogarithmicScale
);

interface Props {
  data: { n: number; absolute_error: number; relative_error: number }[];
}

export default function ErrorChart({ data }: Props) {
  const labels = data.map((d) => d.n.toString());

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Error Absoluto',
        data: data.map((d) => d.absolute_error),
        borderColor: '#e53e3e',
        backgroundColor: 'rgba(229, 62, 62, 0.1)',
        borderWidth: 2,
        pointRadius: 4,
        tension: 0.3,
      },
      {
        label: 'Error Relativo',
        data: data.map((d) => d.relative_error),
        borderColor: '#dd6b20',
        backgroundColor: 'rgba(221, 107, 32, 0.1)',
        borderWidth: 2,
        pointRadius: 4,
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Error vs Número de Particiones (n)',
        font: { size: 14 },
      },
      legend: {
        position: 'bottom' as const,
      },
      tooltip: {
        callbacks: {
          label: (ctx: TooltipItem<'line'>) => formatNum(ctx.parsed.y),
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: 'n (particiones)' },
        type: 'linear' as const,
        ticks: { maxRotation: 0 },
      },
      y: {
        title: { display: true, text: 'Error' },
        type: 'logarithmic' as const,
        ticks: {
          callback: (tickValue: string | number) => {
            const v = typeof tickValue === 'string' ? parseFloat(tickValue) : tickValue;
            if (v === 0) return '0';
            const exp = Math.round(Math.log10(v));
            return `10^${exp}`;
          },
        },
      },
    },
  };

  return (
    <div className="chart-container">
      <Line data={chartData} options={options} />
    </div>
  );
}
