import tkinter as tk
from tkinter import ttk

class Usuarios(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)  
        self.controlador = controlador
        self.widgets()
    
    def widgets(self):
        # Configuración de LabelFrame
        Labelframe = tk.LabelFrame(self, text="Usuarios", font="sans 12 bold", bg="#C6D9E3", padx=10, pady=10)
        Labelframe.place(x=25, y=30, width=1045, height=400)

        # Treeview para mostrar la tabla Usuarios
        self.tree = ttk.Treeview(Labelframe, columns=("Id", "Nombre", "Correo", "Rol"), show="headings", height=10)
        self.tree.heading("Id", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Rol", text="Rol")

        self.tree.column("Id", width=50, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        self.tree.column("Correo", width=250, anchor="w")
        self.tree.column("Rol", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para cargar datos
        btn_cargar = tk.Button(self, text="Cargar Datos", command=self.cargar_datos, bg="#4CAF50", fg="white", font="sans 10 bold")
        btn_cargar.place(x=25, y=450, width=150, height=40)

    def cargar_datos(self):
        # Esta función debe obtener los datos de la tabla Usuarios desde la base de datos
        # Aquí va el código para conectarse a la base de datos y recuperar los datos
        datos = [
            (1, "Juan Pérez", "juan@example.com", "Administrador"),
            (2, "Ana López", "ana@example.com", "Vendedor"),
            (3, "Carlos Díaz", "carlos@example.com", "Administrador"),
        ]

        # Limpiar el Treeview antes de cargar nuevos datos
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        # Insertar los datos en el Treeview
        for dato in datos:
            self.tree.insert("", "end", values=dato)

