import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Reportes(tk.Frame):
    def __init__(self, padre, controlador=None):
        super().__init__(padre)
        self.controlador = controlador
        self.pack(fill="both", expand=True)
        self.widgets()

    def widgets(self):
        # Título principal
        titulo = tk.Label(self, text="REPORTES", font=("sans", 16, "bold"), bg="#C6D9E3", anchor="center")
        titulo.pack(fill="x")

        # Contenedor para los botones
        contenedor_botones = tk.Frame(self, bg="#C6D9E3")
        contenedor_botones.pack(pady=20)

        # Lista de botones con nombres e íconos
        botones = [
            ("Reporte ventas totales", "icons/report_ventas_totales.png"),
            ("Reporte ganancias", "icons/report_ganancias.png"),
            ("Reporte costo total inventario", "icons/report_inventario.png"),
            ("Reporte costo total ventas", "icons/report_costos_ventas.png"),
            ("Gráfico Ventas por Mes", "icons/chart_ventas_mes.png"),
            ("Gráfico Ganancias por Mes", "icons/chart_ganancias_mes.png"),
            ("Gráfico por Categorías", "icons/chart_categorias.png"),
            ("Gráfico por Sucursal", "icons/chart_sucursal.png"),
        ]

        # Crear botones en una cuadrícula
        filas = 2
        columnas = 4

        for i, (texto, icono) in enumerate(botones):
            # Frame para cada botón
            frame_boton = tk.Frame(contenedor_botones, bg="#C6D9E3", padx=10, pady=10)
            frame_boton.grid(row=i // columnas, column=i % columnas, padx=15, pady=15)

            # Crear el ícono del botón
            try:
                imagen = tk.PhotoImage(file=icono)  # Requiere que el archivo PNG esté disponible
            except:
                imagen = None  # Si no se encuentra el archivo, se usa None

            boton = tk.Button(
                frame_boton,
                text=texto,
                image=imagen,
                compound="top",
                font=("sans", 10),
                bg="white",
                fg="black",
                command=lambda t=texto: self.mostrar_mensaje(t)
            )
            boton.image = imagen  # Necesario para evitar que la imagen sea recolectada por el garbage collector
            boton.pack()

    def mostrar_mensaje(self, texto):
        """Muestra un mensaje indicando qué botón fue presionado."""
        messagebox.showinfo("Acción", f"Presionaste el botón: {texto}")


# Ejecución principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Interfaz de Reportes")
    root.geometry("800x500")  # Tamaño de la ventana
    root.configure(bg="#C6D9E3")  # Fondo similar al diseño mostrado
    app = Reportes(root)
    root.mainloop()
