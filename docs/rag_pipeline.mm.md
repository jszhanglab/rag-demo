# 🧠 RAG Demo Pipeline (v1)

## 🟣 Step 1. OCR & Text Extraction
- 🧰 **Model**: PaddleOCR
- 🈶 **Support**: Chinese / Japanese / vertical layout
- 🧾 **Output**: clean text, page metadata

## 🔵 Step 2. Chunking
- 🧰 **Tool**: RecursiveCharacterTextSplitter
- ⚙️ **Params**: 500–800 tokens / overlap 50–100
- 📦 **Output**: structured chunks with doc_id, page, offset

## 🟢 Step 3. Embedding
- 🧰 **Model**: SentenceTransformers (all-MiniLM-L6-v2)
- 🔄 **Batch process**: multiprocessing enabled
- 🪣 **Save to**: ChromaDB (namespace by user_id)

## 🟠 Step 4. Retrieval
- ⚙️ **Method**: cosine similarity top-k
- 🧰 **Option**: BM25 hybrid search (next version)
- 📊 **Output**: top evidence + score + metadata

## 🔴 Step 5. Generation & Citation
- 🧰 **LLM**: GPT-4-mini / local model
- 🧩 **Template**: must include citations `[1][2]`
- 📚 **Sidebar**: evidence list with page + score
