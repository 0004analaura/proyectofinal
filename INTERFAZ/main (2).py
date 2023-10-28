import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario Proyecto ALgoritmos")
        self.root.configure(bg="teal")
        self.root.geometry('500x300')

        # Conectar a la base de datos SQLite
        self.conexion = sqlite3.connect("inventario.db")
        self.crear_tabla()

        # Crear widgets
        self.etiqueta_nombre = ttk.Label(root, text="Nombre:")
        self.entry_nombre = ttk.Entry(root)

        self.etiqueta_descripcion = ttk.Label(root, text="Descripción:")
        self.entry_descripcion = ttk.Entry(root)

        self.etiqueta_cantidad = ttk.Label(root, text="Cantidad:")
        self.entry_cantidad = ttk.Entry(root)

        self.etiqueta_proveedor = ttk.Label(root, text="Proveedor:")
        self.entry_proveedor = ttk.Entry(root)

        self.etiqueta_id_producto = ttk.Label(root, text="ID del Producto:")
        self.entry_id_producto = ttk.Entry(root)

        self.etiqueta_id_cliente = ttk.Label(root, text="ID del Cliente:")
        self.entry_id_cliente = ttk.Entry(root)

        self.boton_agregar = ttk.Button(root, text="Agregar", command=self.agregar_producto)
        self.boton_editar = ttk.Button(root, text="Editar", command=self.editar_producto)
        self.boton_guardar = ttk.Button(root, text="Guardar", command=self.guardar_edicion)
        self.boton_guardar.grid_remove()  # Ocultar el botón Guardar inicialmente

        self.etiqueta_busqueda = ttk.Label(root, text="Búsqueda:")
        self.entry_busqueda = ttk.Entry(root)
        self.boton_buscar = ttk.Button(root, text="Buscar", command=self.buscar_productos)


   # Crear estilo personalizado para el Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12), background="gray", foreground="black")
        style.configure("Treeview", font=("Helvetica", 11), background="green", foreground="black")
        style.map("Treeview", background=[("selected", "blue")])

        # Posicionar widgets
        self.etiqueta_busqueda.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_busqueda.grid(row=9, column=1, padx=5, pady=5)
        self.boton_buscar.grid(row=10, column=1, padx=10, pady=10)
    

        # Treeview para mostrar los productos existentes
        self.tree = ttk.Treeview(root, columns=('ID', 'Nombre', 'Descripción', 'Cantidad', 'Proveedor', 'ID Producto', 'ID Cliente'))
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Proveedor', text='Proveedor')
        self.tree.heading('ID Producto', text='ID Producto')
        self.tree.heading('ID Cliente', text='ID Cliente')

        # Posicionar widgets
        self.etiqueta_nombre.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        self.etiqueta_descripcion.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

        self.etiqueta_cantidad.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5)

        self.etiqueta_proveedor.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_proveedor.grid(row=3, column=1, padx=5, pady=5)

        self.etiqueta_id_producto.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id_producto.grid(row=4, column=1, padx=5, pady=5)

        self.etiqueta_id_cliente.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id_cliente.grid(row=5, column=1, padx=5, pady=5)

        self.boton_agregar.grid(row=7, column=0, columnspan=2, pady=10)
        self.boton_editar.grid(row=10, column=2, columnspan=2, pady=10, padx=10)
        self.boton_eliminar = ttk.Button(root, text="Eliminar", command=self.eliminar_producto)
        self.boton_eliminar.grid(row=7, column=2, columnspan=2, pady=10,padx=10)

        self.tree.grid(row=0, column=2, rowspan=7, padx=10)
       
        # Crear widgets
        self.boton_actualizar = ttk.Button(root, text="Actualizar", command=self.actualizar_tabla)

# Posicionar widgets
        self.boton_actualizar.grid(row=8, column=2, columnspan=2, pady=10)

        # Cargar productos existentes al Treeview
        self.cargar_productos()

        

    def buscar_productos(self):
        # Obtener el criterio de búsqueda
        cursor = self.conexion.cursor()
        criterio = self.entry_busqueda.get()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        # Filtrar los productos
        productos_filtrados = []
        for producto in productos:
            if criterio in producto[1]:
                productos_filtrados.append(producto)

        # Actualizar el Treeview
        self.tree.delete(*self.tree.get_children())
        for producto in productos_filtrados:
            self.tree.insert('', 'end', values=producto)
    def actualizar_tabla(self):
        # Cargar los productos de la base de datos

        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        # Limpiar el Treeview
        self.tree.delete(*self.tree.get_children())

        # Agregar los productos al Treeview
        for producto in productos:
            self.tree.insert('', 'end', values=producto)


    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                proveedor TEXT,
                id_producto TEXT,
                id_cliente TEXT
            )
        ''')
        self.conexion.commit()

    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()
        cantidad = self.entry_cantidad.get()
        proveedor = self.entry_proveedor.get()
        id_producto = self.entry_id_producto.get()
        id_cliente = self.entry_id_cliente.get()

        if nombre and cantidad:
            cursor = self.conexion.cursor()
            cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, proveedor, id_producto, id_cliente) VALUES (?, ?, ?, ?, ?, ?)",
                           (nombre, descripcion, cantidad, proveedor, id_producto, id_cliente))
            self.conexion.commit()
            print("Producto agregado correctamente.")
            self.limpiar_campos()
            self.cargar_productos()
        else:
            print("Por favor, ingrese nombre y cantidad.")

    def cargar_productos(self):
        # Limpiar productos existentes en el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        for producto in productos:
            self.tree.insert('', 'end', values=producto)

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_proveedor.delete(0, tk.END)
        self.entry_id_producto.delete(0, tk.END)
        self.entry_id_cliente.delete(0, tk.END)

    def editar_producto(self):
        # Obtener el item seleccionado en el Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            print("Por favor, seleccione un producto para editar.")
            return

        # Obtener los valores del item seleccionado
        values = self.tree.item(selected_item)['values']

        # Almacenar temporalmente los valores editados
        self.valores_editados = values

        # Eliminar la fila seleccionada del Treeview
        self.tree.delete(selected_item)

        # Mostrar los valores en los campos de entrada para su edición
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, self.valores_editados[1])

        self.entry_descripcion.delete(0, tk.END)
        self.entry_descripcion.insert(0, self.valores_editados[2])

        self.entry_cantidad.delete(0, tk.END)
        self.entry_cantidad.insert(0, self.valores_editados[3])

        self.entry_proveedor.delete(0, tk.END)
        self.entry_proveedor.insert(0, self.valores_editados[4])

        self.entry_id_producto.delete(0, tk.END)
        self.entry_id_producto.insert(0, self.valores_editados[5])

        self.entry_id_cliente.delete(0, tk.END)
        self.entry_id_cliente.insert(0, self.valores_editados[6])

        # Mostrar el botón "Guardar" y ocultar "Editar"
        self.boton_guardar.grid()
        self.boton_editar.grid_remove()

    def guardar_edicion(self):
        # Verificar si hay valores editados almacenados
        if self.valores_editados:
            # Obtener los valores actualizados
            producto_id = self.valores_editados[0]
            nombre = self.entry_nombre.get()
            descripcion = self.entry_descripcion.get()
            cantidad = self.entry_cantidad.get()
            proveedor = self.entry_proveedor.get()
            id_producto = self.entry_id_producto.get()
            id_cliente = self.entry_id_cliente.get()

            # Actualizar la base de datos
            self.actualizar_producto(producto_id, nombre, descripcion, cantidad, proveedor, id_producto, id_cliente)

            # Limpiar los valores editados y mostrar el botón "Editar"
            self.valores_editados = None
            self.boton_editar.grid()

        # Resto de tu código...

    def actualizar_producto(self, producto_id, nombre, descripcion, cantidad, proveedor, id_producto, id_cliente):
        cursor = self.conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=?, descripcion=?, cantidad=?, proveedor=?, id_producto=?, id_cliente=? WHERE id=?",
                       (nombre, descripcion, cantidad, proveedor, id_producto, id_cliente, producto_id))
        self.conexion.commit()
        print("Producto actualizado correctamente.")
        self.cargar_productos()

    def eliminar_producto(self):
        # Obtener el item seleccionado en el Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Error", "Por favor, seleccione un producto para eliminar.")
            return

        # Obtener el ID del producto seleccionado
        producto_id = self.tree.item(selected_item)['values'][0]

        # Confirmar la eliminación
        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?")
        if confirmacion:
            # Eliminar el producto de la base de datos
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
            self.conexion.commit()

            # Eliminar el producto del Treeview
            self.tree.delete(selected_item)

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")




if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()

       
