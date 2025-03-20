import flet as ft
from datetime import datetime
from db_config import conectar_bd
bd = conectar_bd()
cursor = bd.cursor()
import subprocess
import os

usuario_actual = "Roberto Empleado"  # Se puede cambiar dinámicamente desde el login


def main(page: ft.Page):
    page.title = "Menú de Platillos"
    page.bgcolor = "#121212"
    page.window_width = 390
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    
    carrito = []
    pedidos = []

    
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
                    leading=ft.Icon(ft.Icons.LIST),
                    title=ft.Text("Comandas"),
                    on_click=lambda e: abrir_archivo("comandas.py")  # ✅ Ejecuta comandas.py
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HOME),
                    title=ft.Text("Home"),
                    on_click=lambda e: abrir_archivo("main.py")  # ✅ Ejecuta menu.py
                ),
            ], spacing=10)
        ]
    )

    
    page.appbar = ft.AppBar(
        title=ft.Text("Menú de Platillos", color="#F2E8EC"),
        leading=ft.IconButton(ft.Icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        actions=[ft.IconButton(ft.Icons.SHOPPING_CART, on_click=lambda e: mostrar_carrito(e), icon_color="#E71790")],
        bgcolor="#5D0E41"
    )
    
    
    def mostrar_menu():
        page.clean()
        lista_platillos = ft.GridView(
            runs_count=2,
            max_extent=350,
            spacing=10,
            run_spacing=10,
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Image(src=p["imagen"], width=150, height=120, border_radius=10),
                        ft.Text(p["nombre"], size=20, weight=ft.FontWeight.BOLD, color="#F2E8EC"),
                        ft.Text(f"${p['precio']}", size=18, color="#E71790"),
                        ft.ElevatedButton("Ver Detalle", on_click=lambda e, p=p: mostrar_detalle(e, p), bgcolor="#E71790", color="white")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                    padding=10,
                    border_radius=15,
                    bgcolor="#2E2E2E",
                    shadow=ft.BoxShadow(blur_radius=8, color="#5D0E41")
                ) for p in platillos
            ]
        )
        
 
       

    
    def mostrar_carrito(e):
        carrito_drawer = ft.NavigationDrawer(
            controls=[
                ft.Text("Carrito de Compras", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Divider(),
                *(ft.Text(f"{p['nombre']} - ${p['precio']} - Ingredientes: {', '.join(p['ingredientes'])}", size=16, color="#F2E8EC") for p in carrito),
                ft.Text(f"Total: ${sum(p['precio'] for p in carrito)}", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.TextButton("Estatus del Pedido", icon=ft.icons.CHECK_CIRCLE, style=ft.ButtonStyle(color="#F2E8EC"), on_click=lambda e: ver_estatus_pedido()),
                ft.ElevatedButton("Confirmar Pedido", on_click=lambda e: confirmar_pedido(), bgcolor="#28A745", color="white"),
                ft.ElevatedButton("Cerrar", on_click=lambda e: cerrar_carrito(), bgcolor="#E71790", color="white")
            ]
        )
        page.end_drawer = carrito_drawer
        page.end_drawer.open = True
        page.update()
    
    def cerrar_carrito():
        page.end_drawer.open = False
        page.update()
    
    platillos = [
        {"nombre": "Pizza Hawaiana", "imagen": "image/1.png", "precio": 120, "ingredientes": ["Piña", "Jamón", "Queso"]},
        {"nombre": "Hamburguesa BBQ", "imagen": "image/2.jpeg", "precio": 150, "ingredientes": ["Carne", "Queso", "Salsa BBQ", "Tocino", "Lechuga", "Papas"]},
        {"nombre": "Tacos al Pastor", "imagen": "tacos/3.png", "precio": 100, "ingredientes": ["Pastor", "Cilantro", "Cebolla"]},
    ]
    
    def agregar_al_carrito(e, platillo, ingredientes_seleccionados):
        carrito.append({"nombre": platillo["nombre"], "precio": platillo["precio"], "ingredientes": ingredientes_seleccionados})
        page.snack_bar = ft.SnackBar(content=ft.Text(f"{platillo['nombre']} agregado al carrito!"))
        page.snack_bar.open = True
        mostrar_menu()

    def confirmar_pedido():
        if carrito:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.now().strftime("%H:%M:%S")
            descripcion = "Pedido de comida"

            try:
                # Insertar el pedido en la tabla 'generarrecibo'
                sql_recibo = "INSERT INTO generarrecibo (FechaRecibo, HoraRecibo, descripcion, Ventas_IdVentas) VALUES (%s, %s, %s, %s)"
                valores_recibo = (fecha_actual, hora_actual, descripcion, 1)  # Reemplaza '1' con el ID correcto

                cursor.execute(sql_recibo, valores_recibo)
                bd.commit()

                # Obtener el ID del recibo insertado
                recibo_id = cursor.lastrowid

                # Insertar cada platillo en la base de datos
                for item in carrito:
                    sql_platillo = "INSERT INTO platillos (Nombre, Precio, Ingredientes, CorteCaja_idCorteCaja) VALUES (%s, %s, %s, %s)"
                    valores_platillo = (item["nombre"], item["precio"], ", ".join(item["ingredientes"]), 1)  # '1' es un ejemplo de CorteCaja

                    cursor.execute(sql_platillo, valores_platillo)
                    bd.commit()

                # Insertar el estado del pedido en 'estatuspedido'
                sql_estatus = "INSERT INTO estatuspedido (SituacionPedido) VALUES (%s)"
                valores_estatus = ("En preparación",)

                cursor.execute(sql_estatus, valores_estatus)
                bd.commit()

                # Vaciar el carrito
                carrito.clear()
                cerrar_carrito()

                page.snack_bar = ft.SnackBar(content=ft.Text("Pedido guardado en la base de datos!"))
                page.snack_bar.open = True
                page.update()

            except Exception as e:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(e)}"))
                page.snack_bar.open = True
                page.update()



    
    def ver_pedidos():
        page.clean()
        
        try:
            # Consultar los pedidos desde la base de datos
            cursor.execute("SELECT FechaRecibo, HoraRecibo, descripcion FROM generarrecibo")
            pedidos_db = cursor.fetchall()

            if not pedidos_db:
                page.snack_bar = ft.SnackBar(content=ft.Text("No hay pedidos registrados."))
                page.snack_bar.open = True
                page.update()
                return

            page.add(
                ft.Column([
                    ft.Text("Pedidos Realizados", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                    ft.Divider(),
                    *(ft.Text(f"Fecha: {p[0]} - Hora: {p[1]} - Descripción: {p[2]}", size=16, color="#F2E8EC") for p in pedidos_db),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_menu(), bgcolor="#E71790", color="white")
                ], spacing=10)
            )

        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al obtener pedidos: {str(e)}"))
            page.snack_bar.open = True
            page.update()


        

    def ver_estatus_pedido():
        page.clean()
        
        try:
            # Obtener el estatus del pedido desde la base de datos
            cursor.execute("SELECT IdEstatusPedido, SituacionPedido FROM estatuspedido ORDER BY IdEstatusPedido DESC LIMIT 5")
            estatus_db = cursor.fetchall()

            page.add(
                ft.Column([
                    ft.Text("Estatus del Pedido", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                    ft.Divider(),
                    *(ft.Text(f"ID: {p[0]} - Estatus: {p[1]}", size=16, color="#F2E8EC") for p in estatus_db),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_menu(), bgcolor="#E71790", color="white")
                ], spacing=10)
            )

        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al obtener estatus de pedidos: {str(e)}"))
            page.snack_bar.open = True
            page.update()



    def mostrar_detalle(e, platillo):
        checkboxes = [ft.Checkbox(label=i, value=False) for i in platillo["ingredientes"]]
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_menu()),
                    ft.Text(platillo["nombre"], size=26, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Image(src=platillo["imagen"], width=320, height=220, border_radius=10),
                ft.Text(f"Precio: ${platillo['precio']}", size=20, color="#F2E8EC"),
                ft.Text("Selecciona ingredientes:", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Column(checkboxes, spacing=5),
                ft.ElevatedButton("Agregar al Carrito", on_click=lambda e: agregar_al_carrito(e, platillo, [c.label for c in checkboxes if c.value]), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        )
    
    def mostrar_menu():
        page.clean()
        lista_platillos = ft.GridView(
            runs_count=2,
            max_extent=350,
            spacing=10,
            run_spacing=10,
            controls=[
                ft.Container(
                    ft.Column([
                        ft.Image(src=p["imagen"], width=150, height=120, border_radius=10),
                        ft.Text(p["nombre"], size=20, weight=ft.FontWeight.BOLD, color="#F2E8EC"),
                        ft.Text(f"${p['precio']}", size=18, color="#E71790"),
                        ft.ElevatedButton("Ver Detalle", on_click=lambda e, p=p: mostrar_detalle(e, p), bgcolor="#E71790", color="white")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                    padding=10,
                    border_radius=15,
                    bgcolor="#2E2E2E",
                    shadow=ft.BoxShadow(blur_radius=8, color="#5D0E41")
                ) for p in platillos
            ]
        )
        
        page.add(
            ft.Row([
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            lista_platillos
        )
    
    mostrar_menu()
    
ft.app(target=main)
