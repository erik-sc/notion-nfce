## NFC-e to Notion Integration

Python project that parses Brazilian NFC-e (consumer electronic invoices) from a QR code and logs them into a Notion database.

### Features

- Reads NFC-e data from the QR code URL
- Extracts issuer, CNPJ, date, items, and totals
- Creates a page in Notion with all invoice data
- Creates subpages for each item

### Setup
1. Clone the repository
    ```bash
    git clone https://github.com/yourusername/nfce-notion.git
    cd nfce-notion
    ```
2. Create and setup your Virtual Environment
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```
3. Configure .ENV with Notion info
4. Run