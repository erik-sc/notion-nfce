import re
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

from models.receipt import Receipt, ReceiptItem


class NfceParser:

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def parse_to_receipt(self, url: str) -> Receipt:
        raw_data = self._fetch_and_parse(url)
        items = [ReceiptItem(**item) for item in raw_data.get("itens", [])]

        return Receipt(
            url=url,
            emitente=raw_data.get("emitente", ""),
            cnpj=raw_data.get("cnpj", ""),
            data_emissao=raw_data.get("data_emissao", ""),
            qtd_itens=raw_data.get("qtd_itens", ""),
            valor_total=raw_data.get("valor_total", ""),
            itens=items
        )

    def _fetch_and_parse(self, url: str) -> Dict[str, Any]:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        data = {
            "emitente": self._extract_emitente(soup),
            "cnpj": self._extract_cnpj(soup),
            "itens": self._extract_itens(soup),
            "valor_total": self._extract_valor_total(soup),
            "qtd_itens": self._extract_qtd_itens(soup),
            "data_emissao": self._extract_data_emissao(soup),
        }

        return {k: v for k, v in data.items() if v}

    def _extract_emitente(self, soup: BeautifulSoup) -> str:
        node = soup.find("div", {"id": "u20"})
        return node.text.strip() if node else ""

    def _extract_cnpj(self, soup: BeautifulSoup) -> str:
        node = soup.find("div", class_="text", string=lambda x: x and "CNPJ:" in x)
        return node.text.replace("CNPJ:", "").strip() if node else ""

    def _extract_itens(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        items = []
        table = soup.find("table", {"id": "tabResult"})
        if not table:
            return items

        for row in table.find_all("tr"):
            nome = row.find("span", class_="txtTit")
            qtd = row.find("span", class_="Rqtd")
            unit = row.find("span", class_="RvlUnit")
            total = row.find("span", class_="valor")

            items.append({
                "descricao": nome.text.strip() if nome else "",
                "quantidade": self._clean_label(qtd.text, "Qtde.:") if qtd else "",
                "valor_unitario": self._clean_label(unit.text, "Vl. Unit.:") if unit else "",
                "valor_total": total.text.strip() if total else "",
            })
        return items

    def _extract_valor_total(self, soup: BeautifulSoup) -> str:
        node = soup.find("span", class_="txtMax")
        return node.text.strip() if node else ""

    def _extract_qtd_itens(self, soup: BeautifulSoup) -> str:
        node = soup.find("span", class_="totalNumb")
        return node.text.strip() if node else ""

    def _extract_data_emissao(self, soup: BeautifulSoup) -> str:
        info = soup.find("div", {"id": "infos"})
        if not info:
            return ""
        return self._extract_emission_date(info)

    def _extract_emission_date(self, element: BeautifulSoup) -> str:
        text = element.get_text(" ", strip=True)
        match = re.search(r"Emissão:\s*([\d/]+\s+\d{2}:\d{2}:\d{2})", text)
        return match.group(1) if match else ""

    def _clean_label(self, text: str, label: str) -> str:
        return text.replace(label, "").strip()
