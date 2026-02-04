"""
    Main Entry Point for Crypto Market Data Project with SQL server Intergration.
"""

import logging
from scraper import scrape_coinmarketcap
from scraper import scrape_coinmarketcap_all_pages
from database import save_to_sql_server
from config import LOG_FILE , LOG_LEVEL , LOG_FORMAT

def setup_logging():
    logging.basicConfig(
        level=getattr(logging,LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )


def main():

    """Main Application Function."""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Scrape Data
        logger.info("Starting Cryptocurrency Scrapping....")

        # Pass the Number of Pages to Scrape from Crypto Market Website
        crypto_data = scrape_coinmarketcap_all_pages(2)
        if not crypto_data:
            logger.error("Failed to Scrape Data")
            return
        
        logger.info(f"Successfully Scraped {len(crypto_data)} cryptocurrencies.")

        # Save Data to SQL Server
        logger.info("Saving Data to SQL Server...")
        if save_to_sql_server(crypto_data):
            logger.info("Successfully Saved Data to Database.")
        else:
            logger.error("Failed to Save Data to Database.")
    except KeyboardInterrupt:
        logger.info("Operation Cancelled By User")
    except Exception as e:
        logger.error(f"Application Error {e}" , exc_info=True)

if __name__ == "__main__":
    main()