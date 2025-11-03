# main.py
"""
Master script to run the full RAG E-Commerce Chatbot pipeline.
Steps:
1️⃣ Upload file to Azure Blob Storage
2️⃣ Recreate Azure Cognitive Search index
3️⃣ Extract products from PDF and upload to Search
4️⃣ Launch RAG-powered Chatbot UI
"""

import os
import time
import subprocess

print("🚀 Starting E-Commerce RAG Chatbot setup...\n")

# Step 1: Upload PDF to Azure Blob Storage
print("📦 Step 1: Uploading PDF to Azure Blob Storage...")
os.system("python storage_upload.py")
print("✅ File uploaded successfully.\n")

# Step 2: Recreate Azure Cognitive Search Index
print("🔄 Step 2: Recreating Search Index...")
os.system("python recreate_index.py")
print("✅ Search index ready.\n")

# Step 3: Extract products from PDF and upload to Azure Search
print("📄 Step 3: Extracting product data from PDF and uploading to Search...")
os.system("python pdf_to_search_upload.py")
print("✅ Products uploaded successfully.\n")

# Step 4: Launch Chatbot Interface
print("💬 Step 4: Launching Chatbot (Gradio interface)...\n")
time.sleep(2)
os.system("python rag_chatbot.py")

