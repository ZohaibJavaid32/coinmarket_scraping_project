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

## 🔍 Module Usage Examples

### Using Scraper Module

```python
from scraper import scrape_coinmarketcap
from scraper import scrape_coinmarketcap_all_pages

# Scrape cryptocurrency data
crypto_data = scrape_coinmarketcap()

crypto_data = scrape_coinmarketcap_al_pages(5) # Pass number of pages to scrape data.

for crypto in crypto_data[:5]:
    print(f"{crypto['rank']} - {crypto['name']}: {crypto['price']}")
```

### Using Database Module

```python
from database import save_to_sql_server, get_crypto_statistics

# Save data
save_to_sql_server(crypto_data)

# Get statistics
stats = get_crypto_statistics()
print(f"Total records: {stats['total_records']}")
```

### Using Utils Module

```python
from utils import get_latest_crypto_dataframe, export_to_csv, get_top_gainers

# Get data as DataFrame
df = get_latest_crypto_dataframe(100)

# Export to CSV
export_to_csv('output.csv', limit=50)

# Get top gainers
gainers = get_top_gainers(10)
print(gainers)
```

## 📊 Database Schema

**Table: CryptoCurrency**

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| rank | INT | Cryptocurrency rank |
| name | NVARCHAR(100) | Cryptocurrency name |
| price | NVARCHAR(50) | Current price |
| one_hour_change | NVARCHAR(20) | 1-hour change percentage |
| twenty_four_hour_change | NVARCHAR(20) | 24-hour change percentage |
| seven_day_change | NVARCHAR(20) | 7-day change percentage |
| market_cap | NVARCHAR(50) | Market capitalization |
| volume_24h | NVARCHAR(50) | 24-hour trading volume |
| circulating_supply | NVARCHAR(100) | Circulating supply |
| scraped_at | DATETIME | Timestamp of data collection |

**Indexes:**
- `idx_name` on `name`
- `idx_rank` on `rank`
- `idx_scraped_at` on `scraped_at`

## 🔐 SQL Server Authentication

### Windows Authentication (Recommended)
Leave `username` and `password` empty in `config.py`:
```python
DB_CONFIG = {
    'server': 'localhost',
    'database': 'CryptoData',
    'username': '',
    'password': '',
    'driver': '{ODBC Driver 17 for SQL Server}'
}
```

### SQL Server Authentication
Provide credentials in `config.py`:
```python
DB_CONFIG = {
    'server': 'localhost',
    'database': 'CryptoData',
    'username': 'your_username',
    'password': 'your_password',
    'driver': '{ODBC Driver 17 for SQL Server}'
}
```

## 📝 Logging

Logs are saved to `crypto_scraper.log` with the following levels:
- **INFO**: Normal operation messages
- **WARNING**: Non-critical issues
- **ERROR**: Errors that need attention
- **DEBUG**: Detailed debug information (use `--verbose`)

## ⚠️ Troubleshooting

### Chrome WebDriver Issues
- Make sure Chrome browser is installed
- WebDriver will be automatically managed by Selenium 4+

### Database Connection Issues
- Verify SQL Server is running
- Check if the database exists
- Confirm ODBC driver is installed
- Test connection settings
- Check Windows Firewall settings

### ODBC Driver Not Found
Install ODBC Driver 17:
- Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Or use `{SQL Server}` driver in config.py

### Module Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## 🛡️ Best Practices

1. **Rate Limiting**: The scraper includes built-in delays to avoid overwhelming the server
2. **Error Handling**: All functions include proper error handling
3. **Resource Cleanup**: Context managers ensure proper cleanup of resources
4. **Logging**: Comprehensive logging for debugging and monitoring
5. **Data Validation**: Input validation before database insertion

## 📈 Future Enhancements

- [ ] Add scheduling support (cron/Windows Task Scheduler)
- [ ] Implement data visualization dashboard
- [ ] Add support for other data sources
- [ ] Implement data comparison between scrapes
- [ ] Add email notifications for price alerts
- [ ] Create REST API wrapper

## 📄 License

This project is for educational purposes. Please respect CoinMarketCap's robots.txt and Terms of Service.

## 👤 Author

Created for cryptocurrency data analysis and tracking.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests.

## ⭐ Acknowledgments

- CoinMarketCap for providing cryptocurrency data
- Selenium and BeautifulSoup communities
- Python community

---

**Note**: This scraper is for educational and personal use. Always check and respect the website's robots.txt and Terms of Service. Use responsibly and don't overload the server with requests.

