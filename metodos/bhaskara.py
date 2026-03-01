import math

def bhaskara(a, b, c):
    """
    Calcula las raíces de una ecuación cuadrática ax^2 + bx + c = 0.
    """
    discriminante = b**2 - 4*a*c
    
    if discriminante < 0:
        return None, discriminante
    
    raiz_delta = math.sqrt(discriminante)
    x1 = (-b + raiz_delta) / (2 * a)
    x2 = (-b - raiz_delta) / (2 * a)
    
    return (x1, x2), discriminante
