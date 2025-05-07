import flet as ft
from datetime import datetime
from db_config import conectar_bd
bd = conectar_bd()
cursor = bd.cursor()
import subprocess
import os

usuario_actual = "Roberto Empleado"  # Se puede cambiar dinámicamente desde el login
carrito = []

def main(page: ft.Page):
    page.title = "Menú de Platillos"
    page.bgcolor = "#121212"
    page.window_width = 390
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    
    pedidos = []

    
    def toggle_sidebar(e):
        page.drawer.open = not page.drawer.open
        page.update()



# 👉 Barra lateral derecha
    page.end_drawer = ft.NavigationDrawer(
        controls=[
            ft.Text("Accesos Rápidos", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
            ft.Divider(),
            ft.ListTile(
                leading=ft.Icon(ft.icons.SHOPPING_CART),
                title=ft.Text("Ver Carrito"),
                on_click=lambda e: mostrar_carrito(e)
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.LIST),
                title=ft.Text("Ver Pedidos"),
                on_click=lambda e: mostrar_estatus_pedido()
            ),
            
        ],
        bgcolor="#5D0E41"
    )

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
    
       

    
    def mostrar_carrito(e):
        carrito_drawer = ft.NavigationDrawer(
            controls=[
                ft.Text("Carrito de Compras", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Divider(),
                *(ft.Text(f"{p['nombre']} - ${p['precio']} - Ingredientes: {', '.join(p['ingredientes'])}", size=16, color="#F2E8EC") for p in carrito),
                ft.Text(f"Total: ${sum(p['precio'] for p in carrito)}", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.TextButton("Pedidos Realizados", icon=ft.icons.CHECK_CIRCLE, style=ft.ButtonStyle(color="#F2E8EC"), on_click=lambda e: mostrar_estatus_pedido()),
                ft.ElevatedButton("Confirmar Pedido", on_click=lambda e: [cerrar_carrito(), confirmar_pedido()], bgcolor="#28A745", color="white"),
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
    
    def agregar_al_carrito(e, platillo, ingredientes_seleccionados):
        descripcion = f"{platillo['nombre']} - Ingredientes: {', '.join(ingredientes_seleccionados)}"
        carrito.append({
            "nombre": platillo["nombre"],
            "precio": platillo["precio"],
            "ingredientes": ingredientes_seleccionados,
            "descripcion_completa": descripcion
        })
        page.snack_bar = ft.SnackBar(content=ft.Text(f"{platillo['nombre']} agregado al carrito!"))
        page.snack_bar.open = True
        page.update()


    def confirmar_pedido():
        global bd, cursor

        if not carrito:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("❌ No hay productos en el carrito."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            fecha_actual = datetime.now().date()
            hora_actual = datetime.now().strftime("%H:%M:%S")
            estatus = "Pedido Realizado"
            id_cliente = 1  # Cliente fijo
            numero_mesa = 1  # Mesa fija o puedes hacerla dinámica

            # Obtener ID del estatus desde la base de datos
            cursor.execute("SELECT IdEstatusPedido FROM estatuspedido WHERE SituacionPedido = %s", (estatus,))
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception("No se encontró el estatus en la base de datos.")
            id_estatus = resultado[0]

            # Insertar cada producto del carrito como un pedido individual
            for producto in carrito:
                descripcion_pedido = f"{producto['nombre']} (Ingredientes: {producto['descripcion_completa']})"

                cursor.execute("""
                    INSERT INTO generarpedido 
                    (HoraPedido, FechaPedido, Producto, NumeroMesa, Estatus, EstatusPedido_IdEstatusPedido, Clientes_Idcliente)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    hora_actual,
                    fecha_actual,
                    descripcion_pedido,
                    numero_mesa,
                    estatus,
                    id_estatus,
                    id_cliente
                ))

            bd.commit()
            carrito.clear()

            page.snack_bar = ft.SnackBar(
                content=ft.Text("✅ Pedido confirmado con éxito."),
                bgcolor="#28A745"
            )
            page.snack_bar.open = True
            mostrar_menu()

        except Exception as e:
            print(f"❌ ERROR SQL: {e}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ Error al guardar el pedido: {str(e)}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()




    # ✅ Función para cerrar el recibo
    def cerrar_recibo():
        page.dialog.open = False
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


        
    def mostrar_estatus_pedido():
        carrito.clear()
        cerrar_carrito()
        page.clean()

        try:
            cursor.execute("""
                SELECT g.IdGenerarPedido, g.FechaPedido, g.HoraPedido, g.Producto, g.NumeroMesa, e.SituacionPedido 
                FROM generarpedido g
                JOIN estatuspedido e ON g.EstatusPedido_IdEstatusPedido = e.IdEstatusPedido
                ORDER BY g.IdGenerarPedido DESC
            """)
            pedidos = cursor.fetchall()

            if not pedidos:
                page.snack_bar = ft.SnackBar(content=ft.Text("No hay pedidos registrados."))
                page.snack_bar.open = True
                page.update()
                return

            lista = ft.Column([
                ft.Row([
                    ft.IconButton(ft.icons.ARROW_BACK, icon_color="#AED2FF", on_click=lambda e: mostrar_menu()),
                    ft.Text("Pedidos Realizados", size=30, weight=ft.FontWeight.BOLD, color="#E71790"),
                ]),
                ft.Text(
                    "📋 Aquí puedes consultar todos los pedidos realizados junto con su estado actual.",
                    size=16,
                    color="white"
                ),
                ft.Divider()
            ], scroll=ft.ScrollMode.ALWAYS)

            for p in pedidos:
                producto = p[3]
                if "Ingredientes:" in producto:
                    platillo, ingredientes = producto.split("Ingredientes:", 1)
                    producto_formateado = f"{platillo.strip()}\n🧂 Ingredientes:\n{ingredientes.strip()}"
                else:
                    producto_formateado = producto

                lista.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"🧾 Orden N.º {p[0]}", size=16, color="#E71790"),
                            ft.Text(f"📅 Fecha: {p[1]}", size=16, color="white"),
                            ft.Text(f"⏰ Hora: {p[2]}", size=16, color="white"),
                            ft.Text(f"🍽️ Producto: {producto_formateado}", color="white", size=16),
                            ft.Text(f"🪑 Mesa: {p[4]}", size=16, color="white"),
                            ft.Text(f"✅ Estatus: {p[5]}", size=16, color="#4CAF50"),
                        ], spacing=5),
                        padding=10,
                        bgcolor="#2A2A2A",
                        border_radius=10,
                        margin=ft.margin.only(bottom=10)
                    )
                )


            page.add(ft.Container(expand=True, content=lista, padding=20))

        except Exception as e:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al obtener pedidos: {e}"))
            page.snack_bar.open = True
            contenido_pedidos = ft.Column(
                scroll="auto",  
            )

            page.controls.clear()
            page.add(
                contenido_pedidos
            )
            page.update()





    def mostrar_detalle(e, platillo):
        checkboxes_ingredientes = [ft.Checkbox(label=i, value=True) for i in platillo["ingredientes"]]
        porciones = ["Chica", "Mediana", "Grande"]
        acomp = ["Papas Fritas", "Ensalada", "Arroz"]
        extras = ["Queso Extra", "Salsa Picante", "Guacamole"]

        dropdown_porcion = ft.Dropdown(
            label="Tamaño de Porción",
            options=[ft.dropdown.Option(p) for p in porciones],
            value="Mediana",
            width=300
        )
        
        dropdown_acompanamiento = ft.Dropdown(
            label="Acompañamiento",
            options=[ft.dropdown.Option(a) for a in acomp],
            width=300
        )

        checkboxes_extras = [ft.Checkbox(label=e, value=False) for e in extras]

        page.clean()
        page.add(
            ft.Row(
                [
                    # Barra lateral vacía
                    ft.Container(
                        width=55,
                        bgcolor="#202020"
                    ),
                    # Contenido del detalle del platillo, con scroll habilitado
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            [
                                ft.Row([
                                    ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mostrar_menu()),
                                    ft.Text(platillo["nombre"], size=26, weight=ft.FontWeight.BOLD, color="#E71790"),

                            ]),
                                ft.Image(src=platillo["imagen"], width=320, height=220, border_radius=10),
                                ft.Text(platillo["descripcion"], size=14, color="#CCCCCC", italic=True),
                                ft.Text(f"Precio: ${platillo['precio']}", size=20, color="#F2E8EC"),
                                ft.Text("Ingredientes:", size=18, color="#E71790"),
                                ft.Column(checkboxes_ingredientes, spacing=5),

                                dropdown_porcion,
                                dropdown_acompanamiento,
                                ft.Text("Extras:", size=18, color="#E71790"),
                                ft.Column(checkboxes_extras, spacing=5),

                                ft.ElevatedButton(
                                    "Agregar al Carrito",
                                    on_click=lambda e: agregar_al_carrito(
                                        e,
                                        platillo,
                                        [c.label for c in checkboxes_ingredientes if c.value] +
                                        [dropdown_porcion.value] +
                                        [dropdown_acompanamiento.value] +
                                        [c.label for c in checkboxes_extras if c.value]
                                    ),
                                    bgcolor="#E71790",
                                    color="white"
                                )
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10,
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True
                        )
                    )
                ],
                expand=True  # 👉 Esta línea va aquí y con paréntesis cerrado correctamente
            )
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
                # Barra lateral vacía
                ft.Container(
                    width=55,
                    bgcolor="#202020",
                    content=None
                ),
                # Contenedor para el menú de platillos
                ft.Container(
                    expand=True,
                    content=lista_platillos
                )
            ])
        )
    mostrar_menu()
    
ft.app(target=main)
