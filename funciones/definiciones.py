import math
from typing import Tuple, Optional


def formula_cuadratica(a: float, b: float, c: float) -> Tuple[Optional[float], Optional[float], float]:
    """
    Calcula las raíces de una ecuación de segundo grado ax² + bx + c = 0.
    Utiliza el discriminante Δ = b² - 4ac.

    Args:
        a: Coeficiente de x².
        b: Coeficiente de x.
        c: Término independiente.

    Returns:
        Una tupla con (x1, x2, discriminante). x1 y x2 pueden ser None si son imaginarias.
    """
    if a == 0:
        raise ValueError("El coeficiente 'a' no puede ser cero para una ecuación cuadrática.")

    discriminante = b ** 2 - 4 * a * c

    if discriminante < 0:
        # Raíces complejas (no manejadas en este script básico, retornamos None)
        return None, None, discriminante

    x1 = (-b + math.sqrt(discriminante)) / (2 * a)
    x2 = (-b - math.sqrt(discriminante)) / (2 * a)

    return x1, x2, discriminante
