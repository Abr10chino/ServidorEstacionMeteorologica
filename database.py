import psycopg2
from psycopg2 import pool

DB_CONFIG = {
    "host": "ep-floral-queen-a4wzkfnl-pooler.us-east-1.aws.neon.tech",
    "port": 5432,
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_5o0BbRpjhsTx",
    "sslmode": "require"
}

try:
    connectionPool = psycopg2.pool.SimpleConnectionPool(1,5, **DB_CONFIG)
    print(f"Conexion a la base de datos creada exitosamente: {connectionPool}")
except Exception as e:
    print(f"Error creando conexion a la base de datos: {e}")
    connectionPool = None

def getConnection():
    if connectionPool:
        return connectionPool.getconn()
    
    return None

def releaseConnection(conn):
    if connectionPool and conn:
        connectionPool.putconn(conn)