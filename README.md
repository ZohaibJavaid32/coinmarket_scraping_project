# CoinMarketCap Cryptocurrency Scraper

This project scrapes cryptocurrency data from [CoinMarketCap](https://coinmarketcap.com) and stores data to SQL Server for analysis.

## 🚀 Features

- **Web Scraping**: Automated scraping of cryptocurrency data using Selenium and BeautifulSoup
- **SQL Server Integration**: Store data in SQL Server with automatic table creation
- **Data Export**: Export data to CSV or Excel formats
- **Data Analysis**: Built-in functions for top gainers/losers analysis
- **Logging**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Robust error handling and recovery

## 📋 Requirements

- Python 3.8 or higher
- Chrome browser (for Selenium WebDriver)
- SQL Server (Local or Remote)
- ODBC Driver 17 for SQL Server (or SQL Server driver)

## 🔧 Installation

### 1. Clone or Download the Repository

```bash
cd coinmarketcap_scraping_project
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup SQL Server Database

**Option A: Using SQL Server Management Studio (SSMS)**
1. Open SSMS and connect to your SQL Server instance
2. Run the `setup_database.py` file to generate queries.

**Option B: Automatic Setup**
The application will automatically create the table when you first run it (DB must exist in SQL Server).



### 4. Configure Database Connection

Edit `config.py` and update the `DB_CONFIG` section:

```python
DB_CONFIG = {
    'server': 'localhost',  # or '.\SQLEXPRESS' or IP address
    'database': 'CryptoData',
    'username': '',  # Leave empty for Windows Authentication
    'password': '',  # Leave empty for Windows Authentication
    'driver': '{ODBC Driver 17 for SQL Server}'
}
```

