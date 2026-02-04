from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import logging 
from typing import List , Dict
from contextlib import contextmanager
import json


from config import (
    COINMARKET_URL,
    SCROLL_PAUSE_TIME,
    SCROLL_STEP,
    MAX_SCROLL_ATTEMPTS,
    EXPLICIT_TIME_WAITOUT,
    CHROME_EXPERIMENTAL_OPTIONS,
    CHROME_OPTIONS
)

logger = logging.getLogger(__name__)

@contextmanager
def get_chrome_driver():
    """ Context manager for Chrome WebDriver to ensure proper cleanup."""

    options = Options()
    # Add command line options
    for option in CHROME_OPTIONS:
        options.add_argument(option)

    # Add Experimental Options

    for key, value in CHROME_EXPERIMENTAL_OPTIONS.items():
        options.add_experimental_option(key,value)

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(5)
        logger.info("Chrome WebDriver Initalized Successfully.")
        yield driver
    except Exception as e:
        logger.error(f"Error Occurred in Initialization of WebDriver {e}")
    finally:
        if driver:
            driver.quit()
            logger.info("Browser Closed Successfully.")


def scroll_to_load_content(driver:webdriver.Chrome,max_scrolls: int = MAX_SCROLL_ATTEMPTS) -> None:
    """ 
        Scroll the page to load dynamic content.
        Args: 
            Selenium Web Driver Instance
            max_scrolls: max number of scroll attempts  to prevent infinite loops.
    """
    scroll_attempts = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    logger.info("Starting page scrolling to load dynamic content")

    while scroll_attempts < max_scrolls:
        for i in range(0 , last_height , SCROLL_STEP):
            driver.execute_script(f"window.scroll(0 , {i});")
            time.sleep(SCROLL_PAUSE_TIME)
        
        # wait for next content to load
        time.sleep(1)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logger.info("Reached to end.")
            break

        last_height = new_height
        scroll_attempts +=1
        logger.info(f"Scroll attempt {scroll_attempts}/{max_scrolls}")

    logger.info("Finished Scrolling")

def parse_crypto_data(soup:BeautifulSoup) -> List[Dict[str,str]]:
    """
    
    :param soup: Description
    :type soup: BeautifulSoup
    :return: Description
    :rtype: List[Dict[str, str]]
    """

    crypto_data = []

    table = soup.find('table', {'class':'cmc-table'})
    if not table:
        logger.error('Could not Find cryptocurrency table')
        return crypto_data
    
    rows = table.find_all('tr')
    logger.info(f"Found {len(rows) - 1} rows (excluding header.)")

    for row in rows[1:]: #skip header row
        cols = row.find_all('td')
        if len(cols) >=10:
            try:
                crypto_info = {
                    'rank': cols[1].text.strip(),
                    'name': cols[2].text.strip(),
                    'price': cols[3].text.strip(),
                    '1h_change': cols[4].text.strip(),
                    '24h_change': cols[5].text.strip(),
                    '7d_change': cols[6].text.strip(),
                    'market_cap': cols[7].text.strip(),
                    '24h_volume': cols[8].text.strip(),
                    'circulating_supply': cols[9].text.strip()
                }
                crypto_data.append(crypto_info)
            except (IndexError , AttributeError) as e:
                logger.warning(f'Error parsing now: {e}')
                continue
        else:
            logger.debug('Skipping rows with insufficient columns')
            continue
            
    return crypto_data 



def scrape_coinmarketcap() -> List[Dict[str,str]]:
    """
         scrape cryptocurrency data from CoinMarketCap one page.

        Returns: List of dictionaries containing crypto currency information
    """

    try:
        with get_chrome_driver() as driver:
            logger.info(f"Navigating to {COINMARKET_URL}")
            driver.get(COINMARKET_URL)

            try:
                WebDriverWait(driver , EXPLICIT_TIME_WAITOUT).until(
                    EC.presence_of_element_located((By.CLASS_NAME , 'cmc-table'))
                )
                logger.info("Table Loaded Successfully.")
            except TimeoutException:
                logger.error("Timeout waiting for table to load")
                return []
            
            # Scroll to laod content
            scroll_to_load_content(driver)

            
            soup = BeautifulSoup(driver.page_source ,'html.parser')
            

        # Parse crypto data
        crypto_data = parse_crypto_data(soup)
        logger.info(f"Successfully scraped {len(crypto_data)} cryptocurrencies")

        return crypto_data
    
    except Exception as e:
        logger.error(f"Error during scraping: {e}" , exc_info=True)
        return []



def scrape_coinmarketcap_all_pages(max_pages: int = 10) -> List[Dict[str,str]]:
    """
        Scrape All Cryptocurrencies data.
        args: 
            max_pages: max pages to scrape (to avoid infinite scarping)
        returns:
            List containing dicts of crypto crurrencies.
    """
    all_crypto_data = []
   
    try:
        with get_chrome_driver() as driver:
            for page in range(1, max_pages + 1):
                url=f"{COINMARKET_URL}?page={page}"
                logger.info(f"Navigation to {url}")
                driver.get(url)
                time.sleep(3)
            
                try:
                    WebDriverWait(driver , EXPLICIT_TIME_WAITOUT).until(
                        EC.presence_of_element_located((By.CLASS_NAME , 'cmc-table'))
                    )
                    logger.info(f"Page {page} Loaded Successfully.")
                except TimeoutException:
                    logger.warning(f"Timeout waiting for to load on page {page}.")
                    break

                # scroll to load to content.
                scroll_to_load_content(driver)

                # Parse the Page
                soup = BeautifulSoup(driver.page_source ,'html.parser')
                page_data = parse_crypto_data(soup)
                logger.info(f"{len(page_data)} cryptocurrencies scraped from page {page}.")
                if not page_data:
                    logger.info('No more data found. Stopping Scraping..')
                    break
                all_crypto_data.extend(page_data)
            
            logger.info(f"Finished Scraping {len(all_crypto_data)} cryptocurrencies from {page} pages.")

        return all_crypto_data 

    except Exception as e:
        logger.error("Error during scraping {e}" ,exc_info=True)
        return []


if __name__ == "__main__":
    # Setup logging for standalone execution

    logging.basicConfig(
        level = logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("Starting Coinmarket scrapper....")

    data = scrape_coinmarketcap()

    if data:
        print(f"Successfully scraped {len(data)} cryptocurrencies")
        print("\n First 5 Results: ")
        for crypto in data[:5]:
            print(f"  {crypto['rank']:>4} | {crypto['name']:<20} | {crypto['price']:<15}")
    else:
        print("Failed to scrape data")


# if __name__ == "__main__":

#     # Setup Logging
#     logging.basicConfig(
#         level=logging.INFO,
#         format='%(asctime)s - %(levelname)s - %(message)s'
#     )
#     print("Starting Coinmarket scrapper....")
#     data = scrape_coinmarketcap_all_pages(max_pages=5)  # scrape first 5 pages

#     if data:
#         print(f"Successfully scraped {len(data)} cryptocurrencies")
#         print("\n First 10 Results: ")
#         for crypto in data[:10]:
#             print(f"{crypto['rank']:>4} | {crypto['name']:<20} | {crypto['price']:<15}")
#     else:
#         print("Failed to scrape data")
