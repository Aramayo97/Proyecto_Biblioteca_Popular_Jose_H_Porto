import mysql.connector

# Configuración de la conexión
config = {
    'user': 'tu_usuario',        # ejemplo: 'root' o el usuario que uses
    'password': 'tu_contraseña', # la contraseña para ese usuario
    'host': 'localhost',         # o la IP del servidor de base de datos
    'database': 'biblioteca'
}

try:
    # Establecer conexión
    conexion = mysql.connector.connect(**config)
    
    if conexion.is_connected():
        print("Conexión exitosa a la base de datos")

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM socios")  # ejemplo de consulta

        resultados = cursor.fetchall()

        for fila in resultados:
            print(fila)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada")
