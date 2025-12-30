# app/services/chunk_service.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.utils.config import settings

def chunk_text(ocr_text: str,lang: str) -> list:
    if lang == "zh":
        separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    elif lang == "ja":
        separators = ["\n\n", "\n", "。", "！", "？", "、", " ", ""]
    else:
        separators = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.MAX_CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        add_start_index=True,
        separators=separators,
        length_function=len, #Control chunk length by character count (len) or token count (token)
    )
    docs = text_splitter.create_documents([ocr_text])

    results = []
    for doc in docs:
        start_offset = doc.metadata.get("start_index")
        end_offset = start_offset + len(doc.page_content)
        results.append({
            "text": doc.page_content,
            "start": start_offset,
            "end": end_offset
        })

    return results