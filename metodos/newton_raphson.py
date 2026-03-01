from typing import Callable, Dict, List, Union
import time

class NewtonRaphson:
    """
    Clase que implementa el método numérico de Newton-Raphson.
    """

    def __init__(self, funcion: Callable[[float], float], derivada: Callable[[float], float], tolerancia: float = 1e-10, max_iter: int = 100):
        """
        Inicializa el configurador del método de Newton-Raphson.

        Args:
            funcion: La función matemática a evaluar f(x).
            derivada: La primera derivada de la función f'(x).
            tolerancia: El criterio de parada para el error (10^-10 para este ejercicio).
            max_iter: Número máximo de iteraciones.
        """
        self.funcion = funcion
        self.derivada = derivada
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def calcular(self, x0: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta la iteración de Newton-Raphson a partir del valor inicial x0.
        """
        inicio_tiempo = time.perf_counter()
        iteraciones_data = []
        x_actual = x0

        for n in range(1, self.max_iter + 1):
            fx = self.funcion(x_actual)
            dfx = self.derivada(x_actual)

            if dfx == 0:
                return {
                    'exito': False, 'raiz': x_actual, 'iteraciones_totales': n,
                    'historial': iteraciones_data,
                    'mensaje': f"Falla del método: La derivada f'(x) se hizo cero en la iteración {n}.",
                    'tiempo': (time.perf_counter() - inicio_tiempo) * 1000
                }

            x_siguiente = x_actual - (fx / dfx)

            error_absoluto = abs(x_siguiente - x_actual)
            error_relativo = abs(x_siguiente - x_actual) / abs(x_siguiente) if x_siguiente != 0 else 0.0

            iteraciones_data.append({
                'n': n, 'c': x_actual, 'f(c)': fx, 'f_prima(c)': dfx,
                'error_absoluto': error_absoluto, 'error_relativo': error_relativo * 100
            })

            if error_absoluto < self.tolerancia:
                return {
                    'exito': True, 'raiz': x_siguiente, 'iteraciones_totales': n,
                    'historial': iteraciones_data, 'mensaje': "Convergencia exitosa.",
                    'tiempo': (time.perf_counter() - inicio_tiempo) * 1000
                }

            x_actual = x_siguiente

        return {
            'exito': False, 'raiz': x_actual, 'iteraciones_totales': self.max_iter,
            'historial': iteraciones_data, 'mensaje': "Máximo de iteraciones alcanzado sin convergir.",
            'tiempo': (time.perf_counter() - inicio_tiempo) * 1000
        }