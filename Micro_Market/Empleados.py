import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Empleados(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.config(bg="#C6D9E3")
        self.place(x=0, y=0, width=1100, height=650)
        self.crear_widgets()
        self.cargar_empleados()

    def crear_widgets(self):
        # Título
        titulo = tk.Label(self, text="EMPLEADOS", font=("Arial", 24, "bold"), bg="#C6D9E3")
        titulo.place(x=400, y=10, width=300, height=30)

        # Botones Regresar y Salir
        self.crear_botones_regresar_salir()

        # Etiquetas de Fecha y Hora
        self.crear_fecha_hora_labels()

        Ibframe_seleccion = tk.LabelFrame(
            self, text="Selección:", font="arial 14 bold", bg="#C6D9E3",
            highlightbackground="green", highlightthickness=2
        )
        Ibframe_seleccion.place(x=10, y=110, width=300, height=210)

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
        lblframe_botones.place(x=10, y=320, width=300, height=300)

        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_empleados)
        btn_agregar.place(x=20, y=20, width=180, height=40)

        btn_modificar = tk.Button(lblframe_botones, text="Modificar", font="arial 14 bold", command=self.modificar_empleados)
        btn_modificar.place(x=20, y=70, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_empleados)
        btn_eliminar.place(x=20, y=120, width=180, height=40)

        btn_desactivar = tk.Button(lblframe_botones, text="Desactivar", font="arial 14 bold", command=self.desactivar_empleado)
        btn_desactivar.place(x=20, y=170, width=180, height=40)

        btn_reactivar = tk.Button(lblframe_botones, text="Reactivar", font="arial 14 bold", command=self.reactivar_empleado)
        btn_reactivar.place(x=20, y=220, width=180, height=40)

        self.tree = ttk.Treeview(
            self, columns=("Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Celular", "Estado"), show='headings'
        )
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido Paterno", text="Apellido Paterno")
        self.tree.heading("Apellido Materno", text="Apellido Materno")
        self.tree.heading("CI", text="CI")
        self.tree.heading("Celular", text="Celular")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("Nombre", width=150)
        self.tree.column("Apellido Paterno", width=150)
        self.tree.column("Apellido Materno", width=150)
        self.tree.column("CI", width=100)
        self.tree.column("Celular", width=100)
        self.tree.column("Estado", width=100)
        self.tree.place(x=320, y=110, width=760, height=495)

    def crear_botones_regresar_salir(self):
        boton_regresar = tk.Button(
            self, text="REGRESAR", command=self.regresar, 
            font=("Arial", 14), bg="blue", fg="white"
        )
        boton_regresar.place(x=10, y=10, width=120, height=40)

        boton_salir = tk.Button(
            self, text="SALIR", command=self.salir, 
            font=("Arial", 14), bg="red", fg="white"
        )
        boton_salir.place(x=980, y=10, width=100, height=40)

    def crear_fecha_hora_labels(self):
        self.fecha_label = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#C6D9E3")
        self.fecha_label.place(x=250, y=55, width=350, height=30)

        self.hora_label = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#C6D9E3")
        self.hora_label.place(x=610, y=55, width=350, height=30)

        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        ahora = datetime.now()
        fecha_actual = ahora.strftime("%Y-%m-%d")
        hora_actual = ahora.strftime("%H:%M:%S")
        self.fecha_label.config(text=f"FECHA: {fecha_actual}")
        self.hora_label.config(text=f"HORA: {hora_actual}")
        self.after(1000, self.actualizar_fecha_hora)

    def agregar_empleados(self):
        nombre = self.entry_nombre.get()
        apellido_paterno = self.entry_apellido_paterno.get()
        apellido_materno = self.entry_apellido_materno.get() or None
        ci = self.entry_ci.get()
        celular = self.entry_celular.get()

        if not all([nombre, apellido_paterno, ci, celular]):
            messagebox.showwarning("Advertencia", "Los campos obligatorios no pueden estar vacíos.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Empleado (Nombre, Apellido_Paterno, Apellido_Materno, CI, Celular) "
                "VALUES (%s, %s, %s, %s, %s)",
                (nombre, apellido_paterno, apellido_materno, ci, celular)
            )
            self.db_connection.commit()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Empleado agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado: {e}")
        self.limpiar_entradas()

    def cargar_empleados(self):
        """Carga todos los empleados (activos e inactivos) en la tabla."""
        # Eliminar filas existentes
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Consultar todos los empleados
        query = """
        SELECT Nombre, Apellido_Paterno, COALESCE(Apellido_Materno, ''), CI, Celular, 
            CASE WHEN Estado = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado, Estado
        FROM Empleado
        """
        self.cursor.execute(query)
        empleados = self.cursor.fetchall()

        # Insertar empleados en la tabla con colores según el estado
        for empleado in empleados:
            nombre, apellido_paterno, apellido_materno, ci, celular, estado, estado_valor = empleado
            tag = "activo" if estado_valor == 1 else "inactivo"
            self.tree.insert("", "end", values=(nombre, apellido_paterno, apellido_materno, ci, celular, estado), tags=(tag,))
 
        # Aplicar estilos de colores según los tags
        self.tree.tag_configure("activo", foreground="green")
        self.tree.tag_configure("inactivo", foreground="red")
    
    def desactivar_empleado(self):
        """Marca a un empleado como inactivo."""
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para desactivar.")
            return

        valores = self.tree.item(seleccion, "values")
        ci = valores[3]  # CI como identificador único

        try:
            self.cursor.execute("UPDATE Empleado SET Estado = 0 WHERE CI = %s", (ci,))
            self.db_connection.commit()
            self.cargar_empleados()  # Sin 'activos'
            messagebox.showinfo("Éxito", "Empleado desactivado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo desactivar el empleado: {e}")

    def reactivar_empleado(self):
        """Marca a un empleado como activo."""
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para reactivar.")
            return

        valores = self.tree.item(seleccion, "values")
        ci = valores[3]  # CI como identificador único

        try:
            self.cursor.execute("UPDATE Empleado SET Estado = 1 WHERE CI = %s", (ci,))
            self.db_connection.commit()
            self.cargar_empleados()  # Sin 'activos'
            messagebox.showinfo("Éxito", "Empleado reactivado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reactivar el empleado: {e}")

    def modificar_empleados(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para modificar.")
            return
        
        valores = self.tree.item(seleccion, "values")
        ci = valores[3]  # CI como identificador único

        nuevo_nombre = self.entry_nombre.get()
        nuevo_apellido_paterno = self.entry_apellido_paterno.get()
        nuevo_apellido_materno = self.entry_apellido_materno.get() or None
        nuevo_celular = self.entry_celular.get()

        if not all([nuevo_nombre, nuevo_apellido_paterno, nuevo_celular]):
            messagebox.showwarning("Advertencia", "Los campos obligatorios no pueden estar vacíos.")
            return

        try:
            self.cursor.execute(
                "UPDATE Empleado SET Nombre = %s, Apellido_Paterno = %s, Apellido_Materno = %s, Celular = %s "
                "WHERE CI = %s",
                (nuevo_nombre, nuevo_apellido_paterno, nuevo_apellido_materno, nuevo_celular, ci)
            )
            self.db_connection.commit()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Empleado modificado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el empleado: {e}")
        self.limpiar_entradas()

    def eliminar_empleados(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un empleado para eliminar.")
            return

        valores = self.tree.item(seleccion, "values")
        ci = valores[3]
        estado = valores[5]  # Estado es la columna que contiene "Activo" o "Inactivo"

        try:
            if estado == "Activo":
                messagebox.showwarning(
                    "Advertencia", 
                    "No se puede eliminar un empleado activo. Por favor, desactívelo primero."
                )
                return

            # Confirmar eliminación para empleados inactivos
            if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este empleado inactivo?"):
                self.cursor.execute("DELETE FROM Empleado WHERE CI = %s", (ci,))
                self.db_connection.commit()
                self.cargar_empleados()
                messagebox.showinfo("Éxito", "Empleado inactivo eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el empleado: {e}")


    def limpiar_entradas(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido_paterno.delete(0, tk.END)
        self.entry_apellido_materno.delete(0, tk.END)
        self.entry_ci.delete(0, tk.END)
        self.entry_celular.delete(0, tk.END)

    def regresar(self):
        self.destroy()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()
