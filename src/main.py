import flet as ft
from model.user import Usuario

def main(page: ft.Page):
    # --- Configuración General ---
    page.title = "To-Do List TDD"
    page.window_width = 450
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.DARK
    
    # --- CENTRADO GENERAL ---
    page.vertical_alignment = ft.MainAxisAlignment.CENTER       
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER    

    # ---------------------------------------------------------
    # VISTA 3: DASHBOARD (Pantalla Principal)
    # ---------------------------------------------------------
    def mostrar_dashboard(usuario_objeto):
        # Recibimos 'usuario_objeto' que contiene todos los datos (nombre, apellido, etc.)
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START 
        
        barra_superior = ft.Row(
            [
                ft.Text("Mis Tareas", size=20, weight="bold"),
                ft.TextButton(
                    "Salir", 
                    style=ft.ButtonStyle(color="red"),
                    tooltip="Cerrar Sesión",
                    on_click=lambda e: mostrar_login()
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # --- AQUÍ USAMOS LOS NOMBRES DEL USUARIO ---
        nombre_completo = f"{usuario_objeto.nombre} {usuario_objeto.apellido}"
        
        mensaje = ft.Text(f"Hola, {nombre_completo}", size=18, color="blue", weight="bold")
        pendiente = ft.Text("Tus tareas aparecerán aquí...", italic=True)

        page.add(
            ft.Column(
                [barra_superior, ft.Divider(), mensaje, pendiente],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    # ---------------------------------------------------------
    # VISTA 2: PANTALLA DE REGISTRO
    # ---------------------------------------------------------
    def mostrar_registro(e=None):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        
        titulo = ft.Text("Crear Cuenta", size=24, weight="bold")
        
        nombre = ft.TextField(label="Nombres", width=300, border_radius=10)
        apellido = ft.TextField(label="Apellidos", width=300, border_radius=10)
        nacimiento = ft.TextField(label="Fecha Nacimiento", width=300, border_radius=10)
        
        lbl_genero = ft.Text("Género:")
        genero = ft.RadioGroup(content=ft.Row(
            [ft.Radio(value="Masculino", label="Varón"), ft.Radio(value="Femenino", label="Mujer")],
            alignment=ft.MainAxisAlignment.CENTER
        ))

        email = ft.TextField(label="Correo", width=300, border_radius=10)
        password = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        lbl_error = ft.Text("", color="red")

        def accion_registrar(e):
            if not email.value or not password.value or not nombre.value:
                lbl_error.value = "Faltan datos obligatorios"
                page.update()
                return

            nuevo_usuario = Usuario(
                email.value, password.value, nombre.value, 
                apellido.value, nacimiento.value, genero.value
            )
            
            if nuevo_usuario.guardar():
                page.snack_bar = ft.SnackBar(ft.Text("¡Cuenta creada con éxito!"))
                page.snack_bar.open = True
                mostrar_login()
            else:
                lbl_error.value = "Error: El correo ya existe."
                page.update()

        btn_crear = ft.ElevatedButton("REGISTRARME", width=300, on_click=accion_registrar)
        btn_volver = ft.TextButton("Volver al Login", on_click=lambda e: mostrar_login())

        page.add(ft.Column(
            [titulo, nombre, apellido, nacimiento, lbl_genero, genero, email, password, btn_crear, lbl_error, btn_volver],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ))
        page.update()

    # ---------------------------------------------------------
    # VISTA 1: PANTALLA DE LOGIN
    # ---------------------------------------------------------
    def mostrar_login(e=None):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        titulo = ft.Text("Iniciar Sesión", size=24, weight="bold")
        email = ft.TextField(label="Correo", width=300, border_radius=10)
        password = ft.TextField(label="Contraseña", password=True, width=300, border_radius=10)
        lbl_error = ft.Text("", color="red")

        def accion_login(e):
            # --- CAMBIO IMPORTANTE ---
            usuario_encontrado = Usuario.login(email.value, password.value)
            
            if usuario_encontrado:
                # Si existe, pasamos el objeto entero al dashboard
                mostrar_dashboard(usuario_encontrado)
            else:
                lbl_error.value = "Datos incorrectos"
                page.update()

        btn_entrar = ft.ElevatedButton("INGRESAR", width=300, on_click=accion_login)
        btn_registro = ft.TextButton("Crear cuenta nueva", on_click=mostrar_registro)

        page.add(ft.Column(
            [titulo, email, password, btn_entrar, lbl_error, btn_registro],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ))
        page.update()

    mostrar_login()

if __name__ == "__main__":
    ft.app(target=main)