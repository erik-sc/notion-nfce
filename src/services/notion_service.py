import os
import datetime
from dotenv import load_dotenv
from notion_client import Client
from models.receipt import Receipt, ReceiptItem


class Notion:

    def __init__(self):
        load_dotenv()
        token = os.getenv("NOTION_TOKEN")
        database_id = os.getenv("NOTION_DATABASE_ID")

        if not token or not database_id:
            raise ValueError("NOTION_TOKEN e NOTION_DATABASE_ID must be defined in .env")

        self.client = Client(auth=token)
        self.database_id = database_id

    def get_receipt_tags(self):
        database = self.client.databases.retrieve(self.database_id)
        datasource = self.client.data_sources.retrieve(database['data_sources'][0]['id'])
        tags_property = datasource['properties'].get("Categoria")
        if not tags_property or tags_property["type"] != "select":
            return []

        return [option["name"] for option in tags_property["select"]["options"]]

    def add_receipt(self, receipt: Receipt):
        print("Adding receipt to Notion:")
        print(receipt)
        page = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Nome": {"title": [{"text": {"content": receipt.emitente}}]},
                "CNPJ": {"rich_text": [{"text": {"content": receipt.cnpj}}]},
                "Data de Emissão": {"date": {"start": self._format_date(receipt.data_emissao)}},
                "Quantidade": {"number": int(receipt.qtd_itens)},
                "Valor": {"number": self._parse_float(receipt.valor_total)},
                "Essencialidade": {"number": receipt.essencialidade},
                "URL": {"url": receipt.url}
            },
        )

        for item in receipt.itens:
            self.add_item_subpage(parent_page_id=page["id"], item=item)

        return page

    def add_item_subpage(self, parent_page_id: str, item: ReceiptItem):
        return self.client.pages.create(
            parent={"type": "database_id", "database_id": self.database_id},
            properties={
                "Parent item": {"relation": [{"id": parent_page_id}]},
                "Nome": {"title": [{"text": {"content": item.descricao}}]},
                "Quantidade": {"number": self._parse_float(item.quantidade)},
                "Valor Unitário": {"number": self._parse_float(item.valor_unitario)},
                "Valor": {"number": self._parse_float(item.valor_total)},
                "Categoria": {"select": {"name": item.categoria}},
            },
        )


    def _parse_float(self, value: str) -> float:
        try:
            return float(value.replace(".", "").replace(",", "."))
        except Exception:
            return 0.0

    def _format_date(self, date_str: str) -> str | None:
        try:
            dt = datetime.datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
            return dt.isoformat()
        except Exception:
            return None
