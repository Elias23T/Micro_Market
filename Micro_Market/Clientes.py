import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Clientes(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.config(bg="#C6D9E3")
        self.place(x=0, y=0, width=1100, height=650)
        self.crear_widgets()
        self.cargar_clientes()

    def crear_widgets(self):
        # Título
        tk.Label(self, text="CLIENTES", font=("Arial", 24, "bold"), bg="#C6D9E3").place(x=450, y=10)

        # Botones de Regresar y Salir
        tk.Button(self, text="SALIR", command=self.salir, font=("Arial", 14), bg="red", fg="white").place(x=1000, y=10, width=80, height=30)
        tk.Button(self, text="REGRESAR", command=self.regresar, font=("Arial", 14), bg="blue", fg="white").place(x=10, y=10, width=110, height=30)

        # Contenedor de Entradas
        frame_datos = tk.Frame(self, bg="#C6D9E3", relief="groove", bd=2)
        frame_datos.place(x=10, y=70, width=1080, height=200)

        # Etiquetas de Fecha y Hora en frame_datos
        self.fecha_label = tk.Label(frame_datos, text="", font=("arial",20, "bold"), bg="#C6D9E3")
        self.fecha_label.place(x=750, y=10, width=250, height=30)
        self.hora_label = tk.Label(frame_datos, text="", font=("arial",20, "bold"), bg="#C6D9E3")
        self.hora_label.place(x=750, y=70, width=250, height=30)
        self.actualizar_fecha_hora()

        # Etiquetas y Entradas
        self.campos = {}
        etiquetas = ["Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Celular"]
        for i, etiqueta in enumerate(etiquetas):
            tk.Label(frame_datos, text=f"{etiqueta}:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=10 + i * 40, width=140, height=30)
            entry = tk.Entry(frame_datos, font=("Arial", 12))
            entry.place(x=140, y=10 + i * 40, width=200, height=30)
            self.campos[etiqueta] = entry

        # Botones de Acción
        tk.Button(frame_datos, text="Agregar", font=("Arial", 12), bg="green", fg="white", command=self.agregar_cliente).place(x=400, y=20, width=100, height=30)
        tk.Button(frame_datos, text="Modificar", font=("Arial", 12), bg="orange", fg="white", command=self.modificar_cliente).place(x=400, y=70, width=100, height=30)
        tk.Button(frame_datos, text="Eliminar", font=("Arial", 12), bg="red", fg="white", command=self.eliminar_cliente).place(x=400, y=120, width=100, height=30)

        # Frame para Treeview
        frame_tree = tk.Frame(self, bg="#C6D9E3", relief="ridge", bd=2)
        frame_tree.place(x=10, y=280, width=1080, height=300)

        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tree, orient="vertical")
        scroll_x = ttk.Scrollbar(frame_tree, orient="horizontal")

        # Treeview
        self.tree = ttk.Treeview(
            frame_tree,
            columns=("Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Celular"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        # Configurar columnas
        for col in ("Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Celular"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Configurar y posicionar Scrollbars
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.tree.place(x=0, y=0, width=1060, height=250)
        scroll_y.place(x=1060, y=0, width=20, height=250)
        scroll_x.place(x=0, y=250, width=1060, height=20)

        # Evento para selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cliente)

    def actualizar_fecha_hora(self):
        """Actualizar la fecha y hora en tiempo real."""
        ahora = datetime.now()
        self.fecha_label.config(text=f"Fecha: {ahora.strftime('%Y-%m-%d')}")
        self.hora_label.config(text=f"Hora: {ahora.strftime('%H:%M:%S')}")
        self.after(1000, self.actualizar_fecha_hora)

    def limpiar_campos(self):
        """Limpiar los campos de entrada."""
        for entry in self.campos.values():
            entry.delete(0, tk.END)

    def cargar_clientes(self):
        """Cargar datos de clientes en la tabla."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            self.cursor.execute("SELECT Nombre, Apellido_Paterno, Apellido_Materno, CI, Celular FROM Cliente")
            for cliente in self.cursor.fetchall():
                self.tree.insert("", "end", values=cliente)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {e}")

    def seleccionar_cliente(self, event):
        """Seleccionar un cliente de la tabla y cargar sus datos en las entradas."""
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            self.limpiar_campos()
            for campo, valor in zip(self.campos.values(), valores):
                campo.insert(0, valor)

    def agregar_cliente(self):
        """Agregar un cliente a la base de datos."""
        datos = [campo.get().strip() for campo in self.campos.values()]
        if all(datos):
            try:
                self.cursor.execute(
                    "INSERT INTO Cliente (Nombre, Apellido_Paterno, Apellido_Materno, CI, Celular) VALUES (%s, %s, %s, %s, %s)",
                    datos
                )
                self.db_connection.commit()
                self.cargar_clientes()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
            except Exception as e:
                self.db_connection.rollback()
                messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def modificar_cliente(self):
        """Modificar los datos de un cliente seleccionado."""
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar.")
            return

        datos = [campo.get().strip() for campo in self.campos.values()]
        ci_original = self.tree.item(seleccion, "values")[3]
        
        if all(datos):
            try:
                self.cursor.execute(
                    "UPDATE Cliente SET Nombre=%s, Apellido_Paterno=%s, Apellido_Materno=%s, CI=%s, Celular=%s WHERE CI=%s",
                    (*datos, ci_original)
                )
                self.db_connection.commit()
                self.cargar_clientes()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
            except Exception as e:
                self.db_connection.rollback()
                messagebox.showerror("Error", f"No se pudo modificar el cliente: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def eliminar_cliente(self):
        """Eliminar un cliente seleccionado."""
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return

        ci = self.tree.item(seleccion, "values")[3]
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este cliente?"):
            try:
                self.cursor.execute("DELETE FROM Cliente WHERE CI=%s", (ci,))
                self.db_connection.commit()
                self.cargar_clientes()
                self.limpiar_campos()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            except Exception as e:
                self.db_connection.rollback()
                messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

    def regresar(self):
        """Regresar a la ventana anterior."""
        if messagebox.askyesno("Confirmar", "¿Deseas regresar a la ventana anterior?"):
            self.destroy()

    def salir(self):
        """Salir de la aplicación."""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()