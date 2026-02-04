# CoinMarketCap Scraper - System Architecture

This document describes the architecture of the CoinMarketCap Cryptocurrency Scraper system.

## 🏗️ Component Architecture

┌─────────────────────────────────────────────────────────────────────────┐
│                        COINMARKETCAP SCRAPER SYSTEM                     │
└─────────────────────────────────────────────────────────────────────────┘
flowchart TD
    subgraph Entry ["COINMARKETCAP SCRAPER SYSTEM"]
        direction TB
        A["main.py (Entry)"] --> B["config.py (Settings)"]
        A --> C["scraper.py (Scrape)"]
        A --> D["database.py (Store)"]
        C --> E["External Services"]
        D --> F["SQL Server Database"]
        F --> G["utils.py (Analysis, Optional)"]
    end



