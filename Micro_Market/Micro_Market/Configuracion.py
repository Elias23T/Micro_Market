import tkinter as tk
from tkinter import ttk, messagebox

class Configuracion(tk.Frame):
    def __init__(self, padre, controlador=None):
        super().__init__(padre)
        self.controlador = controlador
        self.pack(fill="both", expand=True)  # Asegura que el Frame se muestre
        self.widgets()
    
    def widgets(self):
        # LabelFrame principal
        Labelframe = tk.LabelFrame(self, text="Crear categoría de producto", font=("sans", 12, "bold"), bg="#C6D9E3")
        Labelframe.place(x=25, y=30, width=400, height=300)
        
        # Etiqueta y entrada para el nombre de la categoría
        lbl_nombre = tk.Label(Labelframe, text="Nombre:", bg="#C6D9E3", font=("sans", 10))
        lbl_nombre.place(x=20, y=30)
        
        self.entry_nombre = tk.Entry(Labelframe, font=("sans", 10), width=25)
        self.entry_nombre.place(x=90, y=30)
        
        # Botón para guardar
        btn_guardar = tk.Button(Labelframe, text="Guardar", command=self.guardar_categoria, bg="#4CAF50", fg="white", font=("sans", 10, "bold"))
        btn_guardar.place(x=150, y=70, width=100, height=30)
        
        # Treeview para mostrar las categorías
        self.tree = ttk.Treeview(Labelframe, columns=("Id", "Nombre"), show="headings", height=8)
        self.tree.heading("Id", text="Id")
        self.tree.heading("Nombre", text="Nombre")
        
        self.tree.column("Id", width=50, anchor="center")
        self.tree.column("Nombre", width=200, anchor="w")
        
        self.tree.place(x=20, y=120, width=350, height=120)
        
        # Scrollbar para el Treeview
        scrollbar = ttk.Scrollbar(Labelframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=375, y=120, height=120)
        
        # Simular datos iniciales (reemplazar con datos de base de datos)
        self.datos = [
            (1, "batallanos"),
            (2, "bebidas"),
        ]
        self.cargar_datos()

    def guardar_categoria(self):
        nombre = self.entry_nombre.get().strip()
        
        if not nombre:
            messagebox.showwarning("Advertencia", "El campo 'Nombre' no puede estar vacío.")
            return
        
        # Aquí se puede agregar la lógica para guardar la categoría en la base de datos
        nuevo_id = len(self.datos) + 1
        self.datos.append((nuevo_id, nombre))
        self.tree.insert("", "end", values=(nuevo_id, nombre))
        
        # Limpiar la entrada
        self.entry_nombre.delete(0, tk.END)
        messagebox.showinfo("Éxito", "Categoría guardada correctamente.")
    
    def cargar_datos(self):
        # Cargar datos en el Treeview
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        
        for dato in self.datos:
            self.tree.insert("", "end", values=dato)
            