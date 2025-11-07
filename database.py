import os
import psycopg2
from psycopg2 import pool

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "sslmode": os.getenv("DB_SSLMODE", "require")
}

try:
    connectionPool = pool.SimpleConnectionPool(1,5, **DB_CONFIG)
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