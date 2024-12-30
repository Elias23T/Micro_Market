import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Configuracion(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.pack(fill="both", expand=True)
        self.config(bg="#C6D9E3")
        self.widgets()
    
    def widgets(self):
        # Título
        titulo = tk.Label(self, text="CATEGORIA", font=("Arial", 24, "bold"), bg="#C6D9E3")
        titulo.place(x=400, y=10, width=300, height=30)

        # Botones Regresar y Salir
        self.crear_botones_regresar_salir()

        # Etiquetas de Fecha y Hora
        self.crear_fecha_hora_labels()

        # LabelFrame principal
        Labelframe = tk.LabelFrame(self, text="Gestión de categorías", font=("sans", 12, "bold"), bg="#C6D9E3")
        Labelframe.place(x=40, y=120, width=1000, height=450)
        
        # Etiqueta y entrada para el nombre de la categoría
        lbl_nombre = tk.Label(Labelframe, text="Nombre:", bg="#C6D9E3", font=("sans", 12))
        lbl_nombre.place(x=20, y=30)
        
        self.entry_nombre = tk.Entry(Labelframe, font=("sans", 12), width=40)
        self.entry_nombre.place(x=120, y=30)
        
        # Botón para guardar
        btn_guardar = tk.Button(Labelframe, text="Guardar", command=self.guardar_categoria, bg="#4CAF50", fg="white", font=("sans", 20, "bold"))
        btn_guardar.place(x=700, y=30, width=150, height=50)
        
        # Treeview para mostrar las categorías
        self.tree = ttk.Treeview(Labelframe, columns=("Id", "Nombre"), show="headings", height=15)
        self.tree.heading("Id", text="Id")
        self.tree.heading("Nombre", text="Nombre")
        
        self.tree.column("Id", width=50, anchor="center")
        self.tree.column("Nombre", width=300, anchor="w")
        
        self.tree.place(x=20, y=100, width=600, height=250)
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(Labelframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=620, y=100, height=250)
        
        # Botones para Editar y Eliminar
        btn_editar = tk.Button(Labelframe, text="Editar", command=self.editar_categoria, bg="#FFC107", fg="black", font=("sans", 20, "bold"))
        btn_editar.place(x=700, y=130, width=150, height=50)
        
        btn_eliminar = tk.Button(Labelframe, text="Eliminar", command=self.eliminar_categoria, bg="#F44336", fg="white", font=("sans", 20, "bold"))
        btn_eliminar.place(x=700, y=260, width=150, height=50)
        
        # Cargar datos desde la base de datos
        self.cargar_datos()

    def crear_botones_regresar_salir(self):
        """Crear botones de Regresar y Salir."""
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
        """Crear etiquetas de Fecha y Hora."""
        self.fecha_label = tk.Label(self, text="", font=("Arial", 14), bg="#C6D9E3")
        self.fecha_label.place(x=400, y=50, width=200, height=30)

        self.hora_label = tk.Label(self, text="", font=("Arial", 14), bg="#C6D9E3")
        self.hora_label.place(x=610, y=50, width=200, height=30)

        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        """Actualizar la Fecha y Hora en tiempo real."""
        ahora = datetime.now()
        fecha_actual = ahora.strftime("%Y-%m-%d")
        hora_actual = ahora.strftime("%H:%M:%S")
        self.fecha_label.config(text=f"FECHA: {fecha_actual}")
        self.hora_label.config(text=f"HORA: {hora_actual}")
        self.after(1000, self.actualizar_fecha_hora)

    def guardar_categoria(self):
        nombre = self.entry_nombre.get().strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El campo 'Nombre' no puede estar vacío.")
            return
        
        try:
            self.cursor.execute("INSERT INTO Categoria (NombreCategoria) VALUES (%s)", (nombre,))
            self.db_connection.commit()
            self.cargar_datos()
            self.entry_nombre.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Categoría guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la categoría: {e}")

    def cargar_datos(self):
        """Cargar datos en el Treeview desde la base de datos."""
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        try:
            self.cursor.execute("SELECT Id_Categoria, NombreCategoria FROM Categoria")
            for row in self.cursor.fetchall():
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

    def editar_categoria(self):
        """Editar la categoría seleccionada."""
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para editar.")
            return

        valores = self.tree.item(seleccion, "values")
        id_categoria = valores[0]
        nuevo_nombre = self.entry_nombre.get().strip()

        if not nuevo_nombre:
            messagebox.showwarning("Advertencia", "El campo 'Nombre' no puede estar vacío.")
            return

        try:
            self.cursor.execute("UPDATE Categoria SET NombreCategoria = %s WHERE Id_Categoria = %s", (nuevo_nombre, id_categoria))
            self.db_connection.commit()
            self.cargar_datos()
            self.entry_nombre.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Categoría editada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la categoría: {e}")

    def eliminar_categoria(self):  
        """Eliminar la categoría seleccionada junto con sus productos."""  
        seleccion = self.tree.focus()  
        if not seleccion:  
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar.")  
            return  

        valores = self.tree.item(seleccion, "values")  
        id_categoria = valores[0]  
        nombre_categoria = valores[1]  

        if not messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar la categoría '{nombre_categoria}' junto con todos sus productos?"):  
            return  

        # Ventana para ingresar la fecha actual como contraseña de seguridad  
        top = tk.Toplevel(self)  
        top.title("Confirmación de Seguridad")  
        top.geometry("300x200")  
        top.config(bg="#C6D9E3")  
        top.resizable(False, False)  

        tk.Label(top, text="Ingrese la fecha actual (YYYY-MM-DD):", font="arial 12 bold", bg="#C6D9E3").place(x=10, y=50)  
        entry_fecha = ttk.Entry(top, font="arial 12 bold")  
        entry_fecha.place(x=10, y=90, width=280)  

        def confirmar_eliminacion():  
            fecha_ingresada = entry_fecha.get()  
            fecha_actual = datetime.now().strftime("%Y-%m-%d")  

            if fecha_ingresada != fecha_actual:  
                messagebox.showerror("Error", "Fecha incorrecta. No se puede proceder con la eliminación.")  
                return  

            try:  
                # Eliminar la categoría y sus productos asociados en cascada  
                self.cursor.execute("DELETE FROM Productos WHERE Id_Categoria = %s", (id_categoria,))  
                self.cursor.execute("DELETE FROM Categoria WHERE Id_Categoria = %s", (id_categoria,))  
                self.db_connection.commit()  

                self.cargar_datos()  
                messagebox.showinfo("Éxito", "Categoría y sus productos eliminados correctamente.")  
                top.destroy()  
            except Exception as e:  
                messagebox.showerror("Error", f"No se pudo eliminar la categoría: {e}")  

        tk.Button(top, text="Confirmar", command=confirmar_eliminacion, font="arial 12 bold", bg="green", fg="white").place(x=30, y=140, width=100)  
        tk.Button(top, text="Cancelar", command=top.destroy, font="arial 12 bold", bg="red", fg="white").place(x=170, y=140, width=100)  

    def regresar(self):
        """Regresar a la ventana anterior."""
        if messagebox.askyesno("Regresar", "¿Deseas regresar a la ventana anterior?"):
            self.destroy()

    def salir(self):
        """Salir de la aplicación."""
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()
