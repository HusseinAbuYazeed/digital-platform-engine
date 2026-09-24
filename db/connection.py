import os
import logging
from dotenv import load_dotenv
import psycopg2

load_dotenv()
db_pass = os.getenv("DATABASE_PASSWORD")

# Configure the standard logger for production logging
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": "digital_platform_db",
    "user": "postgres",
    "password": db_pass,
    "host": "localhost",
    "port": "5432"
}

def get_connection():
    """Connect with the database. Raises psycopg2.Error if connection fails."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as error: 
        # Log the error safely instead of printing
        logger.error(f"Database connection error: {error}")
        # Raise the error so FastAPI can handle it cleanly or return a 500 error
        raise error
