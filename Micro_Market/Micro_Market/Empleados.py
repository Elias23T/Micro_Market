import tkinter as tk
from tkinter import ttk, messagebox

class Empleados(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.config(bg="#C6D9E3")

        self.place(x=300, y=50, width=780, height=580)  # Ajuste el punto Y en el método __init__

        self.crear_widgets()

    def crear_widgets(self):
        Ibframe_seleccion = tk.LabelFrame(
            self, text="Selección:", font="arial 14 bold", bg="#C6D9E3",
            highlightbackground="green", highlightthickness=2
        )
        Ibframe_seleccion.place(x=10, y=50, width=300, height=240)  # Y ajustado

        tk.Label(Ibframe_seleccion, text="Nombre:", font="arial 14", bg="#C6D9E3").place(x=5, y=5)
        tk.Label(Ibframe_seleccion, text="Apellido Paterno:", font="arial 14", bg="#C6D9E3").place(x=5, y=40)
        tk.Label(Ibframe_seleccion, text="Apellido Materno:", font="arial 14", bg="#C6D9E3").place(x=5, y=75)
        tk.Label(Ibframe_seleccion, text="CI:", font="arial 14", bg="#C6D9E3").place(x=5, y=110)
        tk.Label(Ibframe_seleccion, text="Celular:", font="arial 14", bg="#C6D9E3").place(x=5, y=145)

        self.entry_nombre = tk.Entry(Ibframe_seleccion)
        self.entry_apellido_paterno = tk.Entry(Ibframe_seleccion)
        self.entry_apellido_materno = tk.Entry(Ibframe_seleccion)
        self.entry_ci = tk.Entry(Ibframe_seleccion)
        self.entry_celular = tk.Entry(Ibframe_seleccion)

        self.entry_nombre.place(x=150, y=5, width=130)
        self.entry_apellido_paterno.place(x=150, y=40, width=130)
        self.entry_apellido_materno.place(x=150, y=75, width=130)
        self.entry_ci.place(x=150, y=110, width=130)
        self.entry_celular.place(x=150, y=145, width=130)

        lblframe_botones = tk.LabelFrame(
            self, bg="#C6D9E3", text="Opciones", font="arial 14 bold",
            highlightbackground="green", highlightthickness=2
        )
        lblframe_botones.place(x=10, y=260, width=300, height=300)  # Y ajustado

        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_empleado)
        btn_agregar.place(x=20, y=20, width=180, height=40)

        btn_modificar = tk.Button(lblframe_botones, text="Modificar", font="arial 14 bold", command=self.modificar_empleado)
        btn_modificar.place(x=20, y=70, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_empleado)
        btn_eliminar.place(x=20, y=120, width=180, height=40)

        self.tree = ttk.Treeview(
            self, columns=("Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Celular"), show='headings'
        )
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido Paterno", text="Apellido Paterno")
        self.tree.heading("Apellido Materno", text="Apellido Materno")
        self.tree.heading("CI", text="CI")
        self.tree.heading("Celular", text="Celular")
        self.tree.column("Nombre", width=100)
        self.tree.column("Apellido Paterno", width=100)
        self.tree.column("Apellido Materno", width=100)
        self.tree.column("CI", width=80)
        self.tree.column("Celular", width=80)
        self.tree.place(x=320, y=50, width=760, height=495)  # Y ajustado

    def agregar_empleado(self):
        nombre = self.entry_nombre.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get()
        ci = self.entry_ci.get()
        celular = self.entry_celular.get()

        if nombre and apellido_paterno and apellido_materno and ci and celular:
            self.tree.insert("", "end", values=(nombre, apellido_paterno, apellido_materno, ci, celular))
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_empleado(self):
        selected_item = self.tree.selection()
        if selected_item:
            nombre = self.entry_nombre.get()
            apellido_paterno = self.entry_apellido_paterno.get()
            apellido_materno = self.entry_apellido_materno.get()
            ci = self.entry_ci.get()
            celular = self.entry_celular.get()

            if nombre and apellido_paterno and apellido_materno and ci and celular:
                self.tree.item(selected_item, values=(nombre, apellido_paterno, apellido_materno, ci, celular))
                self.limpiar_entradas()
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para modificar.")

    def eliminar_empleado(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar.")

    def limpiar_entradas(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido_paterno.delete(0, tk.END)
        self.entry_apellido_materno.delete(0, tk.END)
        self.entry_ci.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)
