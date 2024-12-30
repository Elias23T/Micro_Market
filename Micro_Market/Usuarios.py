import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class Usuarios(tk.Frame):
    def __init__(self, padre, db_connection, username):  # Added username parameter
        super().__init__(padre)
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()
        self.username = username  # Store the current username
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()

    def widgets(self):
        # Título
        titulo = tk.Label(self, text="USUARIOS", font=("Arial", 24, "bold"), bg="#C6D9E3")
        titulo.place(x=400, y=10, width=300, height=30)

        # Botones Regresar y Salir
        self.crear_botones_regresar_salir()

        # Etiquetas de Fecha y Hora
        self.crear_fecha_hora_labels()

        # Configuración de LabelFrame para entradas
        Labelframe_entradas = tk.LabelFrame(
            self, text="Agregar Usuario", font=("sans", 12, "bold"), bg="#C6D9E3", padx=10, pady=10
        )
        Labelframe_entradas.place(x=25, y=110, width=400, height=300)

        tk.Label(Labelframe_entradas, text="Nombre Usuario:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=20)
        tk.Label(Labelframe_entradas, text="Contraseña:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=60)
        tk.Label(Labelframe_entradas, text="Rol:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=100)
        tk.Label(Labelframe_entradas, text="Empleado:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=140)

        self.entry_nombre = tk.Entry(Labelframe_entradas)
        self.entry_contrasena = tk.Entry(Labelframe_entradas, show="*")
        self.entry_rol = ttk.Combobox(Labelframe_entradas, values=["Vendedor", "Administrador"], state="readonly")
        self.entry_empleado = ttk.Combobox(Labelframe_entradas, state="readonly")

        self.entry_nombre.place(x=150, y=20, width=200)
        self.entry_contrasena.place(x=150, y=60, width=200)
        self.entry_rol.place(x=150, y=100, width=200)
        self.entry_empleado.place(x=150, y=140, width=200)

        self.cargar_empleados()

        # Configuración de LabelFrame para tabla
        Labelframe_tabla = tk.LabelFrame(
            self, text="Usuarios Registrados", font=("sans", 12, "bold"), bg="#C6D9E3", padx=10, pady=10
        )
        Labelframe_tabla.place(x=450, y=110, width=600, height=400)

        self.tree = ttk.Treeview(
            Labelframe_tabla,
            columns=("Id", "Nombre", "Rol", "Empleado"),
            show="headings",
            height=10,
        )
        self.tree.heading("Id", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Empleado", text="Empleado")

        self.tree.column("Id", width=25, anchor="center")
        self.tree.column("Nombre", width=150, anchor="w")
        self.tree.column("Rol", width=100, anchor="center")
        self.tree.column("Empleado", width=150, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones: Guardar, Modificar, Eliminar, Ver Contraseña
        btn_guardar = tk.Button(self, text="Guardar", command=self.guardar_usuario, bg="#4CAF50", fg="white", font=("sans", 10, "bold"))
        btn_guardar.place(x=25, y=550, width=150, height=40)

        btn_modificar = tk.Button(
            self, text="Modificar", command=self.mostrar_interfaz_modificar, bg="#FFC107", fg="black", font=("sans", 10, "bold")
        )
        btn_modificar.place(x=200, y=550, width=150, height=40)

        btn_eliminar = tk.Button(
            self, text="Eliminar", command=self.eliminar_usuario, bg="#F44336", fg="white", font=("sans", 10, "bold")
        )
        btn_eliminar.place(x=375, y=550, width=150, height=40)

        btn_ver_detalles = tk.Button(
            self, text="Ver Contraseña", command=self.ver_detalles_usuario, bg="#00BFFF", fg="white", font=("sans", 10, "bold")
        )
        btn_ver_detalles.place(x=550, y=550, width=150, height=40)

        self.cargar_datos()

    def crear_botones_regresar_salir(self):
        boton_regresar = tk.Button(
            self, text="REGRESAR", command=self.regresar, font=("Arial", 14), bg="blue", fg="white"
        )
        boton_regresar.place(x=10, y=10, width=120, height=40)

        boton_salir = tk.Button(self, text="SALIR", command=self.salir, font=("Arial", 14), bg="red", fg="white")
        boton_salir.place(x=980, y=10, width=100, height=40)

    def crear_fecha_hora_labels(self):
        self.fecha_label = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#C6D9E3")
        self.fecha_label.place(x=250, y=55, width=280, height=30)

        self.hora_label = tk.Label(self, text="", font=("Arial", 20, "bold"), bg="#C6D9E3")
        self.hora_label.place(x=610, y=55, width=250, height=30)

        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        ahora = datetime.now()
        fecha_actual = ahora.strftime("%Y-%m-%d")
        hora_actual = ahora.strftime("%H:%M:%S")
        self.fecha_label.config(text=f"FECHA: {fecha_actual}")
        self.hora_label.config(text=f"HORA: {hora_actual}")
        self.after(1000, self.actualizar_fecha_hora)

    def cargar_empleados(self):
        try:
            self.cursor.execute(
                "SELECT Id_Empleado, CONCAT(Nombre, ' ', Apellido_Paterno) AS NombreCompleto FROM Empleado WHERE Id_Usuario IS NULL"
            )
            empleados = self.cursor.fetchall()
            self.entry_empleado["values"] = [f"{empleado[0]} - {empleado[1]}" for empleado in empleados]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los empleados: {e}")

    def cargar_datos(self):
        try:
            for fila in self.tree.get_children():
                self.tree.delete(fila)

            self.cursor.execute(
                """
                SELECT U.Id_Usuario, U.NombreUsuario, U.Rol, 
                CONCAT(E.Nombre, ' ', E.Apellido_Paterno) AS Empleado
                FROM Usuario U
                LEFT JOIN Empleado E ON U.Id_Usuario = E.Id_Usuario
                """
            )
            for usuario in self.cursor.fetchall():
                self.tree.insert("", "end", values=usuario)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")

    def mostrar_interfaz_modificar(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para modificar.")
            return

        valores = self.tree.item(seleccion, "values")
        id_usuario = valores[0]

        ventana_modificar = tk.Toplevel(self)
        ventana_modificar.title("Modificar Usuario")
        ventana_modificar.geometry("400x300")
        ventana_modificar.configure(bg="#C6D9E3")

        tk.Label(ventana_modificar, text="Nombre Usuario:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=20)
        tk.Label(ventana_modificar, text="Contraseña:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=60)
        tk.Label(ventana_modificar, text="Rol:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=100)

        entry_nombre_mod = tk.Entry(ventana_modificar)
        entry_contrasena_mod = tk.Entry(ventana_modificar, show="*")
        entry_rol_mod = ttk.Combobox(ventana_modificar, values=["Vendedor", "Administrador"], state="readonly")

        entry_nombre_mod.place(x=150, y=20, width=200)
        entry_contrasena_mod.place(x=150, y=60, width=200)
        entry_rol_mod.place(x=150, y=100, width=200)

        entry_nombre_mod.insert(0, valores[1])
        entry_rol_mod.set(valores[2])

        def actualizar():
            nuevo_nombre = entry_nombre_mod.get()
            nueva_contrasena = entry_contrasena_mod.get()
            nuevo_rol = entry_rol_mod.get()

            if not all([nuevo_nombre, nueva_contrasena, nuevo_rol]):
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            try:
                # Prevent changing username to self
                if nuevo_nombre == self.username:
                    messagebox.showwarning("Advertencia", "No puedes cambiar tu propio nombre de usuario.")
                    return

                self.cursor.execute(
                    "UPDATE Usuario SET NombreUsuario = %s, Contrasena = %s, Rol = %s WHERE Id_Usuario = %s",
                    (nuevo_nombre, nueva_contrasena, nuevo_rol, id_usuario),
                )
                self.db_connection.commit()

                self.cargar_datos()
                messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
                ventana_modificar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar el usuario: {e}")

        def cancelar():
            ventana_modificar.destroy()

        btn_actualizar = tk.Button(ventana_modificar, text="Actualizar", command=actualizar, bg="#4CAF50", fg="white")
        btn_actualizar.place(x=100, y=200, width=100, height=30)

        btn_cancelar = tk.Button(ventana_modificar, text="Cancelar", command=cancelar, bg="#F44336", fg="white")
        btn_cancelar.place(x=220, y=200, width=100, height=30)

    def ver_detalles_usuario(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para ver los detalles.")
            return

        valores = self.tree.item(seleccion, "values")
        id_usuario = valores[0]

        ventana_detalles = tk.Toplevel(self)
        ventana_detalles.title("Detalles del Usuario")
        ventana_detalles.geometry("400x200")
        ventana_detalles.configure(bg="#C6D9E3")

        tk.Label(ventana_detalles, text="ID Usuario:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=20)
        tk.Label(ventana_detalles, text="Nombre Usuario:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=60)
        tk.Label(ventana_detalles, text="Contraseña:", font=("Arial", 12), bg="#C6D9E3").place(x=10, y=100)

        try:
            self.cursor.execute(
                "SELECT Contrasena FROM Usuario WHERE Id_Usuario = %s", (id_usuario,)
            )
            contrasena = self.cursor.fetchone()[0]

            tk.Label(ventana_detalles, text=valores[0], font=("Arial", 12), bg="#C6D9E3").place(x=150, y=20)
            tk.Label(ventana_detalles, text=valores[1], font=("Arial", 12), bg="#C6D9E3").place(x=150, y=60)
            tk.Label(ventana_detalles, text=contrasena, font=("Arial", 12), bg="#C6D9E3").place(x=150, y=100)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la contraseña: {e}")

        btn_cerrar = tk.Button(
            ventana_detalles, text="Cerrar", command=ventana_detalles.destroy, bg="#F44336", fg="white"
        )
        btn_cerrar.place(x=150, y=150, width=100, height=30)

    def guardar_usuario(self):
        nombre = self.entry_nombre.get()
        contrasena = self.entry_contrasena.get()
        rol = self.entry_rol.get()
        empleado = self.entry_empleado.get()

        if not all([nombre, contrasena, rol, empleado]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Check for duplicate username
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Usuario WHERE NombreUsuario = %s", (nombre,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "El nombre de usuario ya existe.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar nombre de usuario: {e}")
            return

        id_empleado = empleado.split(" - ")[0]

        try:
            self.cursor.execute(
                "INSERT INTO Usuario (NombreUsuario, Contrasena, Rol) VALUES (%s, %s, %s)",
                (nombre, contrasena, rol),
            )
            self.db_connection.commit()

            id_usuario = self.cursor.lastrowid
            self.cursor.execute("UPDATE Empleado SET Id_Usuario = %s WHERE Id_Empleado = %s", (id_usuario, id_empleado))
            self.db_connection.commit()

            self.cargar_datos()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")

    def eliminar_usuario(self):
        # Check if a user is selected
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
            return

        valores = self.tree.item(seleccion, "values")
        id_usuario = valores[0]
        nombre_usuario = valores[1]

        # Prevent self-deletion
        if nombre_usuario == self.username:
            messagebox.showerror("Error", "No puedes eliminar tu propio usuario.")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este usuario?"):
            return

        try:
            # Primero, desvincula al empleado
            self.cursor.execute("UPDATE Empleado SET Id_Usuario = NULL WHERE Id_Usuario = %s", (id_usuario,))
            
            # Luego elimina el usuario
            self.cursor.execute("DELETE FROM Usuario WHERE Id_Usuario = %s", (id_usuario,))
            
            self.db_connection.commit()
            self.cargar_datos()
            self.cargar_empleados()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")

    def regresar(self):
        self.destroy()

    def salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()