from services.qr_reader import capture_qr
from services.notion_service import NotionService
from services.nfce_parser import NfceParser


parser = NfceParser()
notion = NotionService()
qr = capture_qr()

if qr:
    dados_nf = parser.parse_to_receipt(qr)
    notion.add_receipt(dados_nf)
    print("Nota adicionada no Notion!")
else:
    print("Nenhum QR Code detectado.")