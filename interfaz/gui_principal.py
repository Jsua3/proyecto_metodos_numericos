import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from metodos.falsa_posicion import FalsaPosicion
from metodos.biseccion import Biseccion


class VentanaPrincipal(tk.Tk):
    """
    Clase principal que construye y gestiona la Interfaz Gráfica de Usuario (GUI).
    """

    def __init__(self):
        super().__init__()
        self.title("Resolución de Ecuaciones No Lineales - Alexander von Humboldt")
        self.geometry("1050x750")
        self.configure(bg="#f4f5f7") # Un fondo gris claro muy moderno

        self.configurar_estilos() # <--- Añade esta línea

        # Inicialización de la estructura visual principal
        self.crear_panel_entrada()
        self.crear_tabla_resultados()
        self.crear_panel_graficas()

    def configurar_estilos(self):
        """Aplica un tema oscuro nativo (Dark Mode) usando ttk."""
        self.configure(bg="#2b2b2b")  # Fondo principal oscuro de la ventana
        self.estilo = ttk.Style()

        # Usamos 'clam' como lienzo en blanco porque es el más personalizable
        if 'clam' in self.estilo.theme_names():
            self.estilo.theme_use('clam')

        # Paleta de colores estilo IDE profesional
        bg_color = "#3c3f41"
        fg_color = "#a9b7c6"
        btn_color = "#4b6eaf"
        acento = "#cc7832"  # Un tono naranja para resaltar

        # Estilo de textos y botones
        self.estilo.configure("TLabel", font=("Segoe UI", 10), background=bg_color, foreground=fg_color)
        self.estilo.configure("TButton", font=("Segoe UI", 10, "bold"), background=btn_color, foreground="white",
                              padding=6)
        self.estilo.map("TButton", background=[('active', '#365880')])  # Brillo al pasar el mouse

        # Estilo de los contenedores
        self.estilo.configure("TLabelframe", background=bg_color, foreground=fg_color, bordercolor="#555555")
        self.estilo.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"), background=bg_color,
                              foreground=acento)

        # Estilo de la tabla de resultados
        self.estilo.configure("Treeview",
                              font=("Consolas", 10),
                              rowheight=25,
                              background="#2b2b2b",
                              fieldbackground="#2b2b2b",
                              foreground=fg_color)

        self.estilo.configure("Treeview.Heading",
                              font=("Segoe UI", 10, "bold"),
                              background="#323232",
                              foreground=acento)

    def crear_panel_entrada(self):
        """Construye el panel superior para los parámetros de entrada del usuario."""
        frame_inputs = ttk.LabelFrame(self, text="  Parámetros de Entrada  ")
        frame_inputs.pack(fill="x", padx=10, pady=5)

        # Selección del método
        tk.Label(frame_inputs, text="Método:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_metodo = ttk.Combobox(
            frame_inputs,
            values=["Bisección", "Falsa Posición", "Punto Fijo", "Newton-Raphson", "Secante"],
            width=15
        )
        self.combo_metodo.grid(row=0, column=1, padx=5, pady=5)
        self.combo_metodo.current(1)

        # Campo para a (o x0 para Punto Fijo/Newton)
        tk.Label(frame_inputs, text="Valor Inicial (a / x0):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_a = tk.Entry(frame_inputs, width=8)
        self.entry_a.insert(0, "2.0")  # Valor por defecto
        self.entry_a.grid(row=0, column=3, padx=5, pady=5)

        # Campo para b
        tk.Label(frame_inputs, text="Valor Final (b):").grid(row=0, column=4, padx=5, pady=5)
        self.entry_b = tk.Entry(frame_inputs, width=8)
        self.entry_b.insert(0, "4.0")  # Valor por defecto
        self.entry_b.grid(row=0, column=5, padx=5, pady=5)

        # Botones
        tk.Button(frame_inputs, text="Calcular", command=self.ejecutar_calculo).grid(row=0, column=6, padx=5, pady=5)
        tk.Button(frame_inputs, text="Comparar Bis vs FP", command=self.ejecutar_comparacion, bg="lightblue").grid(
            row=0, column=7, padx=5, pady=5)
        # Botón especial para el Ejercicio 5
        tk.Button(frame_inputs, text="Comparar Secante vs NR",
                  command=self.ejecutar_comparacion_ej5, bg="lightgreen").grid(row=0, column=8, padx=5, pady=5)

    def crear_tabla_resultados(self):
        """Configura el componente Treeview para mostrar el historial de iteraciones."""
        frame_tabla = ttk.LabelFrame(self, text="  Tabla de Resultados  ")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("n", "x_n", "f(x_n)", "Error Abs", "Error Rel (%)")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=5, pady=5)

    def crear_panel_graficas(self):
        """Reserva el espacio inferior donde se incrustará matplotlib."""
        self.frame_grafica = ttk.LabelFrame(self, text="  Visualización de Convergencia  ")
        self.frame_grafica.pack(fill="both", expand=True, padx=10, pady=5)

        # 1. Crear la figura de matplotlib
        self.figura = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figura.add_subplot(111)

        # 2. Crear el lienzo de Tkinter y empaquetarlo
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Etiqueta temporal hasta conectar matplotlib
        tk.Label(self.frame_grafica, text="El área de gráficos se cargará aquí...").pack(pady=50)

    def graficar_funcion(self, funcion, a, b, raiz):
        """Dibuja la función y el punto de la raíz encontrada."""
        self.ax.clear()  # Limpiamos la gráfica anterior

        # Generar 400 puntos entre el intervalo [a, b] con un pequeño margen
        x = np.linspace(a - 0.5, b + 0.5, 400)
        y = [funcion(i) for i in x]

        # Trazar la curva de la función
        self.ax.plot(x, y, label="E(x) = x³ - 6x² + 11x - 6.5", color="blue")

        # Línea horizontal en y=0
        self.ax.axhline(0, color="black", linewidth=1, linestyle="--")

        # Marcar la raíz encontrada
        self.ax.plot(raiz, 0, 'ro', label=f"Raíz aprox: {raiz:.6f}")

        # Configuraciones visuales
        self.ax.set_title("Convergencia - Método de Falsa Posición")
        self.ax.set_xlabel("Eje X (Workers)")
        self.ax.set_ylabel("Eje Y (Eficiencia)")
        self.ax.legend()
        self.ax.grid(True)

        # Actualizar el lienzo
        self.canvas.draw()

    def ejecutar_calculo(self):
        """Callback que ejecuta la lógica matemática y actualiza la vista polimórficamente."""
        seleccion = self.combo_metodo.get()
        import math

        try:
            # Capturamos los valores de los cuadros de texto
            val_a = float(self.entry_a.get())
            val_b = float(self.entry_b.get())

            # Polimorfismo y configuración...
            if seleccion == "Bisección":
                def E(x):
                    return x ** 3 - 6 * x ** 2 + 11 * x - 6.5

                metodo = Biseccion(funcion=E, tolerancia=1e-7)
                resultado = metodo.calcular(a=val_a, b=val_b)  # Usamos las variables aquí
                funcion_graficar = E

            elif seleccion == "Falsa Posición":
                def E(x):
                    return x ** 3 - 6 * x ** 2 + 11 * x - 6.5

                metodo = FalsaPosicion(funcion=E, tolerancia=1e-7)
                resultado = metodo.calcular(a=val_a, b=val_b)  # Y aquí
                funcion_graficar = E

            elif seleccion == "Punto Fijo":
                from metodos.punto_fijo import PuntoFijo
                def g(x):
                    return 0.5 * math.cos(x) + 1.5

                metodo = PuntoFijo(funcion_g=g, tolerancia=1e-8)
                # Para Punto Fijo solo necesitamos x0, que lo leemos del primer cuadro (val_a)
                resultado = metodo.calcular(x0=val_a)
                funcion_graficar = g

            elif seleccion == "Newton-Raphson":
                from metodos.newton import NewtonRaphson
                import sympy as sp

                # 1. Definimos la variable y la función de concurrencia simbólicamente
                x_sym = sp.Symbol('x')
                T_sym = x_sym ** 3 - 8 * x_sym ** 2 + 20 * x_sym - 16

                # 2. SymPy calcula la derivada exacta automáticamente
                dT_sym = sp.diff(T_sym, x_sym)

                # 3. Convertimos (lambdify) las fórmulas simbólicas a funciones de Python ejecutables por NumPy
                T_func = sp.lambdify(x_sym, T_sym, 'numpy')
                dT_func = sp.lambdify(x_sym, dT_sym, 'numpy')

                # 4. Instanciamos nuestra clase inyectando ambas funciones
                metodo = NewtonRaphson(funcion=T_func, derivada=dT_func, tolerancia=1e-10)
                resultado = metodo.calcular(x0=val_a)
                funcion_graficar = T_func
                # ... (código anterior de Newton-Raphson) ...
            elif seleccion == "Secante":
                from metodos.secante import Secante
                import numpy as np

                # Función financiera P(x)
                def P(x):
                    return x * np.exp(-x / 2) - 0.3

                # Instanciamos la clase de la Secante
                metodo = Secante(funcion=P, tolerancia=1e-9)

                # OJO: La secante requiere dos valores iniciales (val_a = 0.5, val_b = 1.0)
                resultado = metodo.calcular(x0=val_a, x1=val_b)
                funcion_graficar = P


            else:
                messagebox.showinfo("En desarrollo", f"El método {seleccion} se implementará pronto.")
                return

            # Limpiamos datos anteriores de la tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Llenamos la tabla
            for fila in resultado['historial']:
                self.tabla.insert("", "end", values=(
                    fila['n'],
                    f"{fila['c']:.8f}",
                    f"{fila['f(c)']:.8f}",  # Para punto fijo esto es g(x_n)
                    f"{fila['error_absoluto']:.8e}",
                    f"{fila['error_relativo']:.8f}"
                ))

            # Mostramos el resultado y decidimos qué gráfica dibujar
            if resultado['exito']:
                messagebox.showinfo("Convergencia Exitosa",
                                    f"Raíz: {resultado['raiz']:.8f}\nIteraciones: {resultado['iteraciones_totales']}")

                if seleccion == "Punto Fijo":
                    self.graficar_telaraña(funcion_graficar, resultado['historial'])
                elif seleccion == "Newton-Raphson":
                    self.graficar_newton(funcion_graficar, resultado['historial'])
                elif seleccion == "Secante":
                    self.graficar_secante(funcion_graficar, resultado['historial'])
                else:
                    self.graficar_funcion(funcion_graficar, val_a, val_b, resultado['raiz'])
            else:
                messagebox.showwarning("Aviso", resultado['mensaje'])

        except Exception as e:
            messagebox.showerror("Error de Cálculo", f"Se produjo un error: {str(e)}")

    def ejecutar_comparacion(self):
        """Ejecuta ambos métodos simultáneamente para el análisis del Ejercicio 2."""

        def E(x):
            return x ** 3 - 6 * x ** 2 + 11 * x - 6.5

        # Instanciamos ambos métodos con las mismas condiciones iniciales
        metodo_bis = Biseccion(funcion=E, tolerancia=1e-7)
        metodo_fp = FalsaPosicion(funcion=E, tolerancia=1e-7)

        try:
            res_bis = metodo_bis.calcular(a=2.0, b=4.0)
            res_fp = metodo_fp.calcular(a=2.0, b=4.0)

            # Mostrar un resumen rápido en pantalla
            mensaje = (
                f"RESULTADOS DEL BALANCEO DE CARGA:\n\n"
                f"Bisección:\nRaíz: {res_bis['raiz']:.8f} | Iteraciones: {res_bis['iteraciones_totales']}\n\n"
                f"Falsa Posición:\nRaíz: {res_fp['raiz']:.8f} | Iteraciones: {res_fp['iteraciones_totales']}"
            )
            messagebox.showinfo("Comparación Completada", mensaje)

            # Llamamos a la función que dibujará la gráfica superpuesta
            self.graficar_comparacion(res_bis['historial'], res_fp['historial'])

        except Exception as e:
            messagebox.showerror("Error", f"Error en la comparación: {str(e)}")

    def graficar_comparacion(self, hist_bis, hist_fp):
        """Dibuja la gráfica superpuesta del error absoluto en escala logarítmica."""
        self.ax.clear()

        # Extraer datos de iteraciones (Eje X) y errores (Eje Y) para Bisección [cite: 178, 179]
        n_bis = [fila['n'] for fila in hist_bis]
        err_bis = [fila['error_absoluto'] for fila in hist_bis if fila['error_absoluto'] > 0]
        n_bis = n_bis[:len(err_bis)]  # Ajustar longitud por si el error llega a 0 exacto

        # Extraer datos para Falsa Posición
        n_fp = [fila['n'] for fila in hist_fp]
        err_fp = [fila['error_absoluto'] for fila in hist_fp if fila['error_absoluto'] > 0]
        n_fp = n_fp[:len(err_fp)]

        # Trazar ambas líneas
        self.ax.plot(n_bis, err_bis, label="Bisección", color="blue", marker='o', linestyle='-')
        self.ax.plot(n_fp, err_fp, label="Falsa Posición", color="red", marker='x', linestyle='--')

        # Configuración visual para análisis de convergencia
        self.ax.set_yscale('log')  # Escala logarítmica exigida [cite: 179]
        self.ax.set_title("Convergencia del Error: Bisección vs Falsa Posición")
        self.ax.set_xlabel("Número de Iteración (n) [cite: 178]")
        self.ax.set_ylabel("Error Absoluto (escala logarítmica) [cite: 179]")
        self.ax.legend()
        self.ax.grid(True, which="both", ls="--", alpha=0.5)

        self.canvas.draw()

    def graficar_telaraña(self, funcion_g, historial):
        """Dibuja el diagrama de telaraña (cobweb plot) para el Punto Fijo."""
        self.ax.clear()

        # 1. Definir el rango de la gráfica basado en los puntos visitados
        puntos_x = [fila['c'] for fila in historial]
        min_x, max_x = min(puntos_x) - 0.5, max(puntos_x) + 0.5
        x_vals = np.linspace(min_x, max_x, 400)

        # 2. Trazar y = g(x) y la línea de identidad y = x
        y_vals = [funcion_g(x) for x in x_vals]
        self.ax.plot(x_vals, y_vals, label="y = g(x)", color="blue")
        self.ax.plot(x_vals, x_vals, label="y = x", color="gray", linestyle="--")

        # 3. Trazar la ruta de la telaraña (segmentos)
        for i in range(len(historial) - 1):
            x_n = historial[i]['c']
            y_n = historial[i]['f(c)']  # que es g(x_n)

            # Línea vertical desde (x_n, x_n) hasta (x_n, g(x_n))
            if i == 0:
                self.ax.plot([x_n, x_n], [0, y_n], color="red", alpha=0.6)  # Primera línea desde el eje x
            else:
                self.ax.plot([x_n, x_n], [x_n, y_n], color="red", alpha=0.6)

            # Línea horizontal desde (x_n, g(x_n)) hasta (g(x_n), g(x_n))
            self.ax.plot([x_n, y_n], [y_n, y_n], color="red", alpha=0.6)

            # Marcar el punto en la curva
            self.ax.plot(x_n, y_n, 'ro', markersize=4)

        # Configuraciones visuales
        self.ax.set_title("Diagrama de Telaraña - Crecimiento de Base de Datos")
        self.ax.set_xlabel("Meses (x)")
        self.ax.set_ylabel("g(x)")
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

    def graficar_newton(self, funcion, historial):
        """Dibuja la función y las rectas tangentes del método de Newton-Raphson."""
        self.ax.clear()

        # Generar rango dinámico para el eje X
        puntos_x = [fila['c'] for fila in historial]
        min_x, max_x = min(puntos_x) - 1.5, max(puntos_x) + 1.5
        x_vals = np.linspace(min_x, max_x, 400)
        y_vals = funcion(x_vals)

        # Trazar la curva principal T(n)
        self.ax.plot(x_vals, y_vals, label="T(n) = n³ - 8n² + 20n - 16", color="blue", linewidth=2)
        self.ax.axhline(0, color="black", linewidth=1, linestyle="--")

        # Dibujar las rectas tangentes de cada iteración
        for i, fila in enumerate(historial):
            x_n = fila['c']
            y_n = fila['f(c)']
            m = fila['f_prima(c)']  # La derivada evaluada actúa como pendiente

            # Ecuación de la recta tangente despejada: y = m * (x - x_n) + y_n
            y_tangente = m * (x_vals - x_n) + y_n

            # Dibujamos la tangente (línea punteada) y el punto de toque
            self.ax.plot(x_vals, y_tangente, linestyle=":", alpha=0.6, label=f"Iteración {i + 1}")
            self.ax.plot(x_n, y_n, 'ro', markersize=4)

            # Marcar la raíz final calculada
        if historial:
            ultima_raiz = historial[-1]['c'] - (historial[-1]['f(c)'] / historial[-1]['f_prima(c)'])
            self.ax.plot(ultima_raiz, 0, 'go', markersize=6, label=f"Raíz: {ultima_raiz:.5f}")

        # Configuraciones visuales
        self.ax.set_title("Análisis de Concurrencia - Newton-Raphson")
        self.ax.set_xlabel("Número de Threads (n)")
        self.ax.set_ylabel("Tiempo T(n)")

        # Limitar la vista en Y para que las tangentes lejanas no deformen la gráfica
        y_min, y_max = min(y_vals) - 5, max(y_vals) + 5
        self.ax.set_ylim([y_min, y_max])

        self.ax.legend(loc='best', fontsize='small')
        self.ax.grid(True)
        self.canvas.draw()

    def graficar_secante(self, funcion, historial):
        """Dibuja la función P(x) y las rectas secantes del Ejercicio 5."""
        self.ax.clear()

        # Generar rango dinámico para el eje X
        puntos_x = [fila['c'] for fila in historial] + [historial[0]['x_n-1']]
        min_x, max_x = min(puntos_x) - 1.0, max(puntos_x) + 2.0
        x_vals = np.linspace(min_x, max_x, 400)
        y_vals = funcion(x_vals)

        # Trazar la curva principal P(x)
        self.ax.plot(x_vals, y_vals, label="P(x) = x*e^(-x/2) - 0.3", color="blue", linewidth=2)
        self.ax.axhline(0, color="black", linewidth=1, linestyle="--")

        # Dibujar las rectas secantes de cada iteración
        for i, fila in enumerate(historial):
            x0 = fila['x_n-1']
            fx0 = fila['f(x_n-1)']
            x1 = fila['c']
            fx1 = fila['f(c)']

            # Ecuación de la recta que pasa por dos puntos
            if fx1 - fx0 != 0:
                m = (fx1 - fx0) / (x1 - x0)
                y_secante = m * (x_vals - x1) + fx1

                # Dibujamos la secante (línea punteada) y los puntos
                self.ax.plot(x_vals, y_secante, linestyle=":", alpha=0.6)
                self.ax.plot([x0, x1], [fx0, fx1], 'ro', markersize=4)

                # Marcar la raíz final calculada
        if historial:
            ultima_raiz = historial[-1]['x_n+1']
            self.ax.plot(ultima_raiz, 0, 'go', markersize=6, label=f"Raíz: {ultima_raiz:.5f}")

        # Configuraciones visuales
        self.ax.set_title("Predicción de Escalabilidad - Método de la Secante")
        self.ax.set_xlabel("Miles de Usuarios Activos (x)")
        self.ax.set_ylabel("Rentabilidad P(x)")

        # Limitar la vista en Y para mayor claridad
        self.ax.set_ylim([min(y_vals) - 0.2, max(y_vals) + 0.2])
        self.ax.legend(loc='best', fontsize='small')
        self.ax.grid(True)
        self.canvas.draw()

    def ejecutar_comparacion_ej5(self):
        """Ejecuta Secante y Newton-Raphson para el Ejercicio 5 y compara su eficiencia."""
        import numpy as np
        import time
        from metodos.newton import NewtonRaphson
        from metodos.secante import Secante

        # 1. Definimos la función y su derivada analítica estricta
        def P(x):
            return x * np.exp(-x / 2) - 0.3

        def dP(x):
            return np.exp(-x / 2) * (1 - x / 2)

        # 2. Instanciamos ambos métodos con la tolerancia exigida de 10^-9
        metodo_nr = NewtonRaphson(funcion=P, derivada=dP, tolerancia=1e-9)
        metodo_sec = Secante(funcion=P, tolerancia=1e-9)

        try:
            # --- MEDIR NEWTON-RAPHSON ---
            inicio_nr = time.perf_counter()
            res_nr = metodo_nr.calcular(x0=0.5)
            fin_nr = time.perf_counter()
            tiempo_nr = fin_nr - inicio_nr

            # En NR evaluamos f(x) y f'(x) en cada ciclo.
            # Total de evaluaciones = iteraciones * 2
            eval_nr = res_nr['iteraciones_totales'] * 2

            # --- MEDIR SECANTE ---
            inicio_sec = time.perf_counter()
            res_sec = metodo_sec.calcular(x0=0.5, x1=1.0)
            fin_sec = time.perf_counter()
            tiempo_sec = fin_sec - inicio_sec

            # 3. Construimos la tabla comparativa final para la interfaz
            mensaje = (
                "TABLA COMPARATIVA: SECANTE VS NEWTON-RAPHSON\n"
                "--------------------------------------------------\n"
                f"MÉTODO DE LA SECANTE:\n"
                f"- Raíz encontrada: {res_sec['raiz']:.9f}\n"
                f"- Número de Iteraciones: {res_sec['iteraciones_totales']}\n"
                f"- Evaluaciones de función: {res_sec['evaluaciones']}\n"
                f"- Tiempo computacional: {tiempo_sec:.6f} segundos\n\n"
                f"MÉTODO NEWTON-RAPHSON:\n"
                f"- Raíz encontrada: {res_nr['raiz']:.9f}\n"
                f"- Número de Iteraciones: {res_nr['iteraciones_totales']}\n"
                f"- Evaluaciones de función: {eval_nr}\n"
                f"- Tiempo computacional: {tiempo_nr:.6f} segundos\n"
                "--------------------------------------------------\n"
                "Análisis: Esto te ayudará a responder si vale la pena el costo "
                "de calcular derivadas analíticas para este problema."
            )

            messagebox.showinfo("Análisis de Escalabilidad (Ejercicio 5)", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error en la comparación: {str(e)}")