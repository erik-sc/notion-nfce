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

### Configuring the Notion Database

To properly log NFC-e invoices, you need to create a Notion database with the following structure:

**Parent Database (Invoices):**
- **Nome** (Title): The name of the issuer.
- **CNPJ** (Rich Text): The issuer's CNPJ number.
- **Data de Emissão** (Date): The issue date of the invoice.
- **Quantidade** (Number): Total number of items in the invoice.
- **Valor** (Number): Total value of the invoice.
- **Essencialidade** (Number): Optional field for priority/essentiality.

**Subpage Database (Items):**
- **Parent item** (Relation): Link to the parent invoice page.
- **Nome** (Title): Item description.
- **Quantidade** (Number): Quantity of the item.
- **Valor Unitário** (Number): Unit price of the item.
- **Valor** (Number): Total value of the item.
- **Categoria** (Select): Category of the item. You can predefine select options to organize items by type.

**Important Notes:**
1. Make sure to copy the **Database ID** and set it in your `.env` as `NOTION_DATABASE_ID`.
2. Create an integration in Notion and give it **full access** to the database.
3. Copy the **Integration Token** to your `.env` as `NOTION_TOKEN`.
4. Double-check that property names in Notion match exactly those used in the code (case-sensitive).

Once the database is ready and `.env` is configured, the script will automatically create invoice pages and item subpages in Notion.
