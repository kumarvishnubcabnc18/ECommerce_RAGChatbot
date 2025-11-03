# recreate_index.py
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField
)
from config import SEARCH_ENDPOINT, SEARCH_API_KEY, SEARCH_INDEX_NAME

def recreate_index():
    index_client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=AzureKeyCredential(SEARCH_API_KEY))

    try:
        index_client.delete_index(SEARCH_INDEX_NAME)
        print(f"🗑️ Deleted old index: {SEARCH_INDEX_NAME}")
    except:
        print("ℹ️ No existing index found, creating a new one.")

    fields = [
        SimpleField(name="id", type="Edm.String", key=True),
        # ✅ Make product_name retrievable so it's returned in searches
        SearchableField(name="product_name", type="Edm.String", analyzer_name="en.lucene", retrievable=True),
        SimpleField(name="price", type="Edm.Double", filterable=True, sortable=True, facetable=True, retrievable=True)
    ]

    index = SearchIndex(name=SEARCH_INDEX_NAME, fields=fields)
    index_client.create_index(index)
    print(f"✅ Created new structured index with retrievable fields: {SEARCH_INDEX_NAME}")

if __name__ == "__main__":
    recreate_index()
