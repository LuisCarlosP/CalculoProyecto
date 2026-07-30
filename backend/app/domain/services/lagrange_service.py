import math
import time
from typing import Callable, List, Optional, Tuple

from app.domain.models.lagrange import (
    ExperimentReport,
    ExperimentResult,
    LagrangeResult,
    Point,
)


def compute_lagrange_basis(x: float, i: int, points: List[Point]) -> float:
    """Evalúa la i-ésima base de Lagrange L_i(x) en el punto x.
    Recorre todos los puntos j ≠ i acumulando el producto de (x - x_j) / (x_i - x_j),
    que es la definición clásica del polinomio base de Lagrange.
    L_i(x) vale exactamente 1 en x = x_i y 0 en cualquier otro punto de interpolación."""
    L_i = 1.0
    n = len(points) - 1
    xi = points[i].x
    for j in range(n + 1):
        if j != i:
            xj = points[j].x
            L_i *= (x - xj) / (xi - xj)
    return L_i


def find_nearest_point(x: float, points: List[Point]) -> int:
    """Busca el punto de interpolación más cercano a x.
    Si la distancia mínima es menor que 1e-12, retorna el índice de ese punto;
    en caso contrario retorna -1 indicando que x no coincide con ningún punto conocido.
    Se usa para optimizar el cálculo de la derivada de L_i."""
    n = len(points)
    nearest = 0
    min_dist = abs(x - points[0].x)
    for k in range(1, n):
        dist = abs(x - points[k].x)
        if dist < min_dist:
            min_dist = dist
            nearest = k
    return nearest if min_dist < 1e-12 else -1


def compute_lagrange_basis_derivative(x: float, i: int, points: List[Point]) -> float:
    """Evalúa la derivada de la i-ésima base de Lagrange L'_i(x) en el punto x.
    Si x coincide con algún punto de interpolación (k encontrado), usa la versión
    simplificada de la derivada (suma de recíprocos o producto reducido).
    Si no, aplica la regla general: L_i(x) * Σ (1/(x - x_j)) para j ≠ i."""
    n = len(points) - 1
    xi = points[i].x
    k = find_nearest_point(x, points)

    if k != -1:
        if i == k:
            total = 0.0
            for j in range(n + 1):
                if j != k:
                    total += 1.0 / (points[k].x - points[j].x)
            return total
        else:
            L = 1.0
            for j in range(n + 1):
                if j != i and j != k:
                    L *= (points[k].x - points[j].x) / (xi - points[j].x)
            return L / (xi - points[k].x)

    L_i = compute_lagrange_basis(x, i, points)
    total = 0.0
    for j in range(n + 1):
        if j != i:
            total += 1.0 / (x - points[j].x)
    return L_i * total


def lagrange_interpolate(x: float, points: List[Point]) -> float:
    """Evalúa el polinomio interpolante de Lagrange P(x) en el punto x.
    Suma ponderada de cada valor y_i por su base L_i(x).
    """
    total = 0.0
    n = len(points)
    for i in range(n):
        L_i = compute_lagrange_basis(x, i, points)
        total += points[i].y * L_i
    return total


def lagrange_derivative(x: float, points: List[Point]) -> float:
    """Evalúa la derivada del polinomio interpolante P'(x) en el punto x.
    Suma ponderada de cada valor y_i por la derivada de su base L'_i(x).
    """
    total = 0.0
    n = len(points)
    for i in range(n):
        L_prime_i = compute_lagrange_basis_derivative(x, i, points)
        total += points[i].y * L_prime_i
    return total


def compute_errors(approximation: float, exact: float) -> Tuple[float, float]:
    """Calcula el error absoluto y relativo entre el valor aproximado y el exacto.
    Error absoluto = |aprox - exact|.
    Error relativo = error_absoluto / |exact|, con manejo del caso exact=0 retornando infinito."""
    abs_error = abs(approximation - exact)
    rel_error = abs_error / abs(exact) if exact != 0.0 else float("inf")
    return abs_error, rel_error


def count_iterations(num_points: int) -> int:
    """Estima la cantidad de operaciones aritméticas realizadas según el número de puntos:
    cada base L_i requiere n productos, cada derivada L'_i requiere n productos + n sumas,
    más las sumas finales de cada término."""
    n = num_points - 1
    basis_ops = n * (n + 1)
    basis_deriv_ops = n * (n + 1) + n
    sum_ops = num_points
    return basis_ops + basis_deriv_ops + sum_ops


def generate_equispaced_points(
    func: Callable[[float], float], a: float, b: float, n: int
) -> List[Point]:
    """Genera n puntos equiespaciados en el intervalo [a, b]
    evaluando la función dada en cada uno. Útil cuando se tiene
    una expresión analítica y se quiere probar el método con
    distintas cantidades de particiones."""
    points = []
    for i in range(n):
        x_i = a + i * (b - a) / (n - 1)
        points.append(Point(x=x_i, y=func(x_i)))
    return points


def generate_plot_data(
    func: Callable[[float], float],
    points: List[Point],
    a: float,
    b: float,
    num_samples: int = 200,
) -> List[Tuple[float, float, float]]:
    """Genera datos para graficar f(x) y P(x) en [a, b].
    Para cada muestra x calcula f(x) (exacto) y P(x) (interpolante de Lagrange)."""
    data = []
    for i in range(num_samples):
        x = a + i * (b - a) / (num_samples - 1)
        f_x = func(x)
        p_x = lagrange_interpolate(x, points)
        data.append((x, f_x, p_x))
    return data


def poly_mul(p: List[float], q: List[float]) -> List[float]:
    """Multiplica dos polinomios representados como listas de coeficientes
    (orden ascendente de grado). Cada coeficiente del resultado es la suma
    de productos p[i] * q[j] donde i+j = k."""
    result = [0.0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            result[i + j] += p[i] * q[j]
    return result


def expand_lagrange_basis_coeffs(i: int, points: List[Point]) -> List[float]:
    """Expande la i-ésima base de Lagrange a coeficientes polinomiales.
    Cada factor (x - x_j)/(x_i - x_j) es un binomio de grado 1.
    Multiplica sucesivamente todos los factores (para j ≠ i)
    usando poly_mul para obtener el polinomio completo L_i(x)."""
    n = len(points)
    xi = points[i].x
    coeffs = [1.0]
    for j in range(n):
        if j == i:
            continue
        xj = points[j].x
        factor_a = 1.0 / (xi - xj)
        factor_b = -xj / (xi - xj)
        coeffs = poly_mul(coeffs, [factor_b, factor_a])
    return coeffs


def compute_polynomial_coeffs(points: List[Point]) -> List[float]:
    """Construye el polinomio interpolante completo P(x) sumando
    cada base L_i(x) escalada por su valor y_i. Al final elimina
    coeficientes de grado superior que sean prácticamente cero."""
    n = len(points)
    result = None
    for i in range(n):
        coeffs = expand_lagrange_basis_coeffs(i, points)
        scaled = [c * points[i].y for c in coeffs]
        if result is None:
            result = scaled
        else:
            max_len = max(len(result), len(scaled))
            result_padded = result + [0.0] * (max_len - len(result))
            scaled_padded = scaled + [0.0] * (max_len - len(scaled))
            result = [a + b for a, b in zip(result_padded, scaled_padded)]
    if result is None:
        return [0.0]
    while len(result) > 1 and abs(result[-1]) < 1e-15:
        result.pop()
    return result


def differentiate_poly(coeffs: List[float]) -> List[float]:
    """Deriva un polinomio: dado [c0, c1, c2, ...] retorna [c1, 2*c2, 3*c3, ...].
    La regla de derivación término a término: d/dx (c_k * x^k) = k * c_k * x^{k-1}."""
    return [coeffs[i] * (i) for i in range(1, len(coeffs))]


def _format_term(c: float, power: int, var: str = "x") -> str:
    """Convierte un término c*x^power a string legible.
    Omite coeficientes prácticamente cero. Maneja casos especiales:
    coeficiente 1 (no se escribe), -1 (solo el signo), potencia 0 (solo el número),
    potencia 1 (no muestra el exponente)."""
    if abs(c) < 1e-15:
        return ""
    if power == 0:
        return f"{c:.6g}"
    coeff_str = ""
    if abs(c - 1.0) < 1e-10:
        coeff_str = ""
    elif abs(c + 1.0) < 1e-10:
        coeff_str = "-"
    else:
        coeff_str = f"{c:.6g}"
    if power == 1:
        return coeff_str + var
    return coeff_str + f"{var}^{power}"


def format_polynomial(coeffs: List[float], var: str = "x") -> str:
    """Convierte una lista de coeficientes a una cadena legible tipo "3x^2 - 2x + 1".
    Ensambla los términos respetando signos y omitiendo términos nulos."""
    terms = []
    for power, c in enumerate(coeffs):
        term = _format_term(c, power, var)
        if term:
            terms.append(term)

    if not terms:
        return "0"

    result = terms[0]
    for t in terms[1:]:
        if t[0] == "-":
            result += " - " + t[1:]
        else:
            result += " + " + t
    return result


def evaluate_derivative(
    func: Callable[[float], float],
    derivative_exact: Callable[[float], float],
    points: List[Point],
    x_eval: float,
) -> LagrangeResult:
    """Evalúa la derivada aproximada por Lagrange en x_eval, mide el tiempo
    de ejecución y calcula el valor exacto junto con los errores.
    Retorna un LagrangeResult con todos los datos."""
    start = time.perf_counter()
    approx = lagrange_derivative(x_eval, points)
    elapsed = time.perf_counter() - start

    exact_val = derivative_exact(x_eval)
    abs_error, rel_error = compute_errors(approx, exact_val)

    interp_val = lagrange_interpolate(x_eval, points)

    return LagrangeResult(
        x_eval=x_eval,
        interpolated_value=interp_val,
        derivative_approx=approx,
        derivative_exact=exact_val,
        absolute_error=abs_error,
        relative_error=rel_error,
        execution_time=elapsed,
        num_points=len(points),
    )


def run_experiment(
    func: Callable[[float], float],
    derivative_exact: Callable[[float], float],
    a: float,
    b: float,
    n_values: List[int],
    x_eval: float,
    function_name: str = "custom",
    plot_n: Optional[int] = None,
) -> ExperimentReport:
    """Ejecuta el experimento variando el número de particiones n.
    Para cada n: genera puntos equiespaciados, evalúa la derivada,
    mide tiempo, calcula errores y cuenta operaciones.
    Retorna un ExperimentReport con todos los resultados agregados
    y datos para graficar f(x) vs P(x). Usa plot_n si se especifica,
    o el n más grande de n_values (máx 20) en caso contrario."""
    report = ExperimentReport(
        function_name=function_name,
        a=a,
        b=b,
        x_eval=x_eval,
    )

    plot_points = None

    for n in n_values:
        points = generate_equispaced_points(func, a, b, n)

        if plot_n is not None and n == plot_n:
            plot_points = points
        elif plot_n is None and plot_points is None and n <= 20:
            plot_points = points

        start = time.perf_counter()
        approx = lagrange_derivative(x_eval, points)
        elapsed = time.perf_counter() - start

        exact_val = derivative_exact(x_eval)
        abs_error, rel_error = compute_errors(approx, exact_val)
        iterations = count_iterations(n)

        report.results.append(
            ExperimentResult(
                n=n,
                result=approx,
                exact_value=exact_val,
                absolute_error=abs_error,
                relative_error=rel_error,
                execution_time=elapsed,
                iterations=iterations,
            )
        )

    if plot_n is not None and plot_points is None:
        plot_points = generate_equispaced_points(func, a, b, plot_n)

    if plot_points is not None:
        report.plot_data = generate_plot_data(func, plot_points, a, b)
        report.interpolation_points = plot_points

    return report
