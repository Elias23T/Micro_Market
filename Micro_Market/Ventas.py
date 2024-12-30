import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from fpdf import FPDF

class Ventas(tk.Frame):
    def __init__(self, padre, db_connection,username, user_role):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.username = username
        self.user_role = user_role

        # Inicializar listas de datos
        self.producto_promocion = []
        self.cliente_ids = []
        self.cliente_nombres = []
        self.producto_ids = []
        self.producto_nombres = []
        self.producto_stocks = []
        self.producto_precios = []
        self.precio_total = 0  # Total de la venta

        # Crear widgets e inicializar la interfaz
        self.crear_widgets()

        # Cargar datos de la base de datos
        self.cargar_clientes()
        self.cargar_productos()
        self.actualizar_fecha_hora()

    def crear_widgets(self):
        """Crea y organiza todos los widgets de la ventana."""
        # Título de la ventana
        titulo = tk.Label(self, text="VENTA DE PRODUCTOS", font=("Arial", 18, "bold"))
        titulo.place(x=400, y=10)

        # Botones principales
        boton_salir = tk.Button(
            self, text="SALIR", command=self.destroy,
            font=("Arial", 20, "bold"), bg="red", fg="white", relief="raised"
        )
        boton_salir.place(x=980, y=10, width=100, height=40)

        boton_regresar = tk.Button(
            self, text="REGRESAR", command=self.regresar,
            font=("Arial", 20, "bold"), bg="blue", fg="white", relief="raised"
        )
        boton_regresar.place(x=10, y=10, width=200, height=40)

        # Fecha y hora
        self.fecha_label = tk.Label(self, text="Fecha: --/--/----", font=("Arial", 12))
        self.fecha_label.place(x=600, y=50)

        self.hora_label = tk.Label(self, text="Hora: --:--:--", font=("Arial", 12))
        self.hora_label.place(x=800, y=50)

        # Contenedor de campos
        campos_frame = tk.Frame(self, relief="groove", bd=2)
        campos_frame.place(x=10, y=80, width=1080, height=150)

        # Campos de cliente
        cliente_label = tk.Label(campos_frame, text="Cliente:", font=("Arial", 12))
        cliente_label.place(x=10, y=10)

        self.cliente_combo = ttk.Combobox(campos_frame, state="readonly")
        self.cliente_combo.place(x=80, y=10, width=300, height=30)

        # Campos de producto
        producto_label = tk.Label(campos_frame, text="Producto:", font=("Arial", 12))
        producto_label.place(x=10, y=50)

        self.producto_combo = ttk.Combobox(campos_frame, state="readonly")
        self.producto_combo.place(x=80, y=50, width=200, height=30)

        # Mostrar stock del producto
        stock_label = tk.Label(campos_frame, text="Stock:", font=("Arial", 12))
        stock_label.place(x=300, y=50)

        self.stock_label = tk.Label(campos_frame, text="0", font=("Arial", 12))
        self.stock_label.place(x=360, y=50)

        # Campo para cantidad
        cantidad_label = tk.Label(campos_frame, text="Cantidad:", font=("Arial", 12))
        cantidad_label.place(x=450, y=10)

        self.cantidad_entry = tk.Entry(campos_frame)
        self.cantidad_entry.place(x=550, y=10, width=100, height=30)

        # Agregar Combobox para tipo de comprobante
        comprobante_label = tk.Label(campos_frame, text="Tipo Comprobante:", font=("Arial", 12))
        comprobante_label.place(x=450, y=50)

        self.comprobante_combo = ttk.Combobox(
            campos_frame,
            state="readonly",
            values=["FACTURA DE VENTA", "BOLETA DE VENTA", "SIN COMPROBANTE DE VENTA"]
        )
        self.comprobante_combo.place(x=600, y=50, width=250, height=30)
        
        # Botón para agregar producto
        agregar_btn = tk.Button(
            self, text="Agregar", font=("Arial", 12), 
            bg="green", fg="white", command=self.agregar_producto
        )
        agregar_btn.place(x=750, y=200, width=100)

        # Botón para generar comprobante
        generar_comprobante_btn = tk.Button(
            self, text="Generar Comprobante", font=("Arial", 12),
            bg="orange", fg="white", command=self.generar_comprobante
        )
        generar_comprobante_btn.place(x=870, y=200, width=200, height=30)

        # Tabla de datos
        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Producto", "Promoción", "Precio", "PrecioPromocion", "Cantidad", "Total"), show="headings")
        self.tree.place(x=10, y=250, width=1080, height=250)

        # Encabezados de la tabla
        for col, text in zip(("ID", "Cliente", "Producto", "Promoción", "Precio", "PrecioPromocion", "Cantidad", "Total"),
                     ("ID", "Cliente", "Producto", "Promoción", "Precio", "Precio Promoción", "Cantidad", "Total")):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120, anchor="center")

        # Botones inferiores
        pagar_btn = tk.Button(
            self, text="Pagar", font=("Arial", 12), 
            bg="green", fg="white", command=self.realizar_pago
        )
        pagar_btn.place(x=10, y=520, width=150)

        ver_ventas_btn = tk.Button(
            self, text="Historial de ventas", font=("Arial", 12), 
            bg="blue", fg="white", command=self.mostrar_historial_ventas
        )
        ver_ventas_btn.place(x=180, y=520, width=250)

        # Precio a pagar
        self.precio_label = tk.Label(
            self, text="Precio a Pagar: 0", 
            font=("Arial", 14, "bold"), fg="gold"
        )
        self.precio_label.place(x=800, y=520)

    def actualizar_fecha_hora(self):
        """Actualiza la fecha y hora en tiempo real."""
        ahora = datetime.now()
        self.fecha_label.config(text=f"Fecha: {ahora.strftime('%d-%m-%Y')}")
        self.hora_label.config(text=f"Hora: {ahora.strftime('%H:%M:%S')}")
        self.after(1000, self.actualizar_fecha_hora)

    def cargar_clientes(self):
        """Carga los clientes desde la base de datos."""
        try:
            self.cursor.execute("SELECT Id_Cliente, Nombre, Apellido_Paterno, Apellido_Materno FROM Cliente")
            clientes = self.cursor.fetchall()
            self.cliente_ids = [c[0] for c in clientes]
            self.cliente_nombres = [f"{c[1]} {c[2]} {c[3]}" for c in clientes]
            self.cliente_combo['values'] = self.cliente_nombres
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar clientes: {e}")

    def cargar_productos(self):
        """Carga los productos con stock disponible y verifica si están en promoción."""
        try:
            self.cursor.execute("""
                SELECT Id_Producto, NombreProducto, Stock, PrecioUnitario, EnPromocion, PrecioPromocion
                FROM Productos
                WHERE Stock > 0
            """)
            productos = self.cursor.fetchall()
             # Limpiar las listas antes de llenarlas
            self.producto_ids = []
            self.producto_nombres = []
            self.producto_stocks = []
            self.producto_precios_unitarios = []
            self.producto_precios_promocion = []
            self.producto_promocion = []

            # Llenar las listas de manera consistente
            for p in productos:
                self.producto_ids.append(p[0])
                self.producto_nombres.append(p[1])
                self.producto_stocks.append(p[2])
                self.producto_precios_unitarios.append(p[3])
                self.producto_precios_promocion.append(p[5] if p[4] else 0)
                self.producto_promocion.append("Sí" if p[4] else "No")

            # Actualizar el Combobox
            self.producto_combo['values'] = self.producto_nombres
            self.producto_combo.bind("<<ComboboxSelected>>", self.mostrar_stock_producto)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")

    def mostrar_stock_producto(self, event=None):
        """Muestra el stock del producto seleccionado."""
        indice = self.producto_combo.current()
        if indice != -1:
            self.stock_label.config(text=str(self.producto_stocks[indice]))

    def agregar_producto(self):  
        """Agrega un producto a la venta o actualiza su cantidad si ya está en la tabla."""  
        try:  
            indice_producto = self.producto_combo.current()  
            if indice_producto == -1:  
                messagebox.showerror("Error", "Seleccione un producto válido.")  
                return  

            if not self.cliente_combo.get():  
                messagebox.showerror("Error", "Seleccione un cliente.")  
                return  

            cantidad = int(self.cantidad_entry.get())  
            if cantidad <= 0 or cantidad > self.producto_stocks[indice_producto]:  
                messagebox.showerror("Error", "Cantidad no válida o insuficiente stock.")  
                return  

            producto_id = self.producto_ids[indice_producto]  
            promocion = self.producto_promocion[indice_producto]  
            
            # Obtener precio_unitario directamente de la base de datos
            self.cursor.execute("SELECT PrecioUnitario FROM Productos WHERE Id_Producto = %s", (producto_id,))
            precio_unitario = self.cursor.fetchone()[0]  # PrecioUnitario directo desde la tabla
            
            precio_promocion = self.producto_precios_promocion[indice_producto]  
            precio_a_usar = precio_promocion if promocion == "Sí" else precio_unitario
            subtotal = cantidad * precio_a_usar

            # Actualizar el stock local
            self.producto_stocks[indice_producto] -= cantidad
            self.stock_label.config(text=str(self.producto_stocks[indice_producto]))  

            # Verificar si el producto ya está en la tabla  
            for item in self.tree.get_children():  
                values = self.tree.item(item, "values")  
                if int(values[0]) == producto_id:  # Si el ID del producto coincide  
                    nueva_cantidad = int(values[6]) + cantidad  
                    nuevo_subtotal = nueva_cantidad * precio_a_usar  
                    self.tree.item(item, values=(  
                        producto_id,  
                        self.cliente_combo.get(),  
                        self.producto_nombres[indice_producto],  
                        promocion,  
                        f"{precio_unitario:.2f}",  
                        f"{precio_promocion:.2f}" if promocion == "Sí" else "0.00",  
                        nueva_cantidad,  
                        f"{nuevo_subtotal:.2f}",  
                    ))  
                    self.precio_total += subtotal  
                    self.precio_label.config(text=f"Precio a Pagar: {self.precio_total:.2f}")  
                    return  

            # Si no está en la tabla, agregar como nuevo producto  
            self.tree.insert("", "end", values=(  
                producto_id,  
                self.cliente_combo.get(),  
                self.producto_nombres[indice_producto],  
                promocion,  
                f"{precio_unitario:.2f}",  
                f"{precio_promocion:.2f}" if promocion == "Sí" else "0.00",  
                cantidad,  
                f"{subtotal:.2f}",  
            ))  
            self.precio_total += subtotal  
            self.precio_label.config(text=f"Precio a Pagar: {self.precio_total:.2f}")  

            self.cantidad_entry.delete(0, tk.END)  

        except ValueError:  
            messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")  
        except Exception as e:  
            messagebox.showerror("Error", f"Error al agregar producto: {e}")    

    def realizar_pago(self):
        """Realiza el proceso de pago de la venta."""
        if self.precio_total == 0:
            messagebox.showerror("Error", "No hay productos en la venta.")
            return

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("300x200")
        ventana_pago.resizable(False, False)

        tk.Label(ventana_pago, text="Realizar pago", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(ventana_pago, text=f"Total a pagar: {float(self.precio_total)}", font=("Arial", 12)).pack(pady=5)

        monto_entry = tk.Entry(ventana_pago, font=("Arial", 12))
        monto_entry.pack(pady=5)

        def confirmar_pago():
            try:
                monto_pagado = float(monto_entry.get())
                total_a_pagar = float(self.precio_total)

                if monto_pagado < total_a_pagar:
                    messagebox.showerror("Error", "El monto pagado es insuficiente.")
                    return

                cambio = monto_pagado - total_a_pagar
                self.registrar_venta()

                messagebox.showinfo(
                    "Pago Realizado",
                    f"Total: {total_a_pagar}\nPagado: {monto_pagado}\nCambio: {cambio:.2f}"
                )

                # Reiniciar la tabla y total
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.precio_total = 0
                self.precio_label.config(text="Precio a Pagar: 0")

                ventana_pago.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingrese un monto válido.")
            except Exception as e:
                messagebox.showerror("Error", f"Error durante el pago: {e}")

        confirmar_btn = tk.Button(ventana_pago, text="Confirmar Pago", font=("Arial", 12), bg="green", fg="white", command=confirmar_pago)
        confirmar_btn.pack(pady=10)

    def registrar_venta(self):
        """Registra la venta en la base de datos."""
        try:
            if not self.tree.get_children():
                messagebox.showerror("Error", "No hay productos en la venta.")
                return

            indice_cliente = self.cliente_combo.current()
            if indice_cliente == -1:
                messagebox.showerror("Error", "Seleccione un cliente válido.")
                return

            cliente_id = self.cliente_ids[indice_cliente]

            # Insertar la venta en la tabla Ventas
            query_venta = """
                INSERT INTO Ventas (FechaVenta, MontoTotal, Id_Empleado, Id_Cliente)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query_venta, (
                datetime.now().strftime('%Y-%m-%d'),
                self.precio_total,
                1,  # Cambiar al empleado actual
                cliente_id,
            ))

            # Obtener el ID de la venta creada
            self.cursor.execute("SELECT SCOPE_IDENTITY()")
            venta_id = self.cursor.fetchone()[0]

            # Insertar detalles de venta
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                query_detalle = """
                    INSERT INTO DetalleVenta (Id_Venta, Id_Producto, Cantidad, PrecioUnitario, TotalVenta)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.cursor.execute(query_detalle, (
                    venta_id,
                    int(values[0]),  # Id_Producto
                    float(values[6]),  # Cantidad
                    float(values[4]),  # PrecioUnitario
                    float(values[7]),  # TotalVenta
                ))

                # Actualizar el stock del producto
                query_stock = """
                    UPDATE Productos
                    SET Stock = Stock - %s
                    WHERE Id_Producto = %s
                """
                self.cursor.execute(query_stock, (
                    int(values[6]),  # Cantidad
                    int(values[0]),  # Id_Producto
                ))

            # Confirmar la transacción
            self.db_connection.commit()
            messagebox.showinfo("Éxito", "Venta registrada correctamente.")

            # Reiniciar la tabla y el total
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.precio_total = 0
            self.precio_label.config(text="Precio a Pagar: 0")

            # Recargar productos para reflejar el cambio en stock
            self.cargar_productos()

        except Exception as e:
            # Revertir transacción en caso de error
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")

    def generar_comprobante(self):  
        """Genera un comprobante en formato PDF según el tipo seleccionado."""  
        tipo_comprobante = self.comprobante_combo.get()  
        if not tipo_comprobante:  
            messagebox.showerror("Error", "Seleccione un tipo de comprobante.")  
            return  

        if not self.tree.get_children():  
            messagebox.showerror("Error", "No hay productos en la venta.")  
            return  

        cliente = self.cliente_combo.get()  
        if not cliente:  
            messagebox.showerror("Error", "Seleccione un cliente válido.")  
            return  

        try:  
            # Obtener el nombre de la vendedora  
            query = """  
                SELECT E.Nombre, E.Apellido_Paterno, E.Apellido_Materno  
                FROM Empleado E  
                INNER JOIN Usuario U ON E.Id_Usuario = U.Id_Usuario  
                WHERE U.NombreUsuario = %s  
            """  
            self.cursor.execute(query, (self.username,))  
            resultado = self.cursor.fetchone()  
            if resultado:  
                vendedora = f"{resultado[0]} {resultado[1]} {resultado[2]}"  
            else:  
                vendedora = "No asignado"  
        except Exception as e:  
            messagebox.showerror("Error", f"Error al obtener el nombre de la vendedora: {e}")  
            return  

        # Crear el documento PDF  
        pdf = FPDF()  
        pdf.add_page()  
        pdf.set_font("Arial", size=12)  

        # Agregar imagen en el encabezado  
        try:  
            pdf.image("Iconos/LogoBanner.png", x=10, y=8, w=190)  # x, y = posición, w = ancho  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")  
            return  

        # Espacio después de la imagen  
        pdf.ln(45)  # Ajusta según el tamaño de la imagen  

        # Encabezado del comprobante  
        pdf.set_font("Arial", style="B", size=16)  
        pdf.cell(150, 15, txt="MICRO MARKET - COMPROBANTE", ln=True, align="C")  
        pdf.cell(150, 15, txt=f"{tipo_comprobante.upper()}", ln=True, align="C")  
        pdf.ln(5)  

        # Detalles del cliente y vendedora  
        pdf.set_font("Arial", size=12)  
        pdf.cell(100, 10, txt=f"Cliente: {cliente}", ln=True)  
        pdf.cell(100, 10, txt=f"Vendedora: {vendedora}", ln=True)  
        pdf.cell(100, 10, txt=f"Fecha: {datetime.now().strftime('%d-%m-%Y')}", ln=True)  
        pdf.ln(10)  

        # Tabla de productos  
        pdf.set_font("Arial", style="B", size=12)  
        pdf.cell(40, 10, txt="Producto", border=1, align="C")  
        pdf.cell(30, 10, txt="Precio", border=1, align="C")  
        pdf.cell(30, 10, txt="Cantidad", border=1, align="C")  
        pdf.cell(30, 10, txt="Total", border=1, align="C")  
        pdf.ln()  

        pdf.set_font("Arial", size=12)  
        total_sin_impuestos = 0  
        for item in self.tree.get_children():  
            values = self.tree.item(item, "values")  
            producto = values[2]  
            precio = float(values[4])  
            cantidad = int(values[6])  
            total = float(values[7])  

            pdf.cell(40, 10, txt=producto, border=1)  
            pdf.cell(30, 10, txt=f"{precio:.2f}", border=1, align="C")  
            pdf.cell(30, 10, txt=f"{cantidad}", border=1, align="C")  
            pdf.cell(30, 10, txt=f"{total:.2f}", border=1, align="C")  
            pdf.ln()  

            total_sin_impuestos += total  

        # Total e impuestos  
        pdf.ln(10)  
        if tipo_comprobante == "FACTURA DE VENTA":  
            impuesto = total_sin_impuestos * 0.13  
            total_con_impuestos = total_sin_impuestos + impuesto  
            pdf.cell(100, 10, txt=f"Subtotal: {total_sin_impuestos:.2f} Bs")  
            pdf.ln()  
            pdf.cell(100, 10, txt=f"IVA (13%): {impuesto:.2f} Bs")  
            pdf.ln()  
            pdf.cell(100, 10, txt=f"Total: {total_con_impuestos:.2f} Bs", ln=True)  
        else:  
            pdf.cell(100, 10, txt=f"Total: {total_sin_impuestos:.2f} Bs", ln=True)  

        # Guardar el archivo PDF  
        try:  
            archivo = f"{tipo_comprobante.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  
            pdf.output(archivo)  
            messagebox.showinfo("Éxito", f"Comprobante generado: {archivo}")  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo generar el comprobante: {e}") 

    def mostrar_historial_ventas(self):  
        """Muestra el historial de ventas en una nueva ventana."""  
        try:  
            self.cursor.execute("""  
                SELECT   
                    v.Id_Venta AS Factura,  
                    CONCAT(c.Nombre, ' ', c.Apellido_Paterno, ' ', c.Apellido_Materno) AS Cliente,  
                    p.NombreProducto AS Producto,  
                    dv.PrecioUnitario AS Precio,  
                    dv.Cantidad AS Cantidad,  
                    dv.TotalVenta AS Total,  
                    v.FechaVenta AS Fecha,  
                    p.EnPromocion,  
                    p.PrecioPromocion  
                FROM Ventas v  
                INNER JOIN DetalleVenta dv ON v.Id_Venta = dv.Id_Venta  
                INNER JOIN Productos p ON dv.Id_Producto = p.Id_Producto  
                INNER JOIN Cliente c ON v.Id_Cliente = c.Id_Cliente  
                ORDER BY v.FechaVenta DESC  
            """)  
            datos = self.cursor.fetchall()  

            if not datos:  
                messagebox.showinfo("Información", "No hay registros en el historial de ventas.")  
                return  

            # Crear ventana para mostrar el historial  
            ventana = tk.Toplevel()  
            ventana.title("Historial de Ventas")  
            ventana.geometry("1100x500")  # Ajustar ancho para nuevas columnas  

            # Crear un Treeview para mostrar los datos  
            columnas = ("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "EnPromocion", "PrecioPromocion")  
            tree = ttk.Treeview(ventana, columns=columnas, show="headings", height=20)  
            tree.pack(fill=tk.BOTH, expand=True)  

            # Definir los encabezados de columnas  
            encabezados = {  
                "Factura": "Factura",  
                "Cliente": "Cliente",  
                "Producto": "Producto",  
                "Precio": "Precio",  
                "Cantidad": "Cantidad",  
                "Total": "Total",  
                "Fecha": "Fecha",  
                "EnPromocion": "En Promoción",  
                "PrecioPromocion": "Precio Promoción"  
            }  

            for col in columnas:  
                tree.heading(col, text=encabezados[col])  
                tree.column(col, anchor=tk.CENTER, width=120)  

            # Insertar los datos en el Treeview  
            for row in datos:  
                factura, cliente, producto, precio, cantidad, total, fecha, en_promocion, precio_promocion = row  

                # Convertir valores de promoción  
                en_promocion_texto = "Sí" if en_promocion else "No"  
                precio_promocion = precio_promocion if en_promocion else ""  

                # Insertar en el Treeview  
                tree.insert("", tk.END, values=(  
                    factura, cliente, producto, precio, cantidad, total, fecha, en_promocion_texto, precio_promocion  
                ))  

            # Agregar scrollbars  
            scrollbar_y = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)  
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)  
            tree.configure(yscrollcommand=scrollbar_y.set)  

            scrollbar_x = ttk.Scrollbar(ventana, orient="horizontal", command=tree.xview)  
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)  
            tree.configure(xscrollcommand=scrollbar_x.set)  

        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo cargar el historial de ventas: {e}")  

    def regresar(self):
        """Vuelve a la ventana anterior."""
        self.destroy()