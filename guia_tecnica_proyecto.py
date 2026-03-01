"""
================================================================================
GUÍA DE ESPECIFICACIONES TÉCNICAS: PROYECTO ANÁLISIS NUMÉRICO
================================================================================
Este documento detalla las fórmulas matemáticas y la lógica de visualización 
utilizada en el proyecto de Calculadora de Métodos Numéricos.

ESTRUCTURA DEL PROYECTO:
- metodos/: Implementaciones algorítmicas de los métodos numéricos.
- interfaz/graficas.py: Motor de renderizado dinámico con Matplotlib.
- funciones/: Utilidades de cálculo y validación.

================================================================================
1. FÓRMULAS DE MÉTODOS NUMÉRICOS
================================================================================

A. MÉTODO DE BISECCIÓN (metodos/biseccion.py)
--------------------------------------------------------------------------------
- Fundamento: Teorema del Valor Intermedio (f(a)*f(b) < 0).
- Fórmula del punto medio:
    c = a + (b - a) / 2.0
- Criterios de parada:
    |f(c)| < 1e-15  O  |c - c_prev| < tolerancia  O  (b - a)/2 < tolerancia

B. MÉTODO DE FALSA POSICIÓN (metodos/falsa_posicion.py)
--------------------------------------------------------------------------------
- Fundamento: Interpolación lineal entre (a, f(a)) y (b, f(b)).
- Fórmula del punto c (Regula Falsi):
    c = b - f(b) * (b - a) / (f(b) - f(a))
- Criterios de parada:
    |c - c_prev| < tolerancia  O  |f(c)| < 1e-15

C. MÉTODO DE NEWTON-RAPHSON (metodos/newton_raphson.py)
--------------------------------------------------------------------------------
- Fundamento: Recta tangente a la curva en el punto x_n.
- Fórmula iterativa:
    x_{n+1} = x_n - f(x_n) / f'(x_n)
- Criterio de parada:
    |x_{n+1} - x_n| < tolerancia
- Restricción: f'(x_n) != 0. Se utiliza derivada numérica si es necesario.

D. MÉTODO DE PUNTO FIJO (metodos/punto_fijo.py)
--------------------------------------------------------------------------------
- Fundamento: Transformar f(x) = 0 en x = g(x).
- Fórmula iterativa:
    x_{n+1} = g(x_n)
- Condición de convergencia: |g'(x)| < 1.
- Derivada numérica (Diferencias Centrales):
    g'(x) ≈ (g(x + h) - g(x - h)) / (2h)

E. MÉTODO DE LA SECANTE (metodos/secante.py)
--------------------------------------------------------------------------------
- Fundamento: Aproximación de la derivada mediante la secante entre dos puntos.
- Fórmula iterativa:
    x_{n+1} = x_1 - f(x_1) * (x_1 - x_0) / (f(x_1) - f(x_0))
- Criterio de parada:
    |x_{n+1} - x_1| < tolerancia

================================================================================
2. LÓGICA DE GRÁFICOS DINÁMICOS (interfaz/graficas.py)
================================================================================
Visualización interactiva con Matplotlib integrada en Tkinter.

A. PANEL DE FUNCIÓN (ax1):
   - Gráfica la función f(x) con la raíz marcada (estrella roja #ff5555).
   - Modo Oscuro: Fondo #0b0b14, línea celeste #6699ff.
   - Modo Claro: Fondo #fdfdfd, línea azul oscura #003366.

B. VISUALIZACIONES ESPECÍFICAS:
   - Punto Fijo: Diagrama de telaraña (Cobweb plot).
   - Newton-Raphson: Líneas tangentes en las primeras iteraciones.
   - Secante: Líneas secantes entre puntos sucesivos.

C. PANEL DE CONVERGENCIA (ax2):
   - Escala logarítmica del error absoluto por cada iteración.

D. INTERACTIVIDAD:
   - Zoom con rueda del ratón.
   - Tooltips (hover) con información del error y coordenadas (x, y).
================================================================================
"""
