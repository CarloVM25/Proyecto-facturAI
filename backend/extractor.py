import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

from backend.ocr_engine import extract_text_from_file

load_dotenv()

_PROMPT_PATH = Path(__file__).parent.parent / "ai" / "prompts" / "extraction_prompt.txt"
_MODEL = "deepseek-chat"


def _load_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def extract_invoice_data(ocr_text: str) -> dict:
    """Call the DeepSeek API to extract structured invoice fields from OCR text."""
    prompt = _load_prompt().replace("{{invoice_text}}", ocr_text)

    client = OpenAI(
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model=_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = response.choices[0].message.content.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"DeepSeek returned invalid JSON: {response_text[:300]}"
        ) from exc


def process_invoice_file(file_path: str) -> dict:
    """Run OCR on a file, extract invoice data, and return an enriched result dict."""
    ocr_text = extract_text_from_file(file_path)
    invoice_data = extract_invoice_data(ocr_text)

    invoice_data["filename"] = Path(file_path).name
    invoice_data["processing_timestamp"] = datetime.utcnow().isoformat()
    invoice_data["ocr_text_length"] = len(ocr_text)

    return invoice_data
