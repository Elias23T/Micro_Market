import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime


class Promociones(tk.Frame):
    def __init__(self, padre, db_connection):
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.config(bg="#C6D9E3")
        self.place(x=0, y=0, width=1100, height=650)
        self.crear_widgets()

    def crear_widgets(self):  
        """Crea y organiza los elementos de la interfaz."""
        # Título  
        titulo = tk.Label(self, text="Productos en Promoción", font=("Arial", 24, "bold"), bg="#C6D9E3", fg="black")  
        titulo.place(x=350, y=10, width=400, height=40)  

        # Botón regresar  
        tk.Button(self, text="REGRESAR", font=("Arial", 14), bg="blue", fg="white", command=self.regresar).place(x=10, y=10, width=150, height=40)  

        # Botón salir  
        tk.Button(self, text="SALIR", font=("Arial", 14), bg="red", fg="white", command=self.salir).place(x=940, y=10, width=150, height=40)  

        # Fecha y Hora  
        self.fecha_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#C6D9E3")  
        self.fecha_label.place(x=700, y=60, width=200, height=30)  
        self.hora_label = tk.Label(self, text="", font=("Arial", 14, "bold"), bg="#C6D9E3")  
        self.hora_label.place(x=900, y=60, width=200, height=30)  

        self.actualizar_fecha_hora()  

        # Tabla de productos en promoción  
        self.crear_tabla_productos_promocion()
        # Botones de acción
        self.crear_botones_acciones()

    def crear_tabla_productos_promocion(self):  
        """Crea la tabla (Treeview) que muestra todos los productos en promoción."""  
        tabla_frame = tk.LabelFrame(self, text="Productos en Promoción", font=("Arial", 14, "bold"), bg="#C6D9E3", highlightbackground="green", highlightthickness=2)  
        tabla_frame.place(x=20, y=100, width=1050, height=400)  

        columnas = ("ID Promoción", "Nombre Promoción", "Producto", "Descuento (%)", "Precio Promoción", "Fecha Inicio", "Fecha Fin", "Estado Promoción")  
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show='headings', height=15)  

        for col in columnas:  
            self.tree.heading(col, text=col)  
            self.tree.column(col, anchor=tk.CENTER, width=120)  

        self.tree.pack(fill=tk.BOTH, expand=True)  

        scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)  
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)  
        self.tree.configure(yscrollcommand=scrollbar_y.set)  

        scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=self.tree.xview)  
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)  
        self.tree.configure(xscrollcommand=scrollbar_x.set)  

        self.cargar_productos_en_promocion()

    def cargar_productos_en_promocion(self):  
        """Carga todos los productos en promoción desde la base de datos al Treeview."""  
        try:  
            self.tree.delete(*self.tree.get_children())  
            self.cursor.execute("""  
                SELECT pr.Id_Promocion, 
                       pr.NombrePromocion, 
                       p.NombreProducto AS Producto, 
                       pr.Descuento, 
                       p.PrecioPromocion, 
                       pr.FechaInicio, 
                       pr.FechaFin,
                       CASE 
                           WHEN p.EnPromocion = 1 THEN 'Activo'
                           ELSE 'Inactivo'
                       END AS EstadoPromocion
                FROM Promociones pr
                INNER JOIN Productos p ON pr.Producto = p.NombreProducto
            """)  
            for row in self.cursor.fetchall():  
                self.tree.insert("", "end", values=row)  
        except Exception as e:  
            messagebox.showerror("Error", f"No se pudo cargar los productos en promoción: {e}")  
    def editar_promocion(self):
        """Permite editar una promoción seleccionada."""
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Advertencia", "Selecciona una promoción para editar.")
            return

        valores = self.tree.item(item, "values")
        try:
            nuevo_descuento = float(simpledialog.askstring("Editar Promoción", "Nuevo descuento (%):", initialvalue=valores[3]))
            self.cursor.execute("""
                UPDATE Promociones 
                SET Descuento = %s, PrecioDescuento = PrecioDescuento * (1 - (%s / 100))
                WHERE Id_Promocion = %s
            """, (nuevo_descuento, nuevo_descuento, valores[0]))
            self.db_connection.commit()
            messagebox.showinfo("Éxito", "Promoción actualizada correctamente.")
            self.cargar_productos_en_promocion()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la promoción: {e}")

    def desactivar_promocion(self):
        """Desactiva la promoción del producto relacionado."""
        self.actualizar_estado_producto(0, "desactivada")

    def activar_promocion(self):
        """Activa la promoción del producto relacionado."""
        self.actualizar_estado_producto(1, "activada")

    def actualizar_estado_producto(self, estado, mensaje):
        """Actualiza el atributo EnPromocion en la tabla Productos."""
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Advertencia", "Selecciona una promoción.")
            return

        valores = self.tree.item(item, "values")
        producto = valores[2]  # Suponiendo que la columna Producto contiene el nombre del producto
        try:
            self.cursor.execute("""
                UPDATE Productos 
                SET EnPromocion = %s 
                WHERE NombreProducto = %s
            """, (estado, producto))
            self.db_connection.commit()
            messagebox.showinfo("Éxito", f"Promoción {mensaje} correctamente para el producto '{producto}'.")
            self.cargar_productos_en_promocion()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la promoción: {e}")

    def actualizar_fecha_hora(self):  
        """Actualiza la fecha y hora en tiempo real."""  
        ahora = datetime.now()  
        self.fecha_label.config(text=f"Fecha: {ahora.strftime('%Y-%m-%d')}")  
        self.hora_label.config(text=f"Hora: {ahora.strftime('%H:%M:%S')}")  
        self.after(1000, self.actualizar_fecha_hora)  

    def crear_botones_acciones(self):
        """Crea botones de acción: Editar, Desactivar, Activar."""
        botones_frame = tk.Frame(self, bg="#C6D9E3")
        botones_frame.place(x=20, y=520, width=1050, height=100)

        tk.Button(botones_frame, text="Editar", font=("Arial", 12), bg="orange", fg="white", command=self.editar_promocion).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(botones_frame, text="Desactivar", font=("Arial", 12), bg="red", fg="white", command=self.desactivar_promocion).pack(side=tk.LEFT, padx=20)
        tk.Button(botones_frame, text="Activar", font=("Arial", 12), bg="green", fg="white", command=self.activar_promocion).pack(side=tk.LEFT, padx=20)

    def regresar(self):  
        """Regresa a la ventana anterior."""  
        if messagebox.askyesno("Regresar", "¿Deseas regresar a la ventana anterior?"):  
            self.destroy()  

    def salir(self):  
        """Cierra la aplicación."""  
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):  
            self.master.destroy()  
