import tkinter as tk
from tkinter import scrolledtext
import spacy
import re

class ChatBot(tk.Frame):  
    def __init__(self, container, controlador, db_connection):
        super().__init__(container) 
        self.controlador = controlador
        self.db_connection = db_connection
        
        # Cargar el modelo de spaCy
        self.nlp = spacy.load("es_core_news_sm")
        
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
            "empleado": {
                "tabla": "Empleado",
                "columnas": {
                    "nombre": "Nombre",
                    "apellido paterno": "Apellido_Paterno",
                    "apellido materno": "Apellido_Materno",
                    "ci": "CI",
                    "celular": "Celular"
                }
            },
            "cliente": {
                "tabla": "Cliente",
                "columnas": {
                    "nombre": "Nombre",
                    "apellido paterno": "Apellido_Paterno",
                    "apellido materno": "Apellido_Materno",
                    "ci": "CI",
                    "celular": "Celular"
                }
            },
            "categoria": {
                "tabla": "Categoria",
                "columnas": {
                    "nombre": "NombreCategoria",
                    "descripcion": "Descripcion"
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
                    "monto": "MontoTotal"
                }
            },
            "detalle venta": {
                "tabla": "DetalleVenta",
                "columnas": {
                    "cantidad": "Cantidad",
                    "precio unitario": "PrecioUnitario",
                    "total": "TotalVenta"
                }
            },
            "proveedor": {
                "tabla": "Proveedor",
                "columnas": {
                    "nombre": "Nombre",
                    "apellido paterno": "Apellido_Paterno",
                    "apellido materno": "Apellido_Materno",
                    "celular": "Celular",
                    "descripcion": "Descripcion"
                }
            },
            "compra": {
                "tabla": "CompraDeProveedor",
                "columnas": {
                    "fecha": "FechaCompra",
                    "monto": "MontoTotal"
                }
            },
            "promocion": {
                "tabla": "Promociones",
                "columnas": {
                    "nombre": "NombrePromocion",
                    "descripcion": "Descripcion",
                    "descuento": "Descuento",
                    "precio descuento": "PrecioDescuento",
                    "fecha inicio": "FechaInicio",
                    "fecha fin": "FechaFin"
                }
            }
        }
        
        self.config(width=1100, height=650, bg="#F0F0F0")
        self.place(x=0, y=0)
        
        # Área de visualización del chat
        self.chat_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', bg="#FFFFFF", font=("Arial", 12))
        self.chat_display.place(x=10, y=10, width=1080, height=550)
        
        # Campo de entrada del usuario
        self.user_input = tk.Entry(self, font=("Arial", 14))
        self.user_input.place(x=10, y=570, width=980, height=40)
        
        # Botón para enviar el mensaje
        send_button = tk.Button(self, text="Enviar", command=self.enviar_mensaje, font=("Arial", 12), bg="#4CAF50", fg="white")
        send_button.place(x=1000, y=570, width=80, height=40)
        
    def enviar_mensaje(self):
        user_text = self.user_input.get()
        self.user_input.delete(0, tk.END)
        
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Tú: " + user_text + "\n")
        self.chat_display.config(state='disabled')
        
        # Procesa el mensaje y genera la respuesta
        respuesta = self.procesar_mensaje(user_text)
        self.mostrar_respuesta(respuesta)
    
    def procesar_mensaje(self, mensaje):
        # Convertir el mensaje a minúsculas
        mensaje = mensaje.lower()
        
        # Detectar la entidad (tabla) y el atributo (columna)
        entidad, atributo = self.detectar_entidad_y_atributo(mensaje)

        if entidad and atributo:
            # Ejecutar la consulta en función de la entidad y el atributo detectado
            return self.ejecutar_consulta(entidad, atributo)
        else:
            return "Lo siento, no entiendo la consulta. ¿Podrías reformularla?"

    def detectar_entidad_y_atributo(self, mensaje):
        # Buscar coincidencias de entidad (tabla) y atributo (columna) en el diccionario de sinónimos
        entidad_detectada = None
        atributo_detectado = None
        
        for entidad, data in self.MAPA_SINONIMOS.items():
            if entidad in mensaje:
                entidad_detectada = data["tabla"]
                for alias, columna in data["columnas"].items():
                    if alias in mensaje:
                        atributo_detectado = columna
                        break
            if entidad_detectada and atributo_detectado:
                break
        
        return entidad_detectada, atributo_detectado

    def ejecutar_consulta(self, entidad, atributo):
        """
        Ejecuta una consulta en función de la entidad y el atributo detectados.
        """
        try:
            cursor = self.db_connection.cursor()
            query = f"SELECT {atributo} FROM {entidad}"
            cursor.execute(query)
            resultado = cursor.fetchall()
            if resultado:
                # Formatea el resultado en una lista o tabla de resultados
                respuesta = "\n".join([f"{fila[0]}" for fila in resultado])
                return f"{atributo} en {entidad}:\n{respuesta}"
            else:
                return f"No se encontraron resultados para {atributo} en {entidad}."
        except Exception as e:
            return f"Error al realizar la consulta: {str(e)}"

    def mostrar_respuesta(self, respuesta):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "Chatbot: " + respuesta + "\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)




 