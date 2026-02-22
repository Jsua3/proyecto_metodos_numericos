from typing import Callable, Dict, List, Union


class Secante:
    """
    Clase que implementa el método numérico de la Secante.
    """

    def __init__(self, funcion: Callable[[float], float], tolerancia: float = 1e-9, max_iter: int = 100):
        """
        Inicializa el configurador del método de la Secante.

        Args:
            funcion: La función matemática a evaluar f(x).
            tolerancia: El criterio de parada para el error.
            max_iter: Número máximo de iteraciones.
        """
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iter = max_iter
        self.evaluaciones_funcion = 0  # Contador de evaluaciones

    def calcular(self, x0: float, x1: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta la iteración de la Secante a partir de dos valores iniciales x0 y x1.

        Args:
            x0: Primera aproximación inicial (n-1).
            x1: Segunda aproximación inicial (n).

        Returns:
            Un diccionario con los resultados estandarizados.
        """
        self.evaluaciones_funcion = 0
        iteraciones_data = []

        fx0 = self.funcion(x0)
        fx1 = self.funcion(x1)
        self.evaluaciones_funcion += 2  # Ya evaluamos f(x) dos veces

        for n in range(1, self.max_iter + 1):
            # Validación para evitar división por cero
            if fx1 - fx0 == 0:
                return {
                    'exito': False,
                    'raiz': x1,
                    'iteraciones_totales': n,
                    'evaluaciones': self.evaluaciones_funcion,
                    'historial': iteraciones_data,
                    'mensaje': f"Falla del método: División por cero (f(x_n) - f(x_{n - 1}) = 0) en la iteración {n}."
                }

            # Fórmula del método de la secante
            x_siguiente = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            fx_siguiente = self.funcion(x_siguiente)
            self.evaluaciones_funcion += 1

            # Cálculo de errores
            error_absoluto = abs(x_siguiente - x1)
            error_relativo = abs(x_siguiente - x1) / abs(x_siguiente) if x_siguiente != 0 else 0.0

            # Guardar en el historial con las llaves requeridas
            iteraciones_data.append({
                'n': n,
                'x_n-1': x0,
                'c': x1,  # Usamos 'c' como x_n para compatibilidad con la tabla GUI
                'f(x_n-1)': fx0,
                'f(c)': fx1,  # f(x_n)
                'x_n+1': x_siguiente,
                'error_absoluto': error_absoluto,
                'error_relativo': error_relativo * 100
            })

            # Criterio de parada
            if error_absoluto < self.tolerancia:
                return {
                    'exito': True,
                    'raiz': x_siguiente,
                    'iteraciones_totales': n,
                    'evaluaciones': self.evaluaciones_funcion,
                    'historial': iteraciones_data,
                    'mensaje': "Convergencia exitosa."
                }

            # Actualizar variables para la siguiente iteración
            x0 = x1
            fx0 = fx1
            x1 = x_siguiente
            fx1 = fx_siguiente

        return {
            'exito': False,
            'raiz': x1,
            'iteraciones_totales': self.max_iter,
            'evaluaciones': self.evaluaciones_funcion,
            'historial': iteraciones_data,
            'mensaje': "Máximo de iteraciones alcanzado sin convergir."
        }