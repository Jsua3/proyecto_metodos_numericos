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
        self.title("Métodos Numéricos - Ingeniería de Software")
        self.geometry("1200x850")
        self.configure(bg="#0b0b14")

        # --- EFECTOS DE TRANSPARENCIA ---
        self.attributes('-alpha', 0.0)
        self.aparecer_paulatinamente()
        # ---------------------------------

        self.configurar_estilos()

        # Layout principal: Sidebar y Contenido
        self.sidebar = tk.Frame(self, bg="#12121e", width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.contenedor_principal = tk.Frame(self, bg="#0b0b14")
        self.contenedor_principal.pack(side="right", fill="both", expand=True)

        self.crear_sidebar_content()
        self.crear_main_content()

    def configurar_estilos(self):
        """Aplica un tema oscuro premium estilo imagen."""
        self.estilo = ttk.Style()
        if 'clam' in self.estilo.theme_names():
            self.estilo.theme_use('clam')

        bg_dark = "#12121e"
        accent_blue = "#3a5aff"
        accent_green = "#00ff88"
        text_white = "#ffffff"
        text_gray = "#a9b7c6"

        self.estilo.configure("TLabel", font=("Segoe UI", 10), background=bg_dark, foreground=text_white)
        self.estilo.configure("Sidebar.TLabel", font=("Segoe UI", 9, "bold"), background=bg_dark, foreground=text_gray)
        
        # Botones personalizados
        self.estilo.configure("Calcular.TButton", font=("Segoe UI", 10, "bold"), background=accent_blue, foreground="white")
        self.estilo.map("Calcular.TButton", background=[('active', '#2d4acc')])
        
        self.estilo.configure("Limpiar.TButton", font=("Segoe UI", 10, "bold"), background="#333333", foreground="white")
        self.estilo.map("Limpiar.TButton", background=[('active', '#444444')])

        self.estilo.configure("Treeview", font=("Consolas", 9), rowheight=25, background="#0b0b14", 
                              fieldbackground="#0b0b14", foreground=text_gray)
        self.estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#1a1a2e", foreground=accent_blue)

        self.estilo.configure("TCheckbutton", background=bg_dark, foreground=text_white, font=("Segoe UI", 9))

    def crear_sidebar_content(self):
        """Construye el contenido de la barra lateral izquierda."""
        padding = {"padx": 20, "pady": 5}
        
        # Título del software
        tk.Label(self.sidebar, text="Seleccione el Método / Ejercicio:", bg="#12121e", fg="white", 
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", **padding, pady=(20, 5))
        
        self.combo_metodo = ttk.Combobox(self.sidebar, values=["Bisección", "Falsa Posición", "Punto Fijo", "Newton-Raphson", "Secante"], state="readonly")
        self.combo_metodo.pack(fill="x", **padding)
        self.combo_metodo.current(2) # Punto Fijo por defecto como en la imagen

        # Panel de Parámetros
        frame_params = tk.LabelFrame(self.sidebar, text=" Parámetros de entrada ", bg="#12121e", fg="#3a5aff", font=("Segoe UI", 9, "bold"), bd=1, relief="flat")
        frame_params.pack(fill="x", **padding, pady=15)

        tk.Label(frame_params, text="Función f(x) / g(x):", bg="#12121e", fg="#a9b7c6", font=("Segoe UI", 8)).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_func = tk.Entry(frame_params, bg="#1a1a2e", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333333")
        self.entry_func.insert(0, "0.5 * np.cos(x) + 1.5")
        self.entry_func.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_params, text="Valor inicial (x0 / a):", bg="#12121e", fg="#a9b7c6", font=("Segoe UI", 8)).pack(anchor="w", padx=10)
        self.entry_a = tk.Entry(frame_params, bg="#1a1a2e", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333333")
        self.entry_a.insert(0, "1.0")
        self.entry_a.pack(fill="x", padx=10, pady=5)

        self.var_comparar = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_params, text="Comparar x0 (0.5, 1.0, 1.5, 2.0)", variable=self.var_comparar).pack(anchor="w", padx=10, pady=5)

        tk.Label(frame_params, text="Tolerancia:", bg="#12121e", fg="#a9b7c6", font=("Segoe UI", 8)).pack(anchor="w", padx=10)
        self.entry_tol = tk.Entry(frame_params, bg="#1a1a2e", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333333")
        self.entry_tol.insert(0, "1e-8")
        self.entry_tol.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_params, text="Máx. Iteraciones:", bg="#12121e", fg="#a9b7c6", font=("Segoe UI", 8)).pack(anchor="w", padx=10)
        self.entry_max_iter = tk.Entry(frame_params, bg="#1a1a2e", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#333333")
        self.entry_max_iter.insert(0, "100")
        self.entry_max_iter.pack(fill="x", padx=10, pady=(5, 15))

        # Checkboxes de visualización
        self.var_grafica = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="Mostrar Gráfica Principal", variable=self.var_grafica).pack(anchor="w", **padding)
        self.var_conv = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="Mostrar Convergencia (Log)", variable=self.var_conv).pack(anchor="w", **padding)
        self.var_tabla = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="Mostrar Tabla", variable=self.var_tabla).pack(anchor="w", **padding)

        # Botones
        frame_btns = tk.Frame(self.sidebar, bg="#12121e")
        frame_btns.pack(fill="x", **padding, pady=20)
        ttk.Button(frame_btns, text="▶ Calcular", style="Calcular.TButton", command=self.ejecutar_calculo).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(frame_btns, text="Limpiar", style="Limpiar.TButton", command=self.limpiar_todo).pack(side="left", expand=True, fill="x")

        # Resultado Final
        self.frame_res = tk.LabelFrame(self.sidebar, text=" Resultado Final ", bg="#12121e", fg="#00ff88", font=("Segoe UI", 9, "bold"), bd=1, relief="flat")
        self.frame_res.pack(fill="both", expand=True, **padding, pady=(0, 20))
        
        self.lbl_res_final = tk.Label(self.frame_res, text="Esperando cálculo...", bg="#12121e", fg="#00ff88", 
                                     font=("Consolas", 9, "bold"), justify="left", anchor="nw")
        self.lbl_res_final.pack(fill="both", expand=True, padx=10, pady=10)

    def crear_main_content(self):
        """Panel derecho con gráficas arriba y tabla abajo."""
        # Contenedor de gráficas
        self.frame_grafica = tk.Frame(self.contenedor_principal, bg="#0b0b14")
        self.frame_grafica.pack(fill="both", expand=True, padx=10, pady=5)
        self.graficador = GraficadorDinamico(self.frame_grafica)

        # Contenedor de tabla
        self.frame_tabla_container = tk.Frame(self.contenedor_principal, bg="#0b0b14", height=250)
        self.frame_tabla_container.pack(fill="x", side="bottom", padx=10, pady=10)
        self.frame_tabla_container.pack_propagate(False)

        columnas = ("n", "x_n", "f(x_n)", "Error Abs", "Error Rel (%)")
        self.tabla = ttk.Treeview(self.frame_tabla_container, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")
        
        # Scrollbar para la tabla
        scrolly = ttk.Scrollbar(self.frame_tabla_container, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrolly.set)
        scrolly.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)

    def limpiar_todo(self):
        self.graficador.limpiar()
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.lbl_res_final.config(text="Esperando cálculo...")

    def ejecutar_calculo(self):
        """Ejecuta el cálculo manejando la comparación de x0 si está activa."""
        import time
        metodo_nombre = self.combo_metodo.get()
        func_str = self.entry_func.get()
        tol = float(self.entry_tol.get())
        max_iter = int(self.entry_max_iter.get())
        
        try:
            # Crear función segura usando numpy
            def f_eval(x):
                return eval(func_str, {"np": np, "math": np, "x": x})

            resultados = []
            x0_list = [float(self.entry_a.get())]
            if self.var_comparar.get():
                x0_list = [0.5, 1.0, 1.5, 2.0]

            mejor_resultado = None
            min_iter = float('inf')

            for x0 in x0_list:
                start_t = time.perf_counter()
                if metodo_nombre == "Punto Fijo":
                    from metodos.punto_fijo import PuntoFijo
                    m = PuntoFijo(f_eval, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(x0=x0)
                elif metodo_nombre == "Newton-Raphson":
                    from metodos.newton_raphson import NewtonRaphson
                    import sympy as sp
                    x_s = sp.Symbol('x')
                    f_s = eval(func_str.replace("np.", "sp.").replace("math.", "sp."), {"sp": sp, "x": x_s})
                    df_s = sp.diff(f_s, x_s)
                    f_n = sp.lambdify(x_s, f_s, 'numpy')
                    df_n = sp.lambdify(x_s, df_s, 'numpy')
                    m = NewtonRaphson(f_n, df_n, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(x0=x0)
                elif metodo_nombre == "Bisección":
                    from metodos.biseccion import Biseccion
                    # Bisección necesita un intervalo, si x0 es el inicio, usamos x0 + 1 como b por defecto si no hay b
                    m = Biseccion(f_eval, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(a=x0, b=x0 + 2) # Ajuste simple
                else:
                    # Otros métodos...
                    res = {'exito': False, 'mensaje': "No implementado para comparación"}
                
                end_t = time.perf_counter()
                res['tiempo_ms'] = (end_t - start_t) * 1000
                res['x0_inicial'] = x0
                resultados.append(res)
                
                if res['exito'] and res['iteraciones_totales'] < min_iter:
                    min_iter = res['iteraciones_totales']
                    mejor_resultado = res

            # Llenar tabla con el primero o el mejor
            for item in self.tabla.get_children(): self.tabla.delete(item)
            res_to_show = mejor_resultado if mejor_resultado else resultados[0]
            for fila in res_to_show['historial']:
                self.tabla.insert("", "end", values=(fila['n'], f"{fila['c']:.6f}", f"{fila['f(c)']:.6f}", f"{fila['error_absoluto']:.2e}", f"{fila['error_relativo']:.4f}"))

            # Graficar
            historias = [r['historial'] for r in resultados if r['exito']]
            if historias:
                self.graficador.graficar_metodo(metodo_nombre, f_eval, historias if self.var_comparar.get() else historias[0], res_to_show['raiz'])

            # Mostrar resultado final en sidebar
            if mejor_resultado:
                txt = (f"🚀 MÁS RÁPIDO: x0 = {mejor_resultado['x0_inicial']}\n"
                       f"RAÍZ: {mejor_resultado['raiz']:.8f}\n"
                       f"ITERACIONES: {mejor_resultado['iteraciones_totales']}\n"
                       f"ERROR: {mejor_resultado['historial'][-1]['error_absoluto']:.2e}\n"
                       f"TIEMPO: {mejor_resultado['tiempo_ms']:.2f} ms")
                self.lbl_res_final.config(text=txt)
            else:
                self.lbl_res_final.config(text="No hubo convergencia.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

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