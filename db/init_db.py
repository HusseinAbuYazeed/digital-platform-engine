import logging
import psycopg2
from db.connection import get_connection

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# 2. إنشاء كائن الـ logger الخاص بهذا الملف
logger = logging.getLogger(__name__)

def init_users_table() -> None:
    """Creates the users table. Raises an exception if the operation fails."""
    sql_script = """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'student',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    conn = get_connection()
    if not conn:
        logger.error("Database connection failed during table initialization.")
        raise psycopg2.OperationalError("Could not connect to the database.")
        
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_script)
        logger.info("Users table created or verified successfully.")
        
    except psycopg2.Error as error:
        logger.error(f"Failed to execute SQL script for users table: {error}")
        raise error
        
    finally:
        if conn:
            conn.close()
