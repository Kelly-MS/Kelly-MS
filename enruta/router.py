import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class Router:
    def __init__(self, nombre, direccion_red, mascara, direccion_gw):
        self.nombre = nombre
        self.enlace_conectado = True
        self.router_siguiente = None
        self.tabla_enrutamiento = {}
        self.direccion_red = direccion_red
        self.mascara = mascara
        self.direccion_gw = direccion_gw
        self.interfaces_red = []
        self.saltos_realizados = 0

    def agregar_ruta(self, destino, router_destino):
        self.tabla_enrutamiento[destino] = {'router_destino': router_destino}

    def agregar_interfaz_red(self, interfaz):
        self.interfaces_red.append(interfaz)

    def realizar_salto(self):
        self.saltos_realizados += 1


class RouterSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Desconexión de Enlace")
        self.root.geometry("800x400")
        self.root.configure(bg="#FFC0CB")

        self.routers = []

        self.router_seleccionado = tk.StringVar()
        self.router_seleccionado.set("")

        self.estado_label = tk.Label(root, text="Estado del Enlace: Conectado", font=("Helvetica", 15, "bold"),
                                     bg="#FFC0CB")

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

        self.mostrar_info_btn = tk.Button(root, text="Mostrar Información del Router", command=self.mostrar_info_router)
        self.mostrar_info_btn.pack(pady=10)

        self.frame_routers = tk.Frame(root, bg="#FFC0CB")
        self.frame_routers.pack()

        self.imagen_conectado = ImageTk.PhotoImage(Image.open("router_conectado.png").convert("RGBA").resize((50, 50)))
        self.imagen_desconectado = ImageTk.PhotoImage(Image.open("router_desconectado.png").convert("RGBA").resize((50, 50)))

        self.labels_routers = []

    def mostrar_info_router(self):
        if not self.routers:
            messagebox.showwarning("Sin Routers", "No hay routers para mostrar información.")
            return

        router_seleccionado_nombre = self.router_seleccionado.get()

        try:
            router_actual = next(router for router in self.routers if router.nombre == router_seleccionado_nombre)
        except StopIteration:
            messagebox.showwarning("Router no encontrado",
                                   f"No se encontró un router con el nombre {router_seleccionado_nombre}.")
            return

        if not router_actual.enlace_conectado:
            messagebox.showwarning("Router Desconectado",
                                   f"No puedes visualizar la información porque el router {router_actual.nombre} está desconectado.")
            return

        mensaje = f"Información del Router {router_actual.nombre}:\n"
        mensaje += f"Dirección de Red: {router_actual.direccion_red}\n"
        mensaje += f"Máscara: {router_actual.mascara}\n"
        mensaje += f"Dirección del Gateway: {router_actual.direccion_gw}\n"
        mensaje += f"Interfaces de Red: {', '.join(router_actual.interfaces_red)}\n"
        mensaje += f"Saltos Realizados: {router_actual.saltos_realizados}\n"

        if router_actual.tabla_enrutamiento:
            mensaje += "\nTabla de Enrutamiento:\n"
            for destino, info_ruta in router_actual.tabla_enrutamiento.items():
                router_destino_nombre = info_ruta['router_destino'].nombre
                if info_ruta['router_destino'].enlace_conectado:
                    mensaje += f"Destino: {destino}, Conectado a: {router_destino_nombre}\n"

        messagebox.showinfo("Información del Router", mensaje)

    def agregar_router(self):
        nuevo_router = Router(f"Router {len(self.routers) + 1}", f"192.168.{len(self.routers) + 1}.0",
                              "255.255.255.0", f"192.168.{len(self.routers) + 1}.1")
        nuevo_router.agregar_interfaz_red(f"Ethernet{len(self.routers)}")

        if self.routers:
            ultimo_router = self.routers[-1]
            ultimo_router.router_siguiente = nuevo_router

        self.routers.append(nuevo_router)

        # Realizar saltos solo al nuevo router
        for router_destino in self.routers:
            if router_destino != nuevo_router:
                nuevo_router.agregar_ruta(router_destino.nombre, router_destino)
                nuevo_router.realizar_salto()

        # Realizar saltos desde los routers existentes hacia el nuevo router
        for router_origen in self.routers:
            if router_origen != nuevo_router:
                router_origen.agregar_ruta(nuevo_router.nombre, nuevo_router)
                router_origen.realizar_salto()

        self.actualizar_icono_router()
        self.actualizar_cuadricula_routers()

        # Actualizar la lista de valores en el menú desplegable
        self.router_menu["values"] = [router.nombre for router in self.routers]

    def actualizar_cuadricula_routers(self):
        for frame, _ in self.labels_routers:
            frame.destroy()

        self.labels_routers = []

        column = 0
        row = 0

        for router in self.routers:
            frame_router = tk.Frame(self.frame_routers, bg="#FFC0CB", width=80,
                                    height=80)

            frame_router.grid(row=row, column=column, padx=10)

            label_router = tk.Label(frame_router,
                                    image=self.imagen_conectado if router.enlace_conectado else self.imagen_desconectado,
                                    bg="#FFC0CB")
            label_router.pack()

            label_nombre_router = tk.Label(frame_router, text=router.nombre, bg="#FFC0CB")
            label_nombre_router.pack()

            self.labels_routers.append((label_router, label_nombre_router))

            column += 1
            if column == 10:
                column = 0
                row += 1

        self.frame_routers.grid_columnconfigure(0, weight=1)

    def actualizar_icono_router(self, event=None):
        for router, (label_router, _) in zip(self.routers, self.labels_routers):
            label_router.config(image=self.imagen_conectado if router.enlace_conectado else self.imagen_desconectado)
    def simular_desconexion(self):
        router_seleccionado_nombre = self.router_seleccionado.get()

        try:
            router_desconectar = next(router for router in self.routers if router.nombre == router_seleccionado_nombre)
        except StopIteration:
            messagebox.showwarning("Router no encontrado",
                                   f"No se encontró un router con el nombre {router_seleccionado_nombre}.")
            return

        if not router_desconectar.enlace_conectado:
            messagebox.showinfo("Enlace ya desconectado",
                                f"El router {router_desconectar.nombre} ya está desconectado.")
            return

        # Guardar el estado del enlace antes de desconectar
        enlace_conectado_antes = router_desconectar.enlace_conectado

        # Desconectar el router
        router_desconectar.enlace_conectado = False
        self.actualizar_icono_router()
        self.actualizar_titulo_ventana(router_desconectar.nombre, False)
        messagebox.showinfo("Desconexión Exitosa",
                            f"Se ha simulado la desconexión del router {router_desconectar.nombre}.")

        # No contar los saltos realizados si el router está desconectado
        if enlace_conectado_antes:
            for router_destino in self.routers:
                if router_destino != router_desconectar and router_destino.enlace_conectado:
                    router_desconectar.agregar_ruta(router_destino.nombre, router_destino)
                    router_desconectar.realizar_salto()

    def simular_conexion(self):
        router_seleccionado_nombre = self.router_seleccionado.get()

        try:
            router_conectar = next(router for router in self.routers if router.nombre == router_seleccionado_nombre)
        except StopIteration:
            messagebox.showwarning("Router no encontrado",
                                   f"No se encontró un router con el nombre {router_seleccionado_nombre}.")
            return

        if router_conectar.enlace_conectado:
            messagebox.showinfo("Enlace ya conectado",
                                f"El router {router_conectar.nombre} ya está conectado.")
            return

        router_conectar.enlace_conectado = True
        self.actualizar_icono_router()
        self.actualizar_titulo_ventana(router_conectar.nombre, True)
        messagebox.showinfo("Conexión Exitosa", f"Se ha simulado la conexión del router {router_conectar.nombre}.")

    def actualizar_titulo_ventana(self, router_nombre, enlace_conectado):
        estado_enlace = "Conectado" if enlace_conectado else "Desconectado"
        color_texto = "green" if enlace_conectado else "red"
        self.estado_label.config(text=f"Estado del Enlace ({router_nombre}): {estado_enlace}", fg=color_texto)


if __name__ == "__main__":
    root = tk.Tk()
    app = RouterSimulation(root)
    root.mainloop()
