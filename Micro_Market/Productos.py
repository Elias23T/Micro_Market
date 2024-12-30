from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
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

        # Actualizar la fecha y hora
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

        # Treeview para productos
        frame = ttk.Frame(self)
        frame.place(x=300, y=150, width=780, height=450)

        columns = ("Id", "Producto", "Precio", "Costo", "Cantidad", "Estado", "Categoria", "En Promoción", "Precio Descuento")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.column("En Promoción", width=120)
        self.tree.column("Precio Descuento", width=120)

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

        # Marco de botones de acción
        lblframe_botones = LabelFrame(self, text="Opciones", font="arial 14 bold", bg="#C6D9E3")
        lblframe_botones.place(x=10, y=250, width=280, height=350)

        btn_agregar = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_articulo)
        btn_agregar.place(x=20, y=20, width=180, height=40)

        btn_editar = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_articulo)
        btn_editar.place(x=20, y=80, width=180, height=40)

        btn_eliminar = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_articulo)
        btn_eliminar.place(x=20, y=140, width=180, height=40)
        
        btn_desactivar = tk.Button(lblframe_botones, text="Desactivar", font="arial 14 bold", command=self.desactivar_producto)
        btn_desactivar.place(x=20, y=200, width=180, height=40)
        
        btn_agregarPromocion = tk.Button(lblframe_botones, text="Agregar Promoción", font="arial 14 bold", command=self.agregar_promocion_producto)
        btn_agregarPromocion.place(x=20, y=260, width=180, height=40)


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
            """
            SELECT p.Id_Producto, p.NombreProducto, p.PrecioUnitario, p.Costo, p.Stock, 
                   p.Estado, c.NombreCategoria, p.EnPromocion, p.PrecioPromocion
            FROM Productos p
            JOIN Categoria c ON p.Id_Categoria = c.Id_Categoria
            """
        )  
        for articulo in self.cursor.fetchall():  
            estado_texto = "Activo" if articulo[5] == 1 else "Inactivo"  
            promocion_texto = "Sí" if articulo[7] else "No"  
            precio_promocion = articulo[8] if articulo[7] else ""  # Mostrar PrecioPromocion si aplica  

            self.tree.insert("", "end", values=(  
                articulo[0],  # ID  
                articulo[1],  # Producto  
                articulo[2],  # Precio  
                articulo[3],  # Costo  
                articulo[4],  # Stock  
                estado_texto,  # Estado  
                articulo[6],  # Categoría  
                promocion_texto,  # EnPromocion  
                precio_promocion  # PrecioPromocion  
            ))
            
    def filtrar_por_categoria(self, event):
        """Filtrar los productos según la categoría seleccionada."""
        categoria_seleccionada = self.comboboxbuscar.get()
        if categoria_seleccionada:
            self.cursor.execute(
                """
                SELECT p.Id_Producto, p.NombreProducto, p.PrecioUnitario, p.Costo, p.Stock, 
                       p.Estado, c.NombreCategoria, p.EnPromocion, p.PrecioPromocion
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
                estado_texto = "Activo" if producto[5] == 1 else "Inactivo"
                promocion_texto = "Sí" if producto[7] else "No"
                precio_promocion = producto[8] if producto[7] else ""  # Mostrar PrecioPromocion si aplica

                self.tree.insert("", "end", values=(
                    producto[0],  # ID
                    producto[1],  # Producto
                    producto[2],  # Precio
                    producto[3],  # Costo
                    producto[4],  # Stock
                    estado_texto,  # Estado
                    producto[6],  # Categoría
                    promocion_texto,  # EnPromocion
                    precio_promocion  # PrecioPromocion
                ))

    def salir(self):
        """Cerrar la aplicación."""
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()

    def regresar(self):
        """Regresar a la ventana anterior."""
        if messagebox.askyesno("Regresar", "¿Deseas regresar a la ventana anterior?"):
            self.destroy()
            
###############################################3agregar articulo##########################################################################

    def agregar_articulo(self):
        """Abrir ventana para agregar un nuevo artículo."""
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("400x350")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)

        tk.Label(top, text="Producto:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20)
        entry_nombre = ttk.Entry(top, font="arial 12 bold")
        entry_nombre.place(x=150, y=20, width=200)

        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=150, y=60, width=200)

        tk.Label(top, text="Costo:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=150, y=100, width=200)

        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=150, y=140, width=200)

        tk.Label(top, text="Categoría:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180)
        combo_categoria = ttk.Combobox(top, font="arial 12 bold", state="readonly")
        combo_categoria.place(x=150, y=180, width=200)

        # Cargar categorías desde la base de datos
        self.cursor.execute("SELECT NombreCategoria FROM Categoria")
        categorias = [row[0] for row in self.cursor.fetchall()]
        combo_categoria['values'] = categorias

        def guardar():
            nombre = entry_nombre.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            categoria = combo_categoria.get()

            if not all([nombre, precio, costo, stock, categoria]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos")
                return

            self.cursor.execute("SELECT Id_Categoria FROM Categoria WHERE NombreCategoria = %s", (categoria,))
            categoria_id = self.cursor.fetchone()
            if not categoria_id:
                messagebox.showerror("Error", "Categoría no encontrada")
                return

            self.cursor.execute(
                "INSERT INTO Productos (NombreProducto, PrecioUnitario, Costo, Stock, Estado, Id_Categoria, EnPromocion, PrecioPromocion) "
                "VALUES (%s, %s, %s, %s, 1, %s, 0, NULL)",  # Estado=1 (activo), EnPromocion=0 (no), PrecioPromocion=NULL
                (nombre, precio, costo, stock, categoria_id[0]),
            )
            self.db_connection.commit()
            messagebox.showinfo("Éxito", "Artículo agregado")
            top.destroy()
            self.cargar_articulos()

        tk.Button(top, text="Guardar", command=guardar).place(x=80, y=260, width=100)
        tk.Button(top, text="Cancelar", command=top.destroy).place(x=220, y=260, width=100)

##################################################editar articulo########################################################################
    def editar_articulo(self):  
        """Abrir ventana para editar un artículo seleccionado."""  
        item_seleccionado = self.tree.focus()  
        if not item_seleccionado:  
            messagebox.showerror("Error", "Por favor, selecciona un producto para editar.")  
            return  

        valores = self.tree.item(item_seleccionado, "values")  
        if not valores:  
            messagebox.showerror("Error", "No se pudo obtener la información del producto seleccionado.")  
            return  

        producto_id = valores[0]  
        nombre_actual = valores[1]  
        precio_actual = valores[2]  
        costo_actual = valores[3]  
        stock_actual = valores[4]  
        categoria_actual = valores[5]  

        top = tk.Toplevel(self)  
        top.title("Editar Artículo")  
        top.geometry("400x350")  
        top.config(bg="#C6D9E3")  
        top.resizable(False, False)  

        tk.Label(top, text="Producto:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20)  
        entry_nombre = ttk.Entry(top, font="arial 12 bold")  
        entry_nombre.place(x=150, y=20, width=200)  
        entry_nombre.insert(0, nombre_actual)  

        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60)  
        entry_precio = ttk.Entry(top, font="arial 12 bold")  
        entry_precio.place(x=150, y=60, width=200)  
        entry_precio.insert(0, precio_actual)  

        tk.Label(top, text="Costo:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100)  
        entry_costo = ttk.Entry(top, font="arial 12 bold")  
        entry_costo.place(x=150, y=100, width=200)  
        entry_costo.insert(0, costo_actual)  

        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140)  
        entry_stock = ttk.Entry(top, font="arial 12 bold")  
        entry_stock.place(x=150, y=140, width=200)  
        entry_stock.insert(0, stock_actual)  

        tk.Label(top, text="Categoría:", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180)  
        combo_categoria = ttk.Combobox(top, font="arial 12 bold", state="readonly")  
        combo_categoria.place(x=150, y=180, width=200)  

        # Cargar categorías desde la base de datos  
        self.cursor.execute("SELECT NombreCategoria FROM Categoria")  
        categorias = [row[0] for row in self.cursor.fetchall()]  
        combo_categoria['values'] = categorias  
        combo_categoria.set(categoria_actual)  

        def actualizar():  
            nombre = entry_nombre.get()  
            precio = entry_precio.get()  
            costo = entry_costo.get()  
            stock = entry_stock.get()  
            categoria = combo_categoria.get()  

            if not all([nombre, precio, costo, stock, categoria]):  
                messagebox.showerror("Error", "Todos los campos son obligatorios")  
                return  

            try:  
                precio = float(precio)  
                costo = float(costo)  
                stock = int(stock)  
            except ValueError:  
                messagebox.showerror("Error", "Datos inválidos")  
                return  

            self.cursor.execute("SELECT Id_Categoria FROM Categoria WHERE NombreCategoria = %s", (categoria,))  
            categoria_id = self.cursor.fetchone()  
            if not categoria_id:  
                messagebox.showerror("Error", "Categoría no encontrada")  
                return  

            self.cursor.execute(  
                "UPDATE Productos SET NombreProducto = %s, PrecioUnitario = %s, Costo = %s, Stock = %s, Id_Categoria = %s WHERE Id_Producto = %s",  
                (nombre, precio, costo, stock, categoria_id[0], producto_id),  
            )  
            self.db_connection.commit()  
            messagebox.showinfo("Éxito", "Producto actualizado")  
            top.destroy()  
            self.cargar_articulos()  

        tk.Button(top, text="Actualizar", command=actualizar).place(x=80, y=250, width=100)  
        tk.Button(top, text="Cancelar", command=top.destroy).place(x=220, y=250, width=100)
        
####################################eliminar productos ##################################################################3

    def eliminar_articulo(self):  
        """Eliminar un producto seleccionado."""  
        item_seleccionado = self.tree.focus()  
        if not item_seleccionado:  
            messagebox.showerror("Error", "Selecciona un producto para eliminar.")  
            return  

        valores = self.tree.item(item_seleccionado, "values")  
        producto_id = valores[0]  

        # Verificar si el producto tiene stock  
        self.cursor.execute("SELECT Stock FROM Productos WHERE Id_Producto = %s", (producto_id,))  
        stock_actual = self.cursor.fetchone()  
        if stock_actual and stock_actual[0] > 0:  
            messagebox.showwarning("Advertencia", "El producto tiene stock y no puede ser eliminado.")  
            return  

        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?")  
        if respuesta:  
            try:  
                # Eliminar registros relacionados en otras tablas  
                self.cursor.execute("DELETE FROM DetalleDeCompra WHERE Id_Producto = %s", (producto_id,))  
                # Ahora eliminar el producto  
                self.cursor.execute("DELETE FROM Productos WHERE Id_Producto = %s", (producto_id,))  
                self.db_connection.commit()  
                messagebox.showinfo("Éxito", "Producto eliminado")  
                self.cargar_articulos()  
            except Exception as e:  
                messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")  
                
 #####################################33 desactivar producto#########################################################33
                
    def desactivar_producto(self):  
        """Marca a un producto como inactivo."""  
        seleccion = self.tree.focus()  
        if not seleccion:  
            messagebox.showwarning("Advertencia", "Seleccione un producto para desactivar.")  
            return  

        valores = self.tree.item(seleccion, "values")  
        producto_id = valores[0]  

        # Verificar si el producto tiene stock  
        self.cursor.execute("SELECT Stock FROM Productos WHERE Id_Producto = %s", (producto_id,))  
        stock_actual = self.cursor.fetchone()  
        if stock_actual and stock_actual[0] > 0:  
            messagebox.showwarning("Advertencia", "El producto tiene stock y no puede ser desactivado.")  
            return  

        try:  
            # Desactivar el producto  
            self.cursor.execute("UPDATE Productos SET Estado = 0 WHERE Id_Producto = %s", (producto_id,))  
            self.db_connection.commit()  
            self.cargar_articulos()  # Refrescar la lista de productos  
            messagebox.showinfo("Éxito", "Producto desactivado correctamente.")  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo desactivar el producto: {e}")
            
#######################agregar productos a promocion######################################################################################
    def agregar_promocion_producto(self):
        """Abrir ventana para agregar una promoción al producto seleccionado."""
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto para agregar a promociones.")
            return

        # Obtener datos del producto seleccionado
        valores = self.tree.item(seleccion, "values")
        if len(valores) < 3:  # Verificar si los valores se obtuvieron correctamente
            messagebox.showerror("Error", "No se pudieron obtener los datos del producto seleccionado.")
            return

        id_producto = valores[0]  # ID del producto
        nombre_producto = valores[1]  # Nombre del producto
        try:
            precio_producto = float(valores[2])  # Precio del producto
        except ValueError:
            messagebox.showerror("Error", "El precio del producto no es válido.")
            return

        # Crear la ventana emergente
        top = tk.Toplevel(self)
        top.title("Agregar a Promoción")
        top.geometry("480x400")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)

        # Etiqueta de título
        tk.Label(top, text="Agregar a Promoción", font=("Arial", 14, "bold"), bg="#C6D9E3").grid(row=0, column=0, columnspan=2, pady=10)

        # Nombre de la promoción
        tk.Label(top, text="Nombre de la Promoción:", font="arial 12", bg="#C6D9E3").place(x=20, y=60)
        entry_nombre_promocion = ttk.Entry(top, font="arial 12")
        entry_nombre_promocion.place(x=220, y=60, width=240)

        # Producto seleccionado (como texto)
        tk.Label(top, text="Producto Seleccionado:", font="arial 12", bg="#C6D9E3").place(x=20, y=100)
        tk.Label(top, text=nombre_producto, font="arial 12", bg="#C6D9E3").place(x=220, y=100, width=240)

        # Precio del producto (como texto)
        tk.Label(top, text="Precio del Producto:", font="arial 12", bg="#C6D9E3").place(x=20, y=140)
        tk.Label(top, text=f"${precio_producto:.2f}", font="arial 12", bg="#C6D9E3").place(x=220, y=140, width=240)

        # Descuento (%)
        tk.Label(top, text="Descuento (%):", font="arial 12", bg="#C6D9E3").place(x=20, y=180)
        entry_descuento = ttk.Entry(top, font="arial 12")
        entry_descuento.place(x=220, y=180, width=240)

        # Precio con descuento
        tk.Label(top, text="Precio con Descuento:", font="arial 12", bg="#C6D9E3").place(x=20, y=220)
        entry_precio_descuento = ttk.Entry(top, font="arial 12", state="readonly")
        entry_precio_descuento.place(x=220, y=220, width=240)

        # Fecha de inicio (automática)
        tk.Label(top, text="Fecha de Inicio:", font="arial 12", bg="#C6D9E3").place(x=20, y=260)
        fecha_inicio_actual = datetime.now().strftime("%Y-%m-%d")
        tk.Label(top, text=fecha_inicio_actual, font="arial 12", bg="#C6D9E3").place(x=200, y=260, width=240)

        # Fecha de fin
        tk.Label(top, text="Fecha Fin de la Promoción:", font="arial 12", bg="#C6D9E3").place(x=20, y=300)
        fecha_fin = DateEntry(top, font="arial 12", date_pattern="yyyy-MM-dd")
        fecha_fin.place(x=220, y=300, width=240)

        # Función para calcular el precio con descuento
        def calcular_precio_descuento(event):
            try:
                descuento = float(entry_descuento.get())
                if 0 <= descuento <= 100:
                    precio_desc = precio_producto * (1 - descuento / 100)
                    entry_precio_descuento.config(state="normal")
                    entry_precio_descuento.delete(0, tk.END)
                    entry_precio_descuento.insert(0, round(precio_desc, 2))
                    entry_precio_descuento.config(state="readonly")
                else:
                    messagebox.showerror("Error", "El descuento debe estar entre 0% y 100%.")
            except ValueError:
                messagebox.showerror("Error", "El descuento debe ser un número válido.")

        # Asociar el cálculo al campo de descuento
        entry_descuento.bind("<FocusOut>", calcular_precio_descuento)

        # Función para guardar la promoción
        def guardar_promocion():
            nombre_promocion = entry_nombre_promocion.get()
            descuento = entry_descuento.get()
            precio_descuento = entry_precio_descuento.get()
            fecha_final = fecha_fin.get()

            if not nombre_promocion or not descuento or not fecha_final:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                # Insertar en Promociones
                self.cursor.execute(
                    """
                    INSERT INTO Promociones (NombrePromocion, Descuento, FechaInicio, FechaFin, Producto)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (nombre_promocion, float(descuento), fecha_inicio_actual, fecha_final, float(precio_descuento), nombre_producto)
                )
                id_promocion = self.cursor.lastrowid

                # Insertar en ProductosPromocion
                self.cursor.execute(
                    "INSERT INTO ProductosPromocion (Id_Promocion, Id_Producto) VALUES (%s, %s)",
                    (id_promocion, id_producto)
                )

                # Actualizar la tabla Productos
                self.cursor.execute(  
                    "UPDATE Productos SET EnPromocion = 1, PrecioPromocion = %s WHERE Id_Producto = %s",  
                    (float(precio_descuento), id_producto)  
                )

                self.db_connection.commit()
                messagebox.showinfo("Éxito", "Promoción agregada correctamente.")
                top.destroy()
                self.cargar_articulos()  # Refresca la tabla
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la promoción: {e}")

        # Botones
        tk.Button(top, text="Guardar", command=guardar_promocion).place(x=120, y=340, width=100, height=30)
        tk.Button(top, text="Cancelar", command=top.destroy).place(x=260, y=340, width=100, height=30)




