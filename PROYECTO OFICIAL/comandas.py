import flet as ft
from datetime import datetime

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
        "platillos": []
    }

    comandas_realizadas = []  # Lista para almacenar las comandas realizadas

    # Función para agregar platillos/bebidas a la comanda
    def agregar_platillo(e):
        platillo = platillo_input.value
        cantidad = cantidad_input.value
        observaciones = observaciones_input.value

        if platillo and cantidad:
            comanda_data["platillos"].append({
                "platillo": platillo,
                "cantidad": cantidad,
                "observaciones": observaciones
            })
            platillos_agregados.controls.append(
                ft.Text(f"{platillo} - Cantidad: {cantidad} - Observaciones: {observaciones}", color="#F2E8EC")
            )
            platillo_input.value = ""
            cantidad_input.value = ""
            observaciones_input.value = ""
            page.update()

    # Función para generar la comanda
    def generar_comanda(e):
        if not comanda_data["platillos"]:
            return  # No generar comanda si no hay platillos

        comanda_data["fecha_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        comanda_data["numero_mesa"] = numero_mesa_dropdown.value
        comanda_data["numero_comensales"] = numero_comensales_dropdown.value

        # Guardar la comanda realizada
        comandas_realizadas.append(comanda_data.copy())

        # Incrementar el número de comanda para la próxima
        comanda_data["numero_comanda"] += 1
        comanda_data["platillos"] = []  # Limpiar la lista de platillos
        platillos_agregados.controls.clear()
        page.update()

    # Función para mostrar las comandas realizadas en el drawer
    def mostrar_comandas_realizadas(e):
        comandas_realizadas_drawer.controls.clear()
        for idx, comanda in enumerate(comandas_realizadas):
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

    # Función para borrar una comanda
    def borrar_comanda(e, idx):
        def confirmar_borrado(e):
            comandas_realizadas.pop(idx)
            mostrar_comandas_realizadas(e)
            page.update()
            page.close_dialog()

        # Mostrar un diálogo de confirmación
        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Borrado", color="#F2E8EC"),
            content=ft.Text("¿Estás seguro de que deseas borrar esta comanda?", color="#F2E8EC"),
            actions=[
                ft.ElevatedButton("Sí", on_click=confirmar_borrado, bgcolor="#FF0000", color="#F2E8EC"),
                ft.ElevatedButton("No", on_click=lambda e: page.close_dialog(), bgcolor="#4CAF50", color="#F2E8EC")
            ],
            bgcolor="#5D0E41"
        )
        page.dialog.open = True
        page.update()

    # Función para modificar una comanda
    def modificar_comanda(e, idx):
        comanda = comandas_realizadas[idx]
        comanda_data.update(comanda)  # Cargar los datos de la comanda seleccionada
        comanda_data["numero_comanda"] = comanda["numero_comanda"]  # Mantener el número de comanda

        # Actualizar los controles con los datos de la comanda
        numero_mesa_dropdown.value = comanda["numero_mesa"]
        numero_comensales_dropdown.value = comanda["numero_comensales"]
        platillos_agregados.controls.clear()
        for platillo in comanda["platillos"]:
            platillos_agregados.controls.append(
                ft.Text(f"{platillo['platillo']} - Cantidad: {platillo['cantidad']} - Observaciones: {platillo['observaciones']}", color="#F2E8EC")
            )

        # Eliminar la comanda de la lista de comandas realizadas
        comandas_realizadas.pop(idx)
        page.update()

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

    platillo_input = ft.TextField(label="Platillo/Bebida", width=300, color="#F2E8EC")
    cantidad_input = ft.TextField(label="Cantidad", width=300, color="#F2E8EC")
    observaciones_input = ft.TextField(label="Observaciones", width=300, color="#F2E8EC")

    platillos_agregados = ft.Column()

    # Drawer para comandas realizadas
    comandas_realizadas_drawer = ft.Column()

    # Sidebar
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Text("Menú", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
            ft.NavigationDrawerDestination(icon=ft.icons.RESTAURANT, label="Platillos"),
            ft.NavigationDrawerDestination(icon=ft.icons.LOCAL_DRINK, label="Bebidas"),
            ft.NavigationDrawerDestination(icon=ft.icons.PAYMENT, label="Pagos"),
        ],
        bgcolor="#8E2453"
    )

    # Drawer para comandas realizadas
    comandas_drawer = ft.NavigationDrawer(
        controls=[
            ft.Text("Comandas Realizadas", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
            comandas_realizadas_drawer
        ],
        bgcolor="#5D0E41"
    )

    def toggle_sidebar(e):
        drawer.open = not drawer.open
        page.update()

    def toggle_comandas_drawer(e):
        mostrar_comandas_realizadas(e)  # Actualizar la lista de comandas
        comandas_drawer.open = not comandas_drawer.open
        page.update()

    # AppBar
    appbar = ft.AppBar(
        title=ft.Text(f"Mesero: {comanda_data['nombre_mesero']}", color="#F2E8EC"),
        leading=ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        actions=[
            ft.IconButton(ft.icons.LIST, on_click=toggle_comandas_drawer, icon_color="#E71790")  # Botón para mostrar comandas
        ],
        bgcolor="#5D0E41"
    )

    page.appbar = appbar
    page.drawer = drawer
    page.end_drawer = comandas_drawer

    page.add(
        ft.Text(f"Comanda # {comanda_data['numero_comanda']}", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
        numero_mesa_dropdown,
        numero_comensales_dropdown,
        ft.Divider(height=20),

        ft.Text("Detalles del Pedido", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
        platillo_input,
        cantidad_input,
        observaciones_input,
        ft.ElevatedButton("Agregar Platillo/Bebida", on_click=agregar_platillo, bgcolor="#E71790", color="#F2E8EC"),
        ft.Divider(height=20),

        ft.Text("Platillos/Bebidas Agregados", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
        platillos_agregados,
        ft.Divider(height=20),

        ft.ElevatedButton("Enviar Comanda", on_click=generar_comanda, bgcolor="#E71790", color="#F2E8EC")
    )

ft.app(target=main)

