import flet as ft
from datetime import datetime
import os
import subprocess
from db_config import conectar_bd

def main(page: ft.Page):
    page.title = "Módulo Meseros"
    page.bgcolor = "#1C1C1C"  # Fondo oscuro para contraste
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 20

    # Variables para almacenar los datos de la comanda
    comanda_data = {
        "numero_comanda": 1,
        "fecha_hora": "",
        "nombre_mesero": "Pedro",
        "numero_mesa": "",
        "numero_comensales": "",
        "platillos": [],
        "estado": "En preparación"  # Estado inicial de la comanda
    }

    comandas_realizadas = []  # Lista para almacenar las comandas realizadas

    # Función para agregar platillos/bebidas a la comanda
    def agregar_platillo(e):
        platillo = platillo_input.value
        cantidad = cantidad_input.value
        observaciones = observaciones_input.value

        if platillo and cantidad:
            precio_unitario = obtener_precio(platillo)
            precio_total = precio_unitario * int(cantidad)

            comanda_data["platillos"].append({
                "id": len(comanda_data["platillos"]) + 1,
                "platillo": platillo,
                "cantidad": cantidad,
                "observaciones": observaciones,
                "precio": precio_total  # ✅ Ahora también guardamos el precio aquí
            })

            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo} - Cantidad: {cantidad} - Observaciones: {observaciones} - ${precio_total}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, idx=len(comanda_data["platillos"]) - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, idx=len(comanda_data["platillos"]) - 1: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )

            platillo_input.value = ""
            cantidad_input.value = ""
            observaciones_input.value = ""
            page.update()



    # Función para generar la comanda
    def generar_comanda(e):
        if not comanda_data["platillos"]:
            return

        comanda_data["fecha_hora"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_actual = comanda_data["fecha_hora"].split()[0]
        hora_actual = comanda_data["fecha_hora"].split()[1]

        comanda_data["numero_mesa"] = int(numero_mesa_dropdown.value)
        comanda_data["numero_comensales"] = int(numero_comensales_dropdown.value)

        descripcion = f"{comanda_data['numero_comensales']} comensales | " + ", ".join([
            f"{p['platillo']} ({p['cantidad']}){' - ' + p['observaciones'] if p['observaciones'] else ''}"
            for p in comanda_data["platillos"]
        ])
        estatus = "Pedido Realizado"
        id_cliente = 1  # puedes cambiar esto según el cliente actual

        try:
            conn = conectar_bd()
            cursor = conn.cursor()

            # Obtener o crear el estatus
            cursor.execute("SELECT IdEstatusPedido FROM estatuspedido WHERE SituacionPedido = %s", (estatus,))
            row = cursor.fetchone()
            if row:
                id_estatus = row[0]
            else:
                cursor.execute("INSERT INTO estatuspedido (SituacionPedido) VALUES (%s)", (estatus,))
                conn.commit()
                id_estatus = cursor.lastrowid

            total_comanda = sum(p["precio"] for p in comanda_data["platillos"])

            # Insertar en generarpedido
            cursor.execute("""
                INSERT INTO generarpedido (HoraPedido, FechaPedido, Producto, NumeroMesa, Total, Estatus, EstatusPedido_IdEstatusPedido, Clientes_Idcliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (hora_actual, fecha_actual, descripcion, comanda_data["numero_mesa"], total_comanda, estatus, id_estatus, id_cliente))


            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar UI
            comandas_realizadas.append(comanda_data.copy())
            comanda_data["numero_comanda"] += 1
            comanda_data["platillos"] = []
            comanda_data["estado"] = "En preparación"
            platillos_agregados.controls.clear()
            comanda_numero_text.value = f"Comanda # {comanda_data['numero_comanda']}"
            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Comanda registrada en base de datos"))
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"❌ Error al guardar: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    # Función para mostrar las comandas realizadas en el drawer
    def mostrar_comandas_realizadas(e):
        comandas_realizadas_drawer.controls.clear()
        for idx, comanda in enumerate(comandas_realizadas):
            # Definir el color y el ícono según el estado
            estado_color = {
                "En preparación": "#FFC107",  # Amarillo
                "Listo": "#4CAF50",  # Verde
                "Entregado": "#2196F3"  # Azul
            }.get(comanda["estado"], "#F2E8EC")  # Color por defecto

            estado_icono = {
                "En preparación": ft.Icons.ACCESS_TIME,
                "Listo": ft.Icons.CHECK_CIRCLE,
                "Entregado": ft.Icons.LOCAL_SHIPPING
            }.get(comanda["estado"], ft.Icons.INFO)  # Ícono por defecto

            estado_dropdown = ft.Dropdown(
                value=comanda["estado"],
                options=[
                    ft.dropdown.Option("En preparación"),
                    ft.dropdown.Option("Listo"),
                    ft.dropdown.Option("Entregado")
                ],
                on_change=lambda e, idx=idx: actualizar_estado(e, idx),
                width=120,
                color=estado_color
            )
            comandas_realizadas_drawer.controls.append(
                ft.Column(
                    [
                        ft.Text(f"Comanda #{comanda['numero_comanda']}", weight=ft.FontWeight.BOLD, color="#E71790"),
                        ft.Text(f"Fecha y Hora: {comanda['fecha_hora']}", color="#F2E8EC"),
                        ft.Text(f"Mesa: {comanda['numero_mesa']} - Comensales: {comanda['numero_comensales']}", color="#F2E8EC"),
                        ft.Text("Platillos/Bebidas:", weight=ft.FontWeight.BOLD, color="#E71790"),
                        *[ft.Text(f"- {platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC") for platillo in comanda['platillos']],
                        ft.Row(
                            [
                                ft.Icon(name=estado_icono, color=estado_color),
                                estado_dropdown
                            ],
                            spacing=10
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton("Borrar", on_click=lambda e, idx=idx: borrar_comanda(e, idx), bgcolor="#FF0000", color="#F2E8EC"),
                                ft.ElevatedButton("Modificar", on_click=lambda e, idx=idx: modificar_comanda(e, idx), bgcolor="#4CAF50", color="#F2E8EC")
                            ],
                            spacing=10
                        )
                    ],
                    spacing=5
                )
            )
        page.update()

    # Función para actualizar el estado de una comanda
    def actualizar_estado(e, idx):
        comandas_realizadas[idx]["estado"] = e.control.value
        mostrar_comandas_realizadas(e)  # Actualizar la lista para reflejar el cambio
        page.update()

    # Función para borrar una comanda
    def borrar_comanda(e, idx):
        # Eliminar la comanda de la lista
        del comandas_realizadas[idx]
        # Actualizar la vista para reflejar el cambio
        mostrar_comandas_realizadas(e)
        # Actualizar el número de comanda en la interfaz
        page.update()

    # Función para modificar una comanda
    def modificar_comanda(e, idx):
        comanda = comandas_realizadas[idx]
        comanda_data.update(comanda)  # Cargar los datos de la comanda seleccionada
        comanda_data["numero_comanda"] = comanda["numero_comanda"]  # Mantener el número de comanda

        # Actualizar los controles con los datos de la comanda
        numero_mesa_dropdown.value = str(comanda["numero_mesa"])  # Convertir de entero a string para el dropdown
        numero_comensales_dropdown.value = str(comanda["numero_comensales"])  # Convertir de entero a string

        platillos_agregados.controls.clear()
        for platillo in comanda["platillos"]:
            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, idx=platillo["id"] - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, idx=platillo["id"] - 1: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )

        # Eliminar la comanda de la lista de comandas realizadas
        comandas_realizadas.pop(idx)
        page.update()

    # Función para eliminar un platillo de la comanda
    def eliminar_platillo(e, idx):
        del comanda_data["platillos"][idx]
        platillos_agregados.controls.clear()
        for platillo in comanda_data["platillos"]:
            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, idx=platillo["id"] - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, idx=platillo["id"] - 1: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )
        page.update()

    # Función para editar un platillo
    def editar_platillo(e, idx):
        platillo = comanda_data["platillos"][idx]
        platillo_input.value = platillo['platillo']
        cantidad_input.value = platillo['cantidad']
        observaciones_input.value = platillo['observaciones']

        # Eliminar el platillo para reemplazarlo
        del comanda_data["platillos"][idx]
        platillos_agregados.controls.clear()
        for platillo in comanda_data["platillos"]:
            platillos_agregados.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC"),
                        ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, idx=platillo["id"] - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, idx=platillo["id"] - 1: editar_platillo(e, idx), icon_color="#4CAF50")
                    ],
                    alignment=ft.MainAxisAlignment.START
                )
            )
        page.update()

    # Validación para los Dropdown
    def validar_dropdown():
        if not numero_mesa_dropdown.value or not numero_comensales_dropdown.value:
            return False
        return True

    # Controles de la interfaz
    numero_mesa_dropdown = ft.Dropdown(
        label="Número de Mesa",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 21)],
        width=300,
        color="#F2E8EC"
    )

    numero_comensales_dropdown = ft.Dropdown(
        label="Número de Comensales",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 11)],
        width=300,
        color="#F2E8EC"
    )

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


    cantidad_input = ft.TextField(
        label="Cantidad",
        width=300,
        color="#F2E8EC",
        keyboard_type=ft.KeyboardType.NUMBER  # Muestra teclado numérico en móviles
    )

    observaciones_input = ft.TextField(label="Observaciones", width=300, color="#F2E8EC")

    platillos_agregados = ft.Column()

    # Drawer para comandas realizadas
    comandas_realizadas_drawer = ft.Column()

    # Sidebar

    def toggle_sidebar(e):
        page.drawer.open = not page.drawer.open
        page.update()

    # ✅ Función para abrir archivos externos
    def abrir_archivo(nombre_archivo):
        ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
        subprocess.Popen(["python", ruta])  # Ejecuta el archivo .py

    # ✅ SIDEBAR (Menú lateral)
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Column([
                ft.Container(
                ),
                ft.Divider(),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGIN),
                    title=ft.Text("Regresar al Login"),
                    on_click=lambda e: abrir_archivo("login.py")  # ✅ Ejecuta login.py
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MENU_BOOK),
                    title=ft.Text("Menú Interactivo"),
                    on_click=lambda e: abrir_archivo("menu.py")  # ✅ Ejecuta menu.py
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME),
                    title=ft.Text("Home"),
                    on_click=lambda e: abrir_archivo("main.py")  # ✅ Ejecuta comandas.py
                ),
            ], spacing=10)
        ]
    )

    # Drawer para comandas realizadas
    comandas_drawer = ft.NavigationDrawer(
        controls=[ft.Text("Comandas Realizadas", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                  comandas_realizadas_drawer],
        bgcolor="#5D0E41"
    )


    def obtener_precio(platillo):
        precios = {
            "Pizza Hawaiana": 120,
            "Hamburguesa BBQ": 150,
            "Tacos al Pastor": 100
        }
        return precios.get(platillo, 0)


    def toggle_comandas_drawer(e):
        mostrar_comandas_realizadas(e)  # Actualizar la lista de comandas
        comandas_drawer.open = not comandas_drawer.open
        page.update()

    # AppBar
    appbar = ft.AppBar(
        title=ft.Text(f"Mesero: {comanda_data['nombre_mesero']}", color="#F2E8EC"),
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        actions=[ft.IconButton(icon=ft.Icons.LIST, on_click=toggle_comandas_drawer, icon_color="#E71790")]  # Botón para mostrar comandas
    )

    page.appbar = appbar
    page.end_drawer = comandas_drawer

    # Texto para mostrar el número de comanda
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
        ft.ElevatedButton("Generar Comanda", on_click=generar_comanda, bgcolor="#4CAF50", color="#F2E8EC"),
    )

ft.app(target=main)

