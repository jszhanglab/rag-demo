# app/services/chunk_service.py
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(structured_ocr_results: List[Dict[str, Any]], lang: str) -> List[Dict[str, Any]]:
    """
    Chunks structured OCR results while preserving page and coordinate metadata.
    """
    # 1. Choose separators based on language
    if lang == "zh":
        separators = ["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
    elif lang == "ja":
        separators = ["\n\n", "\n", "。", "！", "？", "、", " ", ""]
    else:
        separators = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]

    # 2. Reconstruct text while tracking offsets to map back to metadata
    # We combine all lines into a single string to use the splitter's logic,
    # but we need to know which page each character belongs to.
    full_text = ""
    offset_to_metadata = []

    for item in structured_ocr_results:
        start_pos = len(full_text)
        text = item["text"] + " " # Add space to prevent words from sticking
        full_text += text
        end_pos = len(full_text)
        
        offset_to_metadata.append({
            "start": start_pos,
            "end": end_pos,
            "page": item["page"],
            "bbox": item["bbox"]
        })

    # 3. Initialize the splitter
    from app.utils.config import settings
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.MAX_CHUNK_SIZE, # Recommended: 600
        chunk_overlap=settings.CHUNK_OVERLAP, # Recommended: 60
        add_start_index=True,
        separators=separators,
        length_function=len,
    )

    # 4. Create document chunks
    docs = text_splitter.create_documents([full_text])

    results = []
    for doc in docs:
        chunk_text = doc.page_content.strip()
        if len(chunk_text) < 10: # Skip noise
            continue

        start_idx = doc.metadata.get("start_index", 0)
        end_idx = start_idx + len(chunk_text)

        # 5. Find the primary page for this chunk
        # Since a chunk might span pages, we take the page of the first character
        associated_page = 1
        associated_bbox = []
        for meta in offset_to_metadata:
            if meta["start"] <= start_idx < meta["end"]:
                associated_page = meta["page"]
                associated_bbox = meta["bbox"]
                break

        results.append({
            "text": chunk_text,
            "start": start_idx,
            "end": end_idx,
            "page": associated_page,      # Critical for PDF navigation
            "bbox": associated_bbox,      # Critical for Highlighting
        })

    return results