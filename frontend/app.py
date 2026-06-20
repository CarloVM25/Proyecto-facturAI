import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

import streamlit as st

st.set_page_config(
    page_title="FacturAI",
    page_icon="🧾",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Global */
    html, body, [data-testid="stAppViewContainer"] {
        background: #f8f9fc;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Header bar */
    .factur-header {
        background: #1a2744;
        padding: 2rem 2.5rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.75rem;
    }
    .factur-title {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        line-height: 1.1;
    }
    .factur-subtitle {
        color: #c8d0e4;
        font-size: 1.05rem;
        margin: 0 0 1rem 0;
    }
    .badge-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .badge {
        background: rgba(232, 184, 75, 0.18);
        color: #e8b84b;
        border: 1px solid rgba(232, 184, 75, 0.45);
        border-radius: 999px;
        padding: 0.2rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* Upload card */
    .upload-card {
        background: #ffffff;
        border: 2px dashed #cbd3e8;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .file-info {
        background: #eef1fb;
        border-left: 4px solid #1a2744;
        border-radius: 6px;
        padding: 0.6rem 0.9rem;
        font-size: 0.88rem;
        color: #1a2744;
        margin-bottom: 0.75rem;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background: #1a2744;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        font-size: 0.95rem;
        transition: background 0.18s;
    }
    .stButton > button:hover {
        background: #253660;
    }
    .stButton > button:active {
        background: #111c33;
    }
    .download-btn > button {
        background: #e8b84b !important;
        color: #1a2744 !important;
    }
    .download-btn > button:hover {
        background: #d4a43a !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1a2744;
    }
    [data-testid="stSidebar"] * {
        color: #c8d0e4 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e8b84b !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.15) !important;
    }

    /* Tabs */
    [data-testid="stTabs"] button[role="tab"] {
        font-weight: 600;
        color: #1a2744;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        border-bottom: 3px solid #e8b84b;
        color: #1a2744;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="factur-header">
        <p class="factur-title">🧾 FacturAI</p>
        <p class="factur-subtitle">
            Extrae datos de tus facturas y boletas peruanas en segundos
        </p>
        <div class="badge-row">
            <span class="badge">PDF</span>
            <span class="badge">Claude AI</span>
            <span class="badge">Exporta a Excel</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Cómo usar FacturAI")
    st.markdown(
        """
1. **Sube** tu comprobante en PDF
2. **Haz clic** en *Extraer Datos*
3. **Descarga** el archivo Excel con los datos estructurados
        """
    )
    st.markdown("---")
    st.markdown("### Formatos soportados")
    st.markdown("📄 **PDF (Factura Electrónica SUNAT)**")
    st.markdown("---")
    st.markdown("### Campos extraídos")
    st.markdown(
        """
- Tipo de documento
- Serie y número
- Fecha de emisión
- RUC y razón social (emisor y receptor)
- Moneda
- Subtotal, IGV y total
- Detalle de ítems (cantidad, descripción, precio unitario, subtotal)
        """
    )

# ── Session state defaults ────────────────────────────────────────────────────
for key, default in [
    ("extraction_result", None),
    ("excel_path", None),
    ("ocr_text", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Main layout ───────────────────────────────────────────────────────────────
left_col, right_col = st.columns([4, 6], gap="large")

# ─── LEFT: Upload & Process ───────────────────────────────────────────────────
with left_col:
    st.markdown("### Subir comprobante")

    uploaded_file = st.file_uploader(
        "Arrastra tu archivo aquí o haz clic para seleccionar",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        size_kb = len(uploaded_file.getvalue()) / 1024
        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb / 1024:.2f} MB"
        st.markdown(
            f'<div class="file-info">📎 <b>{uploaded_file.name}</b> &nbsp;·&nbsp; {size_str}</div>',
            unsafe_allow_html=True,
        )

        if st.button("Extraer Datos", key="btn_extract"):
            # ── Persist uploaded bytes before rerun ──
            file_bytes = uploaded_file.read()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            suffix = Path(uploaded_file.name).suffix
            safe_stem = "".join(
                c if c.isalnum() or c in "-_" else "_"
                for c in Path(uploaded_file.name).stem
            )
            saved_filename = f"{timestamp}_{safe_stem}{suffix}"

            samples_dir = Path(__file__).parent.parent / "data" / "samples"
            samples_dir.mkdir(parents=True, exist_ok=True)
            saved_path = samples_dir / saved_filename
            saved_path.write_bytes(file_bytes)

            outputs_dir = Path(__file__).parent.parent / "data" / "outputs"
            outputs_dir.mkdir(parents=True, exist_ok=True)
            excel_output = str(outputs_dir / f"{timestamp}_{safe_stem}.xlsx")

            try:
                with st.spinner("Procesando documento..."):
                    with st.status("Extrayendo datos del comprobante...", expanded=True) as status:
                        st.write("Extrayendo texto del PDF...")
                        from backend.ocr_engine import extract_text_from_file
                        ocr_text = extract_text_from_file(str(saved_path))

                        st.write("Analizando con Claude AI...")
                        from backend.extractor import extract_invoice_data
                        result = extract_invoice_data(ocr_text)
                        result["filename"] = uploaded_file.name
                        result["processing_timestamp"] = datetime.utcnow().isoformat()
                        result["ocr_text_length"] = len(ocr_text)

                        st.write("Estructurando datos...")
                        from backend.excel_exporter import export_to_excel
                        export_to_excel(result, excel_output)

                        status.update(label="Extracción completada", state="complete")

                st.session_state.extraction_result = result
                st.session_state.excel_path = excel_output
                st.session_state.ocr_text = ocr_text
                st.success("¡Datos extraídos correctamente!")

            except Exception as exc:
                st.error(f"Error durante el procesamiento: {exc}")

    if st.session_state.excel_path and Path(st.session_state.excel_path).exists():
        excel_bytes = Path(st.session_state.excel_path).read_bytes()
        excel_filename = Path(st.session_state.excel_path).name
        st.markdown('<div class="download-btn">', unsafe_allow_html=True)
        st.download_button(
            label="⬇️  Descargar Excel",
            data=excel_bytes,
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="btn_download",
        )
        st.markdown("</div>", unsafe_allow_html=True)

# ─── RIGHT: Results ───────────────────────────────────────────────────────────
with right_col:
    if st.session_state.extraction_result is None:
        st.markdown(
            """
            <div style="
                height: 340px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: #ffffff;
                border-radius: 10px;
                border: 1.5px solid #e2e6f0;
                color: #8a94b0;
                font-size: 1rem;
            ">
                <div style="font-size: 3rem; margin-bottom: 0.75rem;">📋</div>
                <div>Los datos extraídos aparecerán aquí</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        result = st.session_state.extraction_result
        tab_resumen, tab_items, tab_ocr = st.tabs(
            ["📋 Resumen", "📦 Items", "🔍 Texto OCR"]
        )

        with tab_resumen:
            resumen_fields = [
                ("Tipo de documento",     result.get("tipo_documento")),
                ("Serie y número",        result.get("serie_numero")),
                ("Fecha de emisión",      result.get("fecha_emision")),
                ("RUC emisor",            result.get("ruc_emisor")),
                ("Razón social emisor",   result.get("razon_social_emisor")),
                ("RUC receptor",          result.get("ruc_receptor")),
                ("Razón social receptor", result.get("razon_social_receptor")),
                ("Moneda",                result.get("moneda")),
                ("Subtotal",              result.get("subtotal")),
                ("IGV",                   result.get("igv")),
                ("Total",                 result.get("total")),
                ("Archivo",               result.get("filename")),
                ("Procesado (UTC)",       result.get("processing_timestamp")),
            ]

            import pandas as pd
            df_resumen = pd.DataFrame(resumen_fields, columns=["Campo", "Valor"])
            df_resumen["Valor"] = df_resumen["Valor"].fillna("—")

            st.dataframe(
                df_resumen,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Campo": st.column_config.TextColumn("Campo", width="medium"),
                    "Valor": st.column_config.TextColumn("Valor", width="large"),
                },
            )

        with tab_items:
            items = result.get("descripcion_items") or []
            if items:
                df_items = pd.DataFrame(items)
                col_rename = {
                    "cantidad": "Cantidad",
                    "descripcion": "Descripción",
                    "precio_unitario": "Precio Unitario",
                    "subtotal": "Subtotal",
                }
                df_items = df_items.rename(columns=col_rename)
                st.dataframe(df_items, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron ítems en este comprobante.")

        with tab_ocr:
            ocr_text = st.session_state.ocr_text or ""
            st.text_area(
                "Texto extraído por OCR",
                value=ocr_text,
                height=320,
                disabled=True,
                label_visibility="collapsed",
            )
