import os
import json
import re
from pdfminer.high_level import extract_text

def clean_text(text: str) -> str:
    """
    Remove page number lines and extraneous blank lines.
    """
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        # Skip lines like "Page 3"
        if re.match(r'^\s*Page\s+\d+', line):
            continue
        cleaned.append(line.strip())
    return "\n".join(cleaned)

def chunk_text(text: str, max_chars: int = 1000, overlap: int = 100) -> list[str]:
    """
    Split the text into overlapping chunks of up to max_chars characters.
    """
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + max_chars, length)
        chunks.append(text[start:end])
        start += max_chars - overlap
    return chunks

def process_pdfs(input_dir: str = "data/rules", output_path: str = "data/index/chunks.json"):
    """
    Read all PDFs from input_dir, clean and chunk their text,
    and save the resulting chunks list to output_path as JSON.
    """
    chunks_list = []
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".pdf"):
            continue
        filepath = os.path.join(input_dir, filename)
        raw_text = extract_text(filepath)
        cleaned_text = clean_text(raw_text)
        for i, chunk in enumerate(chunk_text(cleaned_text)):
            chunks_list.append({
                "id": f"{os.path.splitext(filename)[0]}_{i}",
                "source": filename,
                "text": chunk
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks_list, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    process_pdfs()
