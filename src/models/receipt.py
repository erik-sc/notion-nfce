from dataclasses import dataclass
from typing import List

@dataclass
class ReceiptItem:
    descricao: str
    quantidade: str
    valor_unitario: str
    valor_total: str

@dataclass
class Receipt:
    emitente: str
    cnpj: str
    data_emissao: str
    qtd_itens: str
    valor_total: str
    itens: List[ReceiptItem]