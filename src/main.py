from dotenv import load_dotenv
from services.qr_reader import capture_qr
from services.notion_service import Notion
from services.nfce_parser import NfceParser
from services.llm_client import LLMClient
from services.invoice_classifier import InvoiceClassifier

load_dotenv()

parser = NfceParser()
notion = Notion()
qr = capture_qr()

invoiceClassifier = InvoiceClassifier(LLMClient(), tags=notion.get_receipt_tags())

if qr:
    dados_nf = parser.parse_to_receipt(qr)
    classified_data = invoiceClassifier.classify(dados_nf)
    notion.add_receipt(classified_data)
    print("Invoice data created in Notion successfully.")
else:
    print("No QR Code detected.")