
import flet as ft
import mysql.connector
import subprocess
import os
import re
import hashlib
from db_config import conectar_bd
from flet import Animation as anim


def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def limitar_telefono(e, field):
    valor = ''.join(filter(str.isdigit, field.value))
    field.value = valor
    if len(valor) < 10:
        field.error_text = "Teléfono inválido: se requieren 10 dígitos"
    elif len(valor) > 10:
        field.error_text = "Teléfono inválido: máximo 10 dígitos"
    else:
        field.error_text = ""
    e.page.update()

def limitar_contraseña(e, field):
    if len(field.value) > 20:
        field.value = field.value[:20]
        field.error_text = "Máximo 20 caracteres"
    else:
        field.error_text = ""
    e.page.update()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def main(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.bgcolor = "#1A1A1A"
    page.padding = 20

    header = ft.Container(
        content=ft.Text("Punto de Venta", size=24, weight=ft.FontWeight.BOLD, color="white"),
        bgcolor="#62003c",
        padding=15,
        alignment=ft.alignment.center_left,
        animate=ft.Animation(400, "ease_in_out")
    )

    def mostrar_mensaje(texto, color):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto, color="white"),
            bgcolor="#4CAF50" if color == "verde" else "#F44336",
            duration=3000
        )
        page.snack_bar.open = True
        page.update()

    def iniciar_sesion(e):
        NombreUsuario = login_username.value.strip()
        Contraseña = login_password.value.strip()
        if not NombreUsuario or not Contraseña:
            mostrar_mensaje("Todos los campos son obligatorios", "rojo")
            return

        try:
            conn = conectar_bd()
            print("Conexión exitosa a la base de datos")
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario WHERE NombreUsuario = %s AND Contraseña = %s",
                           (NombreUsuario, hash_password(Contraseña)))
            usuario = cursor.fetchone()
            if usuario:
                mostrar_mensaje("Inicio de sesión exitoso!", "verde")
                tipo_usuario = obtener_tipo_usuario(NombreUsuario)

                if tipo_usuario == "Empleado":
                    subprocess.Popen(["python", "main.py", f"--username={NombreUsuario}", f"--tipo={tipo_usuario}"])
                elif tipo_usuario == "Cliente":
                    subprocess.Popen(["python", "menu.py", f"--username={NombreUsuario}", f"--tipo={tipo_usuario}"])

                else:
                    mostrar_mensaje("Tipo de usuario desconocido", "rojo")
                    return
                os._exit(0)
            else:
                mostrar_mensaje("Usuario o contraseña incorrectos", "rojo")
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            mostrar_mensaje(f"Error de conexión: {err}", "rojo")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
                
    def obtener_tipo_usuario(nombre_usuario):
        conn = conectar_bd()
        cursor = conn.cursor()

        try:
            # Verificar si es Empleado
            cursor.execute("""
                SELECT e.IdEmpleado 
                FROM Empleado e
                JOIN Usuario u ON e.Usuario_IdUsuario = u.IdUsuario
                WHERE u.NombreUsuario = %s
            """, (nombre_usuario,))
            if cursor.fetchone():
                return "Empleado"

            # Verificar si es Cliente
            cursor.execute("""
                SELECT c.IdCliente
                FROM Cliente c
                JOIN Usuario u ON c.Usuario_IdUsuario = u.IdUsuario
                WHERE u.NombreUsuario = %s
            """, (nombre_usuario,))
            if cursor.fetchone():
                return "Cliente"

            return "Desconocido"

        finally:
            cursor.close()
            conn.close()


    def toggle_password_visibility(e):
        login_password.password = not login_password.password
        eye_icon.icon = "visibility_off" if login_password.password else "visibility"
        page.update()

    def volver_al_login(e=None):
        login_username.value = ""
        login_password.value = ""
        page.clean()
        page.add(header)
        page.add(ft.Container(content=login_section, alignment=ft.alignment.center))

    def seleccionar_tipo_usuario(e=None):
        page.clean()
        page.add(header)
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Selecciona el tipo de usuario", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    ft.ElevatedButton("Cliente", on_click=lambda e: registro_usuario("cliente"), bgcolor="#e10080", color="white"),
                    ft.ElevatedButton("Empleado", on_click=lambda e: registro_usuario("empleado"), bgcolor="#e10080", color="white"),
                    ft.ElevatedButton("Volver", on_click=volver_al_login, bgcolor="#62003c", color="white")
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=20,
                bgcolor="#000000",
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
                animate=ft.Animation(400, "ease_in_out")
            )
        )

    def registro_usuario(tipo):
        campos = {
            "nombre": ft.TextField(label=f"Nombre {tipo.title()}", width=300),
            "apellido": ft.TextField(label=f"Apellido {tipo.title()}", width=300),
            "telefono": ft.TextField(label=f"Teléfono {tipo.title()}", width=300, hint_text="10 dígitos"),
            "correo": ft.TextField(label=f"Correo {tipo.title()}", width=300, hint_text="ejemplo@email.com"),
            "usuario": ft.TextField(label="Nombre de Usuario", width=300),
            "contraseña": ft.TextField(label="Contraseña", width=300, password=True)
        }

        campos['telefono'].on_change = lambda e: limitar_telefono(e, campos['telefono'])
        campos['contraseña'].suffix = ft.IconButton(icon="visibility", on_click=lambda e: toggle_password(campos['contraseña'], e))

        def toggle_password(field, e):
            field.password = not field.password
            e.control.icon = "visibility_off" if field.password else "visibility"
            page.update()

        def guardar_usuario(e):
            error = False
            for key, campo in campos.items():
                if not campo.value.strip():
                    campo.error_text = "Este campo es obligatorio"
                    error = True
                else:
                    campo.error_text = ""

            if not validar_email(campos['correo'].value):
                campos['correo'].error_text = "Correo inválido"
                error = True

            if len(campos['telefono'].value) != 10:
                campos['telefono'].error_text = "Teléfono inválido: se requieren 10 dígitos"
                error = True

            page.update()
            if error:
                return

            try:
                conn = conectar_bd()
                print("Conexión exitosa a la base de datos")
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM Usuario WHERE NombreUsuario = %s", (campos['usuario'].value,))
                if cursor.fetchone():
                    campos['usuario'].error_text = "Nombre de usuario ya existe"
                    page.update()
                    return

                cursor.execute("SELECT 1 FROM Cliente WHERE Correo = %s UNION SELECT 1 FROM Empleado WHERE Correo = %s",
                               (campos['correo'].value, campos['correo'].value))
                if cursor.fetchone():
                    campos['correo'].error_text = "Este correo ya está registrado"
                    page.update()
                    return

                cursor.execute("INSERT INTO Usuario (NombreUsuario, Contraseña) VALUES (%s, %s)",
                               (campos['usuario'].value, hash_password(campos['contraseña'].value)))
                id_usuario = cursor.lastrowid

                if tipo == "cliente":
                    cursor.execute("INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario) VALUES (%s, %s, %s, %s, %s)",
                                   (campos['nombre'].value, campos['apellido'].value, campos['telefono'].value, campos['correo'].value, id_usuario))
                else:
                    cursor.execute("INSERT INTO Empleado (Nombre, Apellido, Telefono, Correo, Usuario_IdUsuario) VALUES (%s, %s, %s, %s, %s)",
                                   (campos['nombre'].value, campos['apellido'].value, campos['telefono'].value, campos['correo'].value, id_usuario))

                conn.commit()
                mostrar_mensaje(f"{tipo.title()} registrado correctamente!", "verde")
                volver_al_login()

            except mysql.connector.Error as err:
                print(f"Error en la base de datos: {err}")
                mostrar_mensaje(f"Error en la base de datos: {err}", "rojo")
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'conn' in locals():
                    conn.close()

        page.clean()
        page.add(header)
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Registro de {tipo.title()}", size=24, weight=ft.FontWeight.BOLD, color="white"),
                    *campos.values(),
                    ft.ElevatedButton("Registrar", on_click=guardar_usuario, bgcolor="#e10080", color="white"),
                    ft.ElevatedButton("Volver", on_click=seleccionar_tipo_usuario, bgcolor="#62003c", color="white")
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                padding=20,
                bgcolor="#000000",
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
                animate=ft.Animation(400, "ease_in_out")
            )
        )

    login_username = ft.TextField(label="Usuario", width=300, bgcolor="#333", color="white", prefix_icon=ft.Icons.PERSON, border_radius=10)
    eye_icon = ft.IconButton(icon="visibility", on_click=toggle_password_visibility)
    login_password = ft.TextField(label="Contraseña", width=300, password=True, bgcolor="#333", color="white", prefix_icon=ft.Icons.LOCK, border_radius=10, suffix=eye_icon)

    login_section = ft.Container(
        content=ft.Column([
            ft.Text("Pantalla de Login", size=24, weight=ft.FontWeight.BOLD, color="#e10080"),
            login_username,
            login_password,
            ft.ElevatedButton("Iniciar Sesión", on_click=iniciar_sesion, bgcolor="#e10080", color="white"),
            ft.ElevatedButton("Registrarse", on_click=lambda e: seleccionar_tipo_usuario(), bgcolor="#62003c", color="white")
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        bgcolor="#000000",
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, spread_radius=2, color="#444"),
        animate=ft.Animation(400, "ease_in_out")
    )

    volver_al_login()

ft.app(target=main)
