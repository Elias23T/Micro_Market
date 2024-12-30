import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import spacy
from difflib import SequenceMatcher

class ChatBot(tk.Frame):  
    def __init__(self, container, controlador, db_connection):
        super().__init__(container) 
        self.controlador = controlador
        self.db_connection = db_connection
        
        # Cargar el modelo de spaCy
        self.nlp = spacy.load("es_core_news_sm")
        
        # Configuración del marco
        self.config(width=1100, height=650, bg="#F0F0F0")
        self.place(x=0, y=0)
        
        # Título "CHATBOT"
        titulo = tk.Label(self, text="CHATBOT", font=("Arial", 24, "bold"), bg="#F0F0F0")
        titulo.place(x=400, y=15, width=300, height=30)

        # Botones Regresar y Salir
        self.crear_botones_regresar_salir()

        # Etiquetas de Fecha y Hora
        self.crear_fecha_hora_labels()

        # Área de visualización del chat
        self.chat_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', bg="#FFFFFF", font=("Arial", 12))
        self.chat_display.place(x=10, y=80, width=1080, height=450)
        
        # Campo de entrada del usuario
        self.user_input = tk.Entry(self, font=("Arial", 14))
        self.user_input.place(x=10, y=550, width=980, height=40)
        
        # Botón para enviar el mensaje
        send_button = tk.Button(self, text="Enviar", command=self.enviar_mensaje, font=("Arial", 12), bg="#4CAF50", fg="white")
        send_button.place(x=1000, y=550, width=80, height=40)

        # Diccionario de sinónimos de atributos de la base de datos
        self.MAPA_SINONIMOS = {
            "usuario": {
                "tabla": "Usuario",
                "columnas": {
                    "nombre": "NombreUsuario",
                    "contraseña": "Contrasena",
                    "rol": "Rol"
                }
            },
            "producto": {
                "tabla": "Productos",
                "columnas": {
                    "nombre": "NombreProducto",
                    "precio": "PrecioUnitario",
                    "stock": "Stock",
                    "fecha vencimiento": "FechaVencimiento"
                }
            },
            "venta": {
                "tabla": "Ventas",
                "columnas": {
                    "fecha": "FechaVenta",
                    "monto total": "MontoTotal"
                }
            },
            "promocion": {
                "tabla": "Promociones",
                "columnas": {
                    "nombre": "NombrePromocion",
                    "descuento": "Descuento",
                    "precio descuento": "PrecioDescuento"
                }
            }
        }
        
    def crear_botones_regresar_salir(self):
        """Crear botones de Regresar y Salir."""
        boton_regresar = tk.Button(
            self, text="REGRESAR", command=self.regresar, 
            font=("Arial", 14), bg="blue", fg="white"
        )
        boton_regresar.place(x=10, y=15, width=150, height=40)

        boton_salir = tk.Button(
            self, text="SALIR", command=self.salir, 
            font=("Arial", 14), bg="red", fg="white"
        )
        boton_salir.place(x=940, y=15, width=150, height=40)
    
    def crear_fecha_hora_labels(self):
        """Crear etiquetas de Fecha y Hora."""
        self.fecha_label = tk.Label(self, text="", font=("Arial", 14), bg="#F0F0F0")
        self.fecha_label.place(x=180, y=20, width=250, height=30)

        self.hora_label = tk.Label(self, text="", font=("Arial", 14), bg="#F0F0F0")
        self.hora_label.place(x=700, y=20, width=200, height=30)

        self.actualizar_fecha_hora()

    def actualizar_fecha_hora(self):
        """Actualizar la Fecha y Hora en tiempo real."""
        ahora = datetime.now()
        fecha_actual = ahora.strftime("%Y-%m-%d")
        hora_actual = ahora.strftime("%H:%M:%S")
        self.fecha_label.config(text=f"FECHA: {fecha_actual}")
        self.hora_label.config(text=f"HORA: {hora_actual}")
        self.after(1000, self.actualizar_fecha_hora)

    def regresar(self):
        """Regresar a la ventana anterior."""
        if messagebox.askyesno("Regresar", "¿Deseas regresar a la ventana anterior?"):
            self.destroy()

    def salir(self):
        """Salir de la aplicación."""
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?"):
            self.master.destroy()

    def enviar_mensaje(self):
        user_text = self.user_input.get()
        self.user_input.delete(0, tk.END)
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Tú: " + user_text + "\n")
        self.chat_display.config(state='disabled')
        respuesta = self.procesar_mensaje(user_text)
        self.mostrar_respuesta(respuesta)

    def procesar_mensaje(self, mensaje):
        mensaje = mensaje.lower()

        # Detectar frases similares para mostrar productos
        frases_productos = [
            "muéstrame todos los productos",
            "quiero ver mis productos",
            "enséñame los productos",
            "muéstrame mis productos"
        ]
        for frase in frases_productos:
            if self.coincidencia_similar(mensaje, frase) > 0.8:
                return self.consultar_todos_los_productos()
    
        # Proceso normal de detección de entidad y atributo
        entidad, atributo = self.detectar_entidad_y_atributo(mensaje)
        filtro = self.detectar_filtro(mensaje)

        if entidad and atributo:
            tabla = self.MAPA_SINONIMOS[entidad]["tabla"]
            columna = self.MAPA_SINONIMOS[entidad]["columnas"].get(atributo)

            if not columna:
                return f"No se encontró el atributo '{atributo}' en la entidad '{entidad}'."

            return self.ejecutar_consulta(tabla, columna, filtro)
        else:
            return "Lo siento, no entiendo tu consulta. Intenta reformularla."

        
    def consultar_todos_los_productos(self):
        """Consulta todos los productos en la base de datos."""
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT NombreProducto, PrecioUnitario, Stock FROM Productos"
            cursor.execute(query)
            resultado = cursor.fetchall()
        
            if resultado:
                respuesta = "Lista de productos:\n"
                for fila in resultado:
                    respuesta += f"- {fila[0]} | Precio: {fila[1]:.2f} | Stock: {fila[2]}\n"
                return respuesta
            else:
                return "No se encontraron productos en la base de datos."
        except Exception as e:
            return f"Error al consultar productos: {e}"


    def detectar_entidad_y_atributo(self, mensaje):
        entidad_detectada, atributo_detectado = None, None
        for entidad, data in self.MAPA_SINONIMOS.items():
            if entidad in mensaje or f"{entidad}s" in mensaje:  # Detectar plurales
                entidad_detectada = data["tabla"]
                for alias, columna in data["columnas"].items():
                    if alias in mensaje:
                        atributo_detectado = columna
                        break
            if entidad_detectada and atributo_detectado:
                break
        return entidad_detectada, atributo_detectado

    def detectar_filtro(self, mensaje):
        """Detecta un filtro, como 'del producto X'."""
        if "del producto" in mensaje:
            producto = mensaje.split("del producto")[1].strip()
            return {"columna": "NombreProducto", "valor": producto}
        elif "del cliente" in mensaje:
            cliente = mensaje.split("del cliente")[1].strip()
            return {"columna": "Nombre", "valor": cliente}
        return None

    def ejecutar_consulta(self, tabla, columna, filtro):
        try:
            cursor = self.db_connection.cursor()
            query = f"SELECT {columna} FROM {tabla}"
            if filtro:
               query += f" WHERE {filtro['columna']} = ?"
               cursor.execute(query, (filtro['valor'],))
            else:
               cursor.execute(query)
            resultado = cursor.fetchall()
            if resultado:
                return "\n".join([str(fila[0]) for fila in resultado])
            else:
                return f"No se encontraron resultados en la tabla {tabla} para la columna {columna}."
        except Exception as e:
            return f"Error al realizar la consulta: {e}"
        
    def coincidencia_similar(self, texto_usuario, texto_objetivo):
        """
        Calcula la similitud entre dos textos.
        """
        return SequenceMatcher(None, texto_usuario, texto_objetivo).ratio()



    def mostrar_respuesta(self, respuesta):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Chatbot: " + respuesta + "\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)