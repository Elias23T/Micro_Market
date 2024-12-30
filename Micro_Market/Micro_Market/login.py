from tkinter import * 
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pymssql as DB  # Cambiado pyodbc por pymssql
from container import Container

class Login(tk.Frame):
    _codigo_registro = "1234"  # Código de registro requerido para todos los registros

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.connection = None
        self.establecer_conexion()
        self.bg_image = Image.open("Imagenes/MicroMarket.jpg")
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.show_login_interface()

    def establecer_conexion(self):
        # Configurar la conexión a la base de datos
        try:
            self.connection = DB.connect(server='clown', user='Elias23', password='1234', database='Micro_Market')
            print("Conexion exitosa a la base de datos")
        except DB.Error as e:
            messagebox.showerror(title="Error", message="No se conecto a la base de datos: {}".format(e))

    def get_connection(self):
        # Método para acceder a la conexión desde otras clases
        return self.connection

    def validacion(self, user, pas):
        return len(user) > 0 and len(pas) > 0

    def login(self):
        user = self.username.get()
        pas = self.contra.get()

        if self.validacion(user, pas):
            consulta = "SELECT NombreUsuario, Rol FROM dbo.Usuario WHERE NombreUsuario=%s AND Contrasena=%s"
            parametros = (user, pas)
            
            try:
                cursor = self.connection.cursor()
                cursor.execute(consulta, parametros)
                resultado = cursor.fetchone()

                if resultado:
                    username, role = resultado
                    # Configurar el usuario y rol en el controlador (Manager)
                    self.controlador.set_user_info(username, role)
                    # Cambiar a la interfaz principal (Container)
                    self.controlador.show_frame(Container)
                else:
                    self.username.delete(0, 'end')
                    self.contra.delete(0, 'end')
                    messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
                
                cursor.close()

            except DB.Error as e:
                messagebox.showerror(title="Error", message="Error en la conexión a la base de datos: {}".format(e))
        else:
            messagebox.showerror(title="Error", message="Llene todas las casillas")

    def show_register_interface(self):
        # Limpiar la interfaz de inicio de sesión
        for widget in self.winfo_children():
            widget.destroy()
        
        fondo = tk.Frame(self, background="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)
        
        bg_label = ttk.Label(fondo, image=self.bg_image)
        bg_label.image = self.bg_image
        bg_label.place(x=0, y=0, width=1100, height=650)

        frame1 = tk.Frame(self, bg="#C6D9E3", highlightbackground="black", highlightthickness=1)
        frame1.place(x=350, y=70, width=350, height=525)

        tk.Label(frame1, text="Registrarse", font="arial 18 bold", bg="#C6D9E3").place(x=80, y=30)

        tk.Label(frame1, text="Nombre de usuario", font="arial 12 bold", bg="#FFF").place(x=60, y=100)
        self.reg_username = ttk.Entry(frame1, font="arial 12")
        self.reg_username.place(x=60, y=130, width=240, height=30)
        
        tk.Label(frame1, text="Contraseña", font="arial 12 bold", bg="#FFF").place(x=60, y=170)
        self.reg_password = ttk.Entry(frame1, show="*", font="arial 12")
        self.reg_password.place(x=60, y=200, width=240, height=30)
        
        tk.Label(frame1, text="Rol de usuario", font="arial 12 bold", bg="#FFF").place(x=60, y=240)
        self.role_var = StringVar()
        self.role_dropdown = ttk.Combobox(frame1, textvariable=self.role_var, font="arial 12", state="readonly")
        self.role_dropdown['values'] = ("Vendedor", "Administrador")
        self.role_dropdown.place(x=60, y=270, width=240, height=30)
        self.role_dropdown.current(0)  # Seleccionar "Vendedor" por defecto

        tk.Label(frame1, text="Código de registro", font="arial 12 bold", bg="#FFF").place(x=60, y=310)
        self.reg_code = ttk.Entry(frame1, font="arial 12")
        self.reg_code.place(x=60, y=340, width=240, height=30)

        tk.Button(frame1, text="Registrarse", font="arial 12 bold", command=self.save_user).place(x=60, y=380, width=240, height=40)
        tk.Button(frame1, text="Regresar", font="arial 12 bold", command=self.show_login_interface).place(x=60, y=430, width=240, height=40)

    def save_user(self):
        user = self.reg_username.get()
        pas = self.reg_password.get()
        role = self.role_var.get()
        code = self.reg_code.get()

        if code != self._codigo_registro:
            messagebox.showerror(title="Error", message="Codigo de registro incorrecto.")
            return

        if self.validacion(user, pas):
            consulta = "INSERT INTO dbo.Usuario (NombreUsuario, Contrasena, Rol) VALUES (%s, %s, %s)"
            parametros = (user, pas, role)
            
            try:
                cursor = self.connection.cursor()
                cursor.execute(consulta, parametros)
                self.connection.commit()
                messagebox.showinfo(title="Registro", message="Registro exitoso")
                self.show_login_interface()
                cursor.close()

            except DB.Error as e:
                messagebox.showerror(title="Error", message="Error en la conexion a la base de datos: {}".format(e))
        else:
            messagebox.showerror(title="Error", message="Complete todos los campos")

    def show_login_interface(self):   
        for widget in self.winfo_children():
            widget.destroy()
        
        fondo = tk.Frame(self, background="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)
        
        bg_label = ttk.Label(fondo, image=self.bg_image)
        bg_label.image = self.bg_image
        bg_label.place(x=0, y=0, width=1100, height=650)
        
        frame1 = tk.Frame(self, bg="#C6D9E3", highlightbackground="black", highlightthickness=1)
        frame1.place(x=350, y=70, width=350, height=525)
        
        tk.Label(frame1, text="Nombre de usuario", font="arial 16 bold", background="#FFF").place(x=80, y=250)
        self.username = ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=60, y=290, width=240, height=40)
        
        tk.Label(frame1, text="🔒 Contraseña", font="arial 16 bold", background="#FFF").place(x=110, y=340)
        self.contra = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.contra.place(x=60, y=380, width=240, height=40)
        
        tk.Button(frame1, text="Iniciar", font="arial 16 bold", command=self.login).place(x=60, y=430, width=240, height=40)
        
        tk.Button(frame1, text="Registrar", font="arial 16 bold", command=self.show_register_interface).place(x=60, y=480, width=240, height=40)
