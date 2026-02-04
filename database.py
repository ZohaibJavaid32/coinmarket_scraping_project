"""
Database Module for SQL Server Operations
Handles all database connections, table creation, and data operations
"""

import pyodbc
from datetime import datetime
from contextlib import contextmanager
from typing import List , Dict , Optional
import logging


from config import DB_CONFIG , TABLE_NAME

logger = logging.getLogger(__name__)

@contextmanager
def get_sql_connection():
    """
    Context manager for SQL Server connection to ensure proper cleanup.
    
    Yields:
        pyodbc.Connection: Active database connection
    """

    connection = None
    try:
        # Build Connection String
        if DB_CONFIG['username']:
            # SQL Server Authentication
            conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']}"
            )
        else:
            # Window Authentication
            conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"Trusted_Connection=yes"
            )
        
        connection = pyodbc.connect(conn_str)
        logger.info("Database Connection Established!")
        yield connection
    
    except pyodbc.Error as e:
        logger.error("Database Connection Error {e}")
        raise
    finally:

        if connection:
            connection.close()
            logger.info("Database Connection Closed!.")


def create_crypto_table(cursor: pyodbc.Cursor) -> None:
    """
        Create Crypto Currency Table

        Args:
            cursor: Database Cursor Object
    """

    create_table_query = f"""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = '{TABLE_NAME}' and xtype='U')
    CREATE TABLE {TABLE_NAME} (
    id INT IDENTITY(1,1) PRIMARY KEY,
        rank INT,
        name NVARCHAR(100),
        price NVARCHAR(50),
        one_hour_change NVARCHAR(20),
        twenty_four_hour_change NVARCHAR(20),
        seven_day_change NVARCHAR(20),
        market_cap NVARCHAR(50),
        volume_24h NVARCHAR(50),
        circulating_supply NVARCHAR(100),
        scraped_at DATETIME DEFAULT GETDATE(),
        INDEX idx_name (name),
        INDEX idx_rank (rank),
        INDEX idx_scraped_at (scraped_at)
    )
    """

    cursor.execute(create_table_query)
    logger.info(f"Table '{TABLE_NAME}' created or already exists.")


def insert_crypto_data(connection:pyodbc.Connection , crypto_data: List[Dict[str,str]]) ->int:
    """
    Insert Crypto Data into Databse

    Args:
        connection: Active DB connection
        crypto_data : list of crypto currencies.
    
    Returns: 
        Number of crypto currencies inserted
    """

    cursor = connection.cursor()
    try:
        # Create Crypto Table if not Exist
        create_crypto_table(cursor)
        connection.commit()

        # Prepare Insert Statement
        insert_query = f"""
        INSERT INTO {TABLE_NAME}
        (rank, name, price, one_hour_change, twenty_four_hour_change, 
         seven_day_change, market_cap, volume_24h, circulating_supply, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Prepare data for inserts.
        current_time = datetime.now()
        rows_to_insert = []

        for crypto in crypto_data:
            row = (
                int(crypto['rank']) if crypto['rank'].isdigit() else None,
                crypto['name'],
                crypto['price'],
                crypto['1h_change'],
                crypto['24h_change'],
                crypto['7d_change'],
                crypto['market_cap'],
                crypto['24h_volume'],
                crypto['circulating_supply'],
                current_time   
            )
            rows_to_insert.append(row)

        # Execute batch insert
        cursor.executemany(insert_query, rows_to_insert)
        connection.commit()

        rows_inserted = len(rows_to_insert)
        logger.info(f"Successfully inserted {rows_inserted} records into DB.") 

        return rows_inserted    
    except pyodbc.Error as e:
        connection.rollback()
        logger.error(f"Error inerting data: {e}")

    finally:
        cursor.close()

def save_to_sql_server(crypto_data: List[Dict[str, str]]) -> bool:
        """
            Main function to save data to SQL server DB.
            Args:
                list of crypto currencies
            Returns:
                True if successfull else False

        """
        if not crypto_data:
            logger.warning("No data to save.")
            return False
        
        try:
            with get_sql_connection() as connection:
                rows_inserted = insert_crypto_data(connection , crypto_data)
                logger.info(f"Data Saved Successfully. {rows_inserted} inserted.")
                return True
        except Exception as e:
            logger.warning(f"Failed to save data to SQL server {e}" ,exc_info=True)
            return False
            

def get_recent_data(limit: int=10) -> Optional[List]:
    """
        Retrieve most recent cryptocurrency data from DB.

        Args:
            limit : Number of records to retrieve
        Retrurns:
            List of Tuples containing cryptocurrency data.
    """

    try:
        with get_sql_connection() as connection:
            cursor = connection.cursor()

            query = f"""
            SELECT TOP (?)
                rank, name, price, one_hour_change, twenty_four_hour_change,
                seven_day_change, market_cap, volume_24h, circulating_supply, scraped_at
            FROM {TABLE_NAME}
            ORDER BY scraped_at DESC
            """
            cursor.execute(query, limit)
            results = cursor.fetchall()
            cursor.close()
            
            return results
    except Exception as e:
        logger.error(f"Error Retrieving Data {e}")
        return None

def get_crypto_statistics() -> Dict:
    """
        Module for cryptocurrencies stats.

        Returns:
            Dictionary with Stats.
    """

    stats = {}
    try:
        with get_sql_connection() as connection:
            cursor = connection.cursor()
            print("Success..")

            # Total Records
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            stats['total_records'] = cursor.fetchone()[0]

            # Unique Currencies
            cursor.execute(f"SELECT COUNT(DISTINCT(name)) FROM {TABLE_NAME}")
            stats['unique_cryptos'] = cursor.fetchone()[0]

            # Date Range
            cursor.execute(f"""
                SELECT
                    MIN(scraped_at) AS first_scrape,
                    MAX(scraped_at) AS last_scrape
                    FROM {TABLE_NAME}
            """)
            row = cursor.fetchone()
            stats['first_scrape'] = row[0]
            stats['last_scrape'] = row[1]

            # Scrape count
            cursor.execute(f"""
                SELECT COUNT(DISTINCT(scraped_at))
                FROM {TABLE_NAME}
            """)
            row = cursor.fetchone()
            stats['total_scrapes'] = row[0] if row else 0

            cursor.close()
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
    
    return stats

def delete_old_data(days: int = 30) -> int:
    """
        Delete data older than specified days

        Args:
            days : Number of days to keep (default: 30)
        
        Returns:
            Number of rows deleted
    """

    try:
        with get_sql_connection() as connection:
            cursor = connection.cursor()

            delete_query = f"""
            DELETE FROM {TABLE_NAME}
            WHERE scraped_at < DATEADD(day , ? , GETDATE())
            """
            cursor.execute(delete_query , -days)
            rows_deleted = cursor.rowcount
            connection.commit()
            cursor.close()

            logger.info(f"Successfully Deleted {rows_deleted} old records.")
            return rows_deleted
    except Exception as e:
        logger.error(f"Error Deleteing Old Data {e}.")
        return 0



if __name__ == '__main__':
    # Setup Logging for Standalone  Execution.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("Testing Database Connection....")
    try:
        with get_sql_connection() as conn:
            print("✅ Database Connection Successfull.")
        
        #delete_old_data(1)

        stats = get_crypto_statistics()
        if stats:
            print("\n📊 Database Statistics:")
            print(f"   Total Records: {stats.get('total_records', 0)}")
            print(f"   Unique Cryptos: {stats.get('unique_cryptos', 0)}")
            print(f"   Total Scrapes: {stats.get('total_scrapes', 0)}")
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")