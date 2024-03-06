from asyncpg import connection
from config import *


async def get_connection():
    conn = await connection.connect(host=DB_HOST,
                                    port=DB_PORT,
                                    user=DB_USER,
                                    password=DB_PASS,
                                    database=DB_NAME)
    return conn
