from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Proveedor(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.config(bg="#D0E4F5")  # Color de fondo para el frame
        self.crear_widgets()
        self.lista_proveedores = []  # Lista para almacenar los proveedores
    
    def crear_widgets(self):
        # Contenedores y etiquetas con el mismo color de fondo y bordes verdes
        Ibframe_seleccion = tk.LabelFrame(self, text="Datos:", font="arial 14 bold", bg="#C6D9E3", 
                                          highlightbackground="green", highlightthickness=2)
        Ibframe_seleccion.place(x=10, y=10, width=500, height=210)
        
        # Etiquetas de la interfaz
        tk.Label(Ibframe_seleccion, text="Nombre:", font="arial 14", bg="#C6D9E3").place(x=5, y=5)
        tk.Label(Ibframe_seleccion, text="Apellido Paterno:", font="arial 14", bg="#C6D9E3").place(x=5, y=40)
        tk.Label(Ibframe_seleccion, text="Apellido Materno:", font="arial 14", bg="#C6D9E3").place(x=5, y=70)
        tk.Label(Ibframe_seleccion, text="Celular:", font="arial 14", bg="#C6D9E3").place(x=5, y=100)
        tk.Label(Ibframe_seleccion, text="Descripcion:", font="arial 14", bg="#C6D9E3").place(x=5, y=130)

        # Entradas de texto
        self.entry_nombre = tk.Entry(Ibframe_seleccion)
        self.entry_ApellidoPaterno = tk.Entry(Ibframe_seleccion)
        self.entry_ApellidoMaterno = tk.Entry(Ibframe_seleccion)
        self.entry_celular = tk.Entry(Ibframe_seleccion)
        self.entry_descripcion = tk.Entry(Ibframe_seleccion)

        self.entry_nombre.place(x=160, y=5, width=150)
        self.entry_ApellidoPaterno.place(x=160, y=40, width=150)
        self.entry_ApellidoMaterno.place(x=160, y=70, width=150)
        self.entry_celular.place(x=160, y=100, width=150)
        self.entry_descripcion.place(x=160, y=130, width=150)

        # Contenedor para botones
        lblframe_botones = tk.LabelFrame(self, bg="#C6D9E3", text="Opciones", font="arial 14 bold", 
                                         highlightbackground="green", highlightthickness=2)
        lblframe_botones.place(x=400, y=10, width=300, height=210)
        
        # Botones de acción
        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_proveedor)
        btn_agregar.place(x=60, y=20, width=180, height=40)

        btn_modificar = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_proveedor)
        btn_modificar.place(x=60, y=70, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_proveedor)
        btn_eliminar.place(x=60, y=120, width=180, height=40)

        # Tabla para mostrar los proveedores
        self.tree = ttk.Treeview(self, columns=("Nombre", "Apellido Paterno", "Apellido Materno", "Celular", "Descripcion"), show='headings')
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido Paterno", text="Apellido Paterno")  # Corregido
        self.tree.heading("Apellido Materno", text="Apellido Materno")
        self.tree.heading("Celular", text="Celular")
        self.tree.heading("Descripcion", text="Descripcion")
       
        self.tree.column("Nombre", width=150)
        self.tree.column("Apellido Paterno", width=100)
        self.tree.column("Apellido Materno", width=100)
        self.tree.column("Celular", width=100)
        self.tree.column("Descripcion", width=200)
        self.tree.place(x=10, y=220, width=1045, height=300)
    
    # Método para agregar proveedor
    def agregar_proveedor(self):
        nombre = self.entry_nombre.get()
        apellido_paterno = self.entry_ApellidoPaterno.get()
        apellido_materno = self.entry_ApellidoMaterno.get()
        celular = self.entry_celular.get()
        descripcion = self.entry_descripcion.get()

        if not nombre or not apellido_paterno or not apellido_materno or not celular or not descripcion:
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos")
            return

        self.lista_proveedores.append((nombre, apellido_paterno, apellido_materno, celular, descripcion))
        self.actualizar_lista_proveedores()

        # Limpiar los campos
        self.entry_nombre.delete(0, END)
        self.entry_ApellidoPaterno.delete(0, END)
        self.entry_ApellidoMaterno.delete(0, END)
        self.entry_celular.delete(0, END)
        self.entry_descripcion.delete(0, END)

    # Método para editar proveedor
    def editar_proveedor(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            index = self.tree.index(seleccionado)
            proveedor = self.lista_proveedores[index]
            self.entry_nombre.insert(0, proveedor[0])
            self.entry_ApellidoPaterno.insert(0, proveedor[1])
            self.entry_ApellidoMaterno.insert(0, proveedor[2])
            self.entry_celular.insert(0, proveedor[3])
            self.entry_descripcion.insert(0, proveedor[4])

            # Eliminar el proveedor de la lista para luego volver a agregarlo
            del self.lista_proveedores[index]
            self.tree.delete(seleccionado)
        else:
            messagebox.showwarning("Selección vacía", "Por favor, selecciona un proveedor para editar")

    # Método para eliminar proveedor
    def eliminar_proveedor(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            index = self.tree.index(seleccionado)
            del self.lista_proveedores[index]
            self.tree.delete(seleccionado)
        else:
            messagebox.showwarning("Selección vacía", "Por favor, selecciona un proveedor para eliminar")

    # Método para actualizar la lista de proveedores en el Treeview
    def actualizar_lista_proveedores(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for proveedor in self.lista_proveedores:
            self.tree.insert('', 'end', values=proveedor)

