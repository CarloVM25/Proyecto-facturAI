# FacturAI — Dossier de Proyecto
**Data Science con Python 2026-I — Universidad del Pacífico**
**Founder:** Carlo Valderrama Mondragón

---

## 1. One-liner
"Extraemos automáticamente los datos de facturas y boletas electrónicas peruanas en segundos para que contadores y pequeñas empresas olviden el tipeo manual."

## 2. Founder
- **Nombre:** Carlo Valderrama Mondragón
- **Rol en el proyecto:** Solo founder
- **Founder-market fit:** Estudiante de economía con experiencia en análisis de datos públicos (MEF, SUNAT) y construcción de pipelines de datos con Python y agentes de IA.
- **Cobertura de roles con IA:**
  - CTO/Backend: Claude Code generó y optimizó todo el pipeline de extracción
  - Frontend: Claude Code construyó la interfaz Streamlit
  - Data Science: DeepSeek API como motor de extracción estructurada
  - QA: Claude Code como agente de revisión y corrección de bugs

## 3. Problema
**¿Quién lo sufre?**
Contadores independientes, emprendedores con pequeños negocios y personas naturales en Perú que manejan facturas y boletas electrónicas.

**¿Qué tan doloroso?**
- Un contador puede manejar 50-200 facturas mensuales por cliente
- El tipeo manual de una factura toma entre 3-5 minutos
- Riesgo de error humano en montos, RUCs y fechas
- Tiempo perdido: hasta 10-15 horas mensuales solo en digitación

**¿Cómo lo resuelven hoy?**
- Excel manual (el más común)
- Digitación directa en software contable (CONTPAQi, CONTASIS)
- Tercerización a asistentes administrativos

**Evidencia:** 4 entrevistas con contadores, emprendedores y usuarios de finanzas personales confirmaron el pain point. Ver docs/research/entrevistas.md

## 4. Solución & Insight
**Solución:** FacturAI permite subir cualquier comprobante electrónico peruano en PDF, extrae automáticamente todos los campos relevantes usando PyMuPDF + DeepSeek AI, y exporta los datos a Excel listo para usar.

**Insight no obvio:** El 100% de los comprobantes electrónicos peruanos obligatorios (desde 2018 por SUNAT) ya están en formato PDF estructurado — no necesitan OCR de imagen. Esto permite una extracción perfecta sin los errores típicos del reconocimiento de imágenes.

## 5. Why Now?
- SUNAT completó la migración obligatoria a comprobantes electrónicos PDF en 2023
- LLMs como DeepSeek hacen la extracción estructurada accesible y barata (fracción de céntimo por factura)
- PyMuPDF permite extraer texto nativo de PDFs sin OCR, eliminando errores
- Streamlit Cloud permite desplegar en minutos sin infraestructura

## 6. Mercado
**TAM:** ~2.5 millones de empresas formales en Perú (SUNAT 2024) que emiten/reciben comprobantes electrónicos → mercado potencial de S/ 500M+ en software contable
**SAM:** ~300,000 pequeñas empresas y contadores independientes sin software contable integrado → S/ 60M
**SOM (12 meses):** 500 usuarios activos → S/ 30,000 MRR en plan básico

## 7. Competencia y Moat
| Alternativa | Limitación |
|---|---|
| Tipeo manual en Excel | Lento, propenso a errores |
| CONTPAQi / CONTASIS | Caro, complejo, requiere implementación |
| SUNAT Portal | Solo consulta, no exporta estructurado |
| Soluciones genéricas de OCR | No optimizadas para facturas peruanas |
| No hacer nada | Sigue perdiendo 10+ horas/mes |

**Moat:** Especialización en el formato exacto de comprobantes SUNAT + base de datos de patrones de emisores peruanos que se acumula con el uso.

## 8. Producto — Demo y Arquitectura
**URL pública:** https://facturai-mewesuqqkrk2udph4npajp.streamlit.app/

**Flujo del usuario:**
1. Sube PDF de factura/boleta electrónica
2. Clic en "Extraer Datos"
3. Revisa datos extraídos en tabs (Resumen, Items, Texto OCR)
4. Descarga Excel con datos estructurados

**Arquitectura:**
- Frontend: Streamlit (Python)
- OCR: PyMuPDF (extracción nativa de texto PDF)
- IA: DeepSeek API (deepseek-chat) para estructuración JSON
- Export: openpyxl (Excel con 2 hojas: Resumen + Items)
- Deploy: Streamlit Community Cloud

**Herramientas del curso usadas:**
1. PaddleOCR / pytesseract — OCR engine para PDFs escaneados (fallback)
2. DeepSeek API — LLM para extracción estructurada (equivalente a Claude/OpenAI APIs trabajadas en clase)
3. Streamlit — frontend y visualización

**Repositorio:** https://github.com/CarloVM25/facturAI

## 9. Modelo de Negocio
| Plan | Precio | Incluye |
|---|---|---|
| Free | S/ 0/mes | 20 facturas/mes |
| Starter | S/ 29/mes | 200 facturas/mes + soporte email |
| Pro | S/ 79/mes | Ilimitado + API access + soporte prioritario |

**Costo variable por factura:** ~S/ 0.01 (tokens DeepSeek)
**Contribution margin Plan Starter:** ~S/ 27/mes por usuario

## 10. Go-to-Market
- **Primeros 10 usuarios:** Red personal — contadores conocidos, emprendedores de entorno universitario
- **Primeros 100 usuarios:** Comunidades de contadores en Facebook (grupos como "Contadores del Perú" con +50k miembros), LinkedIn
- **Primeros 1,000 usuarios:** Alianza con colegios de contadores (CCPL), integración con SUNAT Portal, contenido en TikTok/YouTube mostrando el ahorro de tiempo

## 11. Tracción
- 4 entrevistas de validación con usuarios reales (ver docs/research/entrevistas.md)
- Demo funcional desplegado en Streamlit Cloud
- Probado con facturas reales de emisores peruanos (clínicas, servicios, comercio)

## 12. Roadmap
- **3 meses:** Soporte multi-factura (subir 10+ PDFs a la vez), integración con Google Sheets
- **6 meses:** API REST para integración con software contable existente, panel de historial de facturas
- **12 meses:** Fine-tuning de modelo con 100k+ facturas peruanas, integración directa con SUNAT SOL

## 13. Riesgos y Mitigación
| Riesgo | Mitigación |
|---|---|
| SUNAT cambia formato de PDFs | Arquitectura modular — solo actualizar el parser |
| DeepSeek sube precios o cierra | Prompt es portable a cualquier LLM (OpenAI, Claude, Gemini) |
| Solo founder — capacidad de ejecución | Claude Code como CTO virtual cubre el desarrollo; priorización estricta de features |

## 14. The Ask
Si tuviera 30 segundos con un inversionista de YC:
"Pedimos $50,000 para 12 meses de runway como solo founder. El dinero va a: infraestructura y créditos API ($5k), desarrollo de la API REST y panel multi-usuario ($30k), y GTM con colegios de contadores ($15k). El milestone que desbloquea: 500 usuarios pagos y S/ 30k MRR en 12 meses."
