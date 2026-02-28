import tkinter as tk
from tkinter import ttk

class MensajePersonalizado(tk.Toplevel):
    """
    Diálogo emergente personalizado que hereda de tk.Toplevel para permitir
    el estilizado acorde al tema de la aplicación.
    """
    def __init__(self, parent, titulo, mensaje, tipo="info", tema="Oscuro", colores=None):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centrar en la ventana principal
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        self.tema = tema
        self.colores = colores if colores else {
            "Oscuro": {"bg": "#12121e", "fg": "#ffffff", "accent": "#3a5aff", "error": "#ff5555", "info": "#6699ff"},
            "Claro": {"bg": "#f0f0f0", "fg": "#1a1a1a", "accent": "#0056b3", "error": "#d32f2f", "info": "#1976d2"}
        }[tema]

        self.configure(bg=self.colores["bg"])
        
        # Frame de borde
        self.main_frame = tk.Frame(self, bg=self.colores["bg"], padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Icono y Texto
        self.content_frame = tk.Frame(self.main_frame, bg=self.colores["bg"])
        self.content_frame.pack(fill="both", expand=True)

        # Determinar color de acento según tipo
        color_tipo = self.colores.get(tipo, self.colores["accent"])
        
        # Simulación de icono (puedes añadir imágenes reales si están disponibles)
        icon_symbol = "ℹ" if tipo == "info" else "⚠" if tipo == "warning" else "❌"
        self.lbl_icon = tk.Label(self.content_frame, text=icon_symbol, font=("Segoe UI Symbol", 30), 
                                 bg=self.colores["bg"], fg=color_tipo)
        self.lbl_icon.pack(side="left", padx=(0, 20))

        self.lbl_msg = tk.Label(self.content_frame, text=mensaje, font=("Segoe UI", 10), 
                                bg=self.colores["bg"], fg=self.colores["fg"], wraplength=280, justify="left")
        self.lbl_msg.pack(side="left", fill="both", expand=True)

        # Botón Aceptar
        self.btn_accept = tk.Button(self.main_frame, text="Aceptar", font=("Segoe UI", 10, "bold"),
                                   bg=self.colores["accent"], fg="white", bd=0, padx=20, pady=5,
                                   command=self.destroy, activebackground=self.colores["accent"],
                                   activeforeground="white", cursor="hand2")
        self.btn_accept.pack(pady=(10, 0))

        # Tecla Enter para cerrar
        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())

    @staticmethod
    def showerror(parent, titulo, mensaje, tema="Oscuro"):
        MensajePersonalizado(parent, titulo, mensaje, tipo="error", tema=tema)

    @staticmethod
    def showinfo(parent, titulo, mensaje, tema="Oscuro"):
        MensajePersonalizado(parent, titulo, mensaje, tipo="info", tema=tema)

    @staticmethod
    def showwarning(parent, titulo, mensaje, tema="Oscuro"):
        MensajePersonalizado(parent, titulo, mensaje, tipo="warning", tema=tema)
