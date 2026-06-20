import fitz
import pytesseract
from PIL import Image, ImageEnhance
import tempfile
import os
from pathlib import Path

def extract_text_from_file(file_path: str) -> str:
    file_path = Path(file_path)
    if file_path.suffix.lower() != '.pdf':
        raise ValueError("Solo se aceptan archivos PDF")

    doc = fitz.open(str(file_path))

    # Step 1: try native text extraction
    native_text = ""
    for page in doc:
        native_text += page.get_text()

    if len(native_text.strip()) > 100:
        doc.close()
        return native_text

    # Step 2: fall back to pytesseract OCR for scanned/image PDFs
    full_text = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(dpi=300)
            img_path = os.path.join(tmp_dir, f"page_{page_num}.png")
            pix.save(img_path)

            img = Image.open(img_path)
            img = img.convert('L')
            img = ImageEnhance.Contrast(img).enhance(2.0)
            img = img.convert('RGB')

            text = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3')
            full_text.append(text)

    doc.close()
    return '\n'.join(full_text)
