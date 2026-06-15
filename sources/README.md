# Fuentes Oficiales

Esta carpeta almacena los PDFs y documentos normativos que respaldan el contenido de `data/`. Sirven como trazabilidad: cualquier `respuesta` en un `qa_entry` debe poder referenciarse a uno de estos documentos.

## Documentos

| Archivo | Descripción | Usado en |
|---|---|---|
| `reglamento_tutorias.pdf` | Reglamento de Tutoría Académica UNSAAC — Res. N° CU-0220-2017-UNSAAC | `tutorias.json` |
| `plan_curricular_2024.pdf` | Plan Curricular 2024 EPIIS-UNSAAC (vigente desde año académico 2025) | `malla_semestralizada.json`, `plan_estudios_resumen.json` |
| `otros_pdfs/` | Documentos complementarios (reglamentos pendientes de incorporación) | `matricula.json`, `titulacion.json` |

## Documentos pendientes de obtener

- Reglamento de Matrícula UNSAAC (para completar `matricula.json`)
- Reglamento de Grados y Títulos UNSAAC (para completar `titulacion.json`)
- Reglamento de Prácticas Pre-Profesionales UNSAAC (para ampliar `practicas.json`)

## Nota

Los PDFs **no se versionan en Git** (están en `.gitignore`) por razones de tamaño y derechos de distribución. Solicítalos directamente a la Dirección de la EPIIS o al Vicerrectorado Académico de la UNSAAC.
