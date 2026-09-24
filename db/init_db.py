import logging
import psycopg2
from db.connection import get_connection

# Configure the logging format for FastAPI production standards
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def init_all_tables() -> None:
    """Initializes the digital store database based on the 5-table schema design."""
    
    # Executed in sequential order due to foreign key dependencies
    table_queries = [
        # 1. Users Table
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # 2. Products Table
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            description TEXT,
            product_type VARCHAR(50) DEFAULT 'downloadable',
            price DECIMAL(10, 2) NOT NULL,
            file_url VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # 3. Orders Table
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            total_amount DECIMAL(10, 2) NOT NULL,
            payment_status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # 4. Order Items Table
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES products(product_id) ON DELETE SET NULL,
            price_at_purchase DECIMAL(10, 2) NOT NULL
        );
        """,
        
        # 5. User Access Table (The Digital Ownership Bridge)
        """
        CREATE TABLE IF NOT EXISTS user_access (
            access_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES products(product_id) ON DELETE CASCADE,
            purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_revoked BOOLEAN DEFAULT FALSE,
            UNIQUE(user_id, product_id)
        );
        """
    ]

    conn = get_connection()
    if not conn:
        logger.critical("Database connection failed. Migration aborted.")
        raise psycopg2.OperationalError("Could not connect to the database.")

    try:
        # Atomic transaction: All tables are created together or none at all
        with conn:
            with conn.cursor() as cursor:
                for query in table_queries:
                    cursor.execute(query)
                    
        logger.info("Database schema initialized successfully with all 5 tables.")

    except psycopg2.Error as error:
        logger.error(f"Migration failed during table creation: {error}")
        raise error

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    logger.info("Running manual database initialization...")
    init_all_tables()
