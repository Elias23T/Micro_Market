from tkinter import *
from tkinter import ttk
from login import Login  # Clase Login que ahora usa pymssql
from container import Container  # Clase Container que también debe estar adaptada a pymssql

class Manager(Tk):  
    # Definir los permisos para cada rol
    roles_permisos = {
        "Vendedor": ["ventas", "productos", "clientes", "proveedor", "promociones"],
        "Administrador": ["ventas", "productos", "clientes", "proveedor", "promociones", "reportes", "configuracion", "empleados", "usuarios", "chatbot"]
    }

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)  
        self.title("Micro_Market")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)
        
        # Variables para almacenar rol y nombre de usuario
        self.current_user_role = None
        self.current_username = None

        # Crear un contenedor (Frame) que contenga todas las interfaces
        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        
        # Crear y almacenar los frames de Login y Container
        self.frames = {}
        self.frames[Login] = Login(container, self)
        self.frames[Container] = None  # Solo se crea cuando es necesario
        
        # Obtener la conexión de la clase Login
        self.db_connection = self.frames[Login].get_connection()

        # Mostrar inicialmente el frame de Login
        self.show_frame(Login)
        
        # Estilos de la aplicación
        self.style = ttk.Style()
        self.style.theme_use("clam")
    
    def show_frame(self, frame_class):
        # Mostrar el frame especificado
        if frame_class == Container:
            # Si el frame de Container no ha sido creado, crearlo
            if self.frames[Container] is None:
                # Crear Container con la conexión y referencia a Manager como controlador
                self.frames[Container] = Container(self.current_user_role, self.current_username, self, self.db_connection)
                self.frames[Container].pack(fill=BOTH, expand=True)
            else:
                # Actualizar la información del usuario y rol en Container
                self.frames[Container].update_user_info(self.current_user_role, self.current_username)
                self.frames[Container].pack(fill=BOTH, expand=True)
                
            # Ocultar Login
            self.frames[Login].pack_forget()
        
        elif frame_class == Login:
            # Ocultar Container y mostrar Login
            if self.frames[Container] is not None:
                self.frames[Container].pack_forget()
            self.frames[Login].pack(fill=BOTH, expand=True)

    def set_user_info(self, username, role):
        # Configurar el rol y nombre de usuario desde Login
        self.current_username = username
        self.current_user_role = role
        # Cambiar a la interfaz principal (Container)
        self.show_frame(Container)
    
    def acceso_tabla(self, tabla):
        """Verifica si el usuario actual tiene acceso a una tabla específica."""
        permisos = self.roles_permisos.get(self.current_user_role, [])
        if tabla in permisos:
            return True
        else:
            print(f"Acceso denegado a {tabla}")
            return False





