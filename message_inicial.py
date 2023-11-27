import tkinter as tk
from tkinter import ttk, messagebox
from credentials import credentials_dict

# DEFINICIÓN DE TÍTULO Y MENSAJE #
title = credentials_dict['popup_title']
message = credentials_dict['popup_message']

class MensajeAutodestructivo:
    def __init__(self):
        self.ventana_principal = tk.Tk()
        self.ventana_principal.withdraw()
        self.ventana_principal.title("Mensaje Principal")

        # Configurar estilo para la etiqueta principal
        style = ttk.Style()
        style.configure(
            "TLabel",
            font=("Arial", 12),
            padding=10,
            background="lightblue",
            foreground="black",
            borderwidth=2,
            relief="solid",
            width=20,
            height=2
        )

        self.etiqueta_principal = ttk.Label(self.ventana_principal, text="Este mensaje principal se autodestruirá en 5 segundos.")
        self.etiqueta_principal.pack()

        self.ventana_secundaria = tk.Toplevel(self.ventana_principal)
        self.ventana_secundaria.withdraw()
        self.etiqueta_secundaria = ttk.Label(self.ventana_secundaria, text="Este es un mensaje secundario.")
        self.etiqueta_secundaria.pack(pady=10)

        # Configurar temporizador para cerrar las ventanas después de 5000 milisegundos (5 segundos)
        self.ventana_principal.after(7000, self.cerrar_ventanas)

        # Mostrar el messagebox.showinfo después de 0.5 segundos y cerrar después de 10 segundos
        self.ventana_principal.after(500, self.mostrar_messagebox)
        self.ventana_principal.after(4000, self.cerrar_ventanas)

        self.ventana_principal.mainloop()

    def cerrar_ventanas(self):
        try:
            self.ventana_principal.destroy()
        except tk.TclError:
            pass

        try:
            self.ventana_secundaria.destroy()
        except tk.TclError:
            pass

    def mostrar_messagebox(self):
        messagebox.showinfo(title=title, message=message)



