import flet as ft

def main(page: ft.Page):
    page.title = "Menú de Platillos"
    page.bgcolor = "#121212"
    page.window_width = 390
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    
    carrito = []
    
    sidebar = ft.NavigationDrawer(
        controls=[
            ft.Text("Menú", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
            ft.Divider(),
            ft.TextButton("Inicio", icon=ft.icons.HOME, style=ft.ButtonStyle(color="#F2E8EC")),
            ft.TextButton("Pedidos", icon=ft.icons.LIST, style=ft.ButtonStyle(color="#F2E8EC")),
            ft.TextButton("Perfil", icon=ft.icons.PERSON, style=ft.ButtonStyle(color="#F2E8EC")),
        ]
    )
    
    def abrir_sidebar(e):
        sidebar.open = True
        page.update()
    
    def mostrar_carrito(e):
        page.clean()
        total = sum(p['precio'] for p in carrito)
        pedidos = "\n".join([f"- {p['nombre']} (${p['precio']}) - Ingredientes: {', '.join(p['ingredientes'])}" for p in carrito]) if carrito else "Carrito vacío."
        page.add(
            ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_menu()),
                    ft.Text("Carrito de Compras", size=26, weight=ft.FontWeight.BOLD, color="#E71790")
                ]),
                ft.Container(
                    ft.Column([
                        ft.Text(pedidos, size=18, color="#F2E8EC"),
                        ft.Text(f"Total: ${total}", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                    ]),
                    padding=10,
                    border_radius=10,
                    bgcolor="#1F1F1F"
                ),
                ft.ElevatedButton("Volver al Menú", on_click=lambda e: mostrar_menu(), bgcolor="#E71790", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )
    
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
                ft.IconButton(ft.icons.MENU, on_click=abrir_sidebar),
                ft.Text("Menú de Platillos", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.IconButton(ft.icons.SHOPPING_CART, on_click=mostrar_carrito, icon_color="#E71790")
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            lista_platillos
        )
    
    mostrar_menu()
    
ft.app(target=main)

