flowchart TD
    A[Start] --> B[get_chrome_driver()]
    B --> C[scrape_coinmarketcap / scrape_coinmarketcap_all_pages]
    C --> D[Load CoinMarketCap URL]
    D --> E[scroll_to_load_content()]
    E --> F[BeautifulSoup(driver.page_source)]
    F --> G[parse_crypto_data()]
    G --> H{More Pages?}
    H -->|Yes| D
    H -->|No| I[Return crypto_data]
