import flet as ft
from db_config import conectar_bd
import subprocess
import os
from datetime import datetime
from flet import animation as anim
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

        conn = conectar_bd()
        cursor = conn.cursor()

        def contar_total(tabla):
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            return cursor.fetchone()[0]

        def sumar_total(tabla, campo_valor):
            cursor.execute(f"SELECT SUM({campo_valor}) FROM {tabla}")
            resultado = cursor.fetchone()[0]
            return float(resultado) if resultado else 0.0

        # ✅ Ventas desde detalleventas
        cursor.execute("""
            SELECT SUM(d.Total)
            FROM ventas v
            JOIN detalleventas d ON v.IdVentas = d.Ventas_IdVentas
        """)
        total_ventas = cursor.fetchone()[0] or 0.0

        total_entradas = contar_total("entradasproductos")
        total_salidas = contar_total("salidasproductos")
        total_pedidos = contar_total("generarpedido")
        total_caja = sumar_total("cortecaja", "DineroFinalizar")

        conn.close()

        page.add(
            ft.Column([
                ft.Text("📊 Reporte General", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Divider(),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"🛒 Ventas Totales: ${total_ventas:.2f}", size=18, color="white"),
                        ft.Text(f"📥 Total Entradas: {total_entradas}", size=18, color="white"),
                        ft.Text(f"📤 Total Salidas: {total_salidas}", size=18, color="white"),
                        ft.Text(f"📦 Pedidos Generados: {total_pedidos}", size=18, color="white"),
                        ft.Text(f"💰 Dinero Total en Caja: ${total_caja:.2f}", size=18, color="white"),
                        ft.Text(f"👤 Usuario: {usuario_actual}", size=18, color="#E71790")
                    ], spacing=10),
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
        cursor.execute("SELECT Nombre, Descripcion FROM productos")
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
            
            # Insertar en entradasproductos
            cursor.execute(
                "INSERT INTO entradasproductos (Cantidad, Fecha, Descripcion, CorteCaja_idCorteCaja) VALUES (%s, CURDATE(), %s, 1)",
                (entrada_cantidad.value, entrada_descripcion.value)
            )

            # Verificar si el producto ya está en productosstock
            cursor.execute("SELECT COUNT(*) FROM productosstock WHERE Nombre = %s", (entrada_producto.value,))
            existe = cursor.fetchone()[0]

            if existe:
                # Si ya existe, sumar la cantidad
                cursor.execute(
                    "UPDATE productosstock SET Cantidad = Cantidad + %s WHERE Nombre = %s",
                    (entrada_cantidad.value, entrada_producto.value)
                )
            else:
                # Si no existe, obtener la descripción del producto original
                descripcion = ""
                for p in productos:
                    if p[0] == entrada_producto.value:
                        descripcion = p[1] if len(p) > 1 else ""
                        break
                cursor.execute(
                    "INSERT INTO productosstock (Nombre, Descripcion, Cantidad, CorteCaja_idCorteCaja) VALUES (%s, %s, %s, 1)",
                    (entrada_producto.value, descripcion, entrada_cantidad.value)
                )

            conn.commit()
            cursor.close()
            conn.close()

            # Limpiar campos
            entrada_producto.value = ""
            entrada_cantidad.value = ""
            entrada_descripcion.value = ""

            page.snack_bar = ft.SnackBar(content=ft.Text("Entrada registrada con éxito"))
            page.snack_bar.open = True
            page.update()

        def registrar_salida(e):
            conn = conectar_bd()
            cursor = conn.cursor()

            # Obtener la cantidad actual del producto seleccionado
            cursor.execute("SELECT Cantidad FROM productosstock WHERE Nombre = %s", (salida_producto.value,))
            resultado = cursor.fetchone()

            if resultado is None:
                page.snack_bar = ft.SnackBar(content=ft.Text("Producto no encontrado en el inventario."))
                page.snack_bar.open = True
                return

            cantidad_actual = float(resultado[0])
            cantidad_salida = float(salida_cantidad.value)

            # Verificar si hay suficiente producto
            if cantidad_salida > cantidad_actual:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"No hay suficiente stock. Disponible: {cantidad_actual}"))
                page.snack_bar.open = True
                return

            # Registrar salida
            cursor.execute(
                "INSERT INTO salidasproductos (Cantidad, FechaSalida, Detalle, CorteCaja_idCorteCaja) VALUES (%s, CURDATE(), %s, 1)",
                (cantidad_salida, salida_descripcion.value)
            )

            # Actualizar inventario
            cursor.execute(
                "UPDATE productosstock SET Cantidad = Cantidad - %s WHERE Nombre = %s",
                (cantidad_salida, salida_producto.value)
            )

            conn.commit()
            cursor.close()
            conn.close()

            # Limpiar campos
            salida_producto.value = ""
            salida_cantidad.value = ""
            salida_descripcion.value = ""

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

        






# Nueva versión de mostrar_caja_chica con UI mejorada y lógica completa

# Nueva versión de mostrar_caja_chica con UI mejorada y lógica completa

    def mostrar_caja_chica(e=None):

        page.clean()
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)

        # Obtener último corte
        cursor.execute("SELECT * FROM cortecaja ORDER BY idCorteCaja DESC LIMIT 1")
        corte = cursor.fetchone()

        if not corte:
            cursor.execute("""
                INSERT INTO cortecaja (
                    Hora_Inicio, Hora_Terminar, Fecha_Inico, DineroEnCaja,
                    IngresoDia, EgresoDia, PlatillosVendidos, DineroFinalizar,
                    TiempoTrascurrido, FechaFinalizar, Administrador_idAdministrador
                ) VALUES (CURTIME(), '00:00', CURDATE(), 0, 0, 0, 0, 0, 0, CURDATE(), 1)
            """)
            conn.commit()
            cursor.execute("SELECT * FROM cortecaja ORDER BY idCorteCaja DESC LIMIT 1")
            corte = cursor.fetchone()

        dinero_actual = corte["DineroEnCaja"]

        # Cargar pedidos pendientes
        cursor.execute("SELECT * FROM generarpedido WHERE Estatus = 'Pedido Realizado'")
        pedidos = cursor.fetchall()

        tabla_pedidos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Acción")),
            ],
            rows=[]
        )

        # Campo para monto recibido
        monto_recibido = ft.TextField(label="Monto recibido", keyboard_type=ft.KeyboardType.NUMBER, width=200)

        def procesar_cobro(pedido):
            conn = conectar_bd()
            cursor = conn.cursor(dictionary=True)

            total = 150
            impuesto = total * 0.16
            subtotal = total - impuesto

            try:
                recibido = float(monto_recibido.value)
            except:
                page.snack_bar = ft.SnackBar(content=ft.Text("❌ Ingrese un monto válido"))
                page.snack_bar.open = True
                return

            if recibido < total:
                page.snack_bar = ft.SnackBar(content=ft.Text("❌ El monto recibido es menor al total"))
                page.snack_bar.open = True
                return

            cambio = recibido - total

            cursor.execute("""
                INSERT INTO ventas (Hora, FechaVenta, DetalleVenta, CorteCaja_idCorteCaja)
                VALUES (CURTIME(), CURDATE(), %s, %s)
            """, (pedido["Producto"], corte["idCorteCaja"]))
            id_venta = cursor.lastrowid

            cursor.execute("""
                INSERT INTO detalleventas (Subtotal, Impuesto, Descuento, Total, Ventas_IdVentas)
                VALUES (%s, %s, 0, %s, %s)
            """, (subtotal, impuesto, total, id_venta))

            cursor.execute("UPDATE generarpedido SET Estatus = 'Pagado' WHERE IdGenerarPedido = %s", (pedido["IdGenerarPedido"],))
            cursor.execute("UPDATE estatuspedido SET SituacionPedido = 'Pagado' WHERE IdEstatusPedido = %s", (pedido["EstatusPedido_IdEstatusPedido"],))

            cursor.execute("""
                UPDATE cortecaja SET DineroEnCaja = DineroEnCaja + %s, IngresoDia = IngresoDia + %s
                WHERE idCorteCaja = %s
            """, (total, total, corte["idCorteCaja"]))

            conn.commit()
            cursor.close()
            conn.close()

            page.dialog = ft.AlertDialog(
                title=ft.Text("💵 Cobro exitoso"),
                content=ft.Text(f"Total: ${total:.2f}\nRecibido: ${recibido:.2f}\nCambio: ${cambio:.2f}"),
                actions=[ft.TextButton("Aceptar", on_click=lambda e: setattr(page.dialog, 'open', False))]
            )
            page.dialog.open = True
            page.update()

            mostrar_caja_chica()

        for pedido in pedidos:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(pedido["IdGenerarPedido"]))),
                    ft.DataCell(ft.Text(pedido["Producto"])),
                    ft.DataCell(ft.Text("$150.00")),
                    ft.DataCell(
                        ft.IconButton(icon=ft.icons.PAID, tooltip="Cobrar", icon_color="green",
                                    on_click=lambda e, p=pedido: procesar_cobro(p))
                    )
                ]
            )
            tabla_pedidos.rows.append(fila)

        cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER)
        descripcion = ft.TextField(label="Descripción")

        def ingreso_egreso(valor):
            try:
                monto = float(cantidad.value)
            except:
                page.snack_bar = ft.SnackBar(content=ft.Text("Cantidad inválida"))
                page.snack_bar.open = True
                return

            if valor > 0:
                cursor.execute("""
                    UPDATE cortecaja SET DineroEnCaja = DineroEnCaja + %s, IngresoDia = IngresoDia + %s
                    WHERE idCorteCaja = %s
                """, (monto, monto, corte["idCorteCaja"]))
            else:
                cursor.execute("""
                    UPDATE cortecaja SET DineroEnCaja = DineroEnCaja - %s, EgresoDia = EgresoDia + %s
                    WHERE idCorteCaja = %s
                """, (monto, monto, corte["idCorteCaja"]))

            conn.commit()
            mostrar_caja_chica()

        sidebar = ft.Container(
            width=300,
            bgcolor="#2A2A2A",
            border_radius=15,
            animate=anim.Animation(500, "easeInOut"),
            content=ft.Column([
                ft.Text("💸 Ingresar / Retirar Dinero", size=20, color="white"),
                cantidad,
                descripcion,
                ft.Row([
                    ft.ElevatedButton("Ingreso", on_click=lambda e: ingreso_egreso(1), bgcolor="blue", color="white"),
                    ft.ElevatedButton("Egreso", on_click=lambda e: ingreso_egreso(-1), bgcolor="red", color="white"),
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ], spacing=15, alignment=ft.MainAxisAlignment.CENTER),
            padding=15
        )

        page.add(
            ft.Row([
                ft.Container(
                    expand=True,
                    content=ft.Column([
                        ft.Text("Caja Chica", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                        ft.Text(f"🪙 Dinero actual en caja: ${dinero_actual:.2f}", size=18, color="white"),
                        ft.Divider(),
                        monto_recibido,
                        tabla_pedidos,
                        ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
                    ], spacing=20, alignment=ft.MainAxisAlignment.START),
                    padding=20
                ),
                sidebar
            ])
        )

        cursor.close()
        conn.close()





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
