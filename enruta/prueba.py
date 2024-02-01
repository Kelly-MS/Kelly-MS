import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class Router:
    def __init__(self, nombre):
        self.nombre = nombre
        self.enlace_conectado = True
        self.router_siguiente = None

class RouterSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Desconexión de Enlace")
        self.root.geometry("800x400")

        self.routers = [Router(f"Router {i+1}") for i in range(4)]
        for i in range(len(self.routers) - 1):
            self.routers[i].router_siguiente = self.routers[i + 1]

        self.router_seleccionado = tk.StringVar()
        self.router_seleccionado.set(self.routers[0].nombre)

        self.estado_label = tk.Label(root, text="Estado del Enlace: Conectado", font=("Helvetica", 12))
        self.estado_label.pack(pady=10)

        self.router_menu = ttk.Combobox(root, textvariable=self.router_seleccionado, values=[router.nombre for router in self.routers], state="readonly")
        self.router_menu.pack(pady=10)

        self.router_menu.bind("<<ComboboxSelected>>", self.actualizar_icono_router)

        self.simular_conexion_btn = tk.Button(root, text="Simular Conexión de Enlace", command=self.simular_conexion)
        self.simular_conexion_btn.pack(pady=10)

        self.simular_desconexion_btn = tk.Button(root, text="Simular Desconexión de Enlace", command=self.simular_desconexion)
        self.simular_desconexion_btn.pack(pady=10)

        self.agregar_router_btn = tk.Button(root, text="Agregar Router", command=self.agregar_router)
        self.agregar_router_btn.pack(pady=10)

        # Crear un frame para la cuadrícula de routers
        self.frame_routers = tk.Frame(root)
        self.frame_routers.pack()

        # Cargar imágenes de los routers
        self.imagen_conectado = ImageTk.PhotoImage(Image.open("router_conectado.png").resize((50, 50)))
        self.imagen_desconectado = ImageTk.PhotoImage(Image.open("router_desconectado.png").resize((50, 50)))

        # Crear etiquetas para mostrar los iconos y nombres de los routers
        self.labels_routers = []
        for router in self.routers:
            frame_router = tk.Frame(self.frame_routers)
            frame_router.grid(row=0, column=self.routers.index(router), padx=10)

            label_router = tk.Label(frame_router, image=self.imagen_conectado)
            label_router.pack()

            label_nombre_router = tk.Label(frame_router, text=router.nombre)
            label_nombre_router.pack()

            self.labels_routers.append((label_router, label_nombre_router))

    def simular_conexion(self):
        router_actual = next(router for router in self.routers if router.nombre == self.router_seleccionado.get())

        if not router_actual.enlace_conectado:
            router_actual.enlace_conectado = True
            self.estado_label.config(text=f"Estado del Enlace ({router_actual.nombre}): Conectado", fg="green")
            messagebox.showinfo("Restablecimiento de Enlace", f"¡Enlace en {router_actual.nombre} restablecido!")

        self.actualizar_icono_router()

    def simular_desconexion(self):
        router_actual = next(router for router in self.routers if router.nombre == self.router_seleccionado.get())

        if router_actual.enlace_conectado:
            router_actual.enlace_conectado = False
            self.estado_label.config(text=f"Estado del Enlace ({router_actual.nombre}): Desconectado", fg="red")
            messagebox.showwarning("Desconexión de Enlace", f"¡Enlace en {router_actual.nombre} desconectado!")

            # Desconectar todos los routers siguientes en la cadena
            router = router_actual.router_siguiente
            while router is not None:
                router.enlace_conectado = False
                router = router.router_siguiente

        self.actualizar_icono_router()

    def agregar_router(self):
        nuevo_router = Router(f"Router {len(self.routers) + 1}")
        if self.routers:
            ultimo_router = self.routers[-1]
            ultimo_router.router_siguiente = nuevo_router
        self.routers.append(nuevo_router)
        self.actualizar_cuadricula_routers()

        # Actualizar la lista de valores en el menú desplegable
        self.router_menu["values"] = [router.nombre for router in self.routers]

    def actualizar_cuadricula_routers(self):
        # Eliminar todos los frames existentes
        for frame, _ in self.labels_routers:
            frame.destroy()

        self.labels_routers = []

        # Contadores para las columnas
        column1 = 0
        column2 = 0

        for router in self.routers:
            # Decide en qué columna colocar el router
            if self.routers.index(router) < 10:
                column = column1
                row = 0  # Los routers del 1 al 10 estarán en la fila 0
                column1 += 1
            else:
                column = column2
                row = 1  # Los routers a partir del 11 estarán en la fila 1
                column2 += 1

            frame_router = tk.Frame(self.frame_routers)
            frame_router.grid(row=row, column=column, padx=10)

            label_router = tk.Label(frame_router, image=self.imagen_conectado)
            label_router.pack()

            label_nombre_router = tk.Label(frame_router, text=router.nombre)
            label_nombre_router.pack()

            self.labels_routers.append((label_router, label_nombre_router))

    def actualizar_icono_router(self, event=None):
        for router, (label_router, _) in zip(self.routers, self.labels_routers):
            if router.enlace_conectado:
                label_router.config(image=self.imagen_conectado)
            else:
                label_router.config(image=self.imagen_desconectado)

if __name__ == "__main__":
    root = tk.Tk()
    app = RouterSimulation(root)
    root.mainloop()
