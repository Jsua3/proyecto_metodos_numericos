# 📊 Calculadora de Métodos Numéricos - Guía de Usuario

Este programa es una herramienta visual e interactiva diseñada para resolver ecuaciones matemáticas complejas de forma automática. Ideal para estudiantes y curiosos que necesitan encontrar soluciones numéricas (raíces) sin complicaciones técnicas.

---

## 🚀 ¿Cómo empezar? (Para Windows)

Si eres un usuario de Windows, ¡esto es lo más sencillo! No necesitas saber comandos.

1.  **Descarga el proyecto** en tu computadora.
2.  Busca el archivo llamado **`run.bat`** en la carpeta principal.
3.  Haz **doble clic** sobre él.
4.  ¡Listo! El programa se encargará de instalar todo lo necesario y abrir la aplicación por ti.

---

## 🛠 ¿Qué puedes hacer con esta aplicación?

Esta herramienta te permite encontrar el valor de "x" que hace que una función sea igual a cero (lo que llamamos "hallar la raíz").

- **Escribe tus fórmulas**: Introduce funciones matemáticas de forma natural (ej. `x^2 - 4`, `sin(x) + x`, etc.).
- **Ve la solución en vivo**: El programa genera una gráfica interactiva donde puedes ver exactamente dónde cruza la función el eje X.
- **Diferentes métodos**: Puedes elegir entre varias estrategias clásicas (Bisección, Newton-Raphson, Punto Fijo, etc.).
- **Resultados paso a paso**: Una tabla detallada te muestra cómo el programa "adivina" y corrige la solución hasta llegar a la más precisa.

---

## 🖱️ Controles rápidos en las gráficas

- **Zoom**: Usa la rueda del ratón para acercarte o alejarte y ver los detalles.
- **Información al pasar el mouse**: Pasa el puntero sobre los puntos para ver el error, el número de paso y las coordenadas (x, y).
- **Botones con contraste**: Los botones principales cambian de color al pasar el mouse para que sea más fácil saber dónde hacer clic.
- **Temas Claro y Oscuro**: Alterna la estética visual según tu preferencia con el botón de modo (🌙/☀️).

---

## 💻 Sección para Desarrolladores (Instalación Manual)

Si prefieres hacerlo manualmente o estás en Linux/Mac:

1.  **Requisito**: Tener instalado Python 3.10 o superior.
2.  **Preparar el entorno**:
    ```bash
    python -m venv venv
    ```
3.  **Activar el entorno**:
    - Windows: `venv\Scripts\activate`
    - Linux/Mac: `source venv/bin/activate`
4.  **Instalar paquetes necesarios**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Iniciar**:
    ```bash
    python main.py
    ```

---

## 📂 Organización del Proyecto

Para los que quieran ver cómo está construido:
- `main.py`: Punto de inicio.
- `metodos/`: Los algoritmos matemáticos base.
- `interfaz/`: Todo el diseño visual y gráficas interactivas.
- `funciones/`: Herramientas para validar y calcular expresiones.
- `guia_tecnica_proyecto.py`: Un reporte detallado con todas las fórmulas matemáticas exactas.

---
*Proyecto de Análisis Numérico - Ingeniería de Software*
