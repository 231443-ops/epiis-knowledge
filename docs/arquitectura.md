# Arquitectura del Chatbot EPIIS-UNSAAC

## Visión general

El chatbot es un sistema de pregunta-respuesta basado en **coincidencia de keywords** y **solapamiento de frases disparadoras**. No depende de modelos de lenguaje externos: todo el procesamiento es local y determinista, lo que facilita el mantenimiento y la trazabilidad de respuestas.

```
Usuario
  │
  ▼
ChatbotEPIIS.ask(pregunta)
  │
  ├─► IntentClassifier.classify(texto)
  │       │
  │       ├─ normalize_text() / tokenize()       [utils.py]
  │       ├─ keyword_score  (keywords.json)
  │       └─ trigger_score  (Jaccard sobre trigger_phrases)
  │
  └─► ResponseGenerator.generate(intent, conf)
          │
          └─ Índice plano intent → qa_entry      [data/*.json]
```

---

## Módulos

### `knowledge_loader.py`
Carga y centraliza todos los archivos JSON del proyecto.

| Método | Retorna |
|---|---|
| `load_intents()` | lista de intents con `id`, `prioridad`, `confianza_minima` |
| `load_keywords_mapping()` | lista de `{intent, keywords, trigger_phrases}` |
| `load_data_files()` | dict `{filename: contenido}` con todos los archivos de `data/` |

El mapeo entre prefijo de intent y archivo de datos está centralizado en `_INTENT_PREFIX_TO_FILE`.

### `intent_classifier.py`
Recibe texto libre y devuelve `(intent, confianza)`.

**Algoritmo de scoring (por intent):**
```
score = 0.65 × keyword_score + 0.35 × trigger_score

keyword_score = keywords_presentes_en_texto / total_keywords_del_intent
trigger_score = max(Jaccard(tokens_usuario, tokens_trigger_i) para todo trigger_i)
```
- Si el mejor `score` no supera `confianza_minima` del intent → retorna `(None, score)`.

### `response_generator.py`
Construye en `__init__` un índice plano `intent → qa_entry` recorriendo todos los `qa_entries` de los archivos de datos. Lookup O(1) en tiempo de respuesta.

### `chatbot.py`
Clase orquestadora `ChatbotEPIIS`. Expone:
- `ask(pregunta) → str` — para uso en producción / notebook
- `ask_debug(pregunta) → dict` — para tests y diagnóstico

### `utils.py`
Funciones de normalización de texto:
- `normalize_text()` — minúsculas + sin tildes + sin puntuación
- `tokenize()` — lista de tokens normalizados

---

## Flujo de clasificación

```
texto_usuario
    │
    ▼
normalize_text()
    │
    ├── keyword_score: ¿cuántos keywords del intent aparecen en el texto?
    │
    └── trigger_score: ¿cuánto se solapa con los ejemplos de trigger_phrases? (Jaccard)
          │
          ▼
   mejor intent → ¿supera confianza_minima?
          │
      Sí  │  No
          │   └── (None, score) → fallback genérico
          ▼
   ResponseGenerator.generate(intent)
          │
          └── qa_entry["respuesta"] + fuente
```

---

## Mapeo intent → archivo de datos

| Prefijo | Archivo |
|---|---|
| TUT, TTUT | `tutorias.json` |
| CUR | `malla_semestralizada.json` |
| ESP | `plan_estudios_resumen.json` |
| PPP | `practicas.json` |
| BIE | `bienestar.json` |
| MOV | `movilidad.json` |
| MAT | `matricula.json` |
| TIT | `titulacion.json` |
| SER | `servicios_academicos.json` |

---

## Extensión futura

Para agregar un nuevo dominio:
1. Crear `data/nuevo_modulo.json` con `qa_entries`.
2. Agregar el prefijo en `_INTENT_PREFIX_TO_FILE` (en `knowledge_loader.py` y `response_generator.py`).
3. Agregar los intents en `knowledge_base/intents.json`.
4. Agregar los keywords en `knowledge_base/keywords.json`.
5. Agregar casos de test en `tests/test_chatbot.py`.
