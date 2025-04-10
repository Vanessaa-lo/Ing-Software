import flet as ft
from datetime import datetime
import os
import subprocess

usuario_actual = "Roberto Empleado"

def main(page: ft.Page):
    page.title = "Módulo Meseros"
    page.bgcolor = "#1C1C1C"  # Fondo oscuro para contraste
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 20

    # Variables para almacenar los datos de la comanda
    comanda_data = {
        "numero_comanda": 1,
        "fecha_hora": "",
        "nombre_mesero": "Roberto",
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
            comanda_data["platillos"].append({
                "id": len(comanda_data["platillos"]) + 1,  # Identificador único para cada platillo
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

    # Función para generar la comanda
    def generar_comanda(e):
        if not comanda_data["platillos"]:
            return  # No generar comanda si no hay platillos

        comanda_data["fecha_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        comanda_data["numero_mesa"] = int(numero_mesa_dropdown.value)  # Convertir a entero
        comanda_data["numero_comensales"] = int(numero_comensales_dropdown.value)  # Convertir a entero

        # Guardar la comanda realizada
        comandas_realizadas.append(comanda_data.copy())

        # Incrementar el número de comanda para la próxima
        comanda_data["numero_comanda"] += 1
        comanda_data["platillos"] = []  # Limpiar la lista de platillos
        comanda_data["estado"] = "En preparación"  # Reiniciar el estado
        platillos_agregados.controls.clear()

        # Actualizar la visualización del número de comanda
        comanda_numero_text.value = f"Comanda # {comanda_data['numero_comanda']}"
        page.update()

    def mostrar_comandas_realizadas(e):
        comandas_realizadas_drawer.controls.clear()
        for idx, comanda in enumerate(comandas_realizadas):
            # Colores e íconos por estado
            estado_color = {
                "En preparación": "#FFC107",  # Amarillo
                "Listo": "#4CAF50",  # Verde
                "Entregado": "#2196F3"  # Azul
            }.get(comanda["estado"], "#B0BEC5")  # Gris pastel suave

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
                        bgcolor="#1E1E2F",  # Fondo más oscuro para contraste
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
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=platillo["id"] - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=platillo["id"] - 1: editar_platillo(e, idx), icon_color="#4CAF50")
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
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=platillo["id"] - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=platillo["id"] - 1: editar_platillo(e, idx), icon_color="#4CAF50")
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
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, idx=platillo["id"] - 1: eliminar_platillo(e, idx), icon_color="#FF0000"),
                        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, idx=platillo["id"] - 1: editar_platillo(e, idx), icon_color="#4CAF50")
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

    platillo_input = ft.TextField(label="Platillo/Bebida", width=300, color="#F2E8EC")
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
                    content=ft.Text(f"Usuario: {usuario_actual}", size=16, color="#E71790"),
                    padding=10
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



    def toggle_comandas_drawer(e):
        mostrar_comandas_realizadas(e)  # Actualizar la lista de comandas
        comandas_drawer.open = not comandas_drawer.open
        page.update()

    # AppBar
    appbar = ft.AppBar(
        title=ft.Text(f"Mesero: {comanda_data['nombre_mesero']}", color="#F2E8EC"),
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        actions=[ft.IconButton(icon=ft.icons.LIST, on_click=toggle_comandas_drawer, icon_color="#E71790")]  # Botón para mostrar comandas
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

