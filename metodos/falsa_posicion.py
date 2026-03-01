from typing import Callable, Dict, List, Union
import time


class FalsaPosicion:
    """
    Clase que implementa el método numérico de Falsa Posición (Regula Falsi).
    """

    def __init__(self, funcion: Callable[[float], float], tolerancia: float = 1e-7, max_iter: int = 100):
        """
        Inicializa el configurador del método.

        Args:
            funcion: La función matemática a evaluar f(x).
            tolerancia: El criterio de parada para el error relativo/absoluto.
            max_iter: Número máximo de iteraciones permitidas.
        """
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def calcular(self, a: float, b: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta el método de falsa posición para encontrar la raíz en el intervalo [a, b].
        """
        inicio_tiempo = time.perf_counter()
        # Validación del intervalo: f(a) y f(b) deben tener signos opuestos
        fa = self.funcion(a)
        fb = self.funcion(b)

        if fa * fb > 0:
            return {
                'exito': False, 'raiz': 0, 'iteraciones_totales': 0,
                'historial': [], 'mensaje': "Error: f(a) y f(b) deben tener signos opuestos.",
                'tiempo': 0
            }

        iteraciones_data = []
        c_anterior = a

        for n in range(1, self.max_iter + 1):
            fa = self.funcion(a)
            fb = self.funcion(b)

            if fb - fa == 0:
                return {
                    'exito': False, 'raiz': a, 'iteraciones_totales': n,
                    'historial': iteraciones_data, 'mensaje': "Error: División por cero.",
                    'tiempo': (time.perf_counter() - inicio_tiempo) * 1000
                }

            c = b - fb * (b - a) / (fb - fa)
            fc = self.funcion(c)

            error_absoluto = abs(c - c_anterior)
            error_relativo = abs(c - c_anterior) / abs(c) if c != 0 else 0.0

            iteraciones_data.append({
                'n': n, 'a': a, 'b': b, 'c': c, 'f(c)': fc,
                'error_absoluto': error_absoluto, 'error_relativo': error_relativo * 100
            })

            if error_absoluto < self.tolerancia or abs(fc) < 1e-15:
                return {
                    'exito': True, 'raiz': c, 'iteraciones_totales': n,
                    'historial': iteraciones_data, 'mensaje': "Convergencia exitosa.",
                    'tiempo': (time.perf_counter() - inicio_tiempo) * 1000
                }

            if fa * fc < 0:
                b = c
            else:
                a = c
            c_anterior = c

        return {
            'exito': False, 'raiz': c, 'iteraciones_totales': self.max_iter,
            'historial': iteraciones_data, 'mensaje': "Máximo de iteraciones alcanzado.",
            'tiempo': (time.perf_counter() - inicio_tiempo) * 1000
        }