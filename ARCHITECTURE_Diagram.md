flowchart LR
    A[Start] --> B[get_chrome_driver]
    B --> C[Open CoinMarketCap URL]
    C --> D[scroll_to_load_content]
    D --> E[Get page_source]
    E --> F[parse_crypto_data]
    F --> G{More Pages?}
    G -->|Yes| C
    G -->|No| H[Return crypto_data]
