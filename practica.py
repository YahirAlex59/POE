from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

usuarios = {
    "admin": {"password": "123", "rol": "Administrador"},
    "vendedor": {"password": "123", "rol": "Vendedor"},
}
clientes = [
    {"id": "C1", "nombre": "Público en General", "telefono": "-"},
    {"id": "C2", "nombre": "Yahir Alexander Orta", "telefono": "7721795916"},
    {"id": "C3", "nombre": "Melanie Bautista", "telefono": "7731569874"},
    {"id": "C4", "nombre": "Drake Jose Reyes", "telefono": "774569789"},
    {"id": "C5", "nombre": "Ruth Valeria soto", "telefono": "7731235697"},
]
articulos = [
    {"id": "P1", "nombre": "Laptop", "precio": 15250.0, "cantidad": 16},
    {"id": "P2", "nombre": "Lego", "precio": 1100.0, "cantidad": 15},
    {"id": "P3", "nombre": "Converse", "precio": 950.0, "cantidad": 16},
    {"id": "P4", "nombre": "Carro rc", "precio": 520.0, "cantidad": 16},
    {"id": "P5", "nombre": "Refrigerador", "precio": 8500.0, "cantidad": 15},
    {"id": "P6", "nombre": "Estufa", "precio": 6950.0, "cantidad": 16},
]
ventas = []
# Inicio
def login():
    sesion = []
    ventana = Tk()
    ventana.title("Inicio de sesion")
    ventana.geometry("420x320")
    ventana.resizable(False, False)
    ventana.iconbitmap("img.ico")

    ventana.update_idletasks()
    ancho = 420
    alto = 320
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    mi_frame = Frame(
        ventana,
        width=380,
        height=280,
        bg="#cceee0",
        bd=4,
        relief="groove"
    )
    mi_frame.pack(padx=18, pady=18, fill="both", expand=True)

    mi_frame.grid_columnconfigure(0, weight=1)
    mi_frame.grid_columnconfigure(1, weight=1)

    Label(
        mi_frame,
        text="Iniciar Sesión",
        bg="#f2f2f2",
        fg="#1a1a1a",
        font=("Arial", 13, "bold"),
        bd=2,
        relief="ridge",
        padx=15,
        pady=6
    ).grid(
        row=0, column=0, columnspan=2,
        padx=20, pady=15
    )

    var_usuario = StringVar()
    var_password = StringVar()

    Label(
        mi_frame,
        text="Usuario:",
        bg="#cceee0",
        font=("Arial", 10, "bold")
    ).grid(
        row=1, column=0,
        sticky="e", padx=10, pady=10
    )

    cuadro_usuario = Entry(
        mi_frame,
        textvariable=var_usuario,
        width=24,
        justify="center"
    )
    cuadro_usuario.grid(
        row=1, column=1,
        padx=10, pady=10
    )

    Label(
        mi_frame,
        text="Contraseña:",
        bg="#cceee0",
        font=("Arial", 10, "bold")
    ).grid(
        row=2, column=0,
        sticky="e", padx=10, pady=10
    )

    cuadro_pass = Entry(
        mi_frame,
        textvariable=var_password,
        width=24,
        justify="center",
        show="*"
    )
    cuadro_pass.grid(
        row=2, column=1,
        padx=10, pady=10
    )

    def entrar():
        usuario = var_usuario.get().strip()
        pwd = var_password.get()
        datos = usuarios.get(usuario)

        if datos and datos["password"] == pwd:
            sesion.extend([usuario, datos["rol"]])
            messagebox.showinfo(
                "Bienvenido admin",
                f"Acceso concedido.\n"
                f"Usuario: {usuario}\n"
                f"Rol asignado: {datos['rol']}",
                parent=ventana
            )
            ventana.destroy()
        else:
            messagebox.showerror(
                "Error de Acceso no concedido",
                "Usuario o contraseña incorrectos.",
                parent=ventana
            )
            cuadro_pass.delete(0, END)
            cuadro_pass.focus_set()
    Button(
        mi_frame,
        text="Iniciar sesión",
        bg="#d9d9d9",
        fg="#000000",
        font=("Arial", 10, "bold"),
        width=18,
        cursor="hand2",
        command=entrar
    ).grid(
        row=3, column=0,
        columnspan=2, pady=12
    )
    ventana.mainloop()
    return sesion

# ____________________________________________________________
#tienda
def tienda(usuario, rol):
    ventana = Tk()
    ventana.title(f"Tienda - {usuario} ({rol})")
    Button(ventana, text="Cerrar sesión", cursor="hand2", command=ventana.destroy).pack(anchor="e", padx=10, pady=5)
    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    tab_ventas = Frame(pestanas)
    carrito = []

    izq = Frame(tab_ventas)
    izq.pack(side="left", anchor="n", padx=10, pady=10)
    Label(izq, text="Cliente:").grid(row=0, column=0, sticky="e", pady=5)
    cb_cliente = ttk.Combobox(izq, state="readonly", width=32)
    cb_cliente.grid(row=0, column=1, columnspan=2)
    Label(izq, text="Producto:").grid(row=1, column=0, sticky="e", pady=5)
    cb_producto = ttk.Combobox(izq, state="readonly", width=32)
    cb_producto.grid(row=1, column=1, columnspan=2)
    Label(izq, text="Cantidad:").grid(row=2, column=0, sticky="e", pady=5)
    e_cantidad = Entry(izq, width=8)
    e_cantidad.insert(0, "1")
    e_cantidad.grid(row=2, column=1, sticky="w")
    der = Frame(tab_ventas)
    der.pack(side="right", padx=10, pady=10)
    ticket = Text(der, width=44, height=24, font=("Courier", 9))
    ticket.pack(side="left")
    scroll = Scrollbar(der, command=ticket.yview)
    scroll.pack(side="right", fill="y")
    ticket.config(yscrollcommand=scroll.set)

    def mostrar_ticket(encabezado="VENTA EN CURSO\n" + "=" * 42):
        total = sum(p["importe"] for p in carrito)  # el precio ya incluye IVA
        subtotal = total / 1.16
        iva = total - subtotal
        lineas = [encabezado, f"{'Producto':<16}{'Cant':>5}{'P.Unit':>10}{'Importe':>11}", "-" * 42]

        if carrito:
            for p in carrito:
                lineas.append(
                    f"{p['nombre'][:15]:<16}{p['cantidad']:>5}"
                    f"{p['precio']:>10.2f}{p['importe']:>11.2f}"
                )
        else:
            lineas.append("Esperando productos...")

        lineas += [
            "-" * 42,
            f"{'Subtotal:':>31}{subtotal:>11.2f}",
            f"{'IVA (16%):':>31}{iva:>11.2f}",
            f"{'TOTAL:':>31}{total:>11.2f}"
        ]
        ticket.delete("1.0", END)
        ticket.insert(END, "\n".join(lineas))
        return subtotal, iva

    def agregar():
        i = cb_producto.current()
        if i < 0:
            return
        art = articulos[i]
        try:
            cant = int(e_cantidad.get())
        except ValueError:
            cant = 0
        en_carrito = sum(p["cantidad"] for p in carrito if p["art"] is art)
        if cant <= 0 or cant + en_carrito > art["cantidad"]:
            messagebox.showwarning("Aviso", f"Cantidad no válida (disponibles: {art['cantidad'] - en_carrito})")
            return
        carrito.append({
            "art": art, "nombre": art["nombre"], "cantidad": cant,
            "precio": art["precio"], "importe": cant * art["precio"]
        })
        mostrar_ticket()

    def cancelar():
        carrito.clear()
        mostrar_ticket()

    def generar_venta():
        if not carrito or not cb_cliente.get():
            messagebox.showwarning(
                "Error",
                "Seleccione un cliente o agregue productos",
                parent=ventana
            )
            return

        cliente_venta = cb_cliente.get()
        folio = len(ventas) + 1
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        subtotal, iva = mostrar_ticket()
        total = subtotal + iva

        detalle_venta = [p.copy() for p in carrito]

        for p in carrito:
            p["art"]["cantidad"] -= p["cantidad"]

        ventas.append({
            "folio": folio,
            "fecha": fecha,
            "cliente": cliente_venta,
            "vendedor": usuario,
            "detalle": detalle_venta,
            "subtotal": subtotal,
            "iva": iva,
            "total": total
        })

        carrito.clear()
        refrescar()

        e_cantidad.delete(0, END)
        e_cantidad.insert(0, "1")
        cb_producto.set("")
        if clientes:
            cb_cliente.current(0)
        else:
            cb_cliente.set("")
        mostrar_ticket()

        # Confirmar la venta
        messagebox.showinfo(
            "Confirmacion de venta",
            f"VENTA REGISTRADA CORRECTAMENTE\n\n",
            parent=ventana
        )

    Button(izq, text="Agregar", command=agregar).grid(row=2, column=2, sticky="ew")
    Button(izq, text="Cancelar venta", command=cancelar).grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)
    Button(izq, text="Generar venta y ticket", bg="#0066cc", fg="white",
           command=generar_venta).grid(row=4, column=1, columnspan=2, sticky="ew")

    #Clientes
    tab_clientes = Frame(pestanas)
    tabla_cli = ttk.Treeview(tab_clientes, columns=("id", "nombre", "telefono"), show="headings", height=12)
    for col in ("id", "nombre", "telefono"):
        tabla_cli.heading(col, text=col.upper())
        tabla_cli.column(col, width=180)
    tabla_cli.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
    entradas_cli = []
    for i, campo in enumerate(("ID", "Nombre", "Teléfono")):
        Label(tab_clientes, text=campo + ":").grid(row=1, column=i * 2, sticky="e")
        e = Entry(tab_clientes, width=15)
        e.grid(row=1, column=i * 2 + 1, padx=5)
        entradas_cli.append(e)

    def agregar_cliente():
        id_c, nombre, tel = [e.get().strip() for e in entradas_cli]
        if not id_c or not nombre:
            messagebox.showwarning("Aviso", "ID y Nombre son obligatorios")
            return
        clientes.append({"id": id_c, "nombre": nombre, "telefono": tel})
        for e in entradas_cli:
            e.delete(0, END)
        refrescar()

    Button(tab_clientes, text="Agregar cliente", command=agregar_cliente).grid(row=2, column=0, columnspan=6, pady=10)

    #Productos
    tab_art = Frame(pestanas)
    tabla_art = ttk.Treeview(tab_art, columns=("id", "nombre", "precio", "cantidad"), show="headings", height=12)
    for col in ("id", "nombre", "precio", "cantidad"):
        tabla_art.heading(col, text=col.upper())
        tabla_art.column(col, width=150)
    tabla_art.grid(row=0, column=0, columnspan=8, padx=10, pady=10)
    entradas_art = []
    for i, campo in enumerate(("ID", "Nombre", "Precio", "Cantidad")):
        Label(tab_art, text=campo + ":").grid(row=1, column=i * 2, sticky="e")
        e = Entry(tab_art, width=12)
        e.grid(row=1, column=i * 2 + 1, padx=5)
        entradas_art.append(e)

    def seleccionar_art(event):
        sel = tabla_art.selection()
        if sel:
            for e, val in zip(entradas_art, tabla_art.item(sel[0], "values")):
                e.delete(0, END)
                e.insert(0, val)

    tabla_art.bind("<<TreeviewSelect>>", seleccionar_art)

    def guardar_articulo():
        id_a, nombre, precio, cant = [e.get().strip() for e in entradas_art]
        if not id_a or not nombre:
            messagebox.showwarning("Aviso", "ID y Nombre son obligatorios")
            return
        try:
            datos = {"id": id_a, "nombre": nombre, "precio": float(precio), "cantidad": int(cant)}
        except ValueError:
            messagebox.showerror("Error", "Precio y Cantidad deben ser numéricos")
            return
        existente = next((a for a in articulos if a["id"] == id_a), None)
        if existente:
            existente.update(datos)
        else:
            articulos.append(datos)
        for e in entradas_art:
            e.delete(0, END)
        refrescar()

    def eliminar_articulo():
        sel = tabla_art.selection()
        if sel:
            id_sel = tabla_art.item(sel[0], "values")[0]
            articulos[:] = [a for a in articulos if a["id"] != id_sel]
            refrescar()

    Button(tab_art, text="Agregar / Editar", command=guardar_articulo).grid(row=2, column=0, columnspan=4, pady=10)
    Button(tab_art, text="Eliminar seleccionado", command=eliminar_articulo).grid(row=2, column=4, columnspan=4, pady=10)

    #Historial
    tab_historial = Frame(pestanas)
    lista_ventas = Listbox(tab_historial, width=90, height=18, font=("Courier", 9))
    lista_ventas.pack(fill="both", expand=True, padx=10, pady=10)

    def refrescar():
        cb_cliente["values"] = [f"{c['id']} - {c['nombre']}" for c in clientes]
        cb_producto["values"] = [f"{a['id']} - {a['nombre']} (${a['precio']:.2f})" for a in articulos]
        tabla_cli.delete(*tabla_cli.get_children())
        for c in clientes:
            tabla_cli.insert("", END, values=(c["id"], c["nombre"], c["telefono"]))
        tabla_art.delete(*tabla_art.get_children())
        for a in articulos:
            tabla_art.insert("", END, values=(a["id"], a["nombre"], f"{a['precio']:.2f}", a["cantidad"]))
        lista_ventas.delete(0, END)
        for v in ventas:
            lista_ventas.insert(END, f"#{v['folio']:04d}  {v['fecha']}  {v['cliente']:<25} "
                                     f"Vendedor: {v['vendedor']:<9} Total: ${v['total']:,.2f}")

    # Roles
    pestanas.add(tab_ventas, text="Ventas")
    pestanas.add(tab_clientes, text="Clientes")
    if rol == "Administrador":
        pestanas.add(tab_art, text="Artículos")
        pestanas.add(tab_historial, text="Historial de ventas")
    refrescar()
    cb_cliente.current(0)
    mostrar_ticket()
    ventana.mainloop()
if __name__ == "__main__":
    while True:
        sesion = login()
        if not sesion:
            break
        tienda(*sesion)