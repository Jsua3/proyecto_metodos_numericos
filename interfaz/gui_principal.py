import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from interfaz.graficas import GraficadorDinamico
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
        """Inicializa el graficador dinámico en el panel inferior."""
        self.frame_grafica = ttk.LabelFrame(self, text="  Visualización Dinámica y Convergencia  ")
        self.frame_grafica.pack(fill="both", expand=True, padx=10, pady=5)

        # Usar la nueva clase de graficación
        self.graficador = GraficadorDinamico(self.frame_grafica)


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
                from metodos.newton_raphson import NewtonRaphson
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
                self.graficador.graficar_metodo(seleccion, funcion_graficar, resultado['historial'], resultado['raiz'])
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
            self.graficador.graficar_comparacion("Bisección vs Falsa Posición", 
                                              res_bis['historial'], "Bisección", 
                                              res_fp['historial'], "Falsa Posición")

        except Exception as e:
            messagebox.showerror("Error", f"Error en la comparación: {str(e)}")


    def ejecutar_comparacion_ej5(self):
        """Ejecuta Secante y Newton-Raphson para el Ejercicio 5 y compara su eficiencia."""
        import numpy as np
        import time
        from metodos.newton_raphson import NewtonRaphson
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

            # Graficamos la comparación de convergencia
            self.graficador.graficar_comparacion("Secante vs Newton-Raphson", 
                                              res_sec['historial'], "Secante", 
                                              res_nr['historial'], "Newton-Raphson")

        except Exception as e:
            messagebox.showerror("Error", f"Error en la comparación: {str(e)}")