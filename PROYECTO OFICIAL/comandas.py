import flet as ft
from datetime import datetime
import os
import subprocess
import uuid
import mysql.connector  # ← NUEVO
from db_config import conectar_bd

usuario_actual = "Roberto Empleado"



def main(page: ft.Page):
    page.title = "Módulo Meseros"
    page.bgcolor = "#1C1C1C"
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 20

    comanda_data = {
        "numero_comanda": 1,
        "fecha_hora": "",
        "nombre_mesero": "Roberto",
        "numero_mesa": "",
        "numero_comensales": "",
        "platillos": [],
        "estado": "En preparación"
    }

    comandas_realizadas = []

    platillo_input = ft.Dropdown(
        label="Platillo/Bebida",
        options=[
            ft.dropdown.Option("Pizza Hawaiana"),
            ft.dropdown.Option("Hamburguesa BBQ"),
            ft.dropdown.Option("Tacos al Pastor")
        ],
        width=300,
        color="#F2E8EC"
    )

    def agregar_platillo(e):
        platillo = platillo_input.value
        cantidad = cantidad_input.value
        observaciones = observaciones_input.value

        if not platillo:
            page.snack_bar = ft.SnackBar(ft.Text("❗ Debes seleccionar un platillo del menú.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            page.snack_bar = ft.SnackBar(ft.Text("❗ La cantidad debe ser un número positivo.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        comanda_data["platillos"].append({
            "id": str(uuid.uuid4()),
            "platillo": platillo,
            "cantidad": cantidad,
            "observaciones": observaciones
        })
        platillos_agregados.controls.append(
            ft.Row(
                [
                    ft.Text(f"{platillo} - Cantidad: {cantidad} - Observaciones: {observaciones}", color="#F2E8EC"),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=len(comanda_data["platillos"]) - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                    ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=len(comanda_data["platillos"]) - 1: editar_platillo(e, idx), icon_color="#4CAF50")
                ],
                alignment=ft.MainAxisAlignment.START
            )
        )
        platillo_input.value = ""
        cantidad_input.value = ""
        observaciones_input.value = ""
        page.update()

    def generar_comanda(e):
        if not validar_dropdown():
            page.snack_bar = ft.SnackBar(ft.Text("❗ Debes seleccionar el número de mesa y comensales.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if not comanda_data["platillos"]:
            page.snack_bar = ft.SnackBar(ft.Text("❗ No se puede generar una comanda sin platillos.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        comanda_data["fecha_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comanda_data["numero_mesa"] = int(numero_mesa_dropdown.value)
        comanda_data["numero_comensales"] = int(numero_comensales_dropdown.value)

        try:
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # 1. Insertar en generarpedido
            sql_generar_pedido = """
                INSERT INTO generarpedido 
                (HoraPedido, FechaPedido, Producto, NumeroMesa, Estatus, EstatusPedido_IdEstatusPedido, Clientes_Idcliente) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores_generar_pedido = (
                datetime.now().hour,
                datetime.now().date(),
                ', '.join([p['platillo'] for p in comanda_data['platillos']]),
                comanda_data['numero_mesa'],
                comanda_data['estado'],
                1,
                1
            )
            cursor.execute(sql_generar_pedido, valores_generar_pedido)
            pedido_id = cursor.lastrowid

            # 2. Insertar en comandas
            sql_comanda = """
                INSERT INTO comandas 
                (fecha_hora, mesero, numero_mesa, numero_comensales, estado) 
                VALUES (%s, %s, %s, %s, %s)
            """
            valores_comanda = (
                comanda_data["fecha_hora"],
                comanda_data["nombre_mesero"],
                comanda_data["numero_mesa"],
                comanda_data["numero_comensales"],
                comanda_data["estado"]
            )
            cursor.execute(sql_comanda, valores_comanda)
            comanda_id = cursor.lastrowid

            # 3. Insertar en comandapedido
            cursor.execute(
                "INSERT INTO comandapedido (GenerarComanda, GenerarPedido_IdGenerarPedido) VALUES (%s, %s)",
                (f"Comanda #{comanda_id}", pedido_id)
            )

            # 4. Insertar platillos_comanda
            for p in comanda_data["platillos"]:
                cursor.execute(
                    "INSERT INTO platillos_comanda (comanda_id, nombre, cantidad, observaciones) VALUES (%s, %s, %s, %s)",
                    (comanda_id, p["platillo"], p["cantidad"], p["observaciones"])
                )

            # 5. Insertar en ventas (CORREGIDO con CorteCaja_idCorteCaja)
            cursor.execute(
                "INSERT INTO ventas (FechaVenta, Hora, DetalleVenta, CorteCaja_idCorteCaja) VALUES (%s, %s, %s, %s)",
                (
                    datetime.now().strftime("%Y-%m-%d"),
                    datetime.now().strftime("%H:%M:%S"),
                    f"Venta generada para mesa {comanda_data['numero_mesa']}",  # contenido del detalle
                    1  # ID de corte de caja por defecto
                )
            )
            venta_id = cursor.lastrowid


            # 6. Insertar en detalleventas (cálculo simple)
            precio_unitario = 50.0
            subtotal = sum(int(p["cantidad"]) * precio_unitario for p in comanda_data["platillos"])
            impuesto = subtotal * 0.16
            total = subtotal + impuesto

            cursor.execute(
                "INSERT INTO detalleventas (Subtotal, Impuesto, Descuento, Total, Ventas_IdVentas) VALUES (%s, %s, %s, %s, %s)",
                (subtotal, impuesto, descuento, total, venta_id)
            )

            # 7. Insertar generarrecibo (relacionado con ventas)
            cursor.execute(
                "INSERT INTO generarrecibo (FechaRecibo, HoraRecibo, descripcion, Ventas_IdVentas) VALUES (%s, %s, %s, %s)",
                (
                    datetime.now().strftime("%Y-%m-%d"),
                    datetime.now().strftime("%H:%M:%S"),
                    f"Pedido de mesa {comanda_data['numero_mesa']}",
                    venta_id
                )
            )

            conexion.commit()
            conexion.close()

            page.snack_bar = ft.SnackBar(ft.Text("✅ Comanda y venta guardadas correctamente.", color="white"), bgcolor="green")
            page.snack_bar.open = True


        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error al guardar en la base de datos: {err}", color="white"), bgcolor="red")
            page.snack_bar.open = True

        comandas_realizadas.append(comanda_data.copy())
        comanda_data["numero_comanda"] += 1
        comanda_data["platillos"] = []
        comanda_data["estado"] = "En preparación"
        platillos_agregados.controls.clear()
        comanda_numero_text.value = f"Comanda # {comanda_data['numero_comanda']}"
        page.update()


    def mostrar_comandas_realizadas(e):
        comandas_realizadas_drawer.controls.clear()
        for idx, comanda in enumerate(comandas_realizadas):
            estado_color = {
                "En preparación": "#FFC107",
                "Listo": "#4CAF50",
                "Entregado": "#2196F3"
            }.get(comanda["estado"], "#B0BEC5")

            estado_icono = {
                "En preparación": ft.icons.ACCESS_TIME,
                "Listo": ft.icons.CHECK_CIRCLE,
                "Entregado": ft.icons.LOCAL_SHIPPING
            }.get(comanda["estado"], ft.icons.INFO)

            estado_dropdown = ft.Dropdown(
                value=comanda["estado"],
                options=[
                    ft.dropdown.Option("En preparación"),
                    ft.dropdown.Option("Listo"),
                    ft.dropdown.Option("Entregado")
                ],
                on_change=lambda e, idx=idx: actualizar_estado(e, idx),
                width=180,
                color=estado_color,
                border_radius=10
            )

            comandas_realizadas_drawer.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(name=estado_icono, color=estado_color, size=24),
                                        ft.Text(f"Comanda #{comanda['numero_comanda']}", weight="bold", size=18, color="#E71790"),
                                        ft.Text(comanda["fecha_hora"], size=12, color="#B0BEC5")
                                    ],
                                    alignment="spaceBetween"
                                ),
                                ft.Text(f"Mesa {comanda['numero_mesa']} | Comensales: {comanda['numero_comensales']}", size=14, color="#F2E8EC"),
                                ft.Divider(height=10, color="#E0E0E0"),
                                ft.Text("Platillos:", weight="bold", size=14, color="#E71790"),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            f"- {p['platillo']} (x{p['cantidad']}) — {p['observaciones']}",
                                            size=13,
                                            color="#F2E8EC"
                                        )
                                        for p in comanda["platillos"]
                                    ],
                                    spacing=2
                                ),
                                ft.Row(
                                    [estado_dropdown],
                                    alignment="start"
                                ),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "🗑 Borrar",
                                            on_click=lambda e, idx=idx: borrar_comanda(e, idx),
                                            bgcolor="#E53935",
                                            color="white",
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                        ),
                                        ft.ElevatedButton(
                                            "✏️ Modificar",
                                            on_click=lambda e, idx=idx: modificar_comanda(e, idx),
                                            bgcolor="#43A047",
                                            color="white",
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                        )
                                    ],
                                    alignment="end",
                                    spacing=10
                                )
                            ],
                            spacing=10
                        ),
                        padding=15,
                        border_radius=15,
                        bgcolor="#1E1E2F",
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.BLACK26,
                            offset=ft.Offset(2, 2)
                        )
                    ),
                    margin=10
                )
            )
        page.update()

    def actualizar_estado(e, idx):
        comandas_realizadas[idx]["estado"] = e.control.value
        mostrar_comandas_realizadas(e)
        page.update()

    def borrar_comanda(e, idx):
        def confirmar_borrado(e):
            del comandas_realizadas[idx]
            mostrar_comandas_realizadas(e)
            page.snack_bar = ft.SnackBar(ft.Text("✅ Comanda eliminada.", color="white"), bgcolor="green")
            page.snack_bar.open = True
            page.update()

        page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Text("⚠️ ¿Deseas eliminar esta comanda?", color="white"),
                ft.TextButton("Sí", on_click=confirmar_borrado),
                ft.TextButton("No", on_click=lambda e: page.snack_bar.close())
            ]),
            bgcolor="red"
        )
        page.snack_bar.open = True
        page.update()

    def modificar_comanda(e, idx):
        comanda = comandas_realizadas[idx]
        comanda_data.update(comanda)
        # comanda_data["numero_comanda"] = comanda["numero_comanda"]  # <- Comentado para no reiniciar el contador

        numero_mesa_dropdown.value = str(comanda["numero_mesa"])
        numero_comensales_dropdown.value = str(comanda["numero_comensales"])

        platillos_agregados.controls.clear()
        for platillo in comanda["platillos"]:
            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=platillo["id"]: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=platillo["id"]: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )
        comandas_realizadas.pop(idx)
        page.update()

    def eliminar_platillo(e, idx):
        del comanda_data["platillos"][idx]
        platillos_agregados.controls.clear()
        for platillo in comanda_data["platillos"]:
            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=platillo["id"]: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=platillo["id"]: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )
        page.update()

    def editar_platillo(e, idx):
        platillo = comanda_data["platillos"][idx]
        platillo_input.value = platillo['platillo']
        cantidad_input.value = platillo['cantidad']
        observaciones_input.value = platillo['observaciones']

        del comanda_data["platillos"][idx]
        platillos_agregados.controls.clear()
        for platillo in comanda_data["platillos"]:
            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=platillo["id"]: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=platillo["id"]: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )
        page.update()

    def validar_dropdown():
        if not numero_mesa_dropdown.value or not numero_comensales_dropdown.value:
            return False
        return True

    numero_mesa_dropdown = ft.Dropdown(label="Número de Mesa", options=[ft.dropdown.Option(str(i)) for i in range(1, 21)], width=300, color="#F2E8EC")
    numero_comensales_dropdown = ft.Dropdown(label="Número de Comensales", options=[ft.dropdown.Option(str(i)) for i in range(1, 11)], width=300, color="#F2E8EC")

    cantidad_input = ft.TextField(label="Cantidad", width=300, color="#F2E8EC", keyboard_type=ft.KeyboardType.NUMBER)
    observaciones_input = ft.TextField(label="Observaciones", width=300, color="#F2E8EC")
    platillos_agregados = ft.Column()
    comandas_realizadas_drawer = ft.Column()

    def toggle_sidebar(e):
        page.drawer.open = not page.drawer.open
        page.update()

    def abrir_archivo(nombre_archivo):
        ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
        subprocess.Popen(["python", ruta])

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Column([
                ft.Container(content=ft.Text(f"Usuario: {usuario_actual}", size=16, color="#E71790"), padding=10),
                ft.Divider(),
                ft.ListTile(leading=ft.Icon(ft.Icons.LOGIN), title=ft.Text("Regresar al Login"), on_click=lambda e: abrir_archivo("login.py")),
                ft.ListTile(leading=ft.Icon(ft.Icons.MENU_BOOK), title=ft.Text("Menú Interactivo"), on_click=lambda e: abrir_archivo("menu.py")),
                ft.ListTile(leading=ft.Icon(ft.Icons.HOME), title=ft.Text("Home"), on_click=lambda e: abrir_archivo("main.py"))
            ], spacing=10)
        ]
    )

    comandas_drawer = ft.NavigationDrawer(
        controls=[ft.Text("Comandas Realizadas", size=20, weight=ft.FontWeight.BOLD, color="#E71790"), comandas_realizadas_drawer],
        bgcolor="#5D0E41"
    )

    def toggle_comandas_drawer(e):
        mostrar_comandas_realizadas(e)
        comandas_drawer.open = not comandas_drawer.open
        page.update()

    appbar = ft.AppBar(
        title=ft.Text(f"Mesero: {comanda_data['nombre_mesero']}", color="#F2E8EC"),
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        actions=[ft.IconButton(icon=ft.icons.LIST, on_click=toggle_comandas_drawer, icon_color="#E71790")]
    )

    page.appbar = appbar
    page.end_drawer = comandas_drawer

    comanda_numero_text = ft.Text(f"Comanda # {comanda_data['numero_comanda']}", size=20, weight=ft.FontWeight.BOLD, color="#E71790")

    page.add(
        comanda_numero_text,
        numero_mesa_dropdown,
        numero_comensales_dropdown,
        ft.Divider(height=20),
        ft.Text("Platillos/Bebidas a Ordenar", size=18, color="#F2E8EC"),
        platillo_input,
        cantidad_input,
        observaciones_input,
        ft.ElevatedButton("Agregar Platillo", on_click=agregar_platillo, bgcolor="#8E2453", color="#F2E8EC"),
        ft.Divider(height=20),
        platillos_agregados,
        ft.Divider(height=20),
        ft.ElevatedButton("Generar Comanda", on_click=generar_comanda, bgcolor="#4CAF50", color="#F2E8EC")
    )

ft.app(target=main)
