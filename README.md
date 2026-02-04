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

## 📁 Project Structure

```
coinmarketcap-scraper/
│
├── main.py                 # Main application entry point
├── scraper.py             # Web scraping logic
├── database.py            # SQL Server operations
├── utils.py               # Utility functions (export, analysis)
├── config.py              # Configuration settings
├── setup_database.py      # Database setup script generator
│
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
│
└── fake_jobs.ipynb       # Jupyter Notebook for Beautiful Soup Practice.
│
└── coin_market_scrapper_selenium.ipynb      # Jupyter Notebook To scrape data from first page.
│
└── coin_market_scrapper_bs4.ipynb       # Jupyter Notebook to scrape data using bs4 (have limitations).
```

## 🎯 Usage

### Basic Usage

Scrape data and save to database:
```bash
python main.py
```

