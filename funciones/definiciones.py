import math
import matplotlib.pyplot as plt
import tkinter as tk
from metodos.bhaskara import bhaskara

def bhaskara_visualmente(a, b, c):
    """
    Muestra el procedimiento de Bhaskara visualmente usando matplotlib.
    """
    raices, discriminante = bhaskara(a, b, c)

    if raices is None:
        ecuaciones = [
            r"$\Delta = b^2 - 4ac$",
            rf"$\Delta = {b}^2 - 4({a})({c})$",
            rf"$\Delta = {discriminante}$",
            r"$\text{No existen raíces reales}$"
        ]
    else:
        x1, x2 = raices
        ecuaciones = [
            r"$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",
            rf"$x_1 = {x1:.4f}$",
            rf"$x_2 = {x2:.4f}$"
        ]

    plt.figure(figsize=(6, 4))
    plt.axis("off")

    y = 0.8
    for eq in ecuaciones:
        plt.text(0.1, y, eq, fontsize=18)
        y -= 0.2

    plt.title(f"Solución de {a}x² + {b}x + {c} = 0")
    plt.tight_layout()
    plt.show()
