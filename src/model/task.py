import sqlite3

class Tarea:
    def __init__(self, titulo, descripcion, usuario_email, estado="pendiente", id=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.usuario_email = usuario_email
        self.estado = estado

    def guardar(self):
        conexion = sqlite3.connect("tareas.db")
        cursor = conexion.cursor()
        
        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                estado TEXT DEFAULT 'pendiente',
                usuario_email TEXT,
                FOREIGN KEY(usuario_email) REFERENCES usuarios(email)
            )
        """)
        
        cursor.execute("INSERT INTO tareas (titulo, descripcion, usuario_email, estado) VALUES (?, ?, ?, ?)",
                       (self.titulo, self.descripcion, self.usuario_email, self.estado))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_por_usuario(email):
        conexion = sqlite3.connect("tareas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, titulo, descripcion, estado FROM tareas WHERE usuario_email = ?", (email,))
        filas = cursor.fetchall()
        conexion.close()
        return [Tarea(f[1], f[2], email, f[3], f[0]) for f in filas]