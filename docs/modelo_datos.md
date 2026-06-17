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

| Archivo | Prefijos | Entradas | Estado |
|---|---|---|---|
| `tutorias.json` | TUT, TTUT | 20 | completo |
| `matricula.json` | MAT | 10 | completo |
| `servicios_academicos.json` | SER | 10 | completo |
| `practicas.json` | PPP | 10 | completo |
| `bienestar.json` | BIE | 10 | completo |
| `movilidad.json` | MOV | 10 | completo |
| `titulacion.json` | TIT | 10 | completo |
| `malla_semestralizada.json` | CUR | 10 | completo |
| `plan_estudios_resumen.json` | ESP | 10 | completo |
| `inicio_clases.json` | CLA | 4 | completo |
| `silabos.json` | SIL | 4 | completo |

**Total:** 11 archivos, **108 qa_entries**

---

## Estadísticas del corpus

- **Categorías:** 11 módulos temáticos
- **Total de pares pregunta-respuesta:** 108 entradas
- **Intents únicos:** 109 (definidos en `knowledge_base/intents.json`)
- **Cobertura temática:**
  - Tutorías y apoyo académico: 20 entradas
  - Procesos administrativos (matrícula, titulación): 20 entradas
  - Servicios estudiantiles (bienestar, movilidad, servicios): 30 entradas
  - Plan de estudios (cursos, especialidades, clases, sílabos): 38 entradas
