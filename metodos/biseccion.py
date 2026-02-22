from typing import Callable, Dict, List, Union


class Biseccion:
    """
    Clase que implementa el método numérico de Bisección.
    """

    def __init__(self, funcion: Callable[[float], float], tolerancia: float = 1e-7, max_iter: int = 100):
        """
        Inicializa el configurador del método de Bisección.

        Args:
            funcion: La función matemática a evaluar f(x).
            tolerancia: El criterio de parada para el error.
            max_iter: Número máximo de iteraciones permitidas.
        """
        self.funcion = funcion
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def calcular(self, a: float, b: float) -> Dict[str, Union[float, int, List[Dict[str, float]], str]]:
        """
        Ejecuta el método de bisección para encontrar la raíz en el intervalo [a, b][cite: 28].

        Args:
            a: Límite inferior del intervalo.
            b: Límite superior del intervalo.

        Returns:
            Un diccionario con el estado de la convergencia, la raíz, iteraciones y errores.
        """
        fa = self.funcion(a)
        fb = self.funcion(b)

        # Validar que f(a) y f(b) tengan signos opuestos [cite: 76]
        if fa * fb > 0:
            raise ValueError("El intervalo no contiene una raíz (f(a) y f(b) tienen el mismo signo).")

        iteraciones_data = []
        c_anterior = a

        for n in range(1, self.max_iter + 1):
            # Calcular el punto medio [cite: 30]
            c = (a + b) / 2.0
            fc = self.funcion(c)

            # Cálculo de errores [cite: 78, 79]
            error_absoluto = abs(c - c_anterior)
            error_relativo = abs(c - c_anterior) / abs(c) if c != 0 else 0.0

            iteraciones_data.append({
                'n': n,
                'a': a,
                'b': b,
                'c': c,
                'f(c)': fc,
                'error_absoluto': error_absoluto,
                'error_relativo': error_relativo * 100
            })

            # Criterio de parada: tolerancia o raíz exacta [cite: 31, 34]
            if error_absoluto < self.tolerancia or fc == 0.0:
                return {
                    'exito': True,
                    'raiz': c,
                    'iteraciones_totales': n,
                    'historial': iteraciones_data,
                    'mensaje': "Convergencia exitosa."
                }

            # Actualización del intervalo [cite: 32, 33]
            if fa * fc < 0:
                b = c
            else:
                a = c
                fa = fc  # Actualizamos fa para la siguiente iteración

            c_anterior = c

        # No convergencia tras iteraciones máximas
        return {
            'exito': False,
            'raiz': c,
            'iteraciones_totales': self.max_iter,
            'historial': iteraciones_data,
            'mensaje': "Máximo de iteraciones alcanzado sin convergir."
        }