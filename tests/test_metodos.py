import unittest
import math
from metodos.biseccion import Biseccion
from metodos.falsa_posicion import FalsaPosicion
from metodos.newton_raphson import NewtonRaphson
from metodos.punto_fijo import PuntoFijo
from metodos.secante import Secante
from metodos.bhaskara import bhaskara as formula_cuadratica

class TestMetodosNumericos(unittest.TestCase):

    def test_biseccion(self):
        f = lambda x: x**2 - 4  # Raíces en 2 y -2
        metodo = Biseccion(f, tolerancia=1e-7)
        resultado = metodo.calcular(0, 3)
        self.assertTrue(resultado['exito'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=6)

    def test_falsa_posicion(self):
        f = lambda x: x**2 - 4
        metodo = FalsaPosicion(f, tolerancia=1e-7)
        resultado = metodo.calcular(0, 3)
        self.assertTrue(resultado['exito'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=6)

    def test_newton_raphson(self):
        f = lambda x: x**2 - 4
        df = lambda x: 2*x
        metodo = NewtonRaphson(f, df, tolerancia=1e-10)
        resultado = metodo.calcular(3)
        self.assertTrue(resultado['exito'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=9)

    def test_punto_fijo(self):
        # f(x) = x^2 - x - 2 = 0  => x = sqrt(x + 2) = g(x)
        g = lambda x: math.sqrt(x + 2)
        metodo = PuntoFijo(g, tolerancia=1e-8)
        resultado = metodo.calcular(1)
        self.assertTrue(resultado['exito'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=7)

    def test_secante(self):
        f = lambda x: x**2 - 4
        metodo = Secante(f, tolerancia=1e-9)
        resultado = metodo.calcular(0, 3)
        self.assertTrue(resultado['exito'])
        self.assertAlmostEqual(resultado['raiz'], 2.0, places=8)

    def test_formula_cuadratica(self):
        # x^2 - 5x + 6 = 0 => raíces 2 y 3
        raices, disc = formula_cuadratica(1, -5, 6)
        x1, x2 = raices
        self.assertEqual(disc, 1)
        self.assertIn(x1, [2, 3])
        self.assertIn(x2, [2, 3])

if __name__ == '__main__':
    unittest.main()
