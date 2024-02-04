import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Router:
    def __init__(self, nombre, x, y, imagen_conectado, imagen_desconectado):
        self.nombre = nombre
        self.x = x
        self.y = y
        self.imagen_conectado = imagen_conectado
        self.imagen_desconectado = imagen_desconectado
        self.enlace_conectado = True
        self.saltos = 0
        self.info_pase = []
        self.conexion = "N/A"
        # Información de la tabla
        self.tipo_enrutamiento = "Conectado"
        self.direccion_red = f"192.168.{x}.{y}"
        self.direccion_mask = "255.255.255.0"
        self.direccion_gw = "N/A"
        self.interfast_red = f"eth{x:02d}"
        self.satos = f"{self.saltos} saltos"

    def get_estado_fila(self):
        return "conectado" if self.enlace_conectado else "desconectado"
    def calcular_saltos_fijos(self, routers_conectados):
        # Esta función calcula los saltos fijos para el router dado
        saltos_fijos = 0

        for connected_router in routers_conectados:
            saltos_fijos += 1  # Puedes ajustar esto según tu lógica específica

        return saltos_fijos

class RouterSimulation:
    def __init__(self, root):
        self.table = None
        self.root = root
        self.root.title("Simulación de Conexión")
        self.estado_label = tk.Label(root, text="Proyecto Enrutamiento", font=("Comic Sans MS", 18, "italic bold"),
                                     bg="#FFD1DC", fg="purple")
        self.estado_label.pack(pady=10)
        self.root.geometry("1425x650")
        self.root.configure(bg="#FFD1DC")

        # Imágenes
        self.imagen_conectado = Image.open("router_conectado.png").convert("RGBA").resize((90, 90))

        self.imagen_desconectado = Image.open("router_desconectado.png").convert("RGBA").resize((90,90))

        self.routers = [
            Router("Router1", 50, 150, ImageTk.PhotoImage(self.imagen_conectado), ImageTk.PhotoImage(self.imagen_desconectado)),
            Router("Router2", 250, 150, ImageTk.PhotoImage(self.imagen_conectado), ImageTk.PhotoImage(self.imagen_desconectado)),
            Router("Router3", 50, 250, ImageTk.PhotoImage(self.imagen_conectado), ImageTk.PhotoImage(self.imagen_desconectado)),
            Router("Router4", 250, 250, ImageTk.PhotoImage(self.imagen_conectado), ImageTk.PhotoImage(self.imagen_desconectado))
        ]
        # Tabla
        self.table_frame = tk.Frame(root, bg="#FFD1DC")
        self.table_frame.pack(side=tk.BOTTOM, padx=1, pady=1)
        self.canvas = tk.Canvas(root, bg="#FFD1DC", height=500, width=300, bd=2, highlightthickness=0)
        self.canvas.pack(side=tk.TOP, anchor=tk.CENTER)
        self.conexiones = []
        self.dibujar_conexiones()
        self.dibujar_routers()
        self.create_routing_table()

    def dibujar_routers(self):
        espacio_entre_routers = 150
        y_position_router_1 = 150
        y_position_router_2 = 150
        for router in self.routers:
            if router.nombre in ["Router1", "Router2"]:
                y_position = y_position_router_1 if router.nombre == "Router1" else y_position_router_2
            else:
                y_position = y_position_router_1 + espacio_entre_routers
            self.dibujar_router(router, y_position)

    def dibujar_router(self, router, y_position):
        router.image_item = self.canvas.create_image(router.x, y_position, anchor=tk.CENTER,
                                                     image=router.imagen_conectado, tags=("router", router.nombre))

        self.posicionar_nombre(router, y_position)

        # Funcion del click con la imagen
        self.canvas.tag_bind(router.image_item, "<Button-1>", lambda event, router=router: self.on_image_click(router))

    def posicionar_nombre(self, router, y_position):
        # Solo mover los nombres de los routers 3 y 4
        if router.nombre in ["Router3", "Router4"]:
            nombre_y_position = y_position + router.imagen_conectado.height() // 2+13
        else:
            nombre_y_position = y_position - 50 if y_position < 200 else y_position + 50

        router.text_item = self.canvas.create_text(router.x, nombre_y_position, text=router.nombre, fill="green",
                                                   font=("Comic Sans MS", 10, "bold"), anchor=tk.S,
                                                   tags=("router", router.nombre))
    def on_image_click(self, router):
        # Simular conexión/desconexión al hacer clic en el router
        router.enlace_conectado = not router.enlace_conectado
        router.tipo_enrutamiento = "Conectado" if router.enlace_conectado else "Desconectado"

        # Actualiza saltos si está conectado
        if router.enlace_conectado:
            router.saltos += 1

        # Se actualiza las conexiones y tabla de enrutamiento
        self.actualizar_conexiones()
        self.actualizar_imagen_router(router)
        self.actualizar_color_nombre(router)
        self.actualizar_tabla()

    def actualizar_conexiones(self):
        # Se actualiza la información de la conexión
        for router in self.routers:
            router.conexion = ", ".join([connected_router.nombre for connected_router in self.routers if
                                         connected_router.enlace_conectado and connected_router != router])
        # Se eliminan todas las conexiones existentes
        for line in self.conexiones:
            self.canvas.delete(line)
        self.dibujar_conexiones()

    def actualizar_imagen_router(self, router):
        imagen = router.imagen_conectado if router.enlace_conectado else router.imagen_desconectado
        self.canvas.itemconfig(router.image_item, image=imagen)

    def actualizar_color_nombre(self, router):
        color = "red" if not router.enlace_conectado else "green"
        self.canvas.itemconfig(router.text_item, fill=color)

    def dibujar_conexiones(self):
        router1, router2, router3, router4 = self.routers

        if router1.enlace_conectado and router2.enlace_conectado:
            self.conexiones.append(
                self.canvas.create_line(router1.x + 30, router1.y, router2.x - 30, router2.y, fill="blue", width=2))

        if router3.enlace_conectado and router4.enlace_conectado:
            desplazamiento_y = 50
            self.conexiones.append(self.canvas.create_line(router3.x + 30, router3.y + desplazamiento_y, router4.x - 30,
                                                           router4.y + desplazamiento_y, fill="blue", width=2))

        if router1.enlace_conectado and router3.enlace_conectado:
            self.conexiones.append(
                self.canvas.create_line(router1.x, router1.y - 0, router3.x, router3.y + 0, fill="blue", width=2))

        if router2.enlace_conectado and router4.enlace_conectado:
            self.conexiones.append(
                self.canvas.create_line(router2.x, router2.y - 0, router4.x, router4.y + 0, fill="blue", width=2))

    def insert_data_to_table(self, router):
        routers_conectados = [connected_router for connected_router in self.routers if
                              connected_router.enlace_conectado and connected_router != router]
        saltos_fijos = router.calcular_saltos_fijos(routers_conectados)
        # Se obtiene los nombres de los routers conectados, excluyendo los desconectados
        routers_conectados_nombres = [connected_router.nombre for connected_router in routers_conectados]

        # Se verifica si el router está conectado
        if router.enlace_conectado:
            # Router conectado con los valores establecidos
            direccion_mask = router.direccion_mask
            index = self.routers.index(router) + 1
            base_direccion_gw = f"192.168.{index * 10}.1"
            direccion_gw = f"{base_direccion_gw}"
            tipo = "C"
            index = self.routers.index(router) + 1
            interfaz_red = f"eth{index:02d}"
            base_direccion_red = "192.168"
            direccion_red = f"{base_direccion_red}.{index * 10}.0"

        else:
            # Router desconectado,  se establecen los valores  "N/A"
            direccion_mask = "N/A"
            direccion_gw = "N/A"
            direccion_red = "N/A"
            interfaz_red = "N/A"
            tipo = "N/A"

        data = [
            router.nombre,
            tipo,
            router.tipo_enrutamiento,
            direccion_red,
            direccion_mask,
            direccion_gw,
            interfaz_red,
            f"{saltos_fijos} saltos" if router.enlace_conectado else "N/A",
            "N/A" if not router.enlace_conectado or not routers_conectados_nombres else routers_conectados_nombres,
            ", ".join(
                [f"{connected_router.nombre} ({connected_router.saltos} saltos)" for connected_router in self.routers if
                 connected_router.enlace_conectado and connected_router != router])
        ]
        # Se obtiene el color de fondo en función del estado del router si esta conectado o desconectado
        estado_fila = router.get_estado_fila()
        bg_color = "lightblue" if estado_fila == "conectado" else "lightcoral"

        # Se inserta los datos en la tabla y se establece el color de fondo
        self.table.insert("", "end", values=data, tags=(router.nombre, estado_fila), iid=router.nombre)
        self.table.tag_configure(estado_fila, background=bg_color)

    def create_routing_table(self):
        columns = ["Nombre", "Tipo","Estado Enrutamiento", "Dirección de Red", "Dirección Mask", "Dirección de GW",
                   "Interfaz de Red", "Saltos", "Conexión"]
        self.table = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse", height=5)
        # Ancho de las columnas
        column_width = 150

        for col in columns:
            self.table.heading(col, text=col, anchor=tk.CENTER)
            self.table.column(col, width=column_width, anchor=tk.CENTER)
        # Tamaño de la última columna ("Conexión") a un valor mayor
        self.table.column(columns[-1], width=250, stretch=tk.YES)
        # Estilo de la tabla para letras
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Comic Sans MS", 10, "bold"))
        style.map("Treeview", foreground=[("selected", "black")], background=[("selected", "#FFD1DC")])
        # Altura de la fila
        style.configure("Treeview", font=("Comic Sans MS", 10), rowheight=25, padding=10)

        for router in self.routers:
            self.insert_data_to_table(router)
        self.table.grid(row=0, column=0)
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=0)
        style.configure("Treeview.Heading", rowheight=4)

    def actualizar_tabla(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for router in self.routers:
            self.insert_data_to_table(router)

root = tk.Tk()
app = RouterSimulation(root)
root.mainloop()