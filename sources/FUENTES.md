# Fuentes Oficiales

Esta carpeta almacena los documentos normativos oficiales de la UNSAAC que respaldan el contenido de `data/`. Sirven como **trazabilidad**: cada `respuesta` de un `qa_entry` cita el artículo o documento del que proviene.

## Documentos disponibles

| Archivo | Documento | Respalda |
|---|---|---|
| `000_RegAcademicoUNSAAC2017(CU-093-2017-UNSAAC).pdf` | Reglamento Académico UNSAAC — Res. N° CU-093-2017-UNSAAC | `matricula.json` (Art. 1°–38°), `titulacion.json` (Art. 117°–157°), `malla_semestralizada.json` (créditos y desaprobación) |
| `ReglamentoTutoriaAcademica.pdf` | Reglamento de Tutoría Académica UNSAAC | `tutorias.json` |
| `Plan_de_estudios_y_Malla_curricular.pdf` | Plan de Estudios y Malla Curricular EPIIS | `malla_semestralizada.json`, `plan_estudios_resumen.json` |
| `plan-estudios-ing-informatica-2025.pdf` | Plan de Estudios de Ingeniería Informática y de Sistemas (vigente desde el año académico 2025) | `malla_semestralizada.json`, `plan_estudios_resumen.json` |

## Fuentes sin PDF en esta carpeta

Algunos módulos de `data/` se basan en información institucional publicada por oficinas de la UNSAAC o en normas nacionales, no en un PDF incluido aquí:

| Archivo | Fuente |
|---|---|
| `bienestar.json` | Dirección de Bienestar Universitario (comedor, becas, residencia, orientación psicológica, deportes) |
| `movilidad.json` | Oficina de Relaciones Internacionales UNSAAC · Programa PAME-UDUAL |
| `servicios_academicos.json` | DRAA · DTI · Biblioteca Central · Aula Virtual (Moodle) · Portal SERUNSA |
| `practicas.json` | Reglamento de Prácticas Pre-Profesionales UNSAAC · Ley N° 28518 · Decreto Legislativo N° 1401 |
