# pdf_to_search_upload.py (updated)

import fitz  # PyMuPDF
import re
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from config import SEARCH_ENDPOINT, SEARCH_API_KEY, SEARCH_INDEX_NAME

def extract_products_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])

    products = []
    price_pattern = re.compile(r"\$([\d,]+(\.\d{1,2})?)")

    lines = text.split("\n")
    buffer = []
    for line in lines:
        if price_pattern.search(line):
            buffer.append(line)
            if len(buffer) >= 3:
                part_number = buffer[0].strip()
                description = buffer[1].strip()
                price_match = price_pattern.search(buffer[2])
                if price_match:
                    price_value = float(price_match.group(1).replace(",", ""))
                    name = f"{part_number} - {description}"
                    products.append({
                        "id": str(len(products) + 1),
                        "product_name": name,
                        "price": price_value
                    })
            buffer = []
        else:
            buffer.append(line)

    return products

def upload_to_search(products):
    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_API_KEY)
    )
    results = search_client.upload_documents(products)
    print(f"✅ Uploaded {len(products)} structured products to {SEARCH_INDEX_NAME}")

if __name__ == "__main__":
    file_path = "appleprice.pdf"
    products = extract_products_from_pdf(file_path)
    for p in products[:10]:
        print(p)
    upload_to_search(products)
    #print(f"📄 Extracted {len(products)} products from PDF")
    #upload_to_search(products)
