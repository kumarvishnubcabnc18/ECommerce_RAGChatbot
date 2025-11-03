# search_index.py
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from config import SEARCH_ENDPOINT, SEARCH_API_KEY, SEARCH_INDEX_NAME

def create_index():
    index_client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT, 
        credential=AzureKeyCredential(SEARCH_API_KEY)
    )

    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        SearchableField(name="content", type="Edm.String", analyzer_name="en.lucene")
    ]

    index = SearchIndex(name=SEARCH_INDEX_NAME, fields=fields)

    try:
        index_client.create_index(index)
        print(f"✅ Created index {SEARCH_INDEX_NAME}")
    except Exception as e:
        print(f"⚠️ Index might already exist: {e}")

def upload_documents(docs):
    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT, 
        index_name=SEARCH_INDEX_NAME, 
        credential=AzureKeyCredential(SEARCH_API_KEY)
    )
    results = search_client.upload_documents(docs)
    print(f"✅ Uploaded {len(docs)} documents to {SEARCH_INDEX_NAME}")

if __name__ == "__main__":
    create_index()
    # Example: upload docs to your new ecommerce index
    sample_docs = [
        {"id": "1", "content": "Running Shoes, lightweight, breathable, Price $80"},
        {"id": "2", "content": "Smartwatch with heart rate monitor, Price $150"},
    ]
    upload_documents(sample_docs)

