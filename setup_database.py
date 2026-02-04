"""
SQL Server Database Setup Script
Run this to create the database and table
"""


CREATE_DATABASE_SQL = """
-- Create Database if it does not exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'CryptoData' )
BEGIN
    CREATE DATABASE CryptoData
    PRINT 'Database CryptoData created successfully';
END
ELSE
BEGIN
    PRINT 'Database CryptoData already exists';
END
GO

-- Use the Database
USE CryptoData;
GO
"""

CREATE_TABLE_SQL = """
-- Create CryptoCurrency table
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CryptoCurrency' AND xtype='U')
BEGIN
    CREATE TABLE CryptoCurrency (
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
    );
    
    PRINT 'Table CryptoCurrency created successfully';
END
ELSE
BEGIN
    PRINT 'Table CryptoCurrency already exists';
END
GO
"""

USEFUL_QUERIES = """
-- ========================================
-- USEFUL SQL QUERIES FOR DATA ANALYSIS
-- ========================================

-- 1. View Data ordered by rank

SELECT * FROM CryptoCurrency
ORDER BY scraped_at DESC,rank;

-- 2. Latest 10 records by date
SELECT TOP 10
    rank, name, price, one_hour_change, twenty_four_hour_change,
    seven_day_change, market_cap, volume_24h, scraped_at
FROM CryptoCurrency
ORDER BY scraped_at DESC , rank;

-- 3. Count Records by Scrape Date
SELECT CAST(scraped_at AS DATE) AS scrape_date,
       COUNT(*) AS total_records
FROM CryptoCurrency
GROUP BY CAST(scraped_at AS DATE)
ORDER BY scrape_date DESC;

-- 4. Top 10 cryptocurrencies by market cap (latest scrape)
SELECT TOP 10 
    rank, name, price, one_hour_change, twenty_four_hour_change,
    seven_day_change, market_cap, volume_24h, scraped_at
FROM CryptoCurrency
WHERE scraped_at = (SELECT MAX(scraped_at) FROM CryptoCurrency)
ORDER BY market_cap;

--5. Search Specific Crypto Currency

SELECT * FROM CryptoCurrency
WHERE name LIKE '%Bitcoin%'
ORDER BY scraped_at DESC, rank;

-- 6. DB stats

SELECT 
    COUNT(*) AS total_records,
    COUNT(DISTINCT name) as total_cryptos,
    COUNT(DISTINCT CAST(scraped_at AS DATE)) as total_scraped_days,
    MIN(scraped_at) AS first_scrape,
    MAX(scraped_at) AS last_scrape
FROM CryptoCurrency

-- 7. Top 10 Coins by twenty_four_hour_change.

SELECT TOP 10 *  
FROM CryptoCurrency ORDER BY  twenty_four_hour_change DESC;

"""

