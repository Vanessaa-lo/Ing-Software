import flet as ft
from datetime import datetime
import os
import subprocess
import uuid
from copy import deepcopy
from functools import partial
from db_config import conectar_bd
import mysql.connector 

usuario_actual = "Roberto Empleado"

# Lista de platillos con detalles
platillos = [
    {
        "nombre": "Pizza Hawaiana",
        "imagen": "image/1.jpeg",
        "precio": 120,
        "ingredientes": ["Piña", "Jamón", "Queso"],
        "descripcion": "Deliciosa pizza con salsa de tomate, queso derretido, jamón y piña sobre una base crujiente."
    },
    {
        "nombre": "Hamburguesa BBQ",
        "imagen": "image/2.jpeg",
        "precio": 150,
        "ingredientes": ["Doble Carne", "Con Queso", "Extra Salsa BBQ", "Con Tocino", "Sin Lechuga y Jitomate", "Con Papas"],
        "descripcion": "Jugosa hamburguesa doble con queso, tocino y un toque especial de salsa BBQ."
    },
    {
        "nombre": "Tacos al Pastor",
        "imagen": "image/3.jpeg",
        "precio": 100,
        "ingredientes": ["Pastor", "Cilantro", "Cebolla"],
        "descripcion": "Tradicionales tacos de pastor servidos con cebolla, cilantro y salsa al gusto."
    }
]

def main(page: ft.Page):
    page.title = "Módulo Meseros"
    page.bgcolor = "#1C1C1C"
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 20

    comanda_data = {
        "id": str(uuid.uuid4()),
        "numero_comanda": 1,
        "fecha_hora": "",
        "nombre_mesero": "Roberto",
        "numero_mesa": "",
        "numero_comensales": "",
        "platillos": [],
        "estado": "En preparación"
    }

    vista_prev_platillo = ft.Container()
    platillos_agregados = ft.Column()
    comandas_realizadas = []
    comandas_realizadas_drawer = ft.Column()

    def mostrar_detalle_platillo(e):
        seleccionado = platillo_input.value
        for p in platillos:
            if p["nombre"] == seleccionado:
                vista_prev_platillo.content = ft.Column([
                    ft.Text(p["nombre"], size=16, weight="bold", color="#E71790"),
                    ft.Text(p["descripcion"], color="#F2E8EC"),
                    ft.Text(f"Ingredientes: {', '.join(p['ingredientes'])}", size=12, color="#F2E8EC"),
                    ft.Text(f"Precio: ${p['precio']}", weight="bold", color="#E71790")
                ], spacing=5)
                page.update()
                break

    def crear_boton_borrar(cid):
        return ft.ElevatedButton(
            "🗑 Borrar",
            on_click=partial(borrar_comanda, comanda_id=cid),
            bgcolor="#E53935",
            color="white"
        )

    def crear_boton_modificar(cid):
        return ft.ElevatedButton(
            "✏️ Modificar",
            on_click=partial(modificar_comanda, comanda_id=cid),
            bgcolor="#43A047",
            color="white"
        )

    def crear_estado_dropdown(comanda_id, estado_actual):
        estado_color = {
            "En preparación": "#FFC107",
            "Listo": "#4CAF50",
            "Entregado": "#2196F3"
        }.get(estado_actual, "#B0BEC5")

        return ft.Dropdown(
            value=estado_actual,
            options=[
                ft.dropdown.Option("En preparación"),
                ft.dropdown.Option("Listo"),
                ft.dropdown.Option("Entregado")
            ],
            on_change=lambda e: actualizar_estado(e, comanda_id),
            width=180,
            color=estado_color,
            border_radius=10
        )

    def actualizar_vista_platillos():
        platillos_agregados.controls.clear()
        for platillo in comanda_data["platillos"]:
            platillos_agregados.controls.append(
                ft.Row([
                    ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, pid=platillo["id"]: eliminar_platillo(e, pid), icon_color="#FF0000"),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, pid=platillo["id"]: editar_platillo(e, pid), icon_color="#4CAF50")
                ], alignment=ft.MainAxisAlignment.START)
            )
        page.update()

    def agregar_platillo(e):
        btn_agregar_platillo.disabled = True
        page.update()

        if not cantidad_input.value.isdigit() or int(cantidad_input.value) <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("❗ La cantidad debe ser un número válido.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            btn_agregar_platillo.disabled = False
            page.update()
            return

        platillo = platillo_input.value
        cantidad = cantidad_input.value
        observaciones = observaciones_input.value

        if platillo and cantidad:
            comanda_data["platillos"].append({
                "id": str(uuid.uuid4()),
                "platillo": platillo,
                "cantidad": cantidad,
                "observaciones": observaciones
            })
            actualizar_vista_platillos()
            platillo_input.value = ""
            cantidad_input.value = ""
            observaciones_input.value = ""
            vista_prev_platillo.content = None

        btn_agregar_platillo.disabled = False
        page.update()

    def eliminar_platillo(e, platillo_id):
        comanda_data["platillos"] = [p for p in comanda_data["platillos"] if p["id"] != platillo_id]
        actualizar_vista_platillos()

    def editar_platillo(e, platillo_id):
        for i, platillo in enumerate(comanda_data["platillos"]):
            if platillo["id"] == platillo_id:
                platillo_input.value = platillo['platillo']
                cantidad_input.value = platillo['cantidad']
                observaciones_input.value = platillo['observaciones']
                del comanda_data["platillos"][i]
                break
        actualizar_vista_platillos()

    def generar_comanda(e):
        if not comanda_data["platillos"]:
            return

        btn_generar_comanda.disabled = True
        page.update()

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Insertar en comandas
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO comandas (fecha_hora, mesero, numero_mesa, numero_comensales, estado) VALUES (%s, %s, %s, %s, %s)",
                (fecha_hora, comanda_data["nombre_mesero"], comanda_data["numero_mesa"], comanda_data["numero_comensales"], comanda_data["estado"])
            )
            comanda_id = cursor.lastrowid

            # Insertar platillos en platillos_comanda
            for p in comanda_data["platillos"]:
                cursor.execute(
                    "INSERT INTO platillos_comanda (comanda_id, nombre, cantidad, observaciones) VALUES (%s, %s, %s, %s)",
                    (comanda_id, p["platillo"], int(p["cantidad"]), p["observaciones"])
                )

            # Insertar en generarpedido
            cursor.execute("SELECT IdEstatusPedido FROM estatuspedido WHERE SituacionPedido = %s", (estatus,))
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception("❌ No se encontró el estatus 'En preparación' en la tabla estatuspedido.")
            id_estatus = resultado[0]

            # Insertar cada platillo como un pedido individual
            pedido_ids = []
            for platillo in comanda_data["platillos"]:
                descripcion = f"{platillo['platillo']} (Obs: {platillo['observaciones']})"
                cursor.execute(
                    "INSERT INTO generarpedido (HoraPedido, FechaPedido, Producto, NumeroMesa, Estatus, EstatusPedido_IdEstatusPedido, Clientes_Idcliente) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (hora, fecha, descripcion, comanda_data["numero_mesa"], estatus, id_estatus, 1)
                )
                pedido_ids.append(cursor.lastrowid)  # Guarda todos los IDs de pedido generados

            # Insertar en comandapedido
            cursor.execute(
                "INSERT INTO comandapedido (GenerarPedido_IdGenerarPedido, GenerarComanda) VALUES (%s, %s)",
                (pedido_id, str(comanda_id))  # Convertimos a string si es int
            )


            # 1. Datos de fecha, hora y total
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora = datetime.now().strftime("%H:%M:%S")
            total = sum(
                int(p["cantidad"]) * (120 if p["platillo"] == "Pizza Hawaiana" else 150 if p["platillo"] == "Hamburguesa BBQ" else 100)
                for p in comanda_data["platillos"]
            )
            detalle = f"Total: ${total}"

            # 2. Insertar en la tabla ventas
            cursor.execute(
                "INSERT INTO ventas (Hora, FechaVenta, DetalleVenta, CorteCaja_idCorteCaja) VALUES (%s, %s, %s, %s)",
                (hora, fecha, detalle, 1)  # ← Asumimos corte de caja ID 1
            )
            venta_id = cursor.lastrowid

            # 3. Insertar en la tabla generarrecibo
            cursor.execute(
                "INSERT INTO generarrecibo (FechaRecibo, HoraRecibo, descripcion, Ventas_IdVentas) VALUES (%s, %s, %s, %s)",
                (fecha, hora, detalle, venta_id)
            )



            conexion.commit()
            conexion.close()

        except Exception as ex:
            print("❌ Error al guardar en base de datos:", ex)

        comanda_data["fecha_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        comanda_data_copy = deepcopy(comanda_data)
        comanda_data_copy["id"] = str(uuid.uuid4())
        comandas_realizadas.append(comanda_data_copy)

        comanda_data["numero_comanda"] += 1
        comanda_data["platillos"] = []
        comanda_data["estado"] = "En preparación"
        comanda_data["id"] = str(uuid.uuid4())

        platillos_agregados.controls.clear()
        vista_prev_platillo.content = None
        comanda_numero_text.value = f"Comanda # {comanda_data['numero_comanda']}"

        btn_generar_comanda.disabled = False
        page.update()

    def borrar_comanda(e, comanda_id):
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM generarrecibo WHERE Comanda_id = %s", (comanda_id,))
            cursor.execute("DELETE FROM comandapedido WHERE Comanda_id = %s", (comanda_id,))
            cursor.execute("DELETE FROM platillos_comanda WHERE comanda_id = %s", (comanda_id,))
            cursor.execute("DELETE FROM comandas WHERE id = %s", (comanda_id,))
            conexion.commit()
            conexion.close()
        except Exception as ex:
            print("❌ Error al eliminar de la base de datos:", ex)

        index = next((i for i, c in enumerate(comandas_realizadas) if c["id"] == comanda_id), None)
        if index is not None:
            del comandas_realizadas[index]
        mostrar_comandas_realizadas(e)
        page.update()
        
    def modificar_comanda(e, comanda_id):
        for i, comanda in enumerate(comandas_realizadas):
            if comanda["id"] == comanda_id:
                comanda_data.update(comanda)
                comanda_data["id"] = str(uuid.uuid4())
                numero_mesa_dropdown.value = str(comanda["numero_mesa"])
                numero_comensales_dropdown.value = str(comanda["numero_comensales"])
                comandas_realizadas.pop(i)
                actualizar_vista_platillos()
                break
        page.update()

    def mostrar_comandas_realizadas(e):
        comandas_realizadas_drawer.controls.clear()
        for comanda in comandas_realizadas:
            comanda_id = comanda["id"]
            estado_icono = {
                "En preparación": ft.icons.ACCESS_TIME,
                "Listo": ft.icons.CHECK_CIRCLE,
                "Entregado": ft.icons.LOCAL_SHIPPING
            }.get(comanda["estado"], ft.icons.INFO)
            estado_dropdown = crear_estado_dropdown(comanda_id, comanda["estado"])

            total = sum(
                int(p['cantidad']) * next((x['precio'] for x in platillos if x['nombre'] == p['platillo']), 0)
                for p in comanda["platillos"]
            )

            comandas_realizadas_drawer.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(name=estado_icono, color=estado_dropdown.color, size=24),
                                ft.Text(f"Comanda #{comanda['numero_comanda']}", weight="bold", size=18, color="#E71790"),
                                ft.Text(comanda["fecha_hora"], size=12, color="#B0BEC5")
                            ], alignment="spaceBetween"),
                            ft.Text(f"Mesa {comanda['numero_mesa']} | Comensales: {comanda['numero_comensales']}", size=14, color="#F2E8EC"),
                            ft.Divider(height=10, color="#E0E0E0"),
                            ft.Text("Platillos:", weight="bold", size=14, color="#E71790"),
                            ft.Text(f"Total: ${total}", size=14, weight="bold", color="#F2E8EC"),
                            ft.Column([
                                ft.Text(f"- {p['platillo']} (x{p['cantidad']}) — {p['observaciones']}", size=13, color="#F2E8EC") for p in comanda["platillos"]
                            ], spacing=2),
                            ft.Row([estado_dropdown], alignment="start"),
                            ft.Row([
                                crear_boton_borrar(comanda_id),
                                crear_boton_modificar(comanda_id)
                            ], alignment="end", spacing=10)
                        ], spacing=10),
                        padding=15,
                        border_radius=15,
                        bgcolor="#1E1E2F",
                        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.colors.BLACK26, offset=ft.Offset(2, 2))
                    ),
                    margin=10
                )
            )
        page.update()

    def actualizar_estado(e, comanda_id):
        nuevo_estado = e.control.value
        for comanda in comandas_realizadas:
            if comanda["id"] == comanda_id:
                comanda["estado"] = nuevo_estado
                break
        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Actualizar estado en comandas
            cursor.execute("UPDATE comandas SET estado = %s WHERE id = %s", (nuevo_estado, comanda_id))

            # Obtener el ID del pedido relacionado
            cursor.execute("SELECT GenerarPedido_IdGenerarPedido FROM comandapedido WHERE Comanda_id = %s", (comanda_id,))
            resultado = cursor.fetchone()
            if resultado:
                pedido_id = resultado[0]
                # Actualizar estado también en generarpedido
                cursor.execute("UPDATE generarpedido SET Estatus = %s WHERE IdGenerarPedido = %s", (nuevo_estado, pedido_id))

            conexion.commit()
            conexion.close()
        except Exception as ex:
            print("❌ Error al actualizar estado en BD:", ex)

        mostrar_comandas_realizadas(e)


    def toggle_sidebar(e):
        page.drawer.open = not page.drawer.open
        page.update()

    def abrir_archivo(nombre_archivo):
        ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
        subprocess.Popen(["python", ruta])

    def toggle_comandas_drawer(e):
        mostrar_comandas_realizadas(e)
        comandas_drawer.open = not comandas_drawer.open
        page.update()

    platillo_input = ft.Dropdown(
        label="Platillo/Bebida",
        options=[ft.dropdown.Option(p["nombre"]) for p in platillos],
        width=300,
        color="#F2E8EC",
        on_change=mostrar_detalle_platillo
    )

    cantidad_input = ft.TextField(label="Cantidad", width=300, color="#F2E8EC", keyboard_type=ft.KeyboardType.NUMBER)
    observaciones_input = ft.TextField(label="Observaciones", width=300, color="#F2E8EC")
    numero_mesa_dropdown = ft.Dropdown(label="Número de Mesa", options=[ft.dropdown.Option(str(i)) for i in range(1, 21)], width=300, color="#F2E8EC")
    numero_comensales_dropdown = ft.Dropdown(label="Número de Comensales", options=[ft.dropdown.Option(str(i)) for i in range(1, 11)], width=300, color="#F2E8EC")

    btn_agregar_platillo = ft.ElevatedButton("Agregar Platillo", on_click=agregar_platillo, bgcolor="#8E2453", color="#F2E8EC")
    btn_generar_comanda = ft.ElevatedButton("Generar Comanda", on_click=generar_comanda, bgcolor="#4CAF50", color="#F2E8EC")

    comanda_numero_text = ft.Text(f"Comanda # {comanda_data['numero_comanda']}", size=20, weight=ft.FontWeight.BOLD, color="#E71790")

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Column([
                ft.Container(
                    content=ft.Text(f"Usuario: {usuario_actual}", size=16, color="#E71790"),
                    padding=10
                ),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGIN),
                    title=ft.Text("Regresar al Login"),
                    on_click=lambda e: abrir_archivo("login.py")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LIST),
                    title=ft.Text("Menú"),
                    on_click=lambda e: abrir_archivo("menu.py")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME),
                    title=ft.Text("Home"),
                    on_click=lambda e: abrir_archivo("main.py")
                ),
            ], spacing=10)
        ]
    )

    comandas_drawer = ft.NavigationDrawer(
        controls=[
            ft.Text("Comandas Realizadas", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
            comandas_realizadas_drawer
        ],
        bgcolor="#5D0E41"
    )

    page.appbar = ft.AppBar(
        title=ft.Text(f"Mesero: {comanda_data['nombre_mesero']}", color="#F2E8EC"),
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        actions=[ft.IconButton(icon=ft.icons.LIST, on_click=toggle_comandas_drawer, icon_color="#E71790")]
    )

    page.end_drawer = comandas_drawer

    page.add(
        ft.Column([
            comanda_numero_text,
            numero_mesa_dropdown,
            numero_comensales_dropdown,
            ft.Divider(height=20),
            ft.Text("Platillos/Bebidas a Ordenar", size=18, color="#F2E8EC"),
            platillo_input,
            vista_prev_platillo,
            cantidad_input,
            observaciones_input,
            btn_agregar_platillo,
            ft.Divider(height=20),
            platillos_agregados,
            ft.Divider(height=20),
            btn_generar_comanda
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )

ft.app(target=main)
