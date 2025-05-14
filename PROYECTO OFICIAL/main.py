import flet as ft
from db_config import conectar_bd
import subprocess
import os
from datetime import datetime
from flet import Animation as anim
import re

    


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
                    ft.Container( 
                    ),
                    
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.HOME),
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
                ], spacing=15),
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
        import flet as ft

        page.clean()

        # Widgets tablas
        tabla_pedidos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Pedido")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("Estatus")),
                ft.DataColumn(ft.Text("Fecha")),
            ],
            rows=[]
        )

        tabla_cobros = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Recibo")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Total")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Hora")),
                ft.DataColumn(ft.Text("Usuario")),
            ],
            rows=[]
        )

        tabla_movimientos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID Corte")),
                ft.DataColumn(ft.Text("Ingreso Día")),
                ft.DataColumn(ft.Text("Egreso Día")),
                ft.DataColumn(ft.Text("Dinero en Caja")),
                ft.DataColumn(ft.Text("Fecha Inicio")),
                ft.DataColumn(ft.Text("Fecha Finalizar")),
            ],
            rows=[]
        )

        resumen_final = ft.Column([], spacing=10)

        # Cargar Pedidos
        def cargar_pedidos():
            conn = conectar_bd()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT IdGenerarPedido, Producto, Total, Estatus, FechaPedido FROM generarpedido ORDER BY IdGenerarPedido DESC")
            pedidos = cursor.fetchall()
            cursor.close()
            conn.close()

            for pedido in pedidos:
                tabla_pedidos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(pedido["IdGenerarPedido"]))),
                            ft.DataCell(ft.Text(pedido["Producto"])),
                            ft.DataCell(ft.Text(f"${pedido['Total']:.2f}")),
                            ft.DataCell(ft.Text(pedido["Estatus"])),
                            ft.DataCell(ft.Text(str(pedido["FechaPedido"]))),
                        ]
                    )
                )

        # Cargar Cobros
        def cargar_cobros():
            conn = conectar_bd()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT IdRecibosPedidos, Producto, Total, Fecha, Hora, Usuario FROM recibospedidos ORDER BY IdRecibosPedidos DESC")
            cobros = cursor.fetchall()
            cursor.close()
            conn.close()

            for cobro in cobros:
                tabla_cobros.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cobro["IdRecibosPedidos"]))),
                            ft.DataCell(ft.Text(cobro["Producto"])),
                            ft.DataCell(ft.Text(f"${cobro['Total']:.2f}")),
                            ft.DataCell(ft.Text(str(cobro["Fecha"]))),
                            ft.DataCell(ft.Text(str(cobro["Hora"]))),
                            ft.DataCell(ft.Text(cobro["Usuario"])),
                        ]
                    )
                )

        # Cargar Movimientos de Caja
        def cargar_movimientos():
            conn = conectar_bd()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT idCorteCaja, IngresoDia, EgresoDia, DineroEnCaja, Fecha_Inico, FechaFinalizar FROM cortecaja ORDER BY idCorteCaja DESC")
            movimientos = cursor.fetchall()
            cursor.close()
            conn.close()

            for mov in movimientos:
                tabla_movimientos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(mov["idCorteCaja"]))),
                            ft.DataCell(ft.Text(f"${mov['IngresoDia']:.2f}")),
                            ft.DataCell(ft.Text(f"${mov['EgresoDia']:.2f}")),
                            ft.DataCell(ft.Text(f"${mov['DineroEnCaja']:.2f}")),
                            ft.DataCell(ft.Text(str(mov["Fecha_Inico"]))),
                            ft.DataCell(ft.Text(str(mov["FechaFinalizar"]))),
                        ]
                    )
                )

        # Cargar Resumen Final
        def cargar_resumen_final():
            conn = conectar_bd()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT SUM(Total) AS VentasTotales FROM recibospedidos")
            ventas = cursor.fetchone()

            cursor.execute("SELECT SUM(IngresoDia) AS TotalIngresos, SUM(EgresoDia) AS TotalEgresos, SUM(DineroEnCaja) AS DineroFinal FROM cortecaja")
            corte = cursor.fetchone()

            cursor.close()
            conn.close()

            resumen_final.controls.clear()
            resumen_final.controls.append(ft.Text("🧮 Resumen General del Proyecto", size=24, weight=ft.FontWeight.BOLD, color="#E71790"))

            resumen_final.controls.append(ft.Text(f"📦 Ventas Totales Realizadas: ${ventas['VentasTotales']:.2f}" if ventas['VentasTotales'] else "📦 Ventas Totales Realizadas: $0.00"))
            resumen_final.controls.append(ft.Text(f"💵 Ingresos Registrados: ${corte['TotalIngresos']:.2f}" if corte['TotalIngresos'] else "💵 Ingresos Registrados: $0.00"))
            resumen_final.controls.append(ft.Text(f"💸 Egresos Registrados: ${corte['TotalEgresos']:.2f}" if corte['TotalEgresos'] else "💸 Egresos Registrados: $0.00"))
            resumen_final.controls.append(ft.Text(f"🪙 Dinero Actual en Caja: ${corte['DineroFinal']:.2f}" if corte['DineroFinal'] else "🪙 Dinero Actual en Caja: $0.00"))

        # Cargar todos los datos
        cargar_pedidos()
        cargar_cobros()
        cargar_movimientos()
        cargar_resumen_final()

        # Layout principal
        page.add(
            ft.Column([
                ft.Text("📋 Reportes Completos del Proyecto", size=30, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Divider(),

                ft.Text("🧾 Pedidos Registrados", size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(
                    content=tabla_pedidos,
                    height=300,
                    bgcolor="#1E1E1E",
                    border_radius=10,
                    padding=10,
                    expand=True
                ),
                ft.Divider(),

                ft.Text("📦 Cobros Realizados", size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(
                    content=tabla_cobros,
                    height=300,
                    bgcolor="#1E1E1E",
                    border_radius=10,
                    padding=10,
                    expand=True
                ),
                ft.Divider(),

                ft.Text("💰 Ingresos y Egresos de Caja", size=24, weight=ft.FontWeight.BOLD, color="white"),
                ft.Container(
                    content=tabla_movimientos,
                    height=300,
                    bgcolor="#1E1E1E",
                    border_radius=10,
                    padding=10,
                    expand=True
                ),
                ft.Divider(),

                resumen_final,
                ft.Divider(),

                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
            ], spacing=20, expand=True, scroll=ft.ScrollMode.ALWAYS)
        )















    def filtrar_precio(e):
        valor = e.control.value
        nuevo_valor = ''.join(c for c in valor if c.isdigit() or c == '.')
        if nuevo_valor.count('.') > 1:
            partes = nuevo_valor.split('.')
            nuevo_valor = partes[0] + '.' + ''.join(partes[1:])
        e.control.value = nuevo_valor
        e.page.update()

    def filtrar_fecha(e):
        valor = ''.join(c for c in e.control.value if c.isdigit())
        if len(valor) > 4:
            valor = valor[:4] + '-' + valor[4:]
        if len(valor) > 7:
            valor = valor[:7] + '-' + valor[7:]
        if len(valor) > 10:
            valor = valor[:10]
        e.control.value = valor
        e.page.update()

    def filtrar_letras(e):
        valor = ''.join(c for c in e.control.value if c.isalpha())
        e.control.value = valor
        e.page.update()



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
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        )

        for prod in productos:
            color = "white" if prod[2] > 0 else "grey"
            leyenda = "" if prod[2] > 0 else " (Sin stock disponible)"
            
            tabla_productos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(prod[0] + leyenda, color=color)),
                        ft.DataCell(ft.Text(prod[1], color=color)),
                        ft.DataCell(ft.Text(str(prod[2]), color=color)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.INFO,
                                tooltip="Ver más información",
                                on_click=lambda e, producto=prod: mostrar_info_producto(e.page, producto)
                            )
                        )
                    ]
                )
            )

        
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Inventario", size=30, weight=ft.FontWeight.BOLD, color="#E71790"),
                tabla_productos,
                ft.Row([
                    ft.ElevatedButton("Agregar Producto", on_click=lambda e: mostrar_formulario_producto(page), bgcolor="#E71790", color="white"),
                    ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
                ], alignment=ft.MainAxisAlignment.CENTER)
            ])
        )


    def mostrar_info_producto(page, producto_stock):
        nombre_producto = producto_stock[0]  # El nombre viene de productosstock

        conn = conectar_bd()
        cursor = conn.cursor()

        # Buscar la información completa en productos
        cursor.execute("""
            SELECT Nombre, Precio, FechaCaducidad, Descripcion, Marca, UnidadMedida
            FROM productos
            WHERE Nombre = %s
        """, (nombre_producto,))
        info_producto = cursor.fetchone()

        cursor.close()
        conn.close()

        if info_producto:
            nombre, precio, fecha, descripcion, marca, unidad = info_producto
        else:
            nombre, precio, fecha, descripcion, marca, unidad = ("Desconocido", None, None, None, None, None)

        # Crear el diálogo
        dialogo = ft.AlertDialog(
            title=ft.Text("Información del Producto"),
            content=ft.Column([
                ft.Text(f"Nombre: {nombre}"),
                ft.Text(f"Descripción: {descripcion or 'No registrada'}"),
                ft.Text(f"Precio: ${precio:.2f}" if precio else "Precio no registrado"),
                ft.Text(f"Fecha de caducidad: {str(fecha)[:4]}-{str(fecha)[4:6]}-{str(fecha)[6:]}" if fecha else "Fecha no registrada"),
                ft.Text(f"Marca: {marca or 'No registrada'}"),
                ft.Text(f"Unidad de medida: {unidad or 'No registrada'}")
            ], spacing=10),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: setattr(dialogo, 'open', False))]
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()



    # --- Formulario de Nuevo Producto ---

    def mostrar_formulario_producto(page):
        nombre = ft.TextField(label="Nombre del Producto")
        precio = ft.TextField(label="Precio", on_change=filtrar_precio)
        fecha_caducidad = ft.TextField(label="Fecha de Caducidad (YYYY-MM-DD)", on_change=filtrar_fecha)
        descripcion = ft.TextField(label="Descripción")
        marca = ft.TextField(label="Marca")
        unidad_medida = ft.TextField(label="Unidad de Medida", on_change=filtrar_letras)

        def guardar_producto(e):
            errores = False

            if not nombre.value.strip():
                nombre.error_text = "Nombre requerido"
                errores = True

            if not precio.value.strip() or not re.match(r'^\d+(\.\d{1,2})?$', precio.value.strip()):
                precio.error_text = "Precio debe ser un número válido"
                errores = True

            if fecha_caducidad.value and not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_caducidad.value.strip()):
                fecha_caducidad.error_text = "Formato de fecha inválido (YYYY-MM-DD)"
                errores = True

            if not marca.value.strip():
                marca.error_text = "Marca requerida"
                errores = True

            if not unidad_medida.value.strip() or not unidad_medida.value.isalpha():
                unidad_medida.error_text = "Unidad de medida inválida (solo letras)"
                errores = True

            if errores:
                page.snack_bar = ft.SnackBar(content=ft.Text("❗ Revisa los campos marcados en rojo"))
                page.snack_bar.open = True
                page.update()
                return

            # Si pasa validación, guardar producto
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (Nombre, Precio, FechaCaducidad, Descripcion, Marca, UnidadMedida, CorteCaja_idCorteCaja) VALUES (%s, %s, %s, %s, %s, %s, 1)",
                (nombre.value.strip(), float(precio.value.strip()), int(fecha_caducidad.value.replace('-', '').strip()), descripcion.value.strip(), marca.value.strip(), unidad_medida.value.strip())
            )
            cursor.execute(
                "INSERT INTO productosstock (Nombre, Descripcion, Cantidad, CorteCaja_idCorteCaja) VALUES (%s, %s, %s, 1)",
                (nombre.value.strip(), descripcion.value.strip(), 0)
            )
            conn.commit()
            cursor.close()
            conn.close()

            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Producto agregado correctamente"))
            page.snack_bar.open = True
            mostrar_inventario(page)

        page.clean()
        page.add(
            ft.Column([
                ft.Text("Agregar Nuevo Producto", size=30, weight=ft.FontWeight.BOLD, color="#E71790"),
                nombre,
                precio,
                fecha_caducidad,
                descripcion,
                marca,
                unidad_medida,
                ft.Row([
                    ft.ElevatedButton("Guardar", on_click=guardar_producto, bgcolor="#E71790"),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_inventario(page), bgcolor="#62003c")
                ], alignment=ft.MainAxisAlignment.CENTER)
            ])
        )

    def volver_al_menu(page):
        # Aquí puedes redirigir al menú principal si lo tienes
        page.snack_bar = ft.SnackBar(content=ft.Text("Volviendo al menú principal..."))
        page.snack_bar.open = True













    def mostrar_entradas_salidas(e=None):
        page.clean()
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT Nombre, Descripcion FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()

        producto_options = [ft.dropdown.Option(prod[0]) for prod in productos] if productos else []

        # --- Funciones auxiliares ---
        def filtrar_numeros(e):
            valor = ''.join(c for c in e.control.value if c.isdigit())
            e.control.value = valor
            page.update()

        stock_actual_entrada = {"cantidad": 0}
        stock_actual_salida = {"cantidad": 0}

        def actualizar_cantidad_stock_entrada():
            if entrada_producto.value:
                conn = conectar_bd()
                cursor = conn.cursor()
                cursor.execute("SELECT Cantidad FROM productosstock WHERE Nombre = %s", (entrada_producto.value,))
                resultado = cursor.fetchone()
                cantidad = resultado[0] if resultado else 0
                stock_actual_entrada["cantidad"] = cantidad
                texto_cantidad_disponible_entrada.value = f"Cantidad actual: {cantidad}"
                cursor.close()
                conn.close()
                page.update()

        def actualizar_cantidad_stock_salida():
            if salida_producto.value:
                conn = conectar_bd()
                cursor = conn.cursor()
                cursor.execute("SELECT Cantidad FROM productosstock WHERE Nombre = %s", (salida_producto.value,))
                resultado = cursor.fetchone()
                cantidad = resultado[0] if resultado else 0
                stock_actual_salida["cantidad"] = cantidad
                texto_cantidad_disponible_salida.value = f"Cantidad disponible: {cantidad}"
                cursor.close()
                conn.close()
                page.update()

        # --- Widgets ---
        entrada_producto = ft.Dropdown(label="Seleccionar Producto", options=producto_options, width=300, on_change=lambda e: actualizar_cantidad_stock_entrada())
        entrada_cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER, width=300, on_change=filtrar_numeros)
        entrada_descripcion = ft.TextField(label="Descripción de Entrada", width=300)
        texto_cantidad_disponible_entrada = ft.Text("", size=16, color="#E71790")

        salida_producto = ft.Dropdown(label="Seleccionar Producto", options=producto_options, width=300, on_change=lambda e: actualizar_cantidad_stock_salida())
        salida_cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER, width=300, on_change=filtrar_numeros)
        salida_descripcion = ft.TextField(label="Motivo de Salida", width=300)
        texto_cantidad_disponible_salida = ft.Text("", size=16, color="#E71790")

        # --- Funciones de registrar entrada/salida ---
        def registrar_entrada(e):
            if not entrada_cantidad.value.isdigit() or int(entrada_cantidad.value) <= 0:
                page.snack_bar = ft.SnackBar(content=ft.Text("❗ Cantidad inválida para entrada"))
                page.snack_bar.open = True
                page.update()
                return

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

            actualizar_cantidad_stock_entrada()

            entrada_producto.value = ""
            entrada_cantidad.value = ""
            entrada_descripcion.value = ""

            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Entrada registrada con éxito"))
            page.snack_bar.open = True
            page.update()

        def registrar_salida(e):
            if not salida_cantidad.value.isdigit() or int(salida_cantidad.value) <= 0:
                page.snack_bar = ft.SnackBar(content=ft.Text("❗ Cantidad inválida para salida"))
                page.snack_bar.open = True
                page.update()
                return

            cantidad_salida = int(salida_cantidad.value)

            if cantidad_salida > stock_actual_salida["cantidad"]:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❗ No puedes retirar más de lo disponible. Stock actual: {stock_actual_salida['cantidad']}")
                )
                page.snack_bar.open = True
                page.update()
                return

            conn = conectar_bd()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO salidasproductos (Cantidad, FechaSalida, Detalle, CorteCaja_idCorteCaja) VALUES (%s, CURDATE(), %s, 1)",
                (cantidad_salida, salida_descripcion.value)
            )

            cursor.execute(
                "UPDATE productosstock SET Cantidad = Cantidad - %s WHERE Nombre = %s",
                (cantidad_salida, salida_producto.value)
            )

            conn.commit()
            cursor.close()
            conn.close()

            actualizar_cantidad_stock_salida()

            salida_producto.value = ""
            salida_cantidad.value = ""
            salida_descripcion.value = ""

            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Salida registrada con éxito"))
            page.snack_bar.open = True
            page.update()

        # --- Diseño corregido ---
        page.add(
            ft.Column([
                ft.Text("Gestión de Entradas y Salidas", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),

                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Registrar Entrada de Productos", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                            entrada_producto,
                            texto_cantidad_disponible_entrada,
                            entrada_cantidad,
                            entrada_descripcion,
                            ft.ElevatedButton("Registrar Entrada", on_click=registrar_entrada, bgcolor="#E71790", color="white")
                        ], spacing=8),
                        padding=15,
                        bgcolor="#2A2A2A",
                        border=ft.border.all(2, "#E71790"),
                        border_radius=12,
                        width=360,
                    ),

                    ft.Container(
                        content=ft.Column([
                            ft.Text("Registrar Salida de Productos", size=20, weight=ft.FontWeight.BOLD, color="#E71790"),
                            salida_producto,
                            texto_cantidad_disponible_salida,
                            salida_cantidad,
                            salida_descripcion,
                            ft.ElevatedButton("Registrar Salida", on_click=registrar_salida, bgcolor="#E71790", color="white")
                        ], spacing=8),
                        padding=15,
                        bgcolor="#2A2A2A",
                        border=ft.border.all(2, "#E71790"),
                        border_radius=12,
                        width=360,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=30),

                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white", width=200)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        )



        



#_----------------------------------------------------------------------------------------------------------------------------








    def mostrar_caja_chica(e=None):
        import flet as ft

        page.clean()

        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)

        # Obtener último corte actual
        cursor.execute("SELECT * FROM cortecaja ORDER BY idCorteCaja DESC LIMIT 1")
        corte = cursor.fetchone()
        dinero_actual = float(corte["DineroEnCaja"]) if corte else 0
        id_corte = corte["idCorteCaja"]

        # Cargar pedidos pendientes
        cursor.execute("SELECT * FROM generarpedido WHERE Estatus = 'Pedido Realizado'")
        pedidos = cursor.fetchall()

        cursor.close()
        conn.close()

        # Variables
        pedido_seleccionado = {"id": None, "total": 0.0, "producto": ""}
        total_a_pagar = ft.Text("Total: $0.00", size=20, color="white")
        monto_recibido_field = ft.TextField(
            label="Monto Recibido",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: validar_monto_recibido()
        )
        cambio_field = ft.Text("Cambio: $0.00", size=20, color="#00FF00")
        ayuda_label = ft.Text("", size=15)

        # Widgets de ingresos/egresos
        cantidad_movimiento = ft.TextField(
            label="Cantidad Movimiento",
            width=200,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        descripcion_movimiento = ft.TextField(
            label="Motivo del Movimiento",
            width=400
        )
        ayuda_movimiento = ft.Text("", size=15)

        tabla_pedidos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Cobrar")),
            ],
            rows=[]
        )

        # ------------------- FUNCIONES ----------------------

        # Validar monto recibido
        def validar_monto_recibido():
            monto = monto_recibido_field.value
            if not monto:
                ayuda_label.value = "Ingrese el monto recibido."
                ayuda_label.color = "orange"
                page.update()
                return

            if not re.match(r'^\d+(\.\d{1,2})?$', monto):
                ayuda_label.value = "❗ Solo números y máximo 2 decimales."
                ayuda_label.color = "red"
            else:
                ayuda_label.value = "✅ Monto válido."
                ayuda_label.color = "green"
            page.update()

        # Seleccionar pedido
        def seleccionar_pedido(pedido):
            pedido_seleccionado["id"] = pedido["IdGenerarPedido"]
            pedido_seleccionado["total"] = float(pedido["Total"])
            pedido_seleccionado["producto"] = pedido["Producto"]

            total_a_pagar.value = f"Total: ${pedido['Total']:.2f}"
            cambio_field.value = "Cambio: $0.00"
            monto_recibido_field.value = ""
            ayuda_label.value = ""
            page.update()

        # Confirmar cobro
        def confirmar_cobro(e):
            nonlocal dinero_actual

            if pedido_seleccionado["id"] is None:
                ayuda_label.value = "❗ Seleccione un pedido antes de cobrar."
                ayuda_label.color = "red"
                page.update()
                return

            if not monto_recibido_field.value:
                ayuda_label.value = "❗ Ingrese el monto recibido."
                ayuda_label.color = "red"
                page.update()
                return

            if not re.match(r'^\d+(\.\d{1,2})?$', monto_recibido_field.value):
                ayuda_label.value = "❗ Formato inválido."
                ayuda_label.color = "red"
                page.update()
                return

            recibido = float(monto_recibido_field.value)
            total = pedido_seleccionado["total"]

            if recibido < total:
                ayuda_label.value = "❗ Monto recibido menor al total."
                ayuda_label.color = "red"
                page.update()
                return

            cambio = recibido - total

            try:
                connc = conectar_bd()
                cursorc = connc.cursor(dictionary=True)

                # Actualizar pedido
                cursorc.execute("UPDATE generarpedido SET Estatus = 'Pagado' WHERE IdGenerarPedido = %s", (pedido_seleccionado["id"],))

                # Actualizar caja chica
                cursorc.execute("""
                    UPDATE cortecaja
                    SET DineroEnCaja = DineroEnCaja + %s, IngresoDia = IngresoDia + %s
                    WHERE idCorteCaja = %s
                """, (total, total, id_corte))

                # Insertar en recibospedidos
                # Antes de insertar el recibo
                nombre_completo = page.client_storage.get("nombre_completo")
                if not nombre_completo:
                    nombre_completo = "Empleado"

                cursorc.execute("""
                    INSERT INTO recibospedidos (Producto, Total, Fecha, Hora, Usuario)
                    VALUES (%s, %s, CURDATE(), CURTIME(), %s)
                """, (
                    pedido_seleccionado["producto"],
                    total,
                    nombre_completo  # <- ya seguro
                ))

                connc.commit()
                cursorc.close()
                connc.close()

                for row in tabla_pedidos.rows:
                    if row.cells[0].content.value == str(pedido_seleccionado["id"]):
                        tabla_pedidos.rows.remove(row)
                        break

                dinero_actual += total
                total_a_pagar.value = "Total: $0.00"
                monto_recibido_field.value = ""
                cambio_field.value = f"Cambio: ${cambio:.2f}"
                ayuda_label.value = "✅ Cobro realizado."
                ayuda_label.color = "green"
                pedido_seleccionado["id"] = None
                pedido_seleccionado["total"] = 0.0
                pedido_seleccionado["producto"] = ""

                page.update()

            except Exception as err:
                ayuda_label.value = f"❌ Error: {err}"
                ayuda_label.color = "red"
                page.update()

        # Confirmar movimiento (Ingreso/Egreso)
        def confirmar_movimiento(valor):
            nonlocal dinero_actual

            if not cantidad_movimiento.value or not descripcion_movimiento.value:
                ayuda_movimiento.value = "❗ Ingrese cantidad y motivo."
                ayuda_movimiento.color = "red"
                page.update()
                return

            if not re.match(r'^\d+(\.\d{1,2})?$', cantidad_movimiento.value):
                ayuda_movimiento.value = "❗ Solo números y punto decimal."
                ayuda_movimiento.color = "red"
                page.update()
                return

            cantidad = float(cantidad_movimiento.value)

            if valor == -1 and cantidad > dinero_actual:
                ayuda_movimiento.value = "❗ No puede retirar más dinero del que hay."
                ayuda_movimiento.color = "red"
                page.update()
                return

            try:
                connm = conectar_bd()
                cursorm = connm.cursor(dictionary=True)

                if valor == 1:
                    cursorm.execute("""
                        UPDATE cortecaja
                        SET DineroEnCaja = DineroEnCaja + %s, IngresoDia = IngresoDia + %s
                        WHERE idCorteCaja = %s
                    """, (cantidad, cantidad, id_corte))
                    dinero_actual += cantidad
                else:
                    cursorm.execute("""
                        UPDATE cortecaja
                        SET DineroEnCaja = DineroEnCaja - %s, EgresoDia = EgresoDia + %s
                        WHERE idCorteCaja = %s
                    """, (cantidad, cantidad, id_corte))
                    dinero_actual -= cantidad

                connm.commit()
                cursorm.close()
                connm.close()

                cantidad_movimiento.value = ""
                descripcion_movimiento.value = ""
                ayuda_movimiento.value = "✅ Movimiento registrado correctamente."
                ayuda_movimiento.color = "green"

                page.update()

            except Exception as err:
                ayuda_movimiento.value = f"❌ Error: {err}"
                ayuda_movimiento.color = "red"
                page.update()

        # ------------------------------------------------------

        # Insertar pedidos
        for pedido in pedidos:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(pedido["IdGenerarPedido"]))),
                    ft.DataCell(ft.Text(pedido["Producto"])),
                    ft.DataCell(ft.Text(f"${float(pedido['Total']):.2f}")),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.PAID,
                            tooltip="Cobrar",
                            icon_color="green",
                            on_click=lambda e, p=pedido: seleccionar_pedido(p)
                        )
                    )
                ]
            )
            tabla_pedidos.rows.append(fila)

        # Layout principal
        page.add(
            ft.Column([
                ft.Row([
                    ft.Text("💸 Caja Chica", size=30, weight=ft.FontWeight.BOLD, color="#E71790"),
                    ft.Text(f"🪙 Dinero en caja: ${dinero_actual:.2f}", size=20, color="white"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                total_a_pagar,
                monto_recibido_field,
                ayuda_label,
                cambio_field,
                ft.ElevatedButton("Confirmar Cobro", on_click=confirmar_cobro, bgcolor="green", color="white"),
                ft.Divider(),
                ft.Text("Pedidos Pendientes:", size=22, weight=ft.FontWeight.BOLD, color="#E71790"),
                ft.Container(
                    content=tabla_pedidos,
                    height=300,
                    bgcolor="#1E1E1E",
                    border_radius=10,
                    padding=10,
                    expand=True
                ),
                ft.Divider(),
                ft.Text("Ingresos/Egresos Manuales:", size=22, weight=ft.FontWeight.BOLD, color="#E71790"),
                cantidad_movimiento,
                descripcion_movimiento,
                ayuda_movimiento,
                ft.Row([
                    ft.ElevatedButton("Registrar Ingreso", on_click=lambda e: confirmar_movimiento(1), bgcolor="blue", color="white"),
                    ft.ElevatedButton("Registrar Egreso", on_click=lambda e: confirmar_movimiento(-1), bgcolor="red", color="white")
                ], spacing=20),
                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
            ], spacing=15, expand=True, scroll=ft.ScrollMode.ALWAYS)
        )



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="Nombre de usuario para la sesión")
    parser.add_argument("--tipo", help="Tipo de usuario (Empleado o Cliente")
    args = parser.parse_args()

ft.app(target=main)
