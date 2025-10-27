from copy import copy
from typing import List

from services.llm_client import LLMClient


class InvoiceClassifier:
    CATEGORY_PROMPT = (
        "Classify the following purchase item into one of these categories: {tags}.\n"
        "Item: \"{item}\"\n"
        "Return only the category name."
    )

    ESSENTIALITY_PROMPT = (
        "On a scale from 0 to 10, rate how essential the purchase was. "
        "0 = not essential, 10 = very essential.\n"
        "Guidelines:\n"
        "- If the item is unknown or unfamiliar, assign a lower essentiality.\n"
        "- If the item is food, consider if it is highly processed, expensive, or a luxury item when assigning essentiality.\n"
        "- Always return only a single number between 0 and 10.\n"
        "Items: \"{items}\""
    )

    def __init__(self, llm_client: LLMClient, tags: List[str]):
        self.llm = llm_client
        self.tags = tags

    def classify(self, receipt) -> None:
        classified_receipt = copy(receipt)
        for item in receipt.itens:
            item.categoria = self.get_category(item.descricao)

        item_names = [item.descricao for item in receipt.itens]
        classified_receipt.essencialidade = self.get_essentiality(item_names)

        return classified_receipt
    
    def get_category(self, item_name: str) -> str:
        prompt = self.CATEGORY_PROMPT.format(tags=", ".join(self.tags), item=item_name)
        category = self.llm.complete(prompt)
        return category if category in self.tags else "Other"

    def get_essentiality(self, item_list: List[str]) -> float:
        prompt = self.ESSENTIALITY_PROMPT.format(items=", ".join(item_list))
        try:
            value = float(self.llm.complete(prompt))
            print(value)
        except Exception:
            value = 0.0
        return max(0.0, min(10.0, value))
