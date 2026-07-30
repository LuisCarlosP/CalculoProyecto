export default function Header() {
  return (
    <header style={{
      backgroundColor: '#1a365d',
      color: 'white',
      padding: '1.5rem 2rem',
      textAlign: 'center',
    }}>
      <h1 style={{ margin: 0, fontSize: '1.8rem' }}>
        Derivación Numérica por Interpolación de Lagrange
      </h1>
      <p style={{ margin: '0.5rem 0 0', opacity: 0.85, fontSize: '0.95rem' }}>
        Cálculo Diferencial e Integral — Proyecto de Cálculo Numérico
      </p>
    </header>
  );
}
