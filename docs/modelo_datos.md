# Modelo de Datos — Chatbot EPIIS-UNSAAC

## Estructura general de un archivo `data/*.json`

```json
{
  "version": "1.0.0",
  "categoria_id": "TUT",
  "nombre": "...",
  "estado": "completo | en_construccion",
  "fuentes_normativas": ["..."],
  "contenido": { /* datos fuente estructurados */ },
  "qa_entries": [
    {
      "id": "TUT-001",
      "intent": "consulta_tutoria_definicion",
      "pregunta": "¿Qué es la tutoría académica?",
      "respuesta": "...",
      "fuente": "Art. 3°"
    }
  ]
}
```

### Campos obligatorios

| Campo | Tipo | Descripción |
|---|---|---|
| `version` | string | Versión semántica del archivo |
| `categoria_id` | string | Prefijo usado en los IDs (TUT, CUR, PPP…) |
| `nombre` | string | Nombre legible del módulo |
| `qa_entries` | array | Lista de pares pregunta-respuesta indexados por intent |

### Campos opcionales

| Campo | Tipo | Descripción |
|---|---|---|
| `estado` | string | `"completo"` o `"en_construccion"` |
| `_nota_modulo` | string | Nota interna para el mantenedor |
| `_pendiente` | string | (dentro de qa_entry) Información a completar |

---

## `knowledge_base/intents.json`

```json
{
  "project": "...",
  "version": "...",
  "global_config": { "min_confidence_global": 0.70 },
  "intents": [
    {
      "id": "TUT-001",
      "intent": "consulta_tutoria_definicion",
      "prioridad": "Alta",
      "confianza_minima": 0.85
    }
  ]
}
```

**Prioridades válidas:** `Muy Alta`, `Alta`, `Media`, `Baja`

**Regla de ID:** `{PREFIJO}-{NNN}` donde el prefijo corresponde a la categoría
y NNN es un número de tres dígitos correlativo dentro de la categoría.

---

## `knowledge_base/keywords.json`

```json
{
  "keywords_mapping": [
    {
      "intent": "consulta_tutoria_definicion",
      "keywords": ["tutoría", "qué es"],
      "trigger_phrases": [
        "¿En qué consiste la tutoría?",
        "¿Cómo funciona la tutoría universitaria?"
      ]
    }
  ]
}
```

- **`keywords`**: términos clave cortos (1-3 palabras). El clasificador busca su presencia normalizada en el texto del usuario.
- **`trigger_phrases`**: frases de ejemplo completas. Se usan para calcular solapamiento Jaccard con la consulta del usuario.

---

## `corpus/corpus_consultas.json`

Archivo de evaluación. No se carga en producción; se usa para medir la calidad del clasificador.

```json
{
  "consultas": [
    {
      "texto": "¿En qué consiste la tutoría académica?",
      "intent_esperado": "consulta_tutoria_definicion",
      "registro": "formal | informal | con_errores",
      "origen": "derivado_trigger_phrases | encuesta_estudiantes | ..."
    }
  ]
}
```

---

## Inventario de archivos de datos

| Archivo | Prefijos | Estado |
|---|---|---|
| `tutorias.json` | TUT, TTUT | completo |
| `malla_semestralizada.json` | CUR | completo |
| `plan_estudios_resumen.json` | ESP | completo |
| `practicas.json` | PPP | completo |
| `bienestar.json` | BIE | verificar |
| `movilidad.json` | MOV | verificar |
| `matricula.json` | MAT | en_construccion |
| `titulacion.json` | TIT | en_construccion |
| `servicios_academicos.json` | SER | verificar |
