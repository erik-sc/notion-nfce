from copy import copy
import json
from typing import List

from services.llm_client import LLMClient
from prompts.invoice_prompts import BULK_CATEGORY_PROMPT, ESSENTIALITY_PROMPT
from models.receipt import Receipt


class InvoiceClassifier:
    
    def __init__(self, llm_client: LLMClient, tags: List[str]):
        self.llm = llm_client
        self.tags = tags

    def classify(self, receipt) -> Receipt:
        classified_receipt = copy(receipt)
        item_names = [item.descricao for item in receipt.itens]
        
        item_categories_map = self.get_category_bulk(item_names)
        for item in classified_receipt.itens:
            item.categoria = item_categories_map.get(item.descricao, "Outros")

        classified_receipt.essencialidade = self.get_essentiality(item_names)

        return classified_receipt

    def get_category_bulk(self, item_list: List[str]) -> dict:
        prompt = BULK_CATEGORY_PROMPT.format(tags=", ".join(self.tags), items=", ".join(item_list))
        categories: str = self.llm.complete(prompt)
        print(categories)
        return json.loads(categories)

    def get_essentiality(self, item_list: List[str]) -> float:
        prompt = ESSENTIALITY_PROMPT.format(items=", ".join(item_list))
        try:
            value = float(self.llm.complete(prompt))
            print(value)
        except Exception:
            value = 0.0
        return max(0.0, min(10.0, value))
