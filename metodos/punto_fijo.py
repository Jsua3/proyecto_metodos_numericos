from typing import Callable, Dict, List, Union
import math


class PuntoFijo:
    """
    Clase que implementa el método numérico de Punto Fijo x = g(x).
    """

    def __init__(self, funcion_g: Callable[[float], float], tolerancia: float = 1e-8, max_iter: int = 100,
                 limite_divergencia: float = 1e6):
        """
        Inicializa el configurador del método de Punto Fijo.

        Args:
            funcion_g: La función iterativa g(x).
            tolerancia: El criterio de parada para el error (10^-8 según la guía).
            max_iter: Número máximo de iteraciones.
            limite_divergencia: Valor máximo permitido antes de asumir que el método diverge.
        """
        self.funcion_g = funcion_g
        self.tolerancia = tolerancia
        self.max_iter = max_iter
        self.limite_divergencia = limite_divergencia

    def calcular(self, x0: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta la iteración de punto fijo a partir del valor inicial x0.

        Args:
            x0: Aproximación inicial.

        Returns:
            Un diccionario estandarizado con los resultados para la interfaz.
        """
        iteraciones_data = []
        x_actual = x0

        for n in range(1, self.max_iter + 1):
            # Calcular el siguiente valor evaluando g(x)
            x_siguiente = self.funcion_g(x_actual)

            # 1. Detección de divergencia exigida por la guía
            if abs(x_siguiente) > self.limite_divergencia:
                return {
                    'exito': False,
                    'raiz': x_actual,
                    'iteraciones_totales': n,
                    'historial': iteraciones_data,
                    'mensaje': f"Divergencia detectada en la iteración {n}. El valor excedió el límite."
                }

            # 2. Cálculo de errores
            error_absoluto = abs(x_siguiente - x_actual)
            error_relativo = abs(x_siguiente - x_actual) / abs(x_siguiente) if x_siguiente != 0 else 0.0

            # 3. Guardar en el historial usando las llaves compatibles con nuestra GUI
            iteraciones_data.append({
                'n': n,
                'c': x_actual,  # Usamos 'c' para mantener compatibilidad con la tabla
                'f(c)': x_siguiente,  # Aquí guardamos g(x_n)
                'error_absoluto': error_absoluto,
                'error_relativo': error_relativo * 100
            })

            # 4. Criterio de parada
            if error_absoluto < self.tolerancia:
                return {
                    'exito': True,
                    'raiz': x_siguiente,
                    'iteraciones_totales': n,
                    'historial': iteraciones_data,
                    'mensaje': "Convergencia exitosa."
                }

            x_actual = x_siguiente

        # Retorno si agota las iteraciones sin éxito
        return {
            'exito': False,
            'raiz': x_actual,
            'iteraciones_totales': self.max_iter,
            'historial': iteraciones_data,
            'mensaje': "Máximo de iteraciones alcanzado sin convergir."
        }