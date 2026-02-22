# Resolución de Ecuaciones No Lineales - Aplicaciones en Ingeniería de Software

Este proyecto es una aplicación con Interfaz Gráfica de Usuario (GUI) desarrollada en Python, diseñada para implementar y comparar cinco métodos numéricos clásicos en la resolución de ecuaciones no lineales aplicadas a problemas de arquitectura y sistemas distribuidos.

Desarrollado para el programa de Ingeniería de Software de la Corporación Universitaria Empresarial Alexander von Humboldt.

## Métodos Implementados
1. **Método de la Bisección:** Optimización de Hash Tables.
2. **Método de Falsa Posición:** Balanceo de carga en servidores.
3. **Método de Punto Fijo:** Predicción de crecimiento de Bases de Datos (incluye *Cobweb Plot*).
4. **Método de Newton-Raphson:** Análisis de concurrencia de hilos (incluye cálculo simbólico de derivadas con SymPy y gráficas de rectas tangentes).
5. **Método de la Secante:** Predicción de escalabilidad en la nube.

## Requisitos Previos
* Python 3.8 o superior.
* Git instalado en su sistema.

## [cite_start]Instrucciones de Instalación [cite: 235, 236]

1. Clone este repositorio en su máquina local:
   ```bash
   git clone https://github.com/Jsua3/proyecto_metodos_numericos.git
   cd proyecto_metodos_numericos

2. Cree un entorno virtual para aislar las dependencias:

    python -m venv .venv

3. Active el entorno virtual:

    Windows: .venv\Scripts\activate
    macOS/Linux: source .venv/bin/activate

4. Instale las dependencias requeridas:

   pip install -r requirements.txt

## Instrucciones de Ejecución 

Para iniciar la interfaz gráfica de usuario, asegúrese de tener su entorno virtual activado y 
ejecute el punto de entrada principal del programa:

python main.py 

## Estructura del Proyecto
    El código sigue estrictamente el estándar PEP 8 y está organizado bajo principios de Programación Orientada a Objetos:

    /metodos/: Clases individuales con la lógica matemática de cada algoritmo.

    /interfaz/: Construcción de la vista visual y gráficas embebidas de Matplotlib.

    /main.py: Punto de entrada que orquesta la aplicación.
   
