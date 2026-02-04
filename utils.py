"""
Utility Functions for Data Analysis and Export
"""

import pandas as pd
import logging 
from typing import List , Dict ,Optional
from tabulate import tabulate
from database import get_sql_connection , TABLE_NAME


logger = logging.getLogger(__name__)

def query_to_dataframe(query: str) -> pd.DataFrame:
    """
        Execute SQL queries and return results as a Dataframe.
        Args: 
            query: SQL query strings.
        Returns:
            pandas Dataframe with query results
    """

    try:
        with get_sql_connection() as connection:
            df = pd.read_sql(query , connection)
            logger.info(f"Query Executed Successfully. Returned {len(df)} rows.")
            return df
    except Exception as e:
        logger.error(f"Error Executing Query: {e}")
        return pd.DataFrame()


def get_latest_crypto_dataframe(limit : int = 5) -> pd.DataFrame:
    """
        Get Latest cryptocurrency data as a Dataframe.

        Args:
            limit : Number of records to retrieve
        
        Returns:
            pandas dataframe with latest crypto data
    """

    query = f"""
    SELECT TOP({limit})
        rank, name, price, one_hour_change as '1h_change',
        twenty_four_hour_change as '24h_change', seven_day_change as '7d_change',
        market_cap, volume_24h, circulating_supply, scraped_at
    FROM {TABLE_NAME}
    ORDER BY scraped_at DESC , rank
    """
    return query_to_dataframe(query)

def export_to_csv(filename: str='crypto_data.csv' , limit : Optional[int] = None) -> bool:
    """
    Export cryptocurrency data to CSV file.
    
    Args:
        filename: Output CSV filename
        limit: Number of records to export (None for all)
        
    Returns:
        True if successful, False otherwise
    """

    try:
        df = get_latest_crypto_dataframe(limit if limit else 10000)
        if not df.empty:
            df.to_csv(filename, index=False)
            logger.info(f"Data Export to {filename}.")
            print(f"Exported {len(df)} records to {filename}.")
            return True
        else:
            logger.warning("No Data to export.")
            return False
    except Exception as e:
        logger.warning(f"Error Exporting Data {e}.")


def export_to_excel(filename: str = 'crypto_data.xlsx' , limit: Optional[int] = None) -> bool:
    """
    Export cryptocurrency data to Excel file.
    
    Args:
        filename: Output Excel filename
        limit: Number of records to export (None for all)
        
    Returns:
        True if successful, False otherwise
    """

    try:
        df = get_latest_crypto_dataframe(limit if limit else 10000)
        if not df.empty:
            df.to_excel(filename , index=False ,engine='openpyxl')
            logger.info(f"Data Exported to {filename}")
            return True
        else:
            logger.warning(f"No Data to Export.")
            return False
    except Exception as e:
        logger.warning(f"Error Exporting data {e}.")
        return False



def search_crypto(name:str)-> pd.DataFrame:
    """
        Function to Fetch Crypto Coin by its Name.

        Args:
            name: Name of Coin
        Returns:
            Dataframe with searched Results. 
    """

    query= f"""
    SELECT
        rank, name, price, one_hour_change as '1h_change',
        twenty_four_hour_change as '24h_change', seven_day_change as '7d_change',
        market_cap, volume_24h, circulating_supply, scraped_at
    FROM {TABLE_NAME}
    WHERE name LIKE '%{name}%'
    ORDER BY scraped_at , rank;
    """

    return query_to_dataframe(query)

def get_crypto_by_rank(rank: int) -> pd.DataFrame:
    """
        Function to get crypto currency by rank
        
        args:
            rank : rank of crypto currency to be fetched.
        Retruns:
            Dataframe containing fetched result.
        
    """
    if not isinstance(rank , int) or rank <=0:
        raise ValueError("Rank Must be a positive Integer greater than 0")
    
    query = f"""
    SELECT
        rank, name, price, one_hour_change as '1h_change',
        twenty_four_hour_change as '24h_change', seven_day_change as '7d_change',
        market_cap, volume_24h, circulating_supply, scraped_at
    FROM {TABLE_NAME}
    WHERE rank = {rank};
    """
    return query_to_dataframe(query)
    

if __name__=='__main__':

    # Setup Logging for standalone Execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("Testing Utility Function....\n")

    # # Get Latest Data
    # print("Latest 5 Cryptocurrencies: ")
    # df = get_latest_crypto_dataframe(5)
    # if not df.empty:
    #     print(df.to_string(index=False))
    # else:
    #     print("No Data Available.")

    # # Export to CSV
    # print("Exporting to CSV....\n")
    # export_to_excel('latest_crypto_data.xlsx' , 5)

    # Search Crypto By Name
    # df = search_crypto('Bitcoin')
    # if df.empty:
    #     print("No Coin Exist with this name.")
    # else:
    #     print(
    #         tabulate(
    #             df,
    #             headers='keys',
    #             tablefmt='pretty',
    #             showindex=False
    #         )
    #     )
    
    # Search by rank
    df = get_crypto_by_rank(5)
    if df.empty:
        print("Argument Was Not an Integer or not a Valid Rank.")
    else:
        print(
            tabulate(
                df,
                headers='keys',
                tablefmt='pretty',
                showindex=False
            )
        )