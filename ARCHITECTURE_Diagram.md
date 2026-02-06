```mermaid
flowchart TD
    A(Start) --> B[get_chrome_driver]
    B --> C[Open CoinMarketCap]
    C --> D[Scroll & load]
    D --> E[Get page source]
    E --> F[Parse data]
    F --> G{More pages?}
    G -->|Yes| C
    G -->|No| H[Return data]
```
