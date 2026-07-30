const SUPERSCRIPTS = '⁰¹²³⁴⁵⁶⁷⁸⁹';

function toSuperscript(n: number): string {
  return String(n).split('').map(d => SUPERSCRIPTS[parseInt(d, 10)]).join('');
}

function formatExponent(n: number): string {
  const [mantissa, expPart] = n.toExponential(4).split('e');
  const exp = parseInt(expPart, 10);
  const sign = exp < 0 ? '⁻' : '';
  return `${mantissa} × 10${sign}${toSuperscript(Math.abs(exp))}`;
}

export function formatNum(n: number | null | undefined): string {
  if (n === null || n === undefined || (typeof n === 'number' && isNaN(n))) return '—';
  if (n === 0) return '0';
  if (!isFinite(n)) return '∞';
  if (Math.abs(n) >= 0.001 && Math.abs(n) < 1e10) {
    return Number(n.toPrecision(6)).toString();
  }
  return formatExponent(n);
}
