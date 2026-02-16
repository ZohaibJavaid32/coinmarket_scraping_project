# CoinMarketCap Scraper - System Architecture

## 📐 Architecture Overview

This document describes the architecture of the CoinMarketCap Cryptocurrency Scraper system.

---

## 🎯 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COINMARKETCAP SCRAPER SYSTEM                     │
└─────────────────────────────────────────────────────────────────────────┘

                                    ┌──────────────┐
                                    │   main.py    │
                                    │   (Entry)    │
                                    └──────┬───────┘
                                           │
                        ┌──────────────────┼──────────────────┐
                        │                  │                  │
                        ▼                  ▼                  ▼
                 ┌──────────┐      ┌──────────┐      ┌──────────┐
                 │ config.py│      │scraper.py│      │database.py│
                 │(Settings)│      │  (Scrape)│      │  (Store)  │
                 └──────────┘      └─────┬────┘      └─────┬─────┘
                                         │                  │
                        ┌────────────────┘                  │
                        │                                   │
                        ▼                                   ▼
            ┌───────────────────────┐         ┌────────────────────────┐
            │   External Services   │         │   SQL Server Database  │
            ├───────────────────────┤         ├────────────────────────┤
            │  • CoinMarketCap Web  │         │  • CryptoData DB       │
            │  • Chrome WebDriver   │         │  • CryptoCurrency Tbl  │
            └───────────────────────┘         └────────────────────────┘

                                    ┌──────────────┐
                                    │   utils.py   │
                                    │  (Analysis)  │
                                    │   Optional   │
                                    └──────────────┘
```

---

## 🏗️ Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                             APPLICATION LAYERS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    PRESENTATION LAYER                          │    │
│  │  ┌──────────────────────────────────────────────────────┐     │    │
│  │  │  main.py                                              │     │    │
│  │  │  • Entry Point                                        │     │    │
│  │  │  • Logging Setup                                      │     │    │
│  │  │  • Orchestration                                      │     │    │
│  │  └──────────────────────────────────────────────────────┘     │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                               │                                        │
│                               ▼                                        │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    BUSINESS LOGIC LAYER                       │    │
│  │  ┌────────────────────┐  ┌────────────────────┐              │    │
│  │  │   scraper.py       │  │   database.py      │              │    │
│  │  │                    │  │                    │              │    │
│  │  │  • get_chrome_     │  │  • get_sql_        │              │    │
│  │  │    driver()        │  │    connection()    │              │    │
│  │  │  • scroll_to_load  │  │  • create_crypto_  │              │    │
│  │  │    _content()      │  │    table()         │              │    │
│  │  │  • parse_crypto_   │  │  • insert_crypto_  │              │    │
│  │  │    data()          │  │    data()          │              │    │
│  │  │  • scrape_         │  │  • save_to_sql_    │              │    │
│  │  │    coinmarketcap() │  │    server()        │              │    │
│  │  └────────────────────┘  └────────────────────┘              │    │
│  │                                                               │    │
│  │  ┌────────────────────────────────────────────┐              │    │
│  │  │   utils.py (Optional)                      │              │    │
│  │  │  • query_to_dataframe()                    │              │    │
│  │  │  • export_to_csv()                         │              │    │
│  │  │  • export_to_excel()                       │              │    │
│  │  │  • get_top_gainers()                       │              │    │
│  │  │  • get_top_losers()                        │              │    │
│  │  └────────────────────────────────────────────┘              │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                               │                                        │
│                               ▼                                        │
│  ┌───────────────────────────────────────────────────────────────┐    │
│  │                    CONFIGURATION LAYER                         │    │
│  │  ┌────────────────────────────────────────────────────────┐   │    │
│  │  │  config.py                                             │   │    │
│  │  │  • Database Configuration                              │   │    │
│  │  │  • Scraping Parameters                                 │   │    │
│  │  │  • Chrome Options                                      │   │    │
│  │  │  • Logging Settings                                    │   │    │
│  │  └────────────────────────────────────────────────────────┘   │    │
│  └───────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌──────────────┐
│   START      │
│   main.py    │
└──────┬───────┘
       │
       │ 1. Initialize
       ▼
┌──────────────────┐
│  Setup Logging   │
│  (LOG_FILE)      │
└──────┬───────────┘
       │
       │ 2. Call Scraper
       ▼
┌─────────────────────────────────────────────────────────┐
<<<<<<< HEAD
│         scraper.py - scrape_coinmarketcap_all_pages()   │
=======
│      scraper.py - scrape_coinmarketcap_all_pages()      │
>>>>>>> c7548e0704ef6a05d382353d0aafa28b2e7199dd
│                                                         │
│  ┌────────────────────────────────────────────────┐    │
│  │ 1. get_chrome_driver()                         │    │
│  │    └─> Initialize Selenium Chrome WebDriver    │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 2. Navigate to CoinMarketCap URL               │    │
│  │    └─> driver.get(COINMARKETCAP_URL)           │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 3. Wait for Table Element                      │    │
│  │    └─> WebDriverWait for 'cmc-table'           │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 4. scroll_to_load_content()                    │    │
│  │    └─> Scroll page to load dynamic content     │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 5. Get Page Source                             │    │
│  │    └─> driver.page_source                      │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 6. parse_crypto_data()                         │    │
│  │    └─> BeautifulSoup parsing                   │    │
│  │    └─> Extract: rank, name, price, changes...  │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 7. Return crypto_data (List[Dict])             │    │
│  └────────┬───────────────────────────────────────┘    │
└───────────┼─────────────────────────────────────────────┘
            │
            │ 3. Data Scraped
            ▼
┌─────────────────────────────────────────────────────────┐
│          database.py - save_to_sql_server()             │
│                                                         │
│  ┌────────────────────────────────────────────────┐    │
│  │ 1. get_sql_connection()                        │    │
│  │    └─> Connect to SQL Server                   │    │
│  │    └─> Use DB_CONFIG settings                  │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 2. insert_crypto_data()                        │    │
│  │    └─> create_crypto_table() if not exists     │    │
│  │    └─> Prepare batch insert data               │    │
│  │    └─> cursor.executemany(INSERT query)        │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 3. connection.commit()                         │    │
│  │    └─> Persist data to database                │    │
│  └────────┬───────────────────────────────────────┘    │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ 4. Return success/failure                      │    │
│  └────────┬───────────────────────────────────────┘    │
└───────────┼─────────────────────────────────────────────┘
            │
            │ 4. Data Saved
            ▼
┌──────────────────┐
│  Log Success     │
│  END             │
└──────────────────┘
```

---

## 🗃️ Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                     CryptoData Database                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           Table: CryptoCurrency                     │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  Column Name               │ Type          │ Key    │   │
│  ├────────────────────────────┼───────────────┼────────┤   │
│  │  id                        │ INT           │ PK     │   │
│  │  rank                      │ INT           │ IDX    │   │
│  │  name                      │ NVARCHAR(100) │ IDX    │   │
│  │  price                     │ NVARCHAR(50)  │        │   │
│  │  one_hour_change           │ NVARCHAR(20)  │        │   │
│  │  twenty_four_hour_change   │ NVARCHAR(20)  │        │   │
│  │  seven_day_change          │ NVARCHAR(20)  │        │   │
│  │  market_cap                │ NVARCHAR(50)  │        │   │
│  │  volume_24h                │ NVARCHAR(50)  │        │   │
│  │  circulating_supply        │ NVARCHAR(100) │        │   │
│  │  scraped_at                │ DATETIME      │ IDX    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Indexes:                                                   │
│  • idx_name (name)                                          │
│  • idx_rank (rank)                                          │
│  • idx_scraped_at (scraped_at)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Module Dependencies

```
┌────────────────────────────────────────────────────────────────┐
│                      DEPENDENCY GRAPH                          │
└────────────────────────────────────────────────────────────────┘

                          ┌─────────────┐
                          │   main.py   │
                          └──────┬──────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │scraper.py│  │database  │  │ config.py│
              │          │  │   .py    │  │          │
              └────┬─────┘  └────┬─────┘  └────┬─────┘
                   │             │             │
                   │             │             │
      ┌────────────┤             │             │
      │            │             │             │
      ▼            ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ selenium │  │BeautifulS│  │  pyodbc  │  │ logging  │
│          │  │  oup4    │  │          │  │          │
└──────────┘  └──────────┘  └──────────┘  └──────────┘


utils.py (Optional - not used by main.py)
    │
    ├─> database.py
    ├─> pandas
    └─> openpyxl
```

---

## 🔐 Security & Configuration Flow

```
┌────────────────────────────────────────────────────────┐
│              CONFIGURATION MANAGEMENT                  │
└────────────────────────────────────────────────────────┘

    config.py
        │
        ├─> Database Settings (DB_CONFIG)
        │       │
        │       ├─> Server: localhost
        │       ├─> Database: CryptoData
        │       ├─> Authentication: Windows/SQL
        │       └─> Driver: ODBC Driver 17
        │
        ├─> Scraping Settings
        │       │
        │       ├─> URL: coinmarketcap.com
        │       ├─> Scroll Settings
        │       └─> Timeout Values
        │
        ├─> Chrome Options
        │       │
        │       ├─> Headless Mode
        │       ├─> Anti-detection Features
        │       └─> Performance Options
        │
        └─> Logging Settings
                │
                ├─> Log Level: INFO
                ├─> Log Format
                └─> Log File: crypto_scraper.log
```

---

## 🚀 Execution Flow

```
User Runs: python main.py
    │
    ├─> 1. Load Configuration (config.py)
    │      └─> Read all settings
    │
    ├─> 2. Setup Logging
    │      └─> Create log file handler
    │      └─> Set format and level
    │
    ├─> 3. Execute Scraper
    │      │
    │      ├─> Initialize Chrome WebDriver
    │      ├─> Navigate to CoinMarketCap
    │      ├─> Wait for content to load
    │      ├─> Scroll to load all data
    │      ├─> Extract HTML content
    │      ├─> Parse with BeautifulSoup
    │      └─> Return structured data
    │
    ├─> 4. Save to Database
    │      │
    │      ├─> Connect to SQL Server
    │      ├─> Create table if not exists
    │      ├─> Insert data (batch operation)
    │      ├─> Commit transaction
    │      └─> Close connection
    │
    └─> 5. Log Results & Exit
           └─> Success/Failure status
```

---

## 🔧 Technology Stack

```
┌────────────────────────────────────────────────────────┐
│                   TECHNOLOGY STACK                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  LANGUAGE:          Python 3.8+                        │
│                                                        │
│  WEB SCRAPING:      • Selenium 4.15+                   │
│                     • BeautifulSoup4 4.12+             │
│                     • Chrome WebDriver                 │
│                                                        │
│  DATABASE:          • SQL Server                       │
│                     • pyodbc 5.0+                      │
│                                                        │
│  DATA ANALYSIS:     • pandas 2.0+ (optional)           │
│                     • openpyxl 3.1+ (optional)         │
│                                                        │
│  LOGGING:           • Python logging module            │
│                                                        │
│  ENVIRONMENT:       • Python venv                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Error Handling Flow

```
┌──────────────────────────────────────────────────────────┐
│                  ERROR HANDLING STRATEGY                 │
└──────────────────────────────────────────────────────────┘

Try-Catch Blocks at Multiple Levels:

1. Main Application Level (main.py)
   │
   ├─> Catch: KeyboardInterrupt
   │      └─> Action: Log graceful shutdown
   │
   └─> Catch: Exception (all others)
          └─> Action: Log error with traceback

2. Scraper Level (scraper.py)
   │
   ├─> Catch: TimeoutException
   │      └─> Action: Return empty list, log error
   │
   ├─> Catch: NoSuchElementException
   │      └─> Action: Log warning, continue
   │
   └─> Catch: Exception (WebDriver errors)
          └─> Action: Log error, return empty list

3. Database Level (database.py)
   │
   ├─> Catch: pyodbc.Error
   │      └─> Action: Rollback transaction, log error
   │
   └─> Catch: Exception
          └─> Action: Log error, return False

4. Context Managers Ensure:
   │
   ├─> WebDriver always closes (get_chrome_driver)
   │
   └─> Database connection always closes (get_sql_connection)
```

---

## 🎯 Design Patterns Used

1. **Context Manager Pattern**: For resource management (WebDriver, Database)
2. **Separation of Concerns**: Each module has a single responsibility
3. **Configuration Management**: Centralized in config.py
4. **Dependency Injection**: Config passed to modules
5. **Error Handling**: Try-except-finally at all levels
6. **Logging Strategy**: Comprehensive logging throughout





---

## End of Architecture Documentation
