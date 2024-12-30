import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from fpdf import FPDF


class Proveedor(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.config(bg="#D0E4F5")
        self.place(x=300, y=10, width=1100, height=650)

        self.crear_widgets()
        self.cargar_proveedores()

    def crear_widgets(self):
        # Título
        titulo = tk.Label(self, text="PROVEEDORES", font=("Arial", 24, "bold"), bg="#D0E4F5")
        titulo.place(x=400, y=10, width=300, height=30)

        # Botones Regresar y Salir
        self.crear_botones_regresar_salir()

        # Etiquetas de Fecha y Hora
        self.crear_fecha_hora_labels()

        # Contenedor de Datos
        Ibframe_seleccion = tk.LabelFrame(self, text="Datos:", font="arial 14 bold", bg="#C6D9E3",
                                          highlightbackground="green", highlightthickness=2)
        Ibframe_seleccion.place(x=10, y=100, width=500, height=210)

        # Etiquetas y Entradas
        etiquetas = ["Nombre", "Apellido Paterno", "Apellido Materno", "Celular", "Descripcion"]
        self.entries = {}
        for i, texto in enumerate(etiquetas):
            tk.Label(Ibframe_seleccion, text=f"{texto}:", font="arial 14", bg="#C6D9E3").place(x=5, y=5 + i * 35)
            self.entries[texto] = tk.Entry(Ibframe_seleccion)
            self.entries[texto].place(x=160, y=5 + i * 35, width=150)

        # Contenedor para los botones de opciones
        lblframe_botones = tk.LabelFrame(
            self, bg="#C6D9E3", text="Opciones", font="arial 14 bold",
            highlightbackground="green", highlightthickness=2
        )
        lblframe_botones.place(x=520, y=100, width=500, height=210)

        # Lista de botones con su texto y función asociada
        botones = [
            ("Agregar", self.agregar_proveedor),
            ("Editar", self.editar_proveedor),
            ("Eliminar", self.eliminar_proveedor),
            ("Registrar Compra", self.registrar_compra),
            ("Historial de Compras", self.historial_compras),
        ]

        # Creación de botones organizados en filas
        for i, (texto, comando) in enumerate(botones):
            tk.Button(
                lblframe_botones, text=texto, font="arial 14 bold", bg="lightblue",
                command=comando
            ).place(
                x=20 + (i % 2) * 240,  # Cambia de columna cada dos botones
                y=5 + (i // 2) * 50,  # Cambia de fila cada dos botones
                width=200, height=40
            )

        # Tabla para mostrar los proveedores
        self.tree = ttk.Treeview(
            self, columns=("Nombre", "Apellido Paterno", "Apellido Materno", "Celular", "Descripcion"), show='headings'
        )
        self.tree = ttk.Treeview(
            self, columns=("Nombre", "Apellido Paterno", "Apellido Materno", "Celular", "Descripcion"), show='headings'
        )
        for col in ["Nombre", "Apellido Paterno", "Apellido Materno", "Celular", "Descripcion"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Descripcion" else 250)
        
        self.tree.place(x=10, y=320, width=1045, height=300)

        # Vincular evento para doble clic en la tabla
        self.tree.bind("<Double-1>", self.cargar_datos_seleccionados)

    def crear_botones_regresar_salir(self):
        boton_regresar = tk.Button(self, text="REGRESAR", command=self.regresar, font=("Arial", 14), bg="blue", fg="white")
        boton_regresar.place(x=10, y=10, width=150, height=40)

        boton_salir = tk.Button(self, text="SALIR", command=self.salir, font=("Arial", 14), bg="red", fg="white")
        boton_salir.place(x=980, y=10, width=100, height=40)

    def crear_fecha_hora_labels(self):
        self.fecha_label = tk.Label(self, text="", font=("Arial", 14), bg="#D0E4F5")
        self.fecha_label.place(x=400, y=60, width=200, height=30)

        self.hora_label = tk.Label(self, text="", font=("Arial", 14), bg="#D0E4F5")
        self.hora_label.place(x=610, y=60, width=200, height=30)

        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        ahora = datetime.now()
        self.fecha_label.config(text=f"FECHA: {ahora.strftime('%Y-%m-%d')}")
        self.hora_label.config(text=f"HORA: {ahora.strftime('%H:%M:%S')}")
        self.after(1000, self.actualizar_fecha_hora)

    def regresar(self):
        if messagebox.askyesno("Regresar", "¿Deseas regresar a la ventana anterior?"):
            self.destroy()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()

    def cargar_proveedores(self):
        """Cargar proveedores desde la base de datos."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute("SELECT Nombre, Apellido_Paterno, Apellido_Materno, Celular, Descripcion FROM Proveedor")
        for proveedor in self.cursor.fetchall():
            self.tree.insert("", "end", values=proveedor)

    def agregar_proveedor(self):
        datos = [self.entries[key].get() for key in self.entries]
        if not all(datos):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos")
            return
        try:
            self.cursor.execute(
                """
                INSERT INTO Proveedor (Nombre, Apellido_Paterno, Apellido_Materno, Celular, Descripcion)
                VALUES (%s, %s, %s, %s, %s)
                """,
                datos
            )
            self.db_connection.commit()
            self.cargar_proveedores()
            self.limpiar_entradas()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el proveedor: {e}")

##################################################################################################################################################################
    def editar_proveedor(self):
        """Abrir una ventana para editar los datos de un proveedor seleccionado."""
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selección", "Selecciona un proveedor para editar")
            return

        valores = self.tree.item(item, "values")  # Obtener datos seleccionados del Treeview
        if not valores:
            return

        # Crear ventana secundaria
        ventana_editar = tk.Toplevel(self)
        ventana_editar.title("Editar Proveedor")
        ventana_editar.geometry("400x400")
        ventana_editar.resizable(False, False)

        # Etiquetas y Entradas para cada atributo
        etiquetas = ["Nombre", "Apellido Paterno", "Apellido Materno", "Celular", "Descripcion"]
        entradas = {}
        for i, texto in enumerate(etiquetas):
            tk.Label(ventana_editar, text=f"{texto}:", font=("Arial", 12)).place(x=20, y=20 + i * 60)
            entrada = tk.Entry(ventana_editar, font=("Arial", 12))
            entrada.place(x=150, y=20 + i * 60, width=200)
            entrada.insert(0, valores[i])  # Cargar valor actual en la entrada
            entradas[texto] = entrada

        # Botón para guardar los cambios
        def guardar_cambios():
            nuevos_datos = [entradas[etiqueta].get() for etiqueta in etiquetas]
            if not all(nuevos_datos):
                messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos")
                return

            try:
                self.cursor.execute(
                """
                    UPDATE Proveedor
                    SET Nombre = %s, Apellido_Paterno = %s, Apellido_Materno = %s, Celular = %s, Descripcion = %s
                    WHERE Nombre = %s AND Apellido_Paterno = %s AND Apellido_Materno = %s
                    """,
                    (*nuevos_datos, valores[0], valores[1], valores[2])  # Nuevos datos y valores originales como filtro
                )
                self.db_connection.commit()
                self.cargar_proveedores()  # Refrescar la tabla principal
                messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
                ventana_editar.destroy()  # Cerrar ventana secundaria
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar el proveedor: {e}")

        tk.Button(
            ventana_editar, text="Guardar Cambios", font=("Arial", 12, "bold"),
            bg="green", fg="white", command=guardar_cambios
        ).place(x=150, y=340, width=200, height=40)

         # Botón para cancelar la edición
        tk.Button(
            ventana_editar, text="Cancelar", font=("Arial", 12, "bold"),
            bg="red", fg="white", command=ventana_editar.destroy
        ).place(x=20, y=340, width=100, height=40)
        
##################################################################################################################################################
    def eliminar_proveedor(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Selección", "Selecciona un proveedor para eliminar")
            return

        valores = self.tree.item(item, "values")
        try:
            self.cursor.execute("DELETE FROM Proveedor WHERE Nombre=%s", (valores[0],))
            self.db_connection.commit()
            self.cargar_proveedores()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")


#########################################################################################################################################3
    def limpiar_entradas(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.focus())
#######################################################################################################################################33333
    def cargar_datos_seleccionados(self, event):
        item = self.tree.focus()
        if not item:
            return
        valores = self.tree.item(item, "values")
        for i, key in enumerate(self.entries):
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, valores[i])
###########################################################################################################################
    def historial_compras(self):
        """Abrir una ventana para mostrar el historial de compras y actualizar automáticamente."""
        def cargar_historial():
            """Cargar los datos del historial de compras en el Treeview."""
            # Limpiar datos previos del Treeview
            for row in tree_historial.get_children():
                tree_historial.delete(row)

            # Ejecutar la consulta para obtener los datos del historial
            try:
                query = """
                    SELECT 
                        c.FechaCompra,
                        c.MontoTotal,
                        CONCAT(p.Nombre, ' ', p.Apellido_Paterno, ' ', p.Apellido_Materno) AS Proveedor,
                        pr.NombreProducto,
                        pr.Costo AS CostoProducto,
                        c.MontoTotal AS TotalCompra
                    FROM CompraDeProveedor c
                    INNER JOIN Proveedor p ON c.Id_Proveedor = p.Id_Proveedor
                    INNER JOIN Productos pr ON c.Id_Producto = pr.Id_Producto;
                """
                self.cursor.execute(query)
                compras = self.cursor.fetchall()

                if not compras:
                    messagebox.showinfo("Historial vacío", "No hay compras registradas en el historial.")
                    return

                for compra in compras:
                    tree_historial.insert("", "end", values=compra)

            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                messagebox.showerror("Error", f"No se pudo cargar el historial de compras:\n{error_details}")

        # Crear ventana secundaria
        ventana_historial = tk.Toplevel(self)
        ventana_historial.title("Historial de Compras")
        ventana_historial.geometry("900x600")
        ventana_historial.resizable(False, False)

        # Título
        tk.Label(ventana_historial, text="Historial de Compras", font=("Arial", 16, "bold")).place(x=20, y=20)

        # Tabla para mostrar las compras
        tree_historial = ttk.Treeview(
            ventana_historial,
            columns=("Fecha", "Monto Total", "Proveedor", "Producto", "Costo Producto", "Total Compra"),
            show="headings"
        )
        tree_historial.heading("Fecha", text="Fecha")
        tree_historial.heading("Monto Total", text="Monto Total")
        tree_historial.heading("Proveedor", text="Proveedor")
        tree_historial.heading("Producto", text="Producto")
        tree_historial.heading("Costo Producto", text="Costo Producto")
        tree_historial.heading("Total Compra", text="Total Compra")

        tree_historial.column("Fecha", width=100)
        tree_historial.column("Monto Total", width=100)
        tree_historial.column("Proveedor", width=150)
        tree_historial.column("Producto", width=150)
        tree_historial.column("Costo Producto", width=100)
        tree_historial.column("Total Compra", width=100)

        tree_historial.place(x=20, y=60, width=850, height=480)

        # Llamar a la función para cargar el historial al abrir la ventana
        cargar_historial()

        # Botón para cerrar la ventana
        tk.Button(
            ventana_historial, text="Cerrar", font=("Arial", 12), bg="red", fg="white", command=ventana_historial.destroy
        ).place(x=750, y=550, width=100, height=30)


###################################registrar compra #################################################################################
    def registrar_compra(self):   
        """Abrir una ventana para registrar una compra a un proveedor seleccionado."""   
        item = self.tree.focus()   
        if not item:   
            messagebox.showwarning("Selección", "Selecciona un proveedor para registrar una compra")   
            return   

        valores = self.tree.item(item, "values")  # Obtener datos seleccionados del proveedor   
        proveedor_nombre = valores[0]   
        proveedor_id = self.obtener_id_proveedor(proveedor_nombre)   

        if not proveedor_id:   
            messagebox.showerror("Error", "No se pudo encontrar el ID del proveedor seleccionado")   
            return   

        # Crear ventana secundaria   
        ventana_compra = tk.Toplevel(self)   
        ventana_compra.title("Registrar Compra")   
        ventana_compra.geometry("800x600")   
        ventana_compra.resizable(False, False)   

        # Variables para total y productos   
        self.productos_seleccionados = []   
        self.monto_total = 0.0   

        # Título   
        tk.Label(ventana_compra, text=f"Registrar Compra - {proveedor_nombre}", font=("Arial", 16, "bold")).place(x=20, y=20)   

        # Sección para agregar productos   
        tk.Label(ventana_compra, text="Nombre Producto:", font=("Arial", 12)).place(x=20, y=60)   
        entry_nombre = tk.Entry(ventana_compra, font=("Arial", 12))   
        entry_nombre.place(x=150, y=60, width=200)   

        tk.Label(ventana_compra, text="Precio Unitario:", font=("Arial", 12)).place(x=20, y=100)   
        entry_precio = tk.Entry(ventana_compra, font=("Arial", 12))   
        entry_precio.place(x=150, y=100, width=200)   

        tk.Label(ventana_compra, text="Costo:", font=("Arial", 12)).place(x=20, y=140)   
        entry_costo = tk.Entry(ventana_compra, font=("Arial", 12))   
        entry_costo.place(x=150, y=140, width=200)   

        tk.Label(ventana_compra, text="Stock:", font=("Arial", 12)).place(x=20, y=180)   
        entry_stock = tk.Entry(ventana_compra, font=("Arial", 12))   
        entry_stock.place(x=150, y=180, width=200)   

        tk.Label(ventana_compra, text="Categoría:", font=("Arial", 12)).place(x=20, y=220)   
        combo_categoria = ttk.Combobox(ventana_compra, font=("Arial", 12), state="readonly")   
        combo_categoria.place(x=150, y=220, width=200)   

        # Cargar categorías en el combobox   
        self.cursor.execute("SELECT Id_Categoria, NombreCategoria FROM Categoria")   
        categorias = self.cursor.fetchall()   
        combo_categoria["values"] = [f"{row[1]} (ID: {row[0]})" for row in categorias]   

        # Tabla para mostrar productos seleccionados   
        tree_productos = ttk.Treeview(ventana_compra, columns=("Nombre", "Precio", "Costo", "Stock", "Categoría"), show="headings")   
        for col in ["Nombre", "Precio", "Costo", "Stock", "Categoría"]:   
            tree_productos.heading(col, text=col)   
            tree_productos.column(col, width=150)   

        tree_productos.place(x=20, y=280, width=760, height=200) 
            # Combobox para tipo de comprobante
        tk.Label(ventana_compra, text="Tipo de Comprobante:", font=("Arial", 12)).place(x=400, y=60)
        combo_comprobante = ttk.Combobox(ventana_compra, font=("Arial", 12), state="readonly")
        combo_comprobante["values"] = ["Con Factura", "Sin Factura"]
        combo_comprobante.place(x=550, y=60, width=200)
        combo_comprobante.set("Con Factura")  # Valor predeterminado

    # Botón para generar la factura en PDF
        def generar_factura():
            tipo_comprobante = combo_comprobante.get()
            if not tipo_comprobante:
                messagebox.showerror("Error", "Seleccione un tipo de comprobante.")
                return

            if not tree_productos.get_children():
                messagebox.showerror("Error", "No hay productos para generar la factura.")
                return

            # Crear PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

        # Encabezado
            pdf.image("Iconos/LogoBanner.png", x=10, y=8, w=190)
            pdf.ln(45)
            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(200, 10, txt="FACTURA DE COMPRA", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Tipo: {tipo_comprobante.upper()}", ln=True, align="C")
            pdf.ln(10)

        # Tabla de productos
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(50, 10, txt="Producto", border=1, align="C")
            pdf.cell(30, 10, txt="Costo", border=1, align="C")
            pdf.cell(30, 10, txt="Stock", border=1, align="C")
            pdf.cell(30, 10, txt="Total", border=1, align="C")
            pdf.ln()

            pdf.set_font("Arial", size=12)
            total = 0
            for item in tree_productos.get_children():
                values = tree_productos.item(item, "values")
                producto, costo, _, stock, _ = values
                costo = float(costo)
                stock = int(stock)
                subtotal = costo * stock

                pdf.cell(50, 10, txt=producto, border=1)
                pdf.cell(30, 10, txt=f"{costo:.2f}", border=1, align="C")
                pdf.cell(30, 10, txt=f"{stock}", border=1, align="C")
                pdf.cell(30, 10, txt=f"{subtotal:.2f}", border=1, align="C")
                pdf.ln()

                total += subtotal

        # Agregar IVA si es con factura
            pdf.ln(10)
            if tipo_comprobante == "Con Factura":
                iva = total * 0.13
                total_con_iva = total + iva
                pdf.cell(100, 10, txt=f"Subtotal: {total:.2f} Bs", ln=True)
                pdf.cell(100, 10, txt=f"IVA (13%): {iva:.2f} Bs", ln=True)
                pdf.cell(100, 10, txt=f"Total: {total_con_iva:.2f} Bs", ln=True)
            else:
                pdf.cell(100, 10, txt=f"Total: {total:.2f} Bs", ln=True)

        # Guardar el PDF
            try:
                nombre_archivo = f"Factura_{tipo_comprobante.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                pdf.output(nombre_archivo)
                messagebox.showinfo("Éxito", f"Factura generada: {nombre_archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la factura: {e}")

        # Botón para generar la factura
        tk.Button(ventana_compra, text="Generar Factura", font=("Arial", 12), bg="orange", fg="white",
            command=generar_factura).place(x=550, y=100, width=200)  

        # Función para agregar producto   
        def agregar_producto():    
            nombre = entry_nombre.get()    
            precio = entry_precio.get()    
            costo = entry_costo.get()    
            stock = entry_stock.get()    
            categoria = combo_categoria.get()    

            if not all([nombre, precio, costo, stock, categoria]):    
                messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos correctamente")    
                return    

            try:    
                precio = float(precio)    
                costo = float(costo)    
                stock = int(stock)    
            except ValueError:    
                messagebox.showerror("Error", "Datos inválidos en campos numéricos")    
                return    

            id_categoria = int(categoria.split("ID: ")[1].strip(")"))    

            try:    
                # Insertar el producto en la tabla Productos    
                self.cursor.execute(    
                    "INSERT INTO Productos (NombreProducto, PrecioUnitario, Costo, Stock, Estado, Id_Categoria) "    
                    "VALUES (%s, %s, %s, %s, 1, %s)",    
                    (nombre, precio, costo, stock, id_categoria),    
                )    
                self.db_connection.commit()    
                id_producto = self.cursor.lastrowid     

                # Añadir el producto a la lista local de productos seleccionados    
                self.productos_seleccionados.append((id_producto, nombre, precio, costo, stock, id_categoria))    

                # Mostrar el producto en la tabla visual    
                tree_productos.insert("", "end", values=(nombre, precio, costo, stock, categoria))    

                # Actualizar el monto total    
                monto_parcial = costo * stock     
                self.monto_total += monto_parcial    
                label_total.config(text=f"Total: {self.monto_total:.2f}")    

                # Limpiar entradas    
                entry_nombre.delete(0, tk.END)    
                entry_precio.delete(0, tk.END)    
                entry_costo.delete(0, tk.END)    
                entry_stock.delete(0, tk.END)    
                combo_categoria.set("")    

            except Exception as e:    
                self.db_connection.rollback()    
                messagebox.showerror("Error", f"No se pudo registrar el producto: {e}")    

        # Botón para agregar productos   
        tk.Button(ventana_compra, text="Agregar Producto", font=("Arial", 12), command=agregar_producto).place(x=600, y=220, width=150)   

        # Etiqueta para monto total   
        label_total = tk.Label(ventana_compra, text=f"Total: {self.monto_total:.2f}", font=("Arial", 14, "bold"))   
        label_total.place(x=20, y=520)   

        # Función para finalizar compra   
        def finalizar_compra():   
            if not self.productos_seleccionados:   
                messagebox.showwarning("Sin productos", "No has agregado ningún producto a la compra")   
                return   

            try:   
                fecha_actual = datetime.now().strftime("%Y-%m-%d")   

                # Insertar en CompraDeProveedor para cada producto seleccionado   
                for producto in self.productos_seleccionados:   
                    id_producto, nombre, precio, costo, stock, id_categoria = producto   
                    monto_parcial = costo * stock   

                    self.cursor.execute(   
                        "INSERT INTO CompraDeProveedor (FechaCompra, MontoTotal, Id_Proveedor, Id_Producto) VALUES (%s, %s, %s, %s)",   
                        (fecha_actual, monto_parcial, proveedor_id, id_producto)   
                    )   

                self.db_connection.commit()   
                messagebox.showinfo("Éxito", "Compra registrada correctamente")   
                ventana_compra.destroy()   

            except Exception as e:   
                self.db_connection.rollback()   
                messagebox.showerror("Error", f"No se pudo registrar la compra: {e}")   

        tk.Button(ventana_compra, text="Finalizar Compra", font=("Arial", 14), bg="green", fg="white", command=finalizar_compra).place(x=600, y=520, width=150)   
        tk.Button(ventana_compra, text="Cancelar", font=("Arial", 14), bg="red", fg="white", command=ventana_compra.destroy).place(x=450, y=520, width=100)   

    def obtener_id_proveedor(self, nombre):   
        """Obtener el ID de un proveedor dado su nombre."""   
        try:   
            self.cursor.execute("SELECT Id_Proveedor FROM Proveedor WHERE Nombre = %s", (nombre,))   
            resultado = self.cursor.fetchone()   
            return resultado[0] if resultado else None   
        except Exception as e:   
            messagebox.showerror("Error", f"No se pudo obtener el ID del proveedor: {e}")   
            return None   