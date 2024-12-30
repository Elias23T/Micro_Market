import tkinter as tk
from tkinter import ttk, messagebox

class Clientes(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.config(bg="#C6D9E3")  # Color de fondo de la interfaz principal
        self.place(x=300, y=10, width=780, height=580)  # Asegurar el mismo tamaño que Productos
        self.crear_widgets()

    def crear_widgets(self):
        # Contenedores y etiquetas con el mismo color de fondo y bordes verdes
        Ibframe_seleccion = tk.LabelFrame(self, text="Selección:", font="arial 14 bold", bg="#C6D9E3", 
                                          highlightbackground="green", highlightthickness=2)
        Ibframe_seleccion.place(x=10, y=10, width=300, height=190)
        
        # Etiquetas de la interfaz
        tk.Label(Ibframe_seleccion, text="Nombre:", font="arial 14", bg="#C6D9E3").place(x=5, y=5)
        tk.Label(Ibframe_seleccion, text="Cédula:", font="arial 14", bg="#C6D9E3").place(x=5, y=40)
        tk.Label(Ibframe_seleccion, text="Celular:", font="arial 14", bg="#C6D9E3").place(x=5, y=70)
        tk.Label(Ibframe_seleccion, text="Dirección:", font="arial 14", bg="#C6D9E3").place(x=5, y=100)
        tk.Label(Ibframe_seleccion, text="Correo:", font="arial 14", bg="#C6D9E3").place(x=5, y=130)

        # Entradas de texto
        self.entry_nombre = tk.Entry(Ibframe_seleccion)
        self.entry_cedula = tk.Entry(Ibframe_seleccion)
        self.entry_celular = tk.Entry(Ibframe_seleccion)
        self.entry_direccion = tk.Entry(Ibframe_seleccion)
        self.entry_correo = tk.Entry(Ibframe_seleccion)

        self.entry_nombre.place(x=120, y=5, width=150)
        self.entry_cedula.place(x=120, y=40, width=150)
        self.entry_celular.place(x=120, y=70, width=150)
        self.entry_direccion.place(x=120, y=100, width=150)
        self.entry_correo.place(x=120, y=130, width=150)

        # Contenedor para botones
        lblframe_botones = tk.LabelFrame(self, bg="#C6D9E3", text="Opciones", font="arial 14 bold", 
                                         highlightbackground="green", highlightthickness=2)
        lblframe_botones.place(x=10, y=210, width=300, height=300)
        
        # Botones de acción
        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_cliente)
        btn_agregar.place(x=20, y=20, width=180, height=40)

        btn_modificar = tk.Button(lblframe_botones, text="Modificar", font="arial 14 bold", command=self.modificar_cliente)
        btn_modificar.place(x=20, y=70, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_cliente)
        btn_eliminar.place(x=20, y=120, width=180, height=40)

        # Tabla para mostrar los clientes
        self.tree = ttk.Treeview(self, columns=("Nombre", "Cédula", "Celular", "Dirección", "Correo"), show='headings')
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cédula", text="Cédula")
        self.tree.heading("Celular", text="Celular")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Correo", text="Correo")
        self.tree.column("Nombre", width=150)
        self.tree.column("Cédula", width=100)
        self.tree.column("Celular", width=100)
        self.tree.column("Dirección", width=200)
        self.tree.column("Correo", width=150)
        self.tree.place(x=320, y=10, width=760, height=495)

    # Método para agregar un cliente
    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        cedula = self.entry_cedula.get()
        celular = self.entry_celular.get()
        direccion = self.entry_direccion.get()
        correo = self.entry_correo.get()

        if nombre and cedula and celular and direccion:
            self.tree.insert("", "end", values=(nombre, cedula, celular, direccion, correo))
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_cliente(self):
        selected_item = self.tree.selection()
        if selected_item:
            nombre = self.entry_nombre.get()
            cedula = self.entry_cedula.get()
            celular = self.entry_celular.get()
            direccion = self.entry_direccion.get()
            correo = self.entry_correo.get()

            if nombre and cedula and celular and direccion:
                self.tree.item(selected_item, values=(nombre, cedula, celular, direccion, correo))
                self.limpiar_entradas()
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar.")

    def eliminar_cliente(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")

    def limpiar_entradas(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_cedula.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
