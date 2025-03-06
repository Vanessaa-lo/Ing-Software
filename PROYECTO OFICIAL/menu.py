import flet as ft

def main(page: ft.Page):
    page.title = "Menú de Platillos"
    page.bgcolor = "#1A1A1A"  # Fondo más oscuro
    page.window_width = 390
    page.window_height = 800
    
    carrito = []
    
    # Sidebar
    sidebar = ft.NavigationDrawer(
        controls=[
            ft.Text("Menú", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
            ft.Divider(),
            ft.TextButton("Inicio", icon=ft.icons.HOME),
            ft.TextButton("Pedidos", icon=ft.icons.LIST),
            ft.TextButton("Perfil", icon=ft.icons.PERSON),
        ],
    )
    
    def abrir_sidebar(e):
        sidebar.open = True
        page.update()
    
    def mostrar_carrito(e):
        page.clean()
        pedidos = "\n".join([f"- {p['nombre']} (${p['precio']})" for p in carrito]) if carrito else "Carrito vacío."
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_menu()),
                    ft.Text("Carrito de Compras", size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Text(pedidos, size=16, color="#F2E8EC"),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    
    # Datos de platillos
    platillos = [
        {"nombre": "Pizza Hawaiana", "imagen": "pizza.png", "precio": 120, "ingredientes": ["Piña", "Jamón", "Queso"]},
        {"nombre": "Hamburguesa BBQ", "imagen": "burger.png", "precio": 150, "ingredientes": ["Carne", "Queso", "Salsa BBQ"]},
        {"nombre": "Tacos al Pastor", "imagen": "tacos.png", "precio": 100, "ingredientes": ["Pastor", "Cilantro", "Cebolla"]},
    ]
    
    def agregar_al_carrito(e, platillo, ingredientes_seleccionados):
        carrito.append({"nombre": platillo["nombre"], "precio": platillo["precio"], "ingredientes": ingredientes_seleccionados})
        page.snack_bar = ft.SnackBar(content=ft.Text(f"{platillo['nombre']} agregado al carrito!"))
        page.snack_bar.open = True
        mostrar_menu()
    
    def mostrar_detalle(e, platillo):
        checkboxes = [ft.Checkbox(label=i, value=False) for i in platillo["ingredientes"]]
        page.clean()
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_menu()),
                    ft.Text(platillo["nombre"], size=24, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Image(src=platillo["imagen"], width=300, height=200),
                ft.Text(f"Precio: ${platillo['precio']}", size=18, color="#F2E8EC"),
                ft.Text("Selecciona ingredientes:", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Column(checkboxes),
                ft.ElevatedButton("Agregar al Carrito", on_click=lambda e: agregar_al_carrito(e, platillo, [c.label for c in checkboxes if c.value]), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    
    def mostrar_menu():
        page.clean()
        lista_platillos = ft.ListView(
            controls=[
                ft.Card(
                    content=ft.Container(
                        ft.Column([
                            ft.Image(src=p["imagen"], width=150, height=120),
                            ft.Text(p["nombre"], size=18, weight=ft.FontWeight.BOLD, color="#F2E8EC"),
                            ft.Text(f"${p['precio']}", size=16, color="#E71790"),
                            ft.ElevatedButton("Ver Detalle", on_click=lambda e, p=p: mostrar_detalle(e, p), bgcolor="#E71790", color="white")
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        padding=10,
                        border_radius=10,
                        bgcolor="#2E2E2E",
                        shadow=ft.BoxShadow(blur_radius=5, color="#5D0E41")
                    ),
                ) for p in platillos
            ]
        )
        
        page.add(
            ft.Row([
                ft.IconButton(ft.icons.MENU, on_click=abrir_sidebar),
                ft.Text("Menú de Platillos", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.IconButton(ft.icons.SHOPPING_CART, on_click=mostrar_carrito, icon_color="#E71790")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            lista_platillos
        )
    
    mostrar_menu()
    
ft.app(target=main)
