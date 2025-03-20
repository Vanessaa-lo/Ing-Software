import flet as ft
from db_config import conectar_bd
import subprocess
import os
usuario_actual = "Roberto Empleado"


def main(page: ft.Page):
    page.title = "Punto de Venta"
    page.bgcolor = "#1C1C1C"
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 10

    def toggle_sidebar(e):
        page.drawer.open = not page.drawer.open
        page.update()

    def abrir_archivo(nombre_archivo):
        ruta = os.path.join(os.path.dirname(__file__), nombre_archivo)
        subprocess.Popen(["python", ruta])  # Ejecuta el archivo .py

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Menú", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text(f"Usuario: {usuario_actual}", size=16, color="#E71790"),  # Muestra el usuario actual
                    ft.Divider(),
                    
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LOGIN),
                        title=ft.Text("Regresar al Login"),
                        on_click=lambda e: abrir_archivo("login.py")
                    ),

                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MENU_BOOK),
                        title=ft.Text("Menú Interactivo"),
                        on_click=lambda e: abrir_archivo("menu.py")
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.LIST),
                        title=ft.Text("Comandas"),
                        on_click=lambda e: abrir_archivo("comandas.py")
                    ),
             ], spacing=20),
                padding=20
            )
        ]
    )

    def mostrar_inicio(e=None):
        page.clean()


        # Lista de opciones del menú principal
        opciones = [
            {"titulo": "Ver Inventario", "accion": mostrar_inventario},
            {"titulo": "Entradas y Salidas", "accion": mostrar_entradas_salidas},
            {"titulo": "Caja Chica", "accion": mostrar_caja_chica},
            {"titulo": "Generar Reportes", "accion": mostrar_reportes}  # ✅ Nueva tarjeta

        ]

        # Generamos las tarjetas con botones
        tarjetas = []
        for opcion in opciones:
            tarjeta = ft.Container(
                content=ft.Column([
                    ft.Text(opcion["titulo"], size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ft.ElevatedButton("Ingresar", on_click=opcion["accion"], bgcolor="#E71790", color="white")
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                width=250,
                height=150,
                bgcolor="#2A2A2A",
                border_radius=10,
                padding=10
            )
            tarjetas.append(tarjeta)

        # Crear GridView y agregar tarjetas correctamente
        grid = ft.GridView(
            expand=True,
            runs_count=2,  # 2 columnas en PC, 1 en móvil
            max_extent=250,  # Tamaño máximo de cada tarjeta
            spacing=10,
            run_spacing=10
        )
        grid.controls.extend(tarjetas)  # ✅ Agregar tarjetas correctamente

        page.add(
            ft.Column([
                grid  # Agregamos el GridView corregido
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )


    def mostrar_login():
        page.clean()
        page.add(ft.Text( size=24, weight=ft.FontWeight.BOLD, color="#E71790"))
        page.update()

    def mostrar_reportes(e=None):
        page.clean()

        # Datos de ejemplo (sin conexión a la base de datos)
        ventas_totales = 12500.50  # Ventas del día en $
        total_productos = 230  # Cantidad de productos en inventario
        dinero_en_caja = 5400.75  # Dinero en caja en $
        total_comandas = 35  # Número de comandas generadas
        usuario_actual = "Roberto Empleado"  # Usuario logueado

        # Mostrar reportes en la pantalla
        page.add(
            ft.Column([
                ft.Text("📊 Reporte del Día", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Divider(),

                ft.Container(
                    content=ft.Column([
                        ft.Text(f"📅 Ventas del Día: ${ventas_totales:.2f}", size=18, color="white"),
                        ft.Text(f"📦 Inventario Disponible: {total_productos} productos", size=18, color="white"),
                        ft.Text(f"💰 Dinero en Caja: ${dinero_en_caja:.2f}", size=18, color="white"),
                        ft.Text(f"📝 Comandas Generadas: {total_comandas}", size=18, color="white"),
                        ft.Text(f"👤 Usuario: {usuario_actual}", size=18, color="#E71790")
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    padding=20,
                    bgcolor="#2A2A2A",
                    border_radius=10,
                    width=400
                ),

                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )



    def mostrar_inventario(e=None):
        page.clean()
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre, Descripcion, Cantidad FROM productosstock")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        tabla_productos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Cantidad"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(prod[0])),
                        ft.DataCell(ft.Text(prod[1])),
                        ft.DataCell(ft.Text(str(prod[2])))
                    ]
                ) for prod in productos
            ]
        )
        
        page.add(
            ft.Column([
                ft.Text("Inventario", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                tabla_productos,
                ft.ElevatedButton("Agregar Producto", on_click=mostrar_formulario_producto, bgcolor="#E71790", color="white"),
                ft.ElevatedButton("Volver", on_click=lambda e: mostrar_inicio(), bgcolor="#5D0E41", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def mostrar_formulario_producto(e):
        page.clean()
        nombre = ft.TextField(label="Nombre del Producto")
        precio = ft.TextField(label="Precio")
        fecha_caducidad = ft.TextField(label="Fecha de Caducidad (YYYY-MM-DD)")
        descripcion = ft.TextField(label="Descripción")
        marca = ft.TextField(label="Marca")
        unidad_medida = ft.TextField(label="Unidad de Medida")
        
        def guardar_producto(e):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (IdProductos, Nombre, Precio, FechaCaducidad, Descripcion, Marca, UnidadMedida) VALUES (NULL, %s, %s, %s, %s, %s, %s)",
                (nombre.value, precio.value, fecha_caducidad.value, descripcion.value, marca.value, unidad_medida.value)
            )
            conn.commit()
            cursor.close()
            conn.close()
            page.snack_bar = ft.SnackBar(content=ft.Text("Producto agregado correctamente!"))
            page.snack_bar.open = True
            mostrar_inventario()
        
        page.add(
            ft.Column([
                ft.Text("Agregar Nuevo Producto", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                nombre,
                precio,
                fecha_caducidad,
                descripcion,
                marca,
                unidad_medida,
                ft.ElevatedButton("Guardar", on_click=guardar_producto, bgcolor="#E71790", color="white"),
                ft.ElevatedButton("Volver", on_click=mostrar_inventario, bgcolor="#5D0E41", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def mostrar_entradas_salidas(e=None):
        page.clean()
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Obtener productos disponibles desde la tabla productos
        cursor.execute("SELECT Nombre FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        producto_options = [ft.dropdown.Option(prod[0]) for prod in productos] if productos else []
        
        # Sección de entrada de productos
        entrada_producto = ft.Dropdown(label="Seleccionar Producto", options=producto_options, width=300)
        entrada_cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER, width=300)
        entrada_descripcion = ft.TextField(label="Descripción de Entrada", width=300)
        
        # Sección de salida de productos
        salida_producto = ft.Dropdown(label="Seleccionar Producto", options=producto_options, width=300)
        salida_cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER, width=300)
        salida_descripcion = ft.TextField(label="Motivo de Salida", width=300)
        
        def registrar_entrada(e):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO entradasproductos (Cantidad, Fecha, Descripcion, CorteCaja_idCorteCaja) VALUES (%s, CURDATE(), %s, 1)",
                (entrada_cantidad.value, entrada_descripcion.value)
            )
            cursor.execute(
                "UPDATE productosstock SET Cantidad = Cantidad + %s WHERE Nombre = %s",
                (entrada_cantidad.value, entrada_producto.value)
            )
            conn.commit()
            cursor.close()
            conn.close()
            page.snack_bar = ft.SnackBar(content=ft.Text("Entrada registrada con éxito"))
            page.snack_bar.open = True
            page.update()

        def registrar_salida(e):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO salidasproductos (Cantidad, FechaSalida, Detalle, CorteCaja_idCorteCaja) VALUES (%s, CURDATE(), %s, 1)",
                (salida_cantidad.value, salida_descripcion.value)
            )
            cursor.execute(
                "UPDATE productosstock SET Cantidad = Cantidad - %s WHERE Nombre = %s",
                (salida_cantidad.value, salida_producto.value)
            )
            conn.commit()
            cursor.close()
            conn.close()
            page.snack_bar = ft.SnackBar(content=ft.Text("Salida registrada con éxito"))
            page.snack_bar.open = True
            page.update()
    
        page.add(
            ft.Column([
                ft.Text("Gestión de Entradas y Salidas", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Registrar Entrada de Productos", size=20, color="#F2E8EC"),
                        entrada_producto,
                        entrada_cantidad,
                        entrada_descripcion,
                        ft.ElevatedButton("Registrar Entrada", on_click=registrar_entrada, bgcolor="#E71790", color="white")
                    ], spacing=10), padding=10, border_radius=10, border=ft.border.all(1, "#E71790")
                ),
                
                ft.Divider(),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Registrar Salida de Productos", size=20, color="#F2E8EC"),
                        salida_producto,
                        salida_cantidad,
                        salida_descripcion,
                        ft.ElevatedButton("Registrar Salida", on_click=registrar_salida, bgcolor="#E71790", color="white")
                    ], spacing=10), padding=10, border_radius=10, border=ft.border.all(1, "#E71790")
                ),
                
                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )


    def mostrar_caja_chica(e=None):
        page.clean()
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT DineroEnCaja FROM cortecaja ORDER BY idCorteCaja DESC LIMIT 1")
        dinero_actual = cursor.fetchone()
        dinero_actual = dinero_actual[0] if dinero_actual else 0.0
        cursor.close()
        conn.close()
        
        cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER)
        descripcion = ft.TextField(label="Descripción")

        def registrar_ingreso(e):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("UPDATE cortecaja SET DineroEnCaja = DineroEnCaja + %s, IngresoDia = IngresoDia + %s WHERE idCorteCaja = (SELECT MAX(idCorteCaja) FROM cortecaja)", 
                           (cantidad.value, cantidad.value))
            conn.commit()
            cursor.close()
            conn.close()
            page.snack_bar = ft.SnackBar(content=ft.Text("Ingreso registrado"))
            page.snack_bar.open = True
            page.update()
            mostrar_caja_chica()
        
        def registrar_egreso(e):
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("UPDATE cortecaja SET DineroEnCaja = DineroEnCaja - %s, EgresoDia = EgresoDia + %s WHERE idCorteCaja = (SELECT MAX(idCorteCaja) FROM cortecaja)", 
                           (cantidad.value, cantidad.value))
            conn.commit()
            cursor.close()
            conn.close()
            page.snack_bar = ft.SnackBar(content=ft.Text("Egreso registrado"))
            page.snack_bar.open = True
            page.update()
            mostrar_caja_chica()

        page.add(
            ft.Column([
                ft.Text("Caja Chica", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Text(f"Dinero en Caja: ${dinero_actual:.2f}", size=20, color="#F2E8EC"),
                cantidad,
                descripcion,
                ft.Row([
                    ft.ElevatedButton("Registrar Ingreso", on_click=registrar_ingreso, bgcolor="#28A745", color="white"),
                    ft.ElevatedButton("Registrar Egreso", on_click=registrar_egreso, bgcolor="#DC3545", color="white")
                ]),
                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )

    def mostrar_menu(e=None):
        page.clean()
        page.add(ft.Text("Menú Interactivo", size=24, weight=ft.FontWeight.BOLD, color="white"))
        page.update()


    def mostrar_comandas(e=None):
        page.clean()
        page.add(ft.Text("Gestión de Comandas", size=24, weight=ft.FontWeight.BOLD, color="white"))
        page.update()


    page.appbar = ft.AppBar(
        title=ft.Text("Punto de Venta", color="#F2E8EC"),
        leading=ft.IconButton(ft.Icons.MENU, on_click=toggle_sidebar, icon_color="#E71790"),
        bgcolor="#5D0E41"
    )
    mostrar_inicio()

ft.app(target=main)
