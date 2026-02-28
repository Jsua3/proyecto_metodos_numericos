import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class GraficadorDinamico:
    """
    Clase encargada del renderizado dinámico de gráficos usando Matplotlib.
    Implementa visualizaciones específicas para métodos numéricos y análisis de convergencia.
    """

    def __init__(self, frame_contenedor):
        """
        Inicializa la figura y los paneles de visualización.
        
        Args:
            frame_contenedor: El frame de Tkinter donde se incrustará el lienzo.
        """
        self.frame = frame_contenedor
        
        # Configuración de la figura con fondo extra oscuro estilo imagen
        self.figura = Figure(figsize=(10, 8), dpi=100, facecolor='#0b0b14')
        
        # Subplot 1: Panel de Función (Arriba)
        self.ax1 = self.figura.add_subplot(211)
        self.ax1.set_facecolor('#0b0b14')
        self.ax1.tick_params(colors='white', labelsize=9)
        for spine in self.ax1.spines.values():
            spine.set_color('#333333')
            
        # Subplot 2: Panel de Convergencia (Abajo)
        self.ax2 = self.figura.add_subplot(212)
        self.ax2.set_facecolor('#0b0b14')
        self.ax2.tick_params(colors='white', labelsize=9)
        for spine in self.ax2.spines.values():
            spine.set_color('#333333')
        
        self.figura.tight_layout(pad=4.0)
        
        # Integración con Tkinter
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame)
        self.widget = self.canvas.get_tk_widget()
        self.widget.pack(fill="both", expand=True)
        self.widget.configure(bg='#0b0b14')
        
        # Tooltip para hover
        self.tooltip = None
        
        # Conectar eventos de interactividad
        self.canvas.mpl_connect("scroll_event", self.on_zoom)
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)
        
        self.datos_puntos_ax2 = [] # Puntos para ax2
        self.curva_ax1 = None # Guardar referencia a la curva principal para hover

    def limpiar(self):
        """Limpia ambos paneles para un nuevo gráfico."""
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_facecolor('#0b0b14')
        self.ax2.set_facecolor('#0b0b14')
        self.datos_puntos_ax2 = []
        self.curva_ax1 = None
        if self.tooltip:
            try:
                self.tooltip.remove()
            except:
                pass
            self.tooltip = None

    def graficar_metodo(self, metodo_nombre, funcion, historial, raiz, extra_params=None):
        """
        Grafica los resultados de un método específico.
        Permite recibir una lista de historiales para comparación si es necesario.
        """
        self.limpiar()
        colores_multi = ['#66ffff', '#55ff55', '#ffaa00', '#aa66ff']
        
        # 1. Graficar en ax1 (Panel de Función)
        self.ax1.set_title(f"Convergencia - {metodo_nombre}", color='white', fontweight='bold', pad=15)
        
        # Determinar rango dinámico
        todas_x = []
        if isinstance(historial, list) and len(historial) > 0 and isinstance(historial[0], list):
            # Caso comparación de múltiples historiales
            for h_list in historial:
                for h in h_list:
                    if 'c' in h: todas_x.append(h['c'])
                    elif 'x_n' in h: todas_x.append(h['x_n'])
            es_comparacion = True
        else:
            # Caso simple
            for h in historial:
                if 'c' in h: todas_x.append(h['c'])
                elif 'x_n' in h: todas_x.append(h['x_n'])
            es_comparacion = False
            
        if not todas_x: todas_x = [raiz]
            
        min_x = min(todas_x + [raiz]) - 0.5
        max_x = max(todas_x + [raiz]) + 0.5
        
        x = np.linspace(min_x, max_x, 500)
        y = [funcion(val) for val in x]
        
        # Guardar referencia para hover
        self.curva_ax1, = self.ax1.plot(x, y, color='#6699ff', linewidth=2, label='f(x)' if metodo_nombre != "Punto Fijo" else 'y = g(x)')
        self.ax1.fill_between(x, y, 0, color='#6699ff', alpha=0.05)
        
        if metodo_nombre == "Punto Fijo":
            self.ax1.plot(x, x, color='white', linestyle='--', alpha=0.4, label='y = x')

        self.ax1.axhline(0, color='#555555', linewidth=0.8)
        
        # Dibujar puntos de convergencia
        if es_comparacion:
            self.datos_puntos_ax2 = []
            for idx, h_list in enumerate(historial):
                label_x0 = f"x0={h_list[0].get('c', h_list[0].get('x_n-1', 'x'))}" if h_list else "x0"
                color = colores_multi[idx % len(colores_multi)]
                
                # Puntos en ax1
                puntos_x = [h.get('c', h.get('x_n', 0)) for h in h_list]
                puntos_y = [funcion(px) for px in puntos_x]
                self.ax1.plot(puntos_x, puntos_y, 'o', color=color, markersize=5, alpha=0.7, label=label_x0)
                
                # Líneas en ax2
                it = [h['n'] for h in h_list]
                err = [h['error_absoluto'] for h in h_list]
                self.ax2.semilogy(it, err, 's-', color=color, markersize=4, label=label_x0, linewidth=1.5)
                self.datos_puntos_ax2.append((it, err, label_x0, color))
        else:
            # Caso simple
            puntos_x = [h.get('c', h.get('x_n', 0)) for h in historial]
            puntos_y = [funcion(px) for px in puntos_x]
            self.ax1.plot(puntos_x, puntos_y, 'o', color='#ffaa00', markersize=5, alpha=0.8)
            
            # ax2 simple
            it = [h['n'] for h in historial]
            err = [h['error_absoluto'] for h in historial]
            self.ax2.semilogy(it, err, 'o-', color='#6699ff', markersize=4)
            self.ax2.fill_between(it, err, 1e-20, color='#6699ff', alpha=0.1)
            self.datos_puntos_ax2 = [(it, err, "Error", '#6699ff')]

        # Raíz estrella roja
        self.ax1.plot(raiz, funcion(raiz), '*', color='#ff5555', markersize=15, label=f'Raíz: {raiz:.6f}', zorder=5)
        
        self.ax1.legend(facecolor='#0b0b14', edgecolor='#333333', labelcolor='white', fontsize=8)
        self.ax1.grid(True, alpha=0.1)

        # Config ax2
        self.ax2.set_title("Convergencia del Error Absoluto (escala log)", color='white', fontweight='bold', fontsize=10)
        self.ax2.set_xlabel("Iteración n", color='white', fontsize=9)
        self.ax2.set_ylabel("Error absoluto", color='white', fontsize=9)
        self.ax2.grid(True, which="both", ls="-", alpha=0.05)
        if es_comparacion:
            self.ax2.legend(facecolor='#0b0b14', edgecolor='#333333', labelcolor='white', fontsize=8)
        
        self.canvas.draw()

    def _graficar_cobweb(self, g, historial):
        """Implementa el gráfico de Telaraña (Cobweb)."""
        # Dibujar la línea y=x
        x_min, x_max = self.ax1.get_xlim()
        self.ax1.plot([x_min, x_max], [x_min, x_max], color='white', linestyle='--', alpha=0.5, label='y=x')
        
        for i in range(min(len(historial), 15)):
            h = historial[i]
            x_n = h['c']
            g_xn = h['f(c)'] # En punto fijo guardamos g(x_n) en f(c)
            
            # (x_n, x_n) -> (x_n, g(x_n))
            self.ax1.plot([x_n, x_n], [x_n, g_xn], color='yellow', alpha=0.6, linewidth=1)
            # (x_n, g(x_n)) -> (g(x_n), g(x_n))
            if i + 1 < len(historial):
                x_next = historial[i+1]['c']
                self.ax1.plot([x_n, x_next], [g_xn, x_next], color='yellow', alpha=0.6, linewidth=1)

    def _graficar_tangentes(self, f, historial, derivada_func):
        """Dibuja las rectas tangentes para Newton-Raphson."""
        for i in range(min(len(historial), 3)): # Solo las primeras 3 para no saturar
            h = historial[i]
            xn = h['c']
            fxn = h['f(c)']
            dfxn = h['f_prima(c)']
            
            # y = f'(x_n)*(x - x_n) + f(x_n)
            # Queremos ver dónde cruza el eje x (y=0) -> 0 = dfxn*(x - xn) + fxn -> x = xn - fxn/dfxn
            x_next = xn - fxn/dfxn
            
            x_range = np.linspace(min(xn, x_next) - 0.2, max(xn, x_next) + 0.2, 10)
            y_tangent = dfxn * (x_range - xn) + fxn
            self.ax1.plot(x_range, y_tangent, 'y--', alpha=0.7)
            self.ax1.plot([xn, xn], [0, fxn], 'white', linestyle=':', alpha=0.5)

    def _graficar_secantes(self, f, historial):
        """Dibuja las líneas secantes."""
        for i in range(min(len(historial), 5)):
            h = historial[i]
            x0 = h['x_n-1']
            x1 = h['c']
            fx0 = h['f(x_n-1)']
            fx1 = h['f(c)']
            
            # Línea que pasa por (x0, fx0) y (x1, fx1)
            x_vals = np.array([x0, x1])
            y_vals = np.array([fx0, fx1])
            
            # Extender la línea hasta el eje X
            if fx1 != fx0:
                x_interseccion = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
                x_plot = np.linspace(min(x0, x1, x_interseccion), max(x0, x1, x_interseccion), 10)
                m = (fx1 - fx0) / (x1 - x0)
                y_plot = m * (x_plot - x1) + fx1
                self.ax1.plot(x_plot, y_plot, 'y--', alpha=0.6)

    def graficar_comparacion(self, titulo, historial_1, label_1, historial_2, label_2):
        """
        Grafica la comparación de convergencia de dos métodos.
        """
        self.limpiar()
        self.ax1.axis('off') # Ocultar panel de función en comparación si se prefiere, o mostrar ambos
        self.ax1.text(0.5, 0.5, "Comparación de\nConvergencia", color='white', 
                     ha='center', va='center', fontsize=14)
        
        self.ax2.set_title(titulo, color='white')
        self.ax2.set_xlabel("Iteración", color='white')
        self.ax2.set_ylabel("Error Absoluto", color='white')
        
        # Método 1
        it1 = [h['n'] for h in historial_1]
        err1 = [h['error_absoluto'] for h in historial_1]
        self.ax2.semilogy(it1, err1, 'o-', label=label_1, markersize=4)
        
        # Método 2
        it2 = [h['n'] for h in historial_2]
        err2 = [h['error_absoluto'] for h in historial_2]
        self.ax2.semilogy(it2, err2, 'x--', label=label_2, markersize=4)
        
        self.ax2.grid(True, which="both", ls="-", alpha=0.2)
        self.ax2.legend()
        
        self.canvas.draw()

    def on_zoom(self, event):
        """Maneja el zoom con la rueda del ratón."""
        if event.inaxes == self.ax1:
            base_scale = 1.1
            if event.button == 'up':
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                scale_factor = base_scale
            else:
                scale_factor = 1
            
            cur_xlim = self.ax1.get_xlim()
            cur_ylim = self.ax1.get_ylim()
            
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            
            relx = (cur_xlim[1] - event.xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - event.ydata) / (cur_ylim[1] - cur_ylim[0])
            
            self.ax1.set_xlim([event.xdata - new_width * (1 - relx), event.xdata + new_width * relx])
            self.ax1.set_ylim([event.ydata - new_height * (1 - rely), event.ydata + new_height * rely])
            self.canvas.draw()

    def on_hover(self, event):
        """Muestra un tooltip al pasar el mouse por los puntos de convergencia o la curva principal."""
        if not event.inaxes:
            if self.tooltip:
                try: self.tooltip.remove()
                except: pass
                self.tooltip = None
                self.canvas.draw_idle()
            return

        if event.inaxes == self.ax2:
            # Hover en gráfica de convergencia
            for data in self.datos_puntos_ax2:
                it_list, err_list, label, color = data
                for it, err in zip(it_list, err_list):
                    if abs(event.xdata - it) < 0.5 and abs(np.log10(event.ydata) - np.log10(err)) < 0.3:
                        if self.tooltip: self.tooltip.remove()
                        self.tooltip = self.ax2.annotate(
                            f"{label}\nIter: {it}\nError: {err:.2e}",
                            xy=(it, err), xytext=(15, 15), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="#0b0b14", ec=color, alpha=0.9),
                            color="white", fontsize=8, arrowprops=dict(arrowstyle="->", color=color)
                        )
                        self.canvas.draw_idle()
                        return
        
        elif event.inaxes == self.ax1:
            # Hover en gráfica principal (mostrar coordenadas dinámicas)
            if event.xdata is not None and event.ydata is not None:
                if self.tooltip: self.tooltip.remove()
                self.tooltip = self.ax1.annotate(
                    f"x = {event.xdata:.4f}\ny = {event.ydata:.4f}",
                    xy=(event.xdata, event.ydata), xytext=(15, 15), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="#0b0b14", ec="#6699ff", alpha=0.9),
                    color="white", fontsize=8, arrowprops=dict(arrowstyle="->", color="#6699ff")
                )
                self.canvas.draw_idle()
                return

        if self.tooltip:
            self.tooltip.remove()
            self.tooltip = None
            self.canvas.draw_idle()
