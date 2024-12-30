import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Productos import Productos
from Ventas import Ventas
from Clientes import Clientes
from Configuracion import Configuracion
from Empleados import Empleados
from Promociones import Promociones
from Proveedor import Proveedor
from Reportes import Reportes
from Usuarios import Usuarios
from ChatBot import ChatBot  # Importar la clase ChatBot
import pymssql  # Cambio de pyodbc a pymssql

class Container(tk.Frame):
    def __init__(self, user_role, username, controlador, db_connection):
        super().__init__(controlador)
        self.config(width=1100, height=650)  # Ajustar tamaño del contenedor sin usar place
        self.pack_propagate(False)  # Mantener el tamaño del contenedor fijo
        self.user_role = user_role
        self.username = username
        self.controlador = controlador  # Referencia al controlador (Manager)
        self.db_connection = db_connection  # Conexión a la base de datos proporcionada por Manager

        # Crear los elementos de la interfaz
        self.create_interface()

        # Mostrar barra de estado en la parte inferior
        self.status_bar()

    def update_user_info(self, user_role, username):
        """Actualiza el rol y nombre de usuario al volver a mostrar la interfaz."""
        self.user_role = user_role
        self.username = username
        # Actualizar la barra de estado con el nuevo usuario y rol
        self.status_bar()

    def create_interface(self):
        # Encabezado
        header = tk.Label(self, text="MICRO_MARKET CHOREÑITO", font=("Arial", 24, "bold"), bg="lightgray")
        header.pack(fill="x", ipady=10)

        # Botón de salida en la esquina superior derecha
        exit_button = tk.Button(self, text="Salir", command=self.exit_to_login, bg="red", fg="white", font=("Arial", 12, "bold"))
        exit_button.place(x=1040, y=10, width=50, height=40)

        # Panel izquierdo
        left_frame = tk.Frame(self, bg="lightblue", highlightbackground="black", highlightthickness=1)
        left_frame.place(x=20, y=70, width=200, height=500)
        
        # Botones del panel izquierdo
        self.add_button(left_frame, "Ventas", self.access_ventas, 10, 20, 180, 60)
        self.add_button(left_frame, "Productos", self.access_productos, 10, 90, 180, 60)
        self.add_button(left_frame, "Clientes", self.access_clientes, 10, 160, 180, 60)
        self.add_button(left_frame, "Proveedor", self.access_proveedor, 10, 230, 180, 60)
        self.add_button(left_frame, "Promociones", self.access_promociones, 10, 300, 180, 60)

        # Panel central para la imagen y la información de contacto
        center_frame = tk.Frame(self, bg="lightblue", highlightbackground="black", highlightthickness=1)
        center_frame.place(x=250, y=70, width=600, height=500)
        
        # Canvas para agregar la imagen de fondo
        canvas = tk.Canvas(center_frame, width=600, height=500)
        canvas.pack(fill="both", expand=True)
        
        # Cargar la imagen de fondo
        image = Image.open("Imagenes/Grupo.jpg")
        image = image.resize((600, 500), Image.LANCZOS)  # Ajustar el tamaño de la imagen
        self.background_image = ImageTk.PhotoImage(image)
        
        # Mostrar la imagen de fondo en el Canvas
        canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        
        # Colocar las etiquetas de texto sobre la imagen de fondo
        canvas.create_text(300, 30, text="ELABORADO", font=("Arial", 24, "bold"), fill="BLACK")
        canvas.create_text(300, 100, text="Elias Terrazas Azurduy",
                           font=("Arial", 14), fill="Black")
        canvas.create_text(300, 470, text="INGENIERIA DE SISTEMAS-2024",
                           font=("Arial", 12), fill="Black")

        # Panel derecho
        right_frame = tk.Frame(self, bg="lightblue", highlightbackground="black", highlightthickness=1)
        right_frame.place(x=880, y=70, width=200, height=500)
        
        # Botones del panel derecho
        self.add_button(right_frame, "Reportes", self.access_reportes, 10, 20, 180, 60)
        self.add_button(right_frame, "Configuración", self.access_configuracion, 10, 90, 180, 60)
        self.add_button(right_frame, "Empleados", self.access_empleados, 10, 160, 180, 60)
        self.add_button(right_frame, "Usuarios", self.access_usuarios, 10, 230, 180, 60)
        self.add_button(right_frame, "ChatBot", self.access_chatbot, 10, 300, 180, 60)

    def add_button(self, parent, text, command, x, y, width, height):
        """Añade un botón a un frame dado."""
        btn = tk.Button(parent, text=text, command=command, font=("Arial", 12, "bold"))
        btn.place(x=x, y=y, width=width, height=height)

    # Métodos de acceso a cada sección con validación de roles
    def access_ventas(self):
        if self.user_role in ["Administrador", "Vendedor"]:
            ventas_frame= Ventas(self.controlador, self.db_connection)
            ventas_frame.place(x=0,y=0, width=1100, height=650)
            ventas_frame.tkraise()
        else:
            self.show_access_denied()

    def access_productos(self):
        if self.user_role in ["Administrador", "Vendedor"]:
            productos_frame = Productos(self.controlador, self.db_connection)
            productos_frame.place(x=0, y=0, width=1100, height=650)
            productos_frame.tkraise()
        else:
            self.show_access_denied()

    def access_clientes(self):
        if self.user_role in ["Administrador", "Vendedor"]:
            clientes_frame= Clientes(self.controlador, self.db_connection)
            clientes_frame.place(x=0,y=0,width=1100, height=650)
            clientes_frame.tkraise()
        else:
            self.show_access_denied()

    def access_proveedor(self):
        if self.user_role in ["Administrador", "Vendedor"]:
            proveedor_frame=Proveedor(self.controlador,self.db_connection)
            proveedor_frame.place(x=0,y=0, width=1100,height=650)
            proveedor_frame.tkraise()
        else:
            self.show_access_denied()

    def access_promociones(self):
        if self.user_role in ["Administrador", "Vendedor"]:
            promociones_frame=Promociones(self.controlador, self.db_connection)
            promociones_frame.place(x=0,y=0, width=1100, height=650)
            promociones_frame.tkraise()
        else:
            self.show_access_denied()

    def access_reportes(self):
        if self.user_role == "Administrador":
            print("Acceso a Reportes")
        else:
            self.show_access_denied()

    def access_configuracion(self):
        if self.user_role == "Administrador":
            configuracion_frame= Configuracion(self.controlador, self.db_connection)
            configuracion_frame.place(x=0,y=0,width=1100, height=650)
            configuracion_frame.tkraise()
        else:
            self.show_access_denied()

    def access_empleados(self):
        if self.user_role == "Administrador":
            empleado_frame=Empleados(self.controlador, self.db_connection)
            empleado_frame.place(x=0,y=0,width=1100, height=650)
            empleado_frame.tkraise()
        else:
            self.show_access_denied()

    def access_usuarios(self):
        if self.user_role == "Administrador":
            usuario_frame=Usuarios(self.controlador, self.db_connection)
            usuario_frame.place(x=0,y=0,width=1100, height=650)
            usuario_frame.tkraise()
        else:
            self.show_access_denied()

    def access_chatbot(self):
        """Muestra la interfaz del ChatBot en la ventana actual."""
        # Crear instancia de ChatBot con los parámetros correctos
        chatbot_frame = ChatBot(self, self.controlador, self.db_connection)  # Instancia de ChatBot
        chatbot_frame.place(x=0, y=0, width=1100, height=650)  # Ajustar tamaño para ocupar todo el contenedor
        chatbot_frame.tkraise()  # Eleva el chatbot al frente para ser visible

    def show_access_denied(self):
        """Muestra un mensaje de acceso denegado."""
        messagebox.showerror("Acceso denegado", "No tienes permiso para acceder a esta sección.")

    def exit_to_login(self):
        if messagebox.askyesno("Confirmación", "¿Desea cerrar la sesión y volver al login?"):
            from login import Login
            self.controlador.show_frame(Login)

    def status_bar(self):
        # Barra de estado en la parte inferior
        status_frame = tk.Frame(self, bg="lightgray")
        status_frame.place(x=0, y=620, width=1100, height=30)

        # Actualiza el texto para mostrar el nombre de usuario y rol actuales
        user_label = tk.Label(status_frame, text=f"Bienvenido: {self.username}", bg="lightgray")
        user_label.pack(side="left", padx=10)

        role_label = tk.Label(status_frame, text=f"Rol: {self.user_role}", bg="lightgray")
        role_label.pack(side="left", padx=10)

