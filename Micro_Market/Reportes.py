import pandas as pd
from fpdf import FPDF
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar


class Reportes(tk.Frame):
    def __init__(self, padre, db_connection):  
        super().__init__(padre)  
        self.db_connection = db_connection  
        self.cursor = db_connection.cursor() if db_connection else None  
        self.pack(fill="both", expand=True)  
        self.config(bg="#C6D9E3")  
        self.widgets()  

    def widgets(self):  
        titulo = tk.Label(self, text="REPORTES", font=("Arial", 24, "bold"), bg="#C6D9E3", anchor="center")  
        titulo.place(x=400, y=10, width=300, height=30)  
        self.crear_botones_regresar_salir()  
        self.crear_fecha_hora_labels()  
        contenedor_botones = tk.Frame(self, bg="#C6D9E3")  
        contenedor_botones.place(x=10, y=100, width=1080, height=400)  

        botones = [  
            ("Reporte Empleados", self.generar_reporte_empleados),  
            ("Reporte Productos", self.generar_reporte_productos),  
            ("Reporte Ganancias", self.generar_reporte_ganancias),  
            ("Reporte Promociones", self.generar_reporte_promociones),  
            ("Reporte Proveedores", self.generar_reporte_proveedores),  
            ("Reporte Ventas", self.generar_reporte_ventas),  
            ("Reporte Clientes", self.generar_reporte_clientes),  
        ]  
    
        
        for i, (texto, comando) in enumerate(botones):  
            boton = tk.Button(  
                contenedor_botones,  
                text=texto,  
                font=("Arial", 14),  
                bg="white",  
                fg="black",  
                command=comando  
            )  
            boton.grid(row=i // 3, column=i % 3, padx=50, pady=30, sticky="ew")  

    def crear_botones_regresar_salir(self):  
        boton_regresar = tk.Button(self, text="REGRESAR", command=self.regresar, font=("Arial", 14), bg="blue", fg="white")  
        boton_regresar.place(x=10, y=10, width=120, height=40)  

        boton_salir = tk.Button(self, text="SALIR", command=self.salir, font=("Arial", 14), bg="red", fg="white")  
        boton_salir.place(x=980, y=10, width=100, height=40)  

    def crear_fecha_hora_labels(self):  
        self.fecha_label = tk.Label(self, text="", font=("Arial", 14), bg="#C6D9E3")  
        self.fecha_label.place(x=400, y=50, width=200, height=30)  

        self.hora_label = tk.Label(self, text="", font=("Arial", 14), bg="#C6D9E3")  
        self.hora_label.place(x=610, y=50, width=200, height=30)  

        self.actualizar_fecha_hora()  

    def actualizar_fecha_hora(self):  
        ahora = datetime.now()  
        fecha_actual = ahora.strftime("%Y-%m-%d")  
        hora_actual = ahora.strftime("%H:%M:%S")  
        self.fecha_label.config(text=f"FECHA: {fecha_actual}")  
        self.hora_label.config(text=f"HORA: {hora_actual}")  
        self.after(1000, self.actualizar_fecha_hora)  

    def generar_pdf(self, titulo, datos, columnas, archivo):  
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(0, 255, 0)  # Color de fondo verde

            # Agregar imagen
            pdf.image("Iconos/LogoBanner.png", x=10, y=8, w=190)  # Posición fija con `.place` equivalente
            pdf.ln(40)  # Espaciado después de la imagen

            # Encabezado
            pdf.set_font("Arial", style="B", size=14)
            pdf.set_text_color(0, 128, 0)  # Texto verde
            pdf.set_xy(10, 70)  # Posicionar el título
            pdf.cell(190, 10, txt="MICRO MARKET", ln=True, align="C")

            pdf.set_xy(10, 75)  # Posicionar ubicación
            pdf.cell(190, 10, txt="Ubicación: Chore", ln=True, align="C")

            pdf.set_xy(10, 80)  # Posicionar celular
            pdf.cell(190, 10, txt="Celular: 64454120", ln=True, align="C")

            pdf.set_xy(10, 85)  # Posicionar correo
            pdf.cell(190, 10, txt="Correo: eliasterrazas48@gmail.com", ln=True, align="C")

            pdf.ln(20)  # Espaciado adicional antes de la tabla

            # Tabla de columnas
            pdf.set_font("Arial", style="B", size=12)
            pdf.set_xy(10, 100)  # Inicio de la tabla
            for col in columnas:
                pdf.cell(40, 10, col, border=1, align="C")
            pdf.ln()

            # Tabla de datos
            pdf.set_font("Arial", size=12)
            y = 110  # Coordenada Y inicial para las filas
            for fila in datos:
                pdf.set_xy(10, y)  # Posicionar fila
                for celda in fila:
                    pdf.cell(40, 10, str(celda), border=1, align="C")
                y += 10  # Incrementar para la siguiente fila

            # Guardar archivo
            pdf.output(archivo)
            messagebox.showinfo("Éxito", f"Reporte generado: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}") 
    
    

    def generar_reporte_empleados(self):  
        try:  
            self.cursor.execute("""  
                SELECT Nombre, Apellido_Paterno, Apellido_Materno, CI,  
                       CASE WHEN Estado = 1 THEN 'Activo' ELSE 'Inactivo' END AS Estado  
                FROM Empleado  
            """)  
            datos = self.cursor.fetchall()  
            columnas = ["Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Estado"]  
            archivo = f"Reporte_Empleados_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  
            self.generar_pdf("Reporte de Empleados - Micro Market", datos, columnas, archivo)  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo generar el reporte de empleados: {e}")
######################################################################################################################################

    def generar_reporte_productos(self):  
        """Genera un reporte detallado de productos ordenados por stock."""  
        try:  
            # Consulta para ordenar los productos por stock (descendente)  
            self.cursor.execute("""  
                SELECT p.NombreProducto AS Producto,  
                       p.Costo AS Costo,  
                       p.PrecioUnitario AS PrecioUnitario,  
                       p.Stock AS Stock  
                FROM Productos p  
                ORDER BY p.Stock DESC  
            """)  
            datos = self.cursor.fetchall()  

            # Columnas para el reporte  
            columnas = ["Producto", "Costo", "Precio Unit.", "Stock"]  

            # Archivo PDF con timestamp  
            archivo = f"Reporte_Productos_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  

            # Generar el PDF  
            self.generar_pdf("Reporte de Productos Ordenado por Stock - Micro Market", datos, columnas, archivo)  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo generar el reporte de productos: {e}")  
            
#############################################################################################################################

    def generar_reporte_ganancias(self):  
        """Genera un reporte detallado de ganancias basado en productos vendidos, con columnas ajustadas."""  

        # Ventana emergente para selección de fechas  
        def seleccionar_fechas():
            ventana_fechas = tk.Toplevel(self)  
            ventana_fechas.title("Seleccionar rango de fechas")  
            ventana_fechas.geometry("400x300")  
            ventana_fechas.config(bg="#C6D9E3")  

            tk.Label(ventana_fechas, text="Fecha inicial:", font=("Arial", 12), bg="#C6D9E3").place(x=50, y=50)  
            cal_inicio = Calendar(ventana_fechas, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)  
            cal_inicio.place(x=50, y=80)  

            tk.Label(ventana_fechas, text="Fecha final:", font=("Arial", 12), bg="#C6D9E3").place(x=200, y=50)  
            cal_fin = Calendar(ventana_fechas, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)  
            cal_fin.place(x=200, y=80)  

            def aplicar_fechas():  
                fecha_inicio = cal_inicio.get_date()  
                fecha_fin = cal_fin.get_date()  
                ventana_fechas.destroy()  
                generar_reporte_con_rango(fecha_inicio, fecha_fin)  

            boton_aplicar = tk.Button(ventana_fechas, text="Aplicar", font=("Arial", 14), bg="green", fg="white", command=aplicar_fechas)  
            boton_aplicar.place(x=150, y=250)  

        # Función para generar el reporte con el rango de fechas seleccionado  
        def generar_reporte_con_rango(fecha_inicio, fecha_fin):  
            try:  
                # Consulta SQL para obtener productos vendidos  
                query = """  
                    SELECT  
                        p.NombreProducto AS Producto,  
                        p.Costo AS Costo,  
                        p.PrecioUnitario AS PrecioUnitario,  
                        SUM(dv.Cantidad) AS Cantidad,  
                        SUM(dv.Cantidad * p.Costo) AS CostoTotal,  
                        SUM(dv.TotalVenta - (dv.Cantidad * p.Costo)) AS GananciaTotal  
                    FROM DetalleVenta dv  
                    INNER JOIN Productos p ON dv.Id_Producto = p.Id_Producto  
                    INNER JOIN Ventas v ON dv.Id_Venta = v.Id_Venta  
                    WHERE v.FechaVenta BETWEEN %s AND %s  
                    GROUP BY p.NombreProducto, p.Costo, p.PrecioUnitario  
                    ORDER BY GananciaTotal DESC  
                """  

                # Ejecutar la consulta  
                self.cursor.execute(query, (fecha_inicio, fecha_fin))  
                datos = self.cursor.fetchall()  

                if not datos:  
                    messagebox.showinfo("Reporte vacío", "No hay datos para generar el reporte de ganancias.")  
                    return  

                # Calcular la ganancia total final  
                ganancia_total = sum(fila[5] for fila in datos)  
                datos.append(("TOTAL", "", "", "", "", ganancia_total))  

                # Columnas con nombres reducidos  
                columnas = ["Producto", "Costo", "PrecioUnitario", "Cantidad", "CostoTotal", "GananciaTotal"]  

                # Generar PDF ajustando los cuadros al tamaño del texto  
                archivo_pdf = f"Reporte_Ganancias_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  
                self.generar_pdf_ajustado("Reporte de Ganancias - Micro Market", datos, columnas, archivo_pdf)  

            except Exception as e:  
                messagebox.showerror("Error", f"No se pudo generar el reporte de ganancias: {e}")  
                
        seleccionar_fechas()

    def generar_pdf_ajustado(self, titulo, datos, columnas, archivo):  
        pdf = FPDF()  
        pdf.add_page()  
        pdf.set_font("Arial", size=10)  

        # Agregar imagen
        pdf.image("Iconos/LogoBanner.png", x=10, y=8, w=190)  # Posición fija con `.place`
        pdf.ln(40)  # Espaciado después de la imagen  

        # Encabezado
        pdf.set_xy(10, 75)  # Mueve "MICRO MARKET" más abajo
        pdf.cell(190, 10, txt="MICRO MARKET", ln=False, align="C")

        pdf.set_xy(10, 80)  # Incrementa y para la siguiente línea
        pdf.cell(190, 10, txt="Ubicación: Chore", ln=False, align="C")

        pdf.set_xy(10, 85)  # Incrementa más la posición
        pdf.cell(190, 10, txt="Celular: 64454120", ln=False, align="C")

        pdf.set_xy(10, 90)  # Mueve la siguiente línea aún más abajo
        pdf.cell(190, 10, txt="Correo: eliasterrazas48@gmail.com", ln=False, align="C")  

        # Título del reporte
        pdf.set_font("Arial", style="B", size=12)  
        pdf.cell(190, 10, txt=titulo, ln=True, align="C")  
        pdf.ln(10)  

        # Calcular anchos de columna basados en el contenido
        anchos = [max(len(str(col)), max(len(str(fila[i])) for fila in datos)) * 2 for i, col in enumerate(columnas)]  

        # Encabezados de columnas
        pdf.set_font("Arial", style="B", size=10)  
        for i, col in enumerate(columnas):  
            pdf.cell(anchos[i], 10, col, border=1, align="C")  
        pdf.ln()  

        # Datos
        pdf.set_font("Arial", size=10)  
        for fila in datos:  
            for i, celda in enumerate(fila):  
                pdf.cell(anchos[i], 10, str(celda), border=1, align="C")  
            pdf.ln()  

        # Guardar archivo
        pdf.output(archivo)  
        messagebox.showinfo("Éxito", f"Reporte generado: {archivo}")  

##################################################################################################################################
    def generar_reporte_proveedores(self):  
        """Genera un reporte detallado de proveedores."""  
        try:  
            self.cursor.execute("""  
                SELECT Nombre, Celular, Descripcion   
                FROM Proveedor  
            """)  
            datos = self.cursor.fetchall()  
            columnas = ["Proveedor", "Celular", "Descripción"]  
            archivo = f"Reporte_Proveedores_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  
            self.generar_pdf("Reporte de Proveedores - Micro Market", datos, columnas, archivo)  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo generar el reporte de proveedores: {e}")  
###############################################################################################################################3
    def generar_reporte_ventas(self):  
        """Genera un reporte detallado de ventas según un rango de fechas."""  
        
        # Ventana emergente para selección de fechas  
        def seleccionar_fechas():  
            ventana_fechas = tk.Toplevel(self)  
            ventana_fechas.title("Seleccionar rango de fechas")  
            ventana_fechas.geometry("400x300")  
            ventana_fechas.config(bg="#C6D9E3")  

            tk.Label(ventana_fechas, text="Fecha inicial:", font=("Arial", 12), bg="#C6D9E3").place(x=50, y=50)  
            cal_inicio = Calendar(ventana_fechas, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)  
            cal_inicio.place(x=50, y=80)  

            tk.Label(ventana_fechas, text="Fecha final:", font=("Arial", 12), bg="#C6D9E3").place(x=200, y=50)  
            cal_fin = Calendar(ventana_fechas, selectmode="day", year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)  
            cal_fin.place(x=200, y=80)  

            def aplicar_fechas():  
                fecha_inicio = cal_inicio.get_date()  
                fecha_fin = cal_fin.get_date()  
                ventana_fechas.destroy()  
                generar_reporte_con_rango(fecha_inicio, fecha_fin)  

            boton_aplicar = tk.Button(ventana_fechas, text="Aplicar", font=("Arial", 14), bg="green", fg="white", command=aplicar_fechas)  
            boton_aplicar.place(x=150, y=250)  

        # Función para generar el reporte con el rango de fechas seleccionado  
        def generar_reporte_con_rango(fecha_inicio, fecha_fin):  
            try:  
                # Consulta SQL con el rango de fechas (correcta para SQL Server)  
                query = """  
                    SELECT v.FechaVenta, c.Nombre AS Cliente,   
                        p.NombreProducto AS Producto,   
                        dv.Cantidad, dv.TotalVenta  
                    FROM Ventas v  
                    INNER JOIN DetalleVenta dv ON v.Id_Venta = dv.Id_Venta  
                    INNER JOIN Productos p ON dv.Id_Producto = p.Id_Producto  
                    INNER JOIN Cliente c ON v.Id_Cliente = c.Id_Cliente  
                    WHERE v.FechaVenta BETWEEN %s AND %s  
                    ORDER BY dv.cantidad, v.FechaVenta ASC   
                """  

                # Ejecutar la consulta  
                self.cursor.execute(query, (fecha_inicio, fecha_fin))  
                datos = self.cursor.fetchall()  
                columnas = ["Fecha", "Cliente", "Producto", "Cantidad", "Total"]  

                if not datos:  
                    messagebox.showinfo("Reporte vacío", "No hay datos para generar el reporte de ventas.")  
                    return  

                # Generar el archivo PDF  
                archivo = f"Reporte_Ventas_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  
                self.generar_pdf("Reporte de Ventas - Micro Market", datos, columnas, archivo)  

            except Exception as e:  
                messagebox.showerror("Error", f"No se pudo generar el reporte de ventas: {e}")  

        # Llamar a la ventana emergente para seleccionar fechas  
        seleccionar_fechas()  
  


    def generar_reporte_clientes(self):  
        """Genera un reporte detallado de clientes ordenados por el total de compras."""  
        try:  
            # Consulta SQL para ordenar los clientes por el total de compras (descendente)  
            self.cursor.execute("""  
                SELECT c.Nombre, c.Apellido_Paterno, c.Apellido_Materno, c.CI, c.Celular,   
                       SUM(dv.TotalVenta) AS TotalCompras  
                FROM Cliente c  
                INNER JOIN Ventas v ON c.Id_Cliente = v.Id_Cliente  
                INNER JOIN DetalleVenta dv ON v.Id_Venta = dv.Id_Venta  
                GROUP BY c.Nombre, c.Apellido_Paterno, c.Apellido_Materno, c.CI, c.Celular  
                ORDER BY TotalCompras DESC  
            """)  
            datos = self.cursor.fetchall()  

            # Columnas para el reporte  
            columnas = ["Nombre", "Apellido Paterno", "Apellido Materno", "CI", "Celular", "Total Compras"]  

            # Archivo PDF con timestamp  
            archivo = f"Reporte_Clientes_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  

            # Generar el PDF  
            self.generar_pdf("Reporte de Clientes - Micro Market", datos, columnas, archivo)  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo generar el reporte de clientes: {e}")  
            
    def generar_reporte_promociones(self):  
        """Genera un reporte detallado de promociones."""  
        try:  
            # Consulta SQL para obtener las promociones  
            self.cursor.execute("""  
                SELECT NombreProducto AS Producto,  
                       PrecioPromocion AS PrecioPromocion,  
                       CONCAT(CAST((100 - (PrecioPromocion / PrecioUnitario * 100)) AS DECIMAL(10, 2)), '%') AS Descuento,  
                       Stock  
                FROM Productos  
                WHERE PrecioPromocion IS NOT NULL  
                ORDER BY NombreProducto  
            """)  
            datos = self.cursor.fetchall()  

            # Columnas para el reporte  
            columnas = ["Producto", "Precio Promoción", "Descuento", "Stock"]  

            # Archivo PDF con timestamp  
            archivo = f"Reporte_Promociones_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"  

            # Generar el PDF  
            self.generar_pdf("Reporte de Promociones - Micro Market", datos, columnas, archivo)  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo generar el reporte de promociones: {e}")  

    def regresar(self):
        self.destroy()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()
