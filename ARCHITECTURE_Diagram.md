```mermaid
flowchart TD
    A[Start] --> B[Get Chrome Driver]
    B --> C[Scrape CoinMarketCap]
    C --> D[Load CoinMarketCap URL]
    D --> E[Scroll to Load Content]
    E --> F[Parse Page Source]
    F --> G[Extract Crypto Data]
    G --> H{More Pages?}
    H -->|Yes| D
    H -->|No| I[Return Crypto Data]
```


