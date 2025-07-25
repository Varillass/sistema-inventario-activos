import pymysql

# Configuración de conexión
DB_CONFIG = {
    'host': '181.224.226.142',
    'user': 'afrodita',
    'password': 'Zxasqw12@@@',
    'database': 'inventario_activos',
    'port': 3306
}

try:
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    print("Estructura de la tabla inventario_equipo:")
    cursor.execute('DESCRIBE inventario_equipo')
    columns = cursor.fetchall()
    
    for i, col in enumerate(columns):
        print(f"{i+1}. {col[0]}: {col[1]}")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}") 