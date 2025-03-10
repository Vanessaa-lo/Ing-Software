import flet as ft

def main(page: ft.Page):
    page.title = "Punto de Venta"
    page.bgcolor = "#1C1C1C"
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 10  # Reducir el padding para móviles

    # Función para abrir/cerrar el sidebar
    def toggle_sidebar(e):
        sidebar.open = not sidebar.open
        page.update()

    # Sidebar
    sidebar = ft.NavigationDrawer(
        controls=[
            ft.Text("Menú Principal", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
            ft.Divider(),
            ft.TextButton("Corte de Caja", icon=ft.icons.ATTACH_MONEY, on_click=lambda e: mostrar_corte_caja()),
            ft.TextButton("Reporte de Productos", icon=ft.icons.INVENTORY, on_click=lambda e: mostrar_reporte_productos()),
            ft.TextButton("Entradas y Salidas", icon=ft.icons.INPUT, on_click=lambda e: mostrar_entradas_salidas()),
            ft.TextButton("Control de Ventas", icon=ft.icons.SHOPPING_CART, on_click=lambda e: mostrar_control_ventas()),
            ft.TextButton("Inventario", icon=ft.icons.STORAGE, on_click=lambda e: mostrar_inventario()),
        ],
        bgcolor="#5D0E41"
    )

    # Función para mostrar el corte de caja
    def mostrar_corte_caja(e=None):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_inicio()),
                    ft.Text("Corte de Caja", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Realiza el corte de caja y genera reportes de ventas.", color="#F2E8EC"),
                ft.ElevatedButton("Generar Reporte", on_click=lambda e: generar_reporte(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para generar un reporte
    def generar_reporte(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_corte_caja()),
                    ft.Text("Reporte Generado", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("El reporte de ventas ha sido generado con éxito.", color="#F2E8EC")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para mostrar el reporte de productos
    def mostrar_reporte_productos(e=None):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_inicio()),
                    ft.Text("Reporte de Productos", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Muestra el estado y detalles de los productos.", color="#F2E8EC"),
                ft.ElevatedButton("Ver Reporte", on_click=lambda e: ver_reporte_productos(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para ver el reporte de productos
    def ver_reporte_productos(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_reporte_productos()),
                    ft.Text("Detalles de Productos", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Aquí se muestran los detalles de los productos.", color="#F2E8EC")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para mostrar entradas y salidas
    def mostrar_entradas_salidas(e=None):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_inicio()),
                    ft.Text("Entradas y Salidas", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Registra entradas y salidas de productos.", color="#F2E8EC"),
                ft.ElevatedButton("Gestionar", on_click=lambda e: gestionar_entradas_salidas(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para gestionar entradas y salidas
    def gestionar_entradas_salidas(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_entradas_salidas()),
                    ft.Text("Gestionar Entradas y Salidas", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Aquí se gestionan las entradas y salidas de productos.", color="#F2E8EC")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para mostrar el control de ventas
    def mostrar_control_ventas(e=None):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_inicio()),
                    ft.Text("Control de Ventas", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Gestiona y revisa los detalles de las ventas.", color="#F2E8EC"),
                ft.ElevatedButton("Ver Ventas", on_click=lambda e: ver_ventas(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para ver las ventas
    def ver_ventas(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_control_ventas()),
                    ft.Text("Detalles de Ventas", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Aquí se muestran los detalles de las ventas.", color="#F2E8EC")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para mostrar el inventario
    def mostrar_inventario(e=None):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_inicio()),
                    ft.Text("Inventario", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Gestiona el inventario de productos.", color="#F2E8EC"),
                ft.ElevatedButton("Ver Inventario", on_click=lambda e: ver_inventario(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para ver el inventario
    def ver_inventario(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_inventario()),
                    ft.Text("Detalles de Inventario", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Aquí se muestra el estado del inventario.", color="#F2E8EC")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    # Función para mostrar la página principal
    def mostrar_inicio():
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar),
                    ft.Text("Punto de Venta", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text("Gestiona ventas, productos, inventario y más", size=16, color="#F2E8EC"),
                ft.Divider(),
                ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(name=ft.icons.ATTACH_MONEY, size=40, color="#8a0e56"),
                            ft.Text("Corte de Caja", size=20, weight=ft.FontWeight.BOLD, color="#780c4a"),
                            ft.Text("Realiza el corte de caja y genera reportes de ventas.", color="#8a0e56"),
                            ft.ElevatedButton("Corte de Caja", on_click=mostrar_corte_caja, bgcolor="#f493cb", color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        width=300,
                        height=200,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(name=ft.icons.INVENTORY, size=40, color="#8a0e56"),
                            ft.Text("Reporte de Productos", size=20, weight=ft.FontWeight.BOLD, color="#780c4a"),
                            ft.Text("Muestra el estado y detalles de los productos.", color="#8a0e56"),
                            ft.ElevatedButton("Ver Reporte", on_click=mostrar_reporte_productos, bgcolor="#f493cb", color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        width=300,
                        height=200,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(name=ft.icons.INPUT, size=40, color="#8a0e56"),
                            ft.Text("Entradas y Salidas", size=20, weight=ft.FontWeight.BOLD, color="#780c4a"),
                            ft.Text("Registra entradas y salidas de productos.", color="#8a0e56"),
                            ft.ElevatedButton("Gestionar", on_click=mostrar_entradas_salidas, bgcolor="#f493cb", color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        width=300,
                        height=200,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(name=ft.icons.SHOPPING_CART, size=40, color="#8a0e56"),
                            ft.Text("Control de Ventas", size=20, weight=ft.FontWeight.BOLD, color="#780c4a"),
                            ft.Text("Gestiona y revisa los detalles de las ventas.", color="#8a0e56"),
                            ft.ElevatedButton("Ver Ventas", on_click=mostrar_control_ventas, bgcolor="#f493cb", color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        width=300,
                        height=200,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(name=ft.icons.STORAGE, size=40, color="#8a0e56"),
                            ft.Text("Inventario", size=20, weight=ft.FontWeight.BOLD, color="#780c4a"),
                            ft.Text("Gestiona el inventario de productos.", color="#8a0e56"),
                            ft.ElevatedButton("Ver Inventario", on_click=mostrar_inventario, bgcolor="#f493cb", color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        padding=20,
                        bgcolor=ft.colors.WHITE,
                        border_radius=15,
                        width=300,
                        height=200,
                    )
                ], spacing=20)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )

    # Barra de aplicación con botón para abrir el sidebar
    appbar = ft.AppBar(
        title=ft.Text("Punto de Venta", color="#F2E8EC"),
        leading=ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        bgcolor="#5D0E41"
    )

    # Asignar el sidebar y la barra de aplicación a la página
    page.appbar = appbar
    page.drawer = sidebar

    # Mostrar la página principal al inicio
    mostrar_inicio()

ft.app(target=main)