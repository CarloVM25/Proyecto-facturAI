# 🧾 FacturAI

Extrae automáticamente los datos de facturas y boletas electrónicas peruanas en segundos.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![DeepSeek](https://img.shields.io/badge/AI-DeepSeek-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Demo en vivo
URL: https://facturai-mewesuqqkrk2udph4npajp.streamlit.app/

## One-liner
Extraemos automáticamente los datos de facturas y boletas electrónicas peruanas en segundos para que contadores y pequeñas empresas olviden el tipeo manual.

## Problema que resuelve
Contadores, emprendedores y personas naturales en Perú pierden entre 10-15 horas mensuales digitando manualmente datos de facturas en Excel. FacturAI elimina ese proceso completamente.

## Arquitectura

PDF (Factura/Boleta SUNAT) → PyMuPDF (extracción nativa de texto) → DeepSeek API (estructuración JSON) → Streamlit Dashboard → Excel (Resumen + Items)

## Herramientas del curso utilizadas

- PyMuPDF + pytesseract: OCR engine para extracción de texto de PDFs
- DeepSeek API (LLM): Extracción estructurada JSON, equivalente a Claude/OpenAI APIs vistas en clase
- Streamlit: Frontend completo y despliegue
- Claude Code: CTO virtual, generó y optimizó todo el código

## Estructura del repositorio

```
facturAI/
├── frontend/app.py
├── backend/extractor.py
├── backend/ocr_engine.py
├── backend/excel_exporter.py
├── ai/prompts/extraction_prompt.txt
├── data/samples/
├── data/outputs/
├── docs/research/entrevistas.md
├── docs/dossier.md
├── .github/workflows/ci.yml
├── .env.example
├── packages.txt
└── requirements.txt
```

## Instalación local

```bash
git clone https://github.com/CarloVM25/facturAI.git
cd facturAI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Add DEEPSEEK_API_KEY to .env
streamlit run frontend/app.py
```

> **Note:** Install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki

## Modelo de negocio

| Plan | Precio | Facturas |
|---|---|---|
| Free | S/ 0/mes | 20 facturas |
| Starter | S/ 29/mes | 200 facturas |
| Pro | S/ 79/mes | Ilimitado |

## Validación

4 entrevistas con contadores, emprendedores y usuarios de finanzas personales confirmaron el pain point. Ver [docs/research/entrevistas.md](docs/research/entrevistas.md)

## Roadmap

- **3 meses:** Soporte multi-factura, integración Google Sheets
- **6 meses:** API REST para software contable
- **12 meses:** Fine-tuning con 100k+ facturas peruanas

## Uso de IA en el desarrollo

Proyecto construido como solo founder con Claude Code como CTO virtual:
- Backend y OCR engine: generado y optimizado con Claude Code
- Frontend Streamlit: construido con Claude Code
- Debugging y fixes: resueltos con Claude Code

## Licencia
MIT

## Autor
Carlo Valderrama Mondragón — Universidad del Pacífico, 2026
