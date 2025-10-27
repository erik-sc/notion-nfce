from copy import copy
import json
from typing import List

from services.llm_client import LLMClient


class InvoiceClassifier:
    BULK_CATEGORY_PROMPT = (
        "Classify the following purchase items into one of these categories: {tags}.\n"
        "Items: \"{items}\"\n"
        "Return a dictionary mapping each item to its category."
        "Example output: {{\"item1\": \"category1\", \"item2\": \"category2\"}}"
        "Always return valid JSON ready to be parsed, without any markdown or other text around it."
    )

    ESSENTIALITY_PROMPT = (
        "On a scale from 0 to 10, rate how essential the purchase was. "
        "0 = not essential, 10 = very essential.\n"
        "Items: \"{items}\""
        "Guidelines:\n"
        "- If the item is unknown or unfamiliar, assign a lower essentiality.\n"
        "- If the item is food, consider if it is highly processed, expensive, or a luxury item when assigning essentiality.\n"
        "- Always return only a single number between 0 and 10.\n"
        "Do not return any additional text or explanations."
    )

    def __init__(self, llm_client: LLMClient, tags: List[str]):
        self.llm = llm_client
        self.tags = tags

    def classify(self, receipt) -> None:
        classified_receipt = copy(receipt)
        item_names = [item.descricao for item in receipt.itens]
        
        item_categories_map = self.get_category_bulk(item_names)
        for item in classified_receipt.itens:
            item.categoria = item_categories_map.get(item.descricao, "Outros")

        classified_receipt.essencialidade = self.get_essentiality(item_names)

        return classified_receipt

    def get_category_bulk(self, item_list: List[str]) -> dict:
        prompt = self.BULK_CATEGORY_PROMPT.format(tags=", ".join(self.tags), items=", ".join(item_list))
        categories: str = self.llm.complete(prompt)
        print(categories)
        return json.loads(categories)

    def get_essentiality(self, item_list: List[str]) -> float:
        prompt = self.ESSENTIALITY_PROMPT.format(items=", ".join(item_list))
        try:
            value = float(self.llm.complete(prompt))
            print(value)
        except Exception:
            value = 0.0
        return max(0.0, min(10.0, value))
