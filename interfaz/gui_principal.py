import tkinter as tk
from tkinter import ttk
import numpy as np
from interfaz.graficas import GraficadorDinamico
from interfaz.mensajes import MensajePersonalizado
from metodos.falsa_posicion import FalsaPosicion
from metodos.biseccion import Biseccion


class VentanaPrincipal(tk.Tk):
    """
    Clase principal que construye y gestiona la Interfaz Gráfica de Usuario (GUI).
    """

    METODOS_CONFIG = {
        "Bisección": {
            "func": "x**3 - x - 2",
            "a": "1.0",
            "b": "2.0",
            "lbl_a": "Límite inferior (a):",
            "lbl_b": "Límite superior (b):",
            "show_b": True,
            "can_compare": False
        },
        "Falsa Posición": {
            "func": "x**3 - x - 2",
            "a": "1.0",
            "b": "2.0",
            "lbl_a": "Límite inferior (a):",
            "lbl_b": "Límite superior (b):",
            "show_b": True,
            "can_compare": False
        },
        "Punto Fijo": {
            "func": "0.5 * np.cos(x) + 1.5",
            "a": "1.0",
            "lbl_a": "Punto inicial (x0):",
            "show_b": False,
            "can_compare": True
        },
        "Newton-Raphson": {
            "func": "x**2 - 2",
            "a": "1.5",
            "lbl_a": "Punto inicial (x0):",
            "show_b": False,
            "can_compare": True
        },
        "Secante": {
            "func": "x**2 - 2",
            "a": "1.0",
            "b": "2.0",
            "lbl_a": "Punto inicial 0 (x0):",
            "lbl_b": "Punto inicial 1 (x1):",
            "show_b": True,
            "can_compare": False
        }
    }

    TEMAS = {
        "Oscuro": {
            "bg_main": "#0b0b14",
            "bg_sidebar": "#12121e",
            "text_main": "#ffffff",
            "text_sidebar": "#a9b7c6",
            "accent_blue": "#3a5aff",
            "accent_green": "#00ff88",
            "entry_bg": "#1a1a2e",
            "entry_fg": "white",
            "border_color": "#333333",
            "tree_bg": "#0b0b14",
            "tree_fg": "#a9b7c6",
            "tree_heading_bg": "#1a1a2e",
            "btn_calc_bg": "#00ff88",
            "btn_calc_fg": "#0b0b14",
            "btn_calc_hover": "#00cc6e",
            "btn_clear_bg": "#2d2d3d",
            "btn_clear_fg": "#ffffff",
            "btn_clear_hover": "#3d3d4d"
        },
        "Claro": {
            "bg_main": "#fdfdfd",
            "bg_sidebar": "#f0f0f0",
            "text_main": "#1a1a1a",
            "text_sidebar": "#444444",
            "accent_blue": "#0056b3",
            "accent_green": "#218838",
            "entry_bg": "#ffffff",
            "entry_fg": "#333333",
            "border_color": "#cccccc",
            "tree_bg": "#ffffff",
            "tree_fg": "#333333",
            "tree_heading_bg": "#e0e0e0",
            "btn_calc_bg": "#218838",
            "btn_calc_fg": "#ffffff",
            "btn_calc_hover": "#1e7e34",
            "btn_clear_bg": "#6c757d",
            "btn_clear_fg": "#ffffff",
            "btn_clear_hover": "#5a6268"
        }
    }

    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos - Ingeniería de Software")
        self.geometry("1200x850")
        
        self.tema_actual = "Oscuro"
        self.configure(bg=self.TEMAS[self.tema_actual]["bg_main"])

        # --- EFECTOS DE TRANSPARENCIA ---
        self.attributes('-alpha', 0.0)
        self.aparecer_paulatinamente()
        # ---------------------------------

        self.configurar_estilos()

        # Layout principal: Sidebar y Contenido
        tema = self.TEMAS[self.tema_actual]
        self.sidebar = tk.Frame(self, bg=tema["bg_sidebar"], width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.contenedor_principal = tk.Frame(self, bg=tema["bg_main"])
        self.contenedor_principal.pack(side="right", fill="both", expand=True)

        self.crear_sidebar_content()
        self.crear_main_content()

    def configurar_estilos(self):
        """Aplica estilos basados en el tema actual."""
        tema = self.TEMAS[self.tema_actual]
        self.estilo = ttk.Style()
        if 'clam' in self.estilo.theme_names():
            self.estilo.theme_use('clam')

        self.estilo.configure("TLabel", font=("Segoe UI", 10), background=tema["bg_sidebar"], foreground=tema["text_main"])
        self.estilo.configure("Sidebar.TLabel", font=("Segoe UI", 9, "bold"), background=tema["bg_sidebar"], foreground=tema["text_sidebar"])
        
        self.estilo.configure("Treeview", font=("Consolas", 9), rowheight=25, background=tema["tree_bg"], 
                              fieldbackground=tema["tree_bg"], foreground=tema["tree_fg"])
        self.estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background=tema["tree_heading_bg"], foreground=tema["accent_blue"])

        self.estilo.configure("TCheckbutton", background=tema["bg_sidebar"], foreground=tema["text_main"], font=("Segoe UI", 9))
        
        # Estilo para el ComboBox
        self.estilo.configure("TCombobox", fieldbackground=tema["entry_bg"], background=tema["bg_sidebar"], foreground=tema["text_main"])

    def configurar_boton_interactivo(self, btn, bg, hover_bg, fg):
        """Añade efectos de hover y cursor a un botón estándar de tkinter."""
        btn.configure(bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))

    def crear_sidebar_content(self):
        """Construye el contenido de la barra lateral izquierda con botones intuitivos."""
        padding = {"padx": 20, "pady": 5}
        tema = self.TEMAS[self.tema_actual]
        
        # Botón de cambio de tema (Modernizado)
        self.btn_tema = tk.Button(self.sidebar, text="🌙 Modo Oscuro" if self.tema_actual == "Oscuro" else "☀️ Modo Claro",
                                  font=("Segoe UI", 8, "bold"), command=self.alternar_tema, bd=0, padx=10, pady=5)
        self.configurar_boton_interactivo(self.btn_tema, tema["btn_clear_bg"], tema["btn_clear_hover"], tema["btn_clear_fg"])
        self.btn_tema.pack(anchor="ne", padx=10, pady=10)

        # Título del software
        self.lbl_metodo_titulo = tk.Label(self.sidebar, text="Seleccione el Método / Ejercicio:", bg=tema["bg_sidebar"], fg=tema["text_main"], 
                 font=("Segoe UI", 10, "bold"))
        self.lbl_metodo_titulo.pack(anchor="w", padx=20, pady=(5, 5))
        
        self.combo_metodo = ttk.Combobox(self.sidebar, values=["Bisección", "Falsa Posición", "Punto Fijo", "Newton-Raphson", "Secante"], state="readonly")
        self.combo_metodo.pack(fill="x", **padding)
        self.combo_metodo.bind("<<ComboboxSelected>>", self.actualizar_campos_metodo)

        # Panel de Parámetros
        self.frame_params = tk.LabelFrame(self.sidebar, text=" Parámetros de entrada ", bg=tema["bg_sidebar"], fg=tema["accent_blue"], font=("Segoe UI", 9, "bold"), bd=1, relief="flat")
        self.frame_params.pack(fill="x", padx=20, pady=15)

        self.lbl_func = tk.Label(self.frame_params, text="Función f(x) / g(x):", bg=tema["bg_sidebar"], fg=tema["text_sidebar"], font=("Segoe UI", 8))
        self.lbl_func.pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_func = tk.Entry(self.frame_params, bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], bd=0, highlightthickness=1, highlightbackground=tema["border_color"])
        self.entry_func.insert(0, "0.5 * np.cos(x) + 1.5")
        self.entry_func.pack(fill="x", padx=10, pady=5)

        self.lbl_a = tk.Label(self.frame_params, text="Valor inicial (x0 / a):", bg=tema["bg_sidebar"], fg=tema["text_sidebar"], font=("Segoe UI", 8))
        self.lbl_a.pack(anchor="w", padx=10)
        self.entry_a = tk.Entry(self.frame_params, bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], bd=0, highlightthickness=1, highlightbackground=tema["border_color"])
        self.entry_a.pack(fill="x", padx=10, pady=5)

        self.lbl_b = tk.Label(self.frame_params, text="Límite superior (b):", bg=tema["bg_sidebar"], fg=tema["text_sidebar"], font=("Segoe UI", 8))
        self.entry_b = tk.Entry(self.frame_params, bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], bd=0, highlightthickness=1, highlightbackground=tema["border_color"])

        self.var_comparar = tk.BooleanVar(value=True)
        self.chk_comparar = ttk.Checkbutton(self.frame_params, text="Comparar x0 (0.5, 1.0, 1.5, 2.0)", variable=self.var_comparar)
        self.chk_comparar.pack(anchor="w", padx=10, pady=5)

        self.lbl_tol = tk.Label(self.frame_params, text="Tolerancia:", bg=tema["bg_sidebar"], fg=tema["text_sidebar"], font=("Segoe UI", 8))
        self.lbl_tol.pack(anchor="w", padx=10)
        self.entry_tol = tk.Entry(self.frame_params, bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], bd=0, highlightthickness=1, highlightbackground=tema["border_color"])
        self.entry_tol.insert(0, "1e-8")
        self.entry_tol.pack(fill="x", padx=10, pady=5)

        self.lbl_max_iter = tk.Label(self.frame_params, text="Máx. Iteraciones:", bg=tema["bg_sidebar"], fg=tema["text_sidebar"], font=("Segoe UI", 8))
        self.lbl_max_iter.pack(anchor="w", padx=10)
        self.entry_max_iter = tk.Entry(self.frame_params, bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], bd=0, highlightthickness=1, highlightbackground=tema["border_color"])
        self.entry_max_iter.insert(0, "100")
        self.entry_max_iter.pack(fill="x", padx=10, pady=(5, 15))

        # Checkboxes de visualización
        self.var_grafica = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="Mostrar Gráfica Principal", variable=self.var_grafica).pack(anchor="w", **padding)
        self.var_conv = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="Mostrar Convergencia (Log)", variable=self.var_conv).pack(anchor="w", **padding)
        self.var_tabla = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.sidebar, text="Mostrar Tabla", variable=self.var_tabla).pack(anchor="w", **padding)

        # Botones Principales (Modernizados con Hover)
        self.frame_btns = tk.Frame(self.sidebar, bg=tema["bg_sidebar"])
        self.frame_btns.pack(fill="x", padx=20, pady=20)
        
        self.btn_calc = tk.Button(self.frame_btns, text="▶ CALCULAR", font=("Segoe UI", 10, "bold"), 
                                 command=self.ejecutar_calculo, bd=0, pady=10)
        self.configurar_boton_interactivo(self.btn_calc, tema["btn_calc_bg"], tema["btn_calc_hover"], tema["btn_calc_fg"])
        self.btn_calc.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_clear = tk.Button(self.frame_btns, text="🗑️ LIMPIAR", font=("Segoe UI", 10, "bold"), 
                                  command=self.limpiar_todo, bd=0, pady=10)
        self.configurar_boton_interactivo(self.btn_clear, tema["btn_clear_bg"], tema["btn_clear_hover"], tema["btn_clear_fg"])
        self.btn_clear.pack(side="left", expand=True, fill="x")

        # Resultado Final
        self.frame_res = tk.LabelFrame(self.sidebar, text=" Resultado Final ", bg=tema["bg_sidebar"], fg=tema["accent_green"], font=("Segoe UI", 9, "bold"), bd=1, relief="flat")
        self.frame_res.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.lbl_res_final = tk.Label(self.frame_res, text="Esperando cálculo...", bg=tema["bg_sidebar"], fg=tema["accent_green"], 
                                     font=("Consolas", 9, "bold"), justify="left", anchor="nw")
        self.lbl_res_final.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.combo_metodo.current(2)
        self.actualizar_campos_metodo()

    def actualizar_campos_metodo(self, event=None):
        """Actualiza los valores por defecto y visibilidad de campos según el método."""
        metodo = self.combo_metodo.get()
        config = self.METODOS_CONFIG.get(metodo)
        if not config: return

        # Limpiar y establecer nuevos valores
        self.entry_func.delete(0, tk.END)
        self.entry_func.insert(0, config["func"])
        
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, config["a"])
        self.lbl_a.config(text=config["lbl_a"])

        # Control de visibilidad para 'b'
        if config["show_b"]:
            self.lbl_b.pack(anchor="w", padx=10, after=self.entry_a)
            self.entry_b.pack(fill="x", padx=10, pady=5, after=self.lbl_b)
            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, config["b"])
            self.lbl_b.config(text=config["lbl_b"])
        else:
            self.lbl_b.pack_forget()
            self.entry_b.pack_forget()

        # Control de comparación (solo para métodos de un punto)
        if config["can_compare"]:
            self.chk_comparar.pack(anchor="w", padx=10, pady=5, after=self.entry_b if config["show_b"] else self.entry_a)
        else:
            self.chk_comparar.pack_forget()

    def crear_main_content(self):
        """Panel derecho con gráficas arriba y tabla abajo."""
        tema = self.TEMAS[self.tema_actual]
        # Contenedor de gráficas
        self.frame_grafica = tk.Frame(self.contenedor_principal, bg=tema["bg_main"])
        self.frame_grafica.pack(fill="both", expand=True, padx=10, pady=5)
        self.graficador = GraficadorDinamico(self.frame_grafica)

        # Contenedor de tabla
        self.frame_tabla_container = tk.Frame(self.contenedor_principal, bg=tema["bg_main"], height=250)
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

    def aparecer_paulatinamente(self):
        """Efecto de fundido al inicio."""
        alpha = self.attributes("-alpha")
        if alpha < 0.97:
            alpha += 0.05
            self.attributes("-alpha", alpha)
            self.after(30, self.aparecer_paulatinamente)

    def alternar_tema(self):
        """Cambia entre el tema claro y oscuro."""
        self.tema_actual = "Claro" if self.tema_actual == "Oscuro" else "Oscuro"
        tema = self.TEMAS[self.tema_actual]
        
        # Actualizar colores de la ventana
        self.configure(bg=tema["bg_main"])
        self.sidebar.configure(bg=tema["bg_sidebar"])
        self.contenedor_principal.configure(bg=tema["bg_main"])
        self.frame_grafica.configure(bg=tema["bg_main"])
        self.frame_tabla_container.configure(bg=tema["bg_main"])
        
        # Actualizar widgets del sidebar
        self.btn_tema.config(text="🌙 Modo Oscuro" if self.tema_actual == "Oscuro" else "☀️ Modo Claro")
        self.configurar_boton_interactivo(self.btn_tema, tema["btn_clear_bg"], tema["btn_clear_hover"], tema["btn_clear_fg"])
        
        self.lbl_metodo_titulo.config(bg=tema["bg_sidebar"], fg=tema["text_main"])
        self.frame_params.config(bg=tema["bg_sidebar"], fg=tema["accent_blue"])
        self.lbl_func.config(bg=tema["bg_sidebar"], fg=tema["text_sidebar"])
        self.entry_func.config(bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], highlightbackground=tema["border_color"])
        self.lbl_a.config(bg=tema["bg_sidebar"], fg=tema["text_sidebar"])
        self.entry_a.config(bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], highlightbackground=tema["border_color"])
        self.lbl_b.config(bg=tema["bg_sidebar"], fg=tema["text_sidebar"])
        self.entry_b.config(bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], highlightbackground=tema["border_color"])
        self.lbl_tol.config(bg=tema["bg_sidebar"], fg=tema["text_sidebar"])
        self.entry_tol.config(bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], highlightbackground=tema["border_color"])
        self.lbl_max_iter.config(bg=tema["bg_sidebar"], fg=tema["text_sidebar"])
        self.entry_max_iter.config(bg=tema["entry_bg"], fg=tema["entry_fg"], insertbackground=tema["entry_fg"], highlightbackground=tema["border_color"])
        self.frame_btns.config(bg=tema["bg_sidebar"])
        
        # Actualizar botones interactivos
        self.configurar_boton_interactivo(self.btn_calc, tema["btn_calc_bg"], tema["btn_calc_hover"], tema["btn_calc_fg"])
        self.configurar_boton_interactivo(self.btn_clear, tema["btn_clear_bg"], tema["btn_clear_hover"], tema["btn_clear_fg"])
        
        self.frame_res.config(bg=tema["bg_sidebar"], fg=tema["accent_green"])
        self.lbl_res_final.config(bg=tema["bg_sidebar"], fg=tema["accent_green"])
        
        # Actualizar estilos ttk
        self.configurar_estilos()
        
        # Actualizar graficador
        self.graficador.set_tema(self.tema_actual)
        
        # Redibujar si hay algo graficado
        if hasattr(self, 'ultimo_redibujado') and self.ultimo_redibujado:
            func, args = self.ultimo_redibujado
            func(*args)

    def ejecutar_calculo(self):
        """Ejecuta el cálculo manejando la comparación de x0 si está activa o intervalos según el método."""
        import time
        metodo_nombre = self.combo_metodo.get()
        func_str = self.entry_func.get()
        tol = float(self.entry_tol.get())
        max_iter = int(self.entry_max_iter.get())
        config = self.METODOS_CONFIG.get(metodo_nombre)
        
        try:
            # Crear función segura usando numpy
            def f_eval(x):
                return eval(func_str, {"np": np, "math": np, "x": x})

            resultados = []
            
            # Determinar puntos iniciales
            if config["can_compare"] and self.var_comparar.get():
                puntos_a = [0.5, 1.0, 1.5, 2.0]
            else:
                puntos_a = [float(self.entry_a.get())]
            
            mejor_resultado = None
            min_iter = float('inf')

            for val_a in puntos_a:
                start_t = time.perf_counter()
                
                if metodo_nombre == "Punto Fijo":
                    from metodos.punto_fijo import PuntoFijo
                    m = PuntoFijo(f_eval, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(x0=val_a)
                elif metodo_nombre == "Newton-Raphson":
                    from metodos.newton_raphson import NewtonRaphson
                    import sympy as sp
                    x_s = sp.Symbol('x')
                    try:
                        f_s = eval(func_str.replace("np.", "sp.").replace("math.", "sp."), {"sp": sp, "x": x_s})
                        df_s = sp.diff(f_s, x_s)
                        f_n = sp.lambdify(x_s, f_s, 'numpy')
                        df_n = sp.lambdify(x_s, df_s, 'numpy')
                    except:
                        f_n = f_eval
                        df_n = lambda x: (f_eval(x + 1e-7) - f_eval(x)) / 1e-7
                    
                    m = NewtonRaphson(f_n, df_n, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(x0=val_a)
                elif metodo_nombre == "Bisección":
                    from metodos.biseccion import Biseccion
                    val_b = float(self.entry_b.get())
                    m = Biseccion(f_eval, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(a=val_a, b=val_b)
                elif metodo_nombre == "Falsa Posición":
                    from metodos.falsa_posicion import FalsaPosicion
                    val_b = float(self.entry_b.get())
                    m = FalsaPosicion(f_eval, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(a=val_a, b=val_b)
                elif metodo_nombre == "Secante":
                    from metodos.secante import Secante
                    val_b = float(self.entry_b.get())
                    m = Secante(f_eval, tolerancia=tol, max_iter=max_iter)
                    res = m.calcular(x0=val_a, x1=val_b)
                else:
                    res = {'exito': False, 'mensaje': "Método no reconocido"}
                
                end_t = time.perf_counter()
                res['tiempo_ms'] = (end_t - start_t) * 1000
                res['x0_inicial'] = val_a
                resultados.append(res)
                
                if res['exito'] and res['iteraciones_totales'] < min_iter:
                    min_iter = res['iteraciones_totales']
                    mejor_resultado = res

            if not mejor_resultado:
                mejor_resultado = resultados[0]

            for item in self.tabla.get_children(): self.tabla.delete(item)
            for fila in mejor_resultado.get('historial', []):
                self.tabla.insert("", "end", values=(fila['n'], f"{fila['c']:.6f}", f"{fila['f(c)']:.6f}", f"{fila['error_absoluto']:.2e}", f"{fila['error_relativo']:.4f}"))

            historias = [r['historial'] for r in resultados if r['exito']]
            if historias:
                if len(puntos_a) > 1:
                    data_graf = (metodo_nombre, f_eval, historias, mejor_resultado['raiz'])
                else:
                    data_graf = (metodo_nombre, f_eval, historias[0], mejor_resultado['raiz'])
                
                self.ultimo_redibujado = (self.graficador.graficar_metodo, data_graf)
                self.graficador.graficar_metodo(*data_graf)

            if mejor_resultado['exito']:
                comp_txt = f"🚀 MÁS RÁPIDO: x0 = {mejor_resultado['x0_inicial']}\n" if len(puntos_a) > 1 else ""
                txt = (f"{comp_txt}"
                       f"RAÍZ: {mejor_resultado['raiz']:.8f}\n"
                       f"ITERACIONES: {mejor_resultado['iteraciones_totales']}\n"
                       f"ERROR: {mejor_resultado['historial'][-1]['error_absoluto']:.2e}\n"
                       f"TIEMPO: {mejor_resultado['tiempo_ms']:.2f} ms")
                self.lbl_res_final.config(text=txt)
            else:
                self.lbl_res_final.config(text=f"Error: {mejor_resultado.get('mensaje', 'No convergió')}")

        except Exception as e:
            MensajePersonalizado.showerror(self, "Error", str(e), tema=self.tema_actual)

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
            MensajePersonalizado.showinfo(self, "Comparación Completada", mensaje, tema=self.tema_actual)

            # Llamamos a la función que dibujará la gráfica superpuesta
            data_graf = ("Bisección vs Falsa Posición", res_bis['historial'], "Bisección", res_fp['historial'], "Falsa Posición")
            self.ultimo_redibujado = (self.graficador.graficar_comparacion, data_graf)
            self.graficador.graficar_comparacion(*data_graf)

        except Exception as e:
            MensajePersonalizado.showerror(self, "Error", f"Error en la comparación: {str(e)}", tema=self.tema_actual)


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

            MensajePersonalizado.showinfo(self, "Análisis de Escalabilidad (Ejercicio 5)", mensaje, tema=self.tema_actual)

            # Graficamos la comparación de convergencia
            data_graf = ("Secante vs Newton-Raphson", res_sec['historial'], "Secante", res_nr['historial'], "Newton-Raphson")
            self.ultimo_redibujado = (self.graficador.graficar_comparacion, data_graf)
            self.graficador.graficar_comparacion(*data_graf)

        except Exception as e:
            MensajePersonalizado.showerror(self, "Error", f"Error en la comparación: {str(e)}", tema=self.tema_actual)