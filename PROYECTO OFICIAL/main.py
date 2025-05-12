import flet as ft
from db_config import conectar_bd
import subprocess
import os
from datetime import datetime
from flet import Animation as anim
import re

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="Nombre de usuario para la sesión")
    parser.add_argument("--tipo", help="Tipo de usuario (Empleado o Cliente)")
    args = parser.parse_args()
    
    ft.app(target=lambda page: main(page, args.username, args.tipo))
    
def obtener_tipo_usuario(nombre_usuario):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Verificar si es empleado
        cursor.execute("""
            SELECT e.Nombre, e.Apellido 
            FROM Empleado e
            JOIN Usuario u ON e.Usuario_IdUsuario = u.IdUsuario
            WHERE u.NombreUsuario = %s
        """, (nombre_usuario,))
        empleado = cursor.fetchone()
        if empleado:
            return "Empleado", f"{empleado[0]} {empleado[1]}"
        
        # Verificar si es cliente
        cursor.execute("""
            SELECT c.Nombre, c.Apellido 
            FROM Cliente c
            JOIN Usuario u ON c.Usuario_IdUsuario = u.IdUsuario
            WHERE u.NombreUsuario = %s
        """, (nombre_usuario,))
        cliente = cursor.fetchone()
        if cliente:
            return "Cliente", f"{cliente[0]} {cliente[1]}"
        
        return "Desconocido", nombre_usuario
    finally:
        cursor.close()
        conn.close()

def main(page: ft.Page, nombre_usuario=None, tipo_usuario=None):
    page.title = "Punto de Venta"
    page.bgcolor = "#1C1C1C"
    page.theme = ft.Theme(font_family="Poppins")
    page.padding = 10
    tipo_usuario, nombre_completo = obtener_tipo_usuario(nombre_usuario) if nombre_usuario else ("Desconocido", "Invitado")

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
                        content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100, color="#E71790"),
                        alignment=ft.alignment.center
                    ),
                    ft.Text(nombre_usuario, size=20, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
                    ft.Text(tipo_usuario, size=16, color="#E71790", text_align=ft.TextAlign.CENTER),
                    ft.Divider(color="white"),
                    
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ACCOUNT_BOX),
                        title=ft.Text("Mi Información"),
                        on_click=lambda e: mostrar_informacion_usuario(page, nombre_usuario, tipo_usuario)
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

    def mostrar_informacion_usuario(page, nombre_usuario, tipo_usuario):
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        
        try:
            if tipo_usuario == "Empleado":
                cursor.execute("""
                    SELECT e.*, u.NombreUsuario 
                    FROM Empleado e
                    JOIN Usuario u ON e.Usuario_IdUsuario = u.IdUsuario
                    WHERE u.NombreUsuario = %s
                """, (nombre_usuario,))
                info = cursor.fetchone()
                
                contenido = [
                    ft.Text("Información del Empleado", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                    ft.Text(f"Nombre: {info['Nombre']} {info['Apellido']}", size=16),
                    ft.Text(f"Teléfono: {info['Telefono']}", size=16),
                    ft.Text(f"Correo: {info['Correo']}", size=16),
                    ft.Text(f"Usuario: {info['NombreUsuario']}", size=16)
                ]
                
            elif tipo_usuario == "Cliente":
                cursor.execute("""
                    SELECT c.*, u.NombreUsuario 
                    FROM Cliente c
                    JOIN Usuario u ON c.Usuario_IdUsuario = u.IdUsuario
                    WHERE u.NombreUsuario = %s
                """, (nombre_usuario,))
                info = cursor.fetchone()
                
                contenido = [
                    ft.Text("Información del Cliente", size=24, weight=ft.FontWeight.BOLD, color="#E71790"),
                    ft.Text(f"Nombre: {info['Nombre']} {info['Apellido']}", size=16),
                    ft.Text(f"Teléfono: {info['Telefono']}", size=16),
                    ft.Text(f"Correo: {info['Correo']}", size=16),
                    ft.Text(f"Usuario: {info['NombreUsuario']}", size=16)
                ]
                
            else:
                contenido = [ft.Text("Información no disponible", size=16)]
                
            page.clean()
            page.add(
                ft.Column([
                    ft.Container(
                        content=ft.Column(contenido, spacing=10),
                        padding=20,
                        bgcolor="#2A2A2A",
                        border_radius=10,
                        width=400
                    ),
                    ft.ElevatedButton("Volver", on_click=lambda e: mostrar_inicio(page), bgcolor="#5D0E41", color="white")
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            )
            
        except Exception as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(err)}"))
            page.snack_bar.open = True
        finally:
            cursor.close()
            conn.close()
            page.update()


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
                        ft.Text(f"👤 Usuario: {nombre_completo}", size=18, color="#E71790"),
                    ], spacing=10),
                    padding=20,
                    bgcolor="#2A2A2A",
                    border_radius=10,
                    width=400
                ),
                ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
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



        





    def mostrar_caja_chica(e=None):
        page.clean()

        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM cortecaja ORDER BY idCorteCaja DESC LIMIT 1")
        corte = cursor.fetchone()

        dinero_actual = corte["DineroEnCaja"] if corte else 0

        cursor.execute("SELECT IdGenerarPedido, Producto FROM generarpedido WHERE Estatus = 'Pedido Realizado'")
        pedidos = cursor.fetchall()
        cursor.close()
        conn.close()

        # --- Sidebar de cobro fijo ---
        producto_seleccionado = ft.Text("")
        total_a_pagar = ft.Text("")
        monto_recibido_field = ft.TextField(label="Monto recibido", keyboard_type=ft.KeyboardType.NUMBER)
        cambio_text = ft.Text("Cambio: $0.00", size=16, color="white")
        id_pedido_actual = {"id": None}

        sidebar = ft.Container(
            content=ft.Column([
                ft.Text("Cobro de Pedido", size=24, weight="bold", color="#E71790"),
                producto_seleccionado,
                total_a_pagar,
                monto_recibido_field,
                cambio_text,
                ft.ElevatedButton("Confirmar Cobro", on_click=lambda e: confirmar_cobro()),
            ], spacing=10),
            width=300,
            bgcolor="#2A2A2A",
            padding=20,
            border_radius=10
        )

        # --- Área de pedidos ---
        tabla_pedidos = ft.ListView(spacing=10, padding=10, expand=True)

        def actualizar_cambio(e):
            try:
                recibido = float(monto_recibido_field.value)
                total = float(total_a_pagar.value.replace("Total: $", ""))
                cambio = recibido - total
                if cambio >= 0:
                    cambio_text.value = f"Cambio: ${cambio:.2f}"
                else:
                    cambio_text.value = "Monto insuficiente"
            except:
                cambio_text.value = "Monto inválido"
            page.update()

        monto_recibido_field.on_change = actualizar_cambio

        # --- Función para seleccionar pedido ---
        def seleccionar_pedido(pedido):
            nombre_limpio = pedido["Producto"].split("-")[0].strip()
            conn2 = conectar_bd()
            cursor2 = conn2.cursor(dictionary=True)
            cursor2.execute("SELECT Precio FROM productos WHERE Nombre LIKE %s", (f"%{nombre_limpio}%",))
            resultado = cursor2.fetchone()
            cursor2.close()
            conn2.close()

            if resultado:
                producto_seleccionado.value = f"Producto: {pedido['Producto']}"
                total_a_pagar.value = f"Total: ${resultado['Precio']:.2f}"
                monto_recibido_field.value = ""
                cambio_text.value = "Cambio: $0.00"
                id_pedido_actual["id"] = pedido["IdGenerarPedido"]
                page.update()
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("❌ No se encontró precio"))
                page.snack_bar.open = True
                page.update()

        # --- Función para confirmar el cobro ---
        def confirmar_cobro():
            if id_pedido_actual["id"] is None:
                page.snack_bar = ft.SnackBar(content=ft.Text("❗ No hay pedido seleccionado"))
                page.snack_bar.open = True
                return

            try:
                recibido = float(monto_recibido_field.value)
                total = float(total_a_pagar.value.replace("Total: $", ""))
            except:
                page.snack_bar = ft.SnackBar(content=ft.Text("❗ Datos inválidos"))
                page.snack_bar.open = True
                return

            if recibido < total:
                page.snack_bar = ft.SnackBar(content=ft.Text("❗ Monto insuficiente"))
                page.snack_bar.open = True
                return

            # Registrar cobro
            conn3 = conectar_bd()
            cursor3 = conn3.cursor()
            cursor3.execute("UPDATE generarpedido SET Estatus = 'Pagado' WHERE IdGenerarPedido = %s", (id_pedido_actual["id"],))
            cursor3.execute("""
                INSERT INTO recibos (Producto, Total, Fecha, Hora, Usuario)
                VALUES (%s, CURDATE(), CURTIME(), 'admin')
            """, (producto_seleccionado.value.replace("Producto: ", ""), total))
            conn3.commit()
            cursor3.close()
            conn3.close()

            page.snack_bar = ft.SnackBar(content=ft.Text("✅ Cobro exitoso"))
            page.snack_bar.open = True
            mostrar_caja_chica()

        # --- Botón de ingresos/egresos ---
        def abrir_ingresos_egresos(e):
            mostrar_ingresos_egresos()

        boton_ingresos_egresos = ft.ElevatedButton("Ingresos / Egresos", on_click=abrir_ingresos_egresos, bgcolor="#5D0E41", color="white", width=200)

        for pedido in pedidos:
            tabla_pedidos.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"ID: {pedido['IdGenerarPedido']}", size=16, color="white"),
                        ft.Text(pedido["Producto"], size=16, color="#E71790", expand=True),
                        ft.ElevatedButton("Cobrar", on_click=lambda e, p=pedido: seleccionar_pedido(p), bgcolor="#28A745", color="white"),
                    ]),
                    padding=10,
                    bgcolor="#1C1C1C",
                    border_radius=10
                )
            )

        page.add(
            ft.Row([
                sidebar,
                ft.Container(
                    content=ft.Column([
                        ft.Text("Caja Chica", size=26, weight=ft.FontWeight.BOLD, color="#E71790"),
                        ft.Text(f"Dinero en caja: ${dinero_actual:.2f}", size=18, color="white"),
                        tabla_pedidos,
                        boton_ingresos_egresos,
                        ft.ElevatedButton("Volver", on_click=mostrar_inicio, bgcolor="#5D0E41", color="white", width=200)
                    ], spacing=20),
                    expand=True,
                    padding=20
                )
            ])
        )
        
    def mostrar_ingresos_egresos(e=None):
        page.clean()

        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)

        # Crear tabla ingresos_egresos si no existe (opcional)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingresos_egresos (
            idMovimiento INT AUTO_INCREMENT PRIMARY KEY,
            TipoMovimiento VARCHAR(20),
            Monto DECIMAL(10,2),
            Descripcion TEXT,
            Fecha DATE,
            Hora TIME
        )
        """)
        conn.commit()

        cursor.execute("SELECT * FROM ingresos_egresos ORDER BY Fecha DESC, Hora DESC")
        movimientos = cursor.fetchall()
        cursor.close()
        conn.close()

        tabla_movimientos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Hora")),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(mov["TipoMovimiento"])),
                    ft.DataCell(ft.Text(f"${mov['Monto']:.2f}")),
                    ft.DataCell(ft.Text(mov["Descripcion"])),
                    ft.DataCell(ft.Text(str(mov["Fecha"]))),
                    ft.DataCell(ft.Text(str(mov["Hora"]))),
                ]) for mov in movimientos
            ]
        )

        # --- Funciones para agregar movimientos ---
        def abrir_ventana_ingreso():
            pedir_contraseña(tipo="Ingreso")

        def abrir_ventana_egreso():
            pedir_contraseña(tipo="Egreso")

        def pedir_contraseña(tipo):
            contraseña_field = ft.TextField(label="Contraseña Admin", password=True, can_reveal_password=True)

            def validar_contraseña(e):
                if contraseña_field.value == "admin":
                    page.dialog.open = False
                    page.update()
                    abrir_formulario_movimiento(tipo)
                else:
                    page.snack_bar = ft.SnackBar(content=ft.Text("❌ Contraseña incorrecta"))
                    page.snack_bar.open = True

            page.dialog = ft.AlertDialog(
                title=ft.Text(f"Validar para {tipo}"),
                content=contraseña_field,
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
                    ft.TextButton("Aceptar", on_click=validar_contraseña),
                ]
            )
            page.dialog.open = True
            page.update()

        def cerrar_dialogo():
            page.dialog.open = False
            page.update()

        def abrir_formulario_movimiento(tipo):
            monto_field = ft.TextField(label="Monto", keyboard_type=ft.KeyboardType.NUMBER)
            descripcion_field = ft.TextField(label="Descripción")

            def guardar_movimiento(e):
                try:
                    monto = float(monto_field.value)
                except:
                    page.snack_bar = ft.SnackBar(content=ft.Text("❗ Monto inválido"))
                    page.snack_bar.open = True
                    return

                conn2 = conectar_bd()
                cursor2 = conn2.cursor()
                cursor2.execute("""
                    INSERT INTO ingresos_egresos (TipoMovimiento, Monto, Descripcion, Fecha, Hora)
                    VALUES (%s, %s, %s, CURDATE(), CURTIME())
                """, (tipo, monto, descripcion_field.value))
                conn2.commit()
                cursor2.close()
                conn2.close()

                page.dialog.open = False
                page.snack_bar = ft.SnackBar(content=ft.Text(f"✅ {tipo} registrado"))
                page.snack_bar.open = True
                mostrar_ingresos_egresos()

            page.dialog = ft.AlertDialog(
                title=ft.Text(f"Agregar {tipo}"),
                content=ft.Column([
                    monto_field,
                    descripcion_field
                ], spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo()),
                    ft.TextButton("Guardar", on_click=guardar_movimiento),
                ]
            )
            page.dialog.open = True
            page.update()

        page.add(
            ft.Column([
                ft.Text("Historial de Ingresos y Egresos", size=26, weight="bold", color="#E71790"),
                ft.Row([
                    ft.ElevatedButton("Agregar Ingreso", on_click=lambda e: abrir_ventana_ingreso(), bgcolor="#28A745", color="white"),
                    ft.ElevatedButton("Agregar Egreso", on_click=lambda e: abrir_ventana_egreso(), bgcolor="#D32F2F", color="white"),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Container(content=tabla_movimientos, expand=True, bgcolor="#1C1C1C", border_radius=10, padding=10),
                ft.ElevatedButton("Volver", on_click=mostrar_caja_chica, bgcolor="#5D0E41", color="white", width=200)
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
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
