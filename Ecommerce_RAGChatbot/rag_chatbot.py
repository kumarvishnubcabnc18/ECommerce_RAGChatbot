# rag_chatbot.py
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import gradio as gr
from openai import AzureOpenAI
from config import SEARCH_ENDPOINT, SEARCH_API_KEY, SEARCH_INDEX_NAME, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_DEPLOYMENT

class RAGChatbot:
    def __init__(self):
        self.search_client = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=SEARCH_INDEX_NAME, credential=AzureKeyCredential(SEARCH_API_KEY))
        self.client = AzureOpenAI(api_key=AZURE_OPENAI_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, api_version="2024-12-01-preview")

    # inside retrieve_docs() of RAGChatbot
    def retrieve_docs(self, query):
        query_lower = query.lower()
        select_fields = ["product_name", "price"]

        if "cheapest" in query_lower or "lowest" in query_lower:
            results = self.search_client.search(
            search_text="*",
            top=1,
            order_by=["price asc"],
            select=select_fields
        )
        elif "most expensive" in query_lower or "highest" in query_lower:
            results = self.search_client.search(
            search_text="*",
            top=1,
            order_by=["price desc"],
            select=select_fields
        )
        else:
            results = self.search_client.search(
            search_text=query,
            top=5,
            select=select_fields
        )

        docs = []
        for doc in results:
            name = doc.get("product_name", "Unknown Product")
            price = doc.get("price", "N/A")
            docs.append(f"{name} - ${price}")
        return docs

    def generate_answer(self, query):
        docs = self.retrieve_docs(query)

    # If no docs found
        if not docs:
            return "No matching product found."

    # Join retrieved items
        context = "\n".join(docs)

    # System prompt clearly explains how to format the answer
        system_prompt = (
        "You are an e-commerce assistant. Use the provided product catalog context to answer the user's query. "
        "Each line contains a product name and price. "
        "Always include both the product name and its price in your answer. "
        "Do not invent or guess any information beyond what appears in the context."
        )

        response = self.client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User question: {query}\n\nCatalog context:\n{context}"}
        ]
    )

        return response.choices[0].message.content

bot = RAGChatbot()

def chat_with_bot(user_input):
    return bot.generate_answer(user_input)

demo = gr.Interface(
    fn=chat_with_bot,
    inputs=gr.Textbox(lines=2, placeholder="Ask about products..."),
    outputs="text",
    title="🛍️ RAG-Powered E-Commerce Chatbot",
    description="Ask about the cheapest, most expensive, or specific products from the catalog."
)

demo.launch() 

