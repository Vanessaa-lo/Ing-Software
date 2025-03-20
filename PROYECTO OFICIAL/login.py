import flet as ft
import mysql.connector
from db_config import conectar_bd

def main(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.bgcolor = "#1A1A1A"
    page.padding = 20
    header = ft.Container(
            content=ft.Text("Punto de Venta", size=24, weight=ft.FontWeight.BOLD, color="white"),
            bgcolor="#62003c",
            padding=15,
            alignment=ft.alignment.center_left,
            animate=ft.animation.Animation(400, "ease_in_out")
        )


    def iniciar_sesion(e):
        NombreUsuario = login_username.value.strip()
        Contraseña = login_password.value.strip()
        
        if not NombreUsuario or not Contraseña:
            page.snack_bar = ft.SnackBar(content=ft.Text("Todos los campos son obligatorios."))
            page.snack_bar.open = True
            page.update()
            return
        
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM Usuario WHERE NombreUsuario = %s AND Contraseña = %s", (NombreUsuario, Contraseña))
            usuario = cursor.fetchone()
            if usuario:
                page.snack_bar = ft.SnackBar(content=ft.Text("Inicio de sesión exitoso!"))
                page.snack_bar.open = True
                page.update()
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("Usuario o contraseña incorrectos"))
                page.snack_bar.open = True
        except mysql.connector.Error as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {err}"))
            page.snack_bar.open = True
        finally:
            cursor.close()
            conn.close()
            page.update()
    
    def toggle_password_visibility(e):
        login_password.password = not login_password.password
        eye_icon.icon = "visibility_off" if login_password.password else "visibility"
        page.update()

    def seleccionar_tipo_usuario(e):
        page.clean()
        page.add(header)
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Selecciona el tipo de usuario", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.ElevatedButton("Cliente", on_click=registro_cliente, bgcolor="#e10080", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.ElevatedButton("Empleado", on_click=registro_empleado, bgcolor="#e10080", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.ElevatedButton("Volver", on_click=volver_al_login, bgcolor="#62003c", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=20,
                bgcolor="#000000",
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
                animate=ft.animation.Animation(400, "ease_in_out")
            )
        )

    login_username = ft.TextField(
        label="Usuario",
        width=300,
        bgcolor="#333",
        color="white",
        prefix_icon=ft.icons.PERSON,
        border_radius=10
    )

    eye_icon = ft.IconButton(icon="visibility", on_click=toggle_password_visibility)
    login_password = ft.TextField(
        label="Contraseña",
        width=300,
        password=True,
        bgcolor="#333",
        color="white",
        prefix_icon=ft.icons.LOCK,
        border_radius=10,
        suffix=eye_icon
    )

    # 🔹 Contenedor del login con animaciones y sombra
    login_section = ft.Container(
        content=ft.Column([
            ft.Text("Pantalla de Login", size=24, weight=ft.FontWeight.BOLD, color="#e10080"),
            login_username,
            login_password,
            ft.ElevatedButton("Iniciar Sesión", on_click=iniciar_sesion, bgcolor="#e10080", color="white", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
            ft.ElevatedButton("Registrarse", on_click=seleccionar_tipo_usuario, bgcolor="#62003c", color="white", 
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        bgcolor="#000000",
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
        animate=ft.animation.Animation(400, "ease_in_out")
    )

    def toggle_password_visibility(e, password_field, eye_icon):
        password_field.password = not password_field.password
        eye_icon.icon = "visibility_off" if password_field.password else "visibility"
        page.update()

    def registro_cliente(e):
        eye_icon_client = ft.IconButton(icon="visibility", on_click=lambda e: toggle_password_visibility(e, register_client_password, eye_icon_client))
        page.clean()
        page.add(header)
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Registro de Cliente", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    register_client_name,
                    register_client_lastname,
                    register_client_phone,
                    register_client_email,
                    register_client_username,
                    ft.Row([register_client_password, eye_icon_client]),
                    ft.ElevatedButton("Registrar Cliente", on_click=guardar_cliente, bgcolor="#e10080", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.ElevatedButton("Volver", on_click=seleccionar_tipo_usuario, bgcolor="#62003c", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=20,
                bgcolor="#000000",
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
                animate=ft.animation.Animation(400, "ease_in_out")
            )
        )
    
    def registro_empleado(e):
        eye_icon_employee = ft.IconButton(icon="visibility", on_click=lambda e: toggle_password_visibility(e, register_employee_password, eye_icon_employee))
        page.clean()
        page.add(header)
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Registro de Empleado", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    register_employee_name,
                    register_employee_lastname,
                    register_employee_phone,
                    register_employee_email,
                    register_employee_username,
                    ft.Row([register_employee_password, eye_icon_employee]),
                    ft.ElevatedButton("Registrar Empleado", on_click=guardar_empleado, bgcolor="#e10080", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))),
                    ft.ElevatedButton("Volver", on_click=seleccionar_tipo_usuario, bgcolor="#62003c", color="white", 
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=20,
                bgcolor="#000000",
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
                animate=ft.animation.Animation(400, "ease_in_out")
            )
        )

    def guardar_cliente(e):
        NombreUsuario = register_client_username.value.strip()
        Contraseña = register_client_password.value.strip()
        Nombre = register_client_name.value.strip()
        Apellido = register_client_lastname.value.strip()
        Telefono = register_client_phone.value.strip()
        Correo = register_client_email.value.strip()
        
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Usuario (NombreUsuario, Contraseña) VALUES (%s, %s)", (NombreUsuario, Contraseña))
            user_id = cursor.lastrowid
            cursor.execute("INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario) VALUES (%s, %s, %s, %s, %s)", (Nombre, Apellido, Telefono, Correo, user_id))
            conn.commit()
            page.snack_bar = ft.SnackBar(content=ft.Text("Cliente registrado correctamente!"))
            page.snack_bar.open = True
            volver_al_login(None)
        except mysql.connector.Error as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {err}"))
            page.snack_bar.open = True
        finally:
            cursor.close()
            conn.close()
            page.update()

    def guardar_empleado(e):
        NombreUsuario = register_employee_username.value.strip()
        Contraseña = register_employee_password.value.strip()
        Nombre = register_employee_name.value.strip()
        Apellido = register_employee_lastname.value.strip()
        Telefono = register_employee_phone.value.strip()
        Correo = register_employee_email.value.strip()
        
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Usuario (NombreUsuario, Contraseña) VALUES (%s, %s)", (NombreUsuario, Contraseña))
            user_id = cursor.lastrowid
            cursor.execute("INSERT INTO Empleado (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario) VALUES (%s, %s, %s, %s, %s)", (Nombre, Apellido, Telefono, Correo, user_id))
            conn.commit()
            page.snack_bar = ft.SnackBar(content=ft.Text("Empleado registrado correctamente!"))
            page.snack_bar.open = True
            volver_al_login(None)
        except mysql.connector.Error as err:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error en la base de datos: {err}"))
            page.snack_bar.open = True
        finally:
            cursor.close()
            conn.close()
            page.update()

    def volver_al_login(e):
        page.clean()  # Limpia la página antes de agregar el diseño mejorado
        page.add(header)  # Mantiene el encabezado
        page.add(ft.Container(content=login_section, alignment=ft.alignment.center))  # Agrega la sección de login con el diseño aplicado


    login_username = ft.TextField(label="Usuario", width=300)
    login_password = ft.TextField(label="Contraseña", width=300, password=True)
    register_client_name = ft.TextField(label="Nombre Cliente", width=300)
    register_client_lastname = ft.TextField(label="Apellido Cliente", width=300)
    register_client_phone = ft.TextField(label="Teléfono Cliente", width=300)
    register_client_email = ft.TextField(label="Correo Cliente", width=300)
    register_client_username = ft.TextField(label="Nombre de Usuario", width=300)
    register_client_password = ft.TextField(label="Contraseña", width=300, password=True)
    register_employee_name = ft.TextField(label="Nombre Empleado", width=300)
    register_employee_lastname = ft.TextField(label="Apellido Empleado", width=300)
    register_employee_phone = ft.TextField(label="Teléfono Empleado", width=300)
    register_employee_email = ft.TextField(label="Correo Empleado", width=300)
    register_employee_username = ft.TextField(label="Nombre de Usuario", width=300)
    register_employee_password = ft.TextField(label="Contraseña", width=300, password=True)

    volver_al_login(None)

ft.app(target=main)
