from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Ventas(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()

        # Listas para almacenar IDs y nombres
        self.cliente_ids = []
        self.cliente_nombres = []
        self.producto_ids = []
        self.producto_nombres = []
        self.producto_stocks = []
        self.producto_precios = []

        self.widgets()
        self.cargar_clientes()
        self.cargar_productos()
        self.actualizar_fecha_hora()

    def widgets(self):
        # Título de la Ventana
        titulo = tk.Label(self, text="VENTA DE PRODUCTOS", font=("Arial", 18, "bold"))
        titulo.place(x=400, y=10)

        # Información del Cajero
        cajero_label = tk.Label(self, text="Cajero:", font=("Arial", 12))
        cajero_label.place(x=10, y=50)

        # Fecha y Hora
        self.fecha_label = tk.Label(self, text="Fecha:", font=("Arial", 12))
        self.fecha_label.place(x=600, y=50)

        self.hora_label = tk.Label(self, text="Hora:", font=("Arial", 12))
        self.hora_label.place(x=800, y=50)
        
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

        # Contenedor para los campos de Cliente y Producto
        campos_frame = tk.Frame(self, relief="groove", bd=2)
        campos_frame.place(x=10, y=80, width=1080, height=100)

        # Campos de Cliente y Producto dentro del contenedor
        cliente_label = tk.Label(campos_frame, text="Cliente:", font=("Arial", 12))
        cliente_label.place(x=10, y=10)

        self.cliente_combo = ttk.Combobox(campos_frame, state="readonly")
        self.cliente_combo.place(x=80, y=10, width=200, height=30)

        producto_label = tk.Label(campos_frame, text="Producto:", font=("Arial", 12))
        producto_label.place(x=10, y=50)

        self.producto_combo = ttk.Combobox(campos_frame, state="readonly")
        self.producto_combo.place(x=80, y=50, width=200, height=30)

        stock_label = tk.Label(campos_frame, text="Stock:", font=("Arial", 12))
        stock_label.place(x=300, y=50)

        self.stock_label = tk.Label(campos_frame, text="0", font=("Arial", 12))
        self.stock_label.place(x=360, y=50)

        cantidad_label = tk.Label(campos_frame, text="Cantidad:", font=("Arial", 12))
        cantidad_label.place(x=300, y=10)

        self.cantidad_entry = tk.Entry(campos_frame)
        self.cantidad_entry.place(x=380, y=10, width=100, height=30)

        # Botones principales
        agregar_btn = tk.Button(self, text="Agregar", font=("Arial", 12), bg="green", fg="white", command=self.agregar_producto)
        agregar_btn.place(x=500, y=100, width=100)

        editar_btn = tk.Button(self, text="Editar", font=("Arial", 12), bg="blue", fg="white")
        editar_btn.place(x=610, y=100, width=100)

        eliminar_btn = tk.Button(self, text="Eliminar", font=("Arial", 12), bg="red", fg="white")
        eliminar_btn.place(x=720, y=100, width=100)

        limpiar_btn = tk.Button(self, text="Limpiar", font=("Arial", 12), bg="orange", fg="white")
        limpiar_btn.place(x=830, y=100, width=100)

        # Tabla de datos
        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tree.place(x=10, y=200, width=1080, height=300)

        # Encabezados de la tabla
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Total", text="Total")

        # Ajustar el ancho de las columnas
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Cliente", width=200, anchor="center")
        self.tree.column("Producto", width=200, anchor="center")
        self.tree.column("Precio", width=100, anchor="center")
        self.tree.column("Cantidad", width=100, anchor="center")
        self.tree.column("Total", width=100, anchor="center")

        # Botones inferiores
        pagar_btn = tk.Button(self, text="Pagar", font=("Arial", 12), bg="green", fg="white", command=self.registrar_venta)
        pagar_btn.place(x=10, y=520, width=150)

        ver_ventas_btn = tk.Button(self, text="Historial de ventas", font=("Arial", 12), bg="blue", fg="white")
        ver_ventas_btn.place(x=180, y=520, width=250)

        impri_factura_btn = tk.Button(self, text="Imprimir Factura", font=("Arial", 12), bg="orange", fg="white")
        impri_factura_btn.place(x=480, y=520, width=200)

        # Precio a pagar
        self.precio_total = 0
        self.precio_label = tk.Label(self, text="Precio a Pagar: 0", font=("Arial", 14, "bold"), fg="gold")
        self.precio_label.place(x=800, y=520)

    def salir(self):
        # Confirmar salida
        respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir del programa?")
        if respuesta:
            self.master.destroy()  # Cierra la ventana principal
            
    def regresar(self):
        # Confirmar regreso
        respuesta = messagebox.askyesno("Regresar", "¿Estás seguro de que deseas regresar?")
        if respuesta:
            self.destroy()  # Cierra el frame actual

    def registrar_venta(self):
        try:
            if not self.tree.get_children():
                messagebox.showerror("Error", "No hay productos en la venta.")
                return

            # Mostrar cuadro de confirmación
            respuesta = messagebox.askyesno("Confirmar Venta", "¿Deseas confirmar la venta?")
            if not respuesta:
                return  # Si el usuario cancela, no se continúa con la venta

            indice_cliente = self.cliente_combo.current()
            cliente_id = self.cliente_ids[indice_cliente]
            empleado_id = self.obtener_id_empleado()

            # Registrar la venta
            self.cursor.execute("""
                INSERT INTO Ventas (FechaVenta, MontoTotal, Id_Empleado, Id_Cliente)
                VALUES (?, ?, ?, ?)
            """, (datetime.now().date(), self.precio_total, empleado_id, cliente_id))
            venta_id = self.cursor.lastrowid

            # Registrar detalles de venta y actualizar stock
            for item in self.tree.get_children():
                producto_id, _, _, precio_unitario, cantidad, subtotal = self.tree.item(item, "values")
                producto_id = int(producto_id)
                precio_unitario = float(precio_unitario)
                cantidad = int(cantidad)
                subtotal = float(subtotal)

                # Registrar detalle de venta
                self.cursor.execute("""
                   INSERT INTO DetalleVenta (Id_Venta, Id_Producto, Cantidad, PrecioUnitario, TotalVenta)
                   VALUES (?, ?, ?, ?, ?)
                """, (venta_id, producto_id, cantidad, precio_unitario, subtotal))

                # Actualizar stock
                self.cursor.execute("""
                   UPDATE Productos
                   SET Stock = Stock - ?
                   WHERE Id_Producto = ?
                """, (cantidad, producto_id))

            self.db_connection.commit()
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")

            # Limpiar la tabla y resetear el precio total
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.precio_total = 0
            self.precio_label.config(text="Precio a Pagar: 0")

            # Recargar productos para actualizar stocks
            self.cargar_productos()
            self.stock_label.config(text="0")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def actualizar_fecha_hora(self):
        ahora = datetime.now()
        self.fecha_label.config(text=f"Fecha: {ahora.strftime('%d-%m-%Y')}")
        self.hora_label.config(text=f"Hora: {ahora.strftime('%H:%M:%S')}")
        self.after(1000, self.actualizar_fecha_hora)

    def cargar_clientes(self):
        self.cursor.execute("SELECT Id_Cliente, Nombre, Apellido_Paterno, Apellido_Materno FROM Cliente")
        clientes = self.cursor.fetchall()
        self.cliente_ids = [cliente[0] for cliente in clientes]
        self.cliente_nombres = [f"{cliente[1]} {cliente[2]} {cliente[3]}" for cliente in clientes]
        self.cliente_combo['values'] = self.cliente_nombres

    def cargar_productos(self):
        self.cursor.execute("SELECT Id_Producto, NombreProducto, Stock, PrecioUnitario FROM Productos WHERE Stock > 0")
        productos = self.cursor.fetchall()
        self.producto_ids = [producto[0] for producto in productos]
        self.producto_nombres = [producto[1] for producto in productos]
        self.producto_stocks = [producto[2] for producto in productos]
        self.producto_precios = [producto[3] for producto in productos]
        self.producto_combo['values'] = self.producto_nombres

        # Vincular evento para actualizar el stock al seleccionar un producto
        self.producto_combo.bind("<<ComboboxSelected>>", self.mostrar_stock)

    def mostrar_stock(self, event):
        try:
            indice = self.producto_combo.current()
            stock = self.producto_stocks[indice]
            self.stock_label.config(text=str(stock))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener el stock: {e}")

    def agregar_producto(self):
        try:
            indice_producto = self.producto_combo.current()
            producto_id = self.producto_ids[indice_producto]
            producto_nombre = self.producto_nombres[indice_producto]
            stock_disponible = self.producto_stocks[indice_producto]
            precio_unitario = self.producto_precios[indice_producto]

            cantidad = int(self.cantidad_entry.get())

            if cantidad > stock_disponible:
                messagebox.showerror("Error", "Stock insuficiente.")
                return

            subtotal = cantidad * precio_unitario
            self.precio_total += subtotal
            self.precio_label.config(text=f"Precio a Pagar: {self.precio_total}")

            # Obtener el nombre del cliente seleccionado
            indice_cliente = self.cliente_combo.current()
            cliente_nombre = self.cliente_nombres[indice_cliente]

            # Agregar a la tabla
            self.tree.insert("", "end", values=(producto_id, cliente_nombre, producto_nombre, precio_unitario, cantidad, subtotal))

            # Limpiar entrada de cantidad
            self.cantidad_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa una cantidad válida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un problema: {e}")

    def obtener_id_empleado(self):
        # Implementa esta función para obtener el ID del empleado logueado
        return 1

    def cargar_articulos(self):
        pass
