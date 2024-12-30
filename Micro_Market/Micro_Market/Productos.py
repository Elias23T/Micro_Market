from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pymssql as DB  # Conexión con pymssql


class Productos(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()

        # Inicialización de widgets
        self.widgets()
        self.actualizar_categorias_combobox()
        self.cargar_articulos()

    def widgets(self):
        """Crear y organizar los widgets de la interfaz."""
        # Título
        titulo = tk.Label(self, text="PRODUCTOS", font=("Arial", 24, "bold"))
        titulo.place(x=400, y=15, width=250, height=25)

        # Etiquetas para Fecha y Hora
        self.fecha_label = tk.Label(self, text="", font=("Arial", 20, "bold"))
        self.fecha_label.place(x=100, y=100, width=250, height=22)

        self.hora_label = tk.Label(self, text="", font=("Arial", 20, "bold"))
        self.hora_label.place(x=600, y=100, width=250, height=22)

        # Llamar a la función para actualizar la fecha y hora
        self.actualizar_fecha_hora()

        # Botones principales
        boton_salir = tk.Button(
            self,
            text="SALIR",
            command=self.salir,
            font=("Arial", 20, "bold"),
            bg="RED",
            fg="white",
            relief="raised",
        )
        boton_salir.place(x=980, y=10, width=100, height=40)

        boton_regresar = tk.Button(
            self,
            text="REGRESAR",
            command=self.regresar,
            font=("Arial", 20, "bold"),
            bg="blue",
            fg="white",
            relief="raised",
        )
        boton_regresar.place(x=10, y=10, width=200, height=40)

        # Marco para Treeview
        frame = ttk.Frame(self)
        frame.place(x=300, y=150, width=780, height=450)

        # Configuración de Treeview
        columns = ("Id", "Producto", "Precio", "Cantidad", "FechaVencimiento", "Categoria")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.column("Id", width=50)
        self.tree.column("Producto", width=150)
        self.tree.column("Precio", width=150)
        self.tree.column("Cantidad", width=100)
        self.tree.column("FechaVencimiento", width=100)
        self.tree.column("Categoria", width=100)

        # Scrollbar para Treeview
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Marco de búsqueda
        lblframe_buscar = LabelFrame(self, text="Buscar por Categoría", font="arial 14 bold", bg="#C6D9E3")
        lblframe_buscar.place(x=10, y=150, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.filtrar_por_categoria)

        # Marco de botones de acciones
        lblframe_botones = LabelFrame(self, text="Opciones", font="arial 14 bold", bg="#C6D9E3")
        lblframe_botones.place(x=10, y=250, width=280, height=350)

        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_articulo)
        btn_agregar.place(x=20, y=20, width=180, height=40)

        btn_editar = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_articulo)
        btn_editar.place(x=20, y=80, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_articulo)
        btn_eliminar.place(x=20, y=140, width=180, height=40)

    def actualizar_fecha_hora(self):
        """Actualizar la fecha y la hora en tiempo real."""
        ahora = datetime.now()
        fecha_actual = ahora.strftime("%Y-%m-%d")
        hora_actual = ahora.strftime("%H:%M:%S")

        # Actualizar las etiquetas
        self.fecha_label.config(text=f"FECHA: {fecha_actual}")
        self.hora_label.config(text=f"HORA: {hora_actual}")

        # Llamar a esta función de nuevo después de 1000ms (1 segundo)
        self.after(1000, self.actualizar_fecha_hora)

    def actualizar_categorias_combobox(self):
        """Actualizar las categorías disponibles en el combobox."""
        self.cursor.execute("SELECT NombreCategoria FROM Categoria")
        categorias = [row[0] for row in self.cursor.fetchall()]
        self.comboboxbuscar["values"] = categorias

    def cargar_articulos(self):
        """Cargar todos los artículos en el Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute(
            "SELECT p.Id_Producto, p.NombreProducto, p.PrecioUnitario, p.Stock, p.FechaVencimiento, c.NombreCategoria "
            "FROM Productos p JOIN Categoria c ON p.Id_Categoria = c.Id_Categoria"
        )
        for articulo in self.cursor.fetchall():
            self.tree.insert("", "end", values=articulo)

    def filtrar_por_categoria(self, event):
        """Filtrar los productos según la categoría seleccionada."""
        categoria_seleccionada = self.comboboxbuscar.get()
        if categoria_seleccionada:
            self.cursor.execute(
                """
                SELECT p.Id_Producto, p.NombreProducto, p.PrecioUnitario, p.Stock, p.FechaVencimiento, c.NombreCategoria
                FROM Productos p
                JOIN Categoria c ON p.Id_Categoria = c.Id_Categoria
                WHERE c.NombreCategoria = %s
                """,
                (categoria_seleccionada,)
            )
            productos = self.cursor.fetchall()

            # Limpiar el Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Agregar los productos filtrados al Treeview
            for producto in productos:
                self.tree.insert("", "end", values=producto)

    def salir(self):
        """Cerrar la aplicación."""
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()

    def regresar(self):
        """Regresar a la ventana anterior."""
        if messagebox.askyesno("Regresar", "¿Deseas regresar a la ventana anterior?"):
            self.destroy()

    def agregar_articulo(self):
        """Abrir ventana para agregar un nuevo artículo."""
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("400x300")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)

        tk.Label(top, text="Producto:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20)
        entry_nombre = ttk.Entry(top, font="arial 12 bold")
        entry_nombre.place(x=150, y=20, width=200)

        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=150, y=60, width=200)

        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=150, y=100, width=200)

        tk.Label(top, text="FechaVencimiento (YYYY-MM-DD):", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140)
        entry_fecha = ttk.Entry(top, font="arial 12 bold")
        entry_fecha.place(x=150, y=140, width=200)

        tk.Label(top, text="Categoria:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180)
        entry_categoria = ttk.Entry(top, font="arial 12 bold")
        entry_categoria.place(x=150, y=180, width=200)

        def guardar():
            nombre = entry_nombre.get()
            precio = entry_precio.get()
            stock = entry_stock.get()
            fecha = entry_fecha.get()
            categoria = entry_categoria.get()

            if not all([nombre, precio, stock, fecha, categoria]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                precio = float(precio)
                stock = int(stock)
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos")
                return

            self.cursor.execute("SELECT Id_Categoria FROM Categoria WHERE NombreCategoria = %s", (categoria,))
            categoria_id = self.cursor.fetchone()
            if not categoria_id:
                messagebox.showerror("Error", "Categoría no encontrada")
                return

            self.cursor.execute(
                "INSERT INTO Productos (NombreProducto, PrecioUnitario, Stock, FechaVencimiento, Id_Categoria) VALUES (%s, %s, %s, %s, %s)",
                (nombre, precio, stock, fecha, categoria_id[0]),
            )
            self.db_connection.commit()
            messagebox.showinfo("Éxito", "Artículo agregado")
            top.destroy()
            self.cargar_articulos()

        tk.Button(top, text="Guardar", command=guardar).place(x=80, y=220, width=100)
        tk.Button(top, text="Cancelar", command=top.destroy).place(x=220, y=220, width=100)

    def editar_articulo(self):
        """Abrir ventana para editar un artículo seleccionado."""
        # Obtener el producto seleccionado en el Treeview
        item_seleccionado = self.tree.focus()
        if not item_seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona un producto para editar.")
            return

        valores = self.tree.item(item_seleccionado, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información del producto seleccionado.")
            return

        # Extraer datos del producto seleccionado
        producto_id = valores[0]
        nombre_actual = valores[1]
        precio_actual = valores[2]
        stock_actual = valores[3]
        fecha_actual = valores[4]
        categoria_actual = valores[5]

        # Crear ventana para editar
        top = tk.Toplevel(self)
        top.title("Editar Artículo")
        top.geometry("400x300")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)

        tk.Label(top, text="Producto:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20)
        entry_nombre = ttk.Entry(top, font="arial 12 bold")
        entry_nombre.place(x=150, y=20, width=200)
        entry_nombre.insert(0, nombre_actual)  # Prellenar con el valor actual

        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=150, y=60, width=200)
        entry_precio.insert(0, precio_actual)  # Prellenar con el valor actual

        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=150, y=100, width=200)
        entry_stock.insert(0, stock_actual)  # Prellenar con el valor actual

        tk.Label(top, text="FechaVencimiento (YYYY-MM-DD):", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140)
        entry_fecha = ttk.Entry(top, font="arial 12 bold")
        entry_fecha.place(x=150, y=140, width=200)
        entry_fecha.insert(0, fecha_actual)  # Prellenar con el valor actual

        tk.Label(top, text="Categoria:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180)
        entry_categoria = ttk.Entry(top, font="arial 12 bold")
        entry_categoria.place(x=150, y=180, width=200)
        entry_categoria.insert(0, categoria_actual)  # Prellenar con el valor actual

        def actualizar():
            """Actualizar los datos del producto seleccionado."""
            nombre = entry_nombre.get()
            precio = entry_precio.get()
            stock = entry_stock.get()
            fecha = entry_fecha.get()
            categoria = entry_categoria.get()

            if not all([nombre, precio, stock, fecha, categoria]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                precio = float(precio)
                stock = int(stock)
                fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos. Revisa los campos.")
                return

        # Verificar si la categoría existe en la base de datos
            self.cursor.execute("SELECT Id_Categoria FROM Categoria WHERE NombreCategoria = %s", (categoria,))
            categoria_id = self.cursor.fetchone()
            if not categoria_id:
               messagebox.showerror("Error", f"La categoría '{categoria}' no existe.")
               return

            # Actualizar el producto en la base de datos
            try:
                self.cursor.execute(
                    """
                    UPDATE Productos
                    SET NombreProducto = %s, PrecioUnitario = %s, Stock = %s, FechaVencimiento = %s, Id_Categoria = %s
                    WHERE Id_Producto = %s
                    """,
                    (nombre, precio, stock, fecha, categoria_id[0], producto_id),
                )
                self.db_connection.commit()
                messagebox.showinfo("Éxito", "El producto ha sido actualizado correctamente.")
                top.destroy()
                self.cargar_articulos()  # Recargar el Treeview
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

        tk.Button(top, text="Actualizar", font="arial 12 bold", command=actualizar).place(x=80, y=220, width=100)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=220, y=220, width=100)
        
    def eliminar_articulo(self):
        """Eliminar un producto seleccionado del Treeview y la base de datos."""
    # Obtener el producto seleccionado en el Treeview
        item_seleccionado = self.tree.focus()
        if not item_seleccionado:
           messagebox.showerror("Error", "Por favor, selecciona un producto para eliminar.")
           return

        valores = self.tree.item(item_seleccionado, "values")
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información del producto seleccionado.")
            return

        # Extraer datos del producto seleccionado
        producto_id = valores[0]
        nombre_producto = valores[1]
        precio_producto = valores[2]

        # Mostrar un cuadro de confirmación
        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el producto '{nombre_producto}' con precio {precio_producto}?"
        )

        if respuesta:  # Si el usuario confirma
            try:
                # Eliminar el producto de la base de datos
                self.cursor.execute("DELETE FROM Productos WHERE Id_Producto = %s", (producto_id,))
                self.db_connection.commit()
                messagebox.showinfo("Éxito", f"El producto '{nombre_producto}' ha sido eliminado correctamente.")
                self.cargar_articulos()  # Recargar el Treeview
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        else:
            messagebox.showinfo("Cancelado", "La eliminación del producto ha sido cancelada.")


