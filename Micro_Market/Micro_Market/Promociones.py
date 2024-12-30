import tkinter as tk
from tkinter import ttk, messagebox

class Promociones(tk.Frame):
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.config(bg="#C6D9E3")  # Color de fondo de la interfaz principal
        self.place(x=300, y=10, width=780, height=580)  # Tamaño de la interfaz
        self.crear_widgets()

    def crear_widgets(self):
        # Contenedor y etiquetas con color de fondo y bordes verdes
        Ibframe_seleccion = tk.LabelFrame(self, text="Detalles de la Promoción:", font="arial 14 bold", bg="#C6D9E3", 
                                          highlightbackground="green", highlightthickness=2)
        Ibframe_seleccion.place(x=10, y=10, width=300, height=270)
        
        # Etiquetas de la interfaz
        tk.Label(Ibframe_seleccion, text="Nombre:", font="arial 14", bg="#C6D9E3").place(x=5, y=5)
        tk.Label(Ibframe_seleccion, text="Descripción:", font="arial 14", bg="#C6D9E3").place(x=5, y=40)
        tk.Label(Ibframe_seleccion, text="Fecha Inicio:", font="arial 14", bg="#C6D9E3").place(x=5, y=75)
        tk.Label(Ibframe_seleccion, text="Fecha Fin:", font="arial 14", bg="#C6D9E3").place(x=5, y=110)
        tk.Label(Ibframe_seleccion, text="Descuento (%):", font="arial 14", bg="#C6D9E3").place(x=5, y=145)

        # Entradas de texto
        self.entry_nombre = tk.Entry(Ibframe_seleccion)
        self.entry_descripcion = tk.Entry(Ibframe_seleccion)
        self.entry_fecha_inicio = tk.Entry(Ibframe_seleccion)
        self.entry_fecha_fin = tk.Entry(Ibframe_seleccion)
        self.entry_descuento = tk.Entry(Ibframe_seleccion)

        self.entry_nombre.place(x=150, y=5, width=130)
        self.entry_descripcion.place(x=150, y=40, width=130)
        self.entry_fecha_inicio.place(x=150, y=75, width=130)
        self.entry_fecha_fin.place(x=150, y=110, width=130)
        self.entry_descuento.place(x=150, y=145, width=130)

        # Contenedor para botones
        lblframe_botones = tk.LabelFrame(self, bg="#C6D9E3", text="Opciones", font="arial 14 bold", 
                                         highlightbackground="green", highlightthickness=2)
        lblframe_botones.place(x=10, y=290, width=300, height=300)
        
        # Botones de acción
        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_promocion)
        btn_agregar.place(x=20, y=20, width=180, height=40)

        btn_modificar = tk.Button(lblframe_botones, text="Modificar", font="arial 14 bold", command=self.modificar_promocion)
        btn_modificar.place(x=20, y=70, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_promocion)
        btn_eliminar.place(x=20, y=120, width=180, height=40)

        # Tabla para mostrar las promociones
        self.tree = ttk.Treeview(self, columns=("Nombre", "Descripción", "Fecha Inicio", "Fecha Fin", "Descuento"), show='headings')
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Fecha Inicio", text="Fecha Inicio")
        self.tree.heading("Fecha Fin", text="Fecha Fin")
        self.tree.heading("Descuento", text="Descuento (%)")
        self.tree.column("Nombre", width=100)
        self.tree.column("Descripción", width=150)
        self.tree.column("Fecha Inicio", width=80)
        self.tree.column("Fecha Fin", width=80)
        self.tree.column("Descuento", width=60)
        self.tree.place(x=320, y=10, width=760, height=495)

    # Método para agregar una promoción
    def agregar_promocion(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_fin.get()
        descuento = self.entry_descuento.get()

        if nombre and descripcion and fecha_inicio and fecha_fin and descuento:
            self.tree.insert("", "end", values=(nombre, descripcion, fecha_inicio, fecha_fin, descuento))
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_promocion(self):
        selected_item = self.tree.selection()
        if selected_item:
            nombre = self.entry_nombre.get()
            descripcion = self.entry_descripcion.get()
            fecha_inicio = self.entry_fecha_inicio.get()
            fecha_fin = self.entry_fecha_fin.get()
            descuento = self.entry_descuento.get()

            if nombre and descripcion and fecha_inicio and fecha_fin and descuento:
                self.tree.item(selected_item, values=(nombre, descripcion, fecha_inicio, fecha_fin, descuento))
                self.limpiar_entradas()
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una promoción para modificar.")

    def eliminar_promocion(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "Seleccione una promoción para eliminar.")

    def limpiar_entradas(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_fecha_inicio.delete(0, tk.END)
        self.entry_fecha_fin.delete(0, tk.END)
        self.entry_descuento.delete(0, tk.END)
