# Arquitectura del Chatbot EPIIS-UNSAAC

## Visión general

El chatbot es un sistema de pregunta-respuesta basado en **Similitud Coseno** sobre representaciones vectoriales TF (Term Frequency) del texto. No depende de modelos de lenguaje externos: todo el procesamiento es local y determinista, lo que facilita el mantenimiento y la trazabilidad de respuestas.

```
Usuario
  │
  ▼
ChatbotEPIIS.ask(pregunta)
  │
  ├─► IntentClassifier.classify(texto)
  │       │
  │       ├─ normalize_text() / tokenize()       [utils.py]
  │       ├─ compute_tf_vector() para query
  │       ├─ compute_tf_vector() para cada intent (keywords + trigger_phrases)
  │       └─ cosine_similarity(query_vec, intent_vec)
  │             Fórmula: sim(Q,D) = (Σ Q_i*D_i) / (√(Σ Q_i²) * √(Σ D_i²))
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
Recibe texto libre y devuelve `(intent, confianza)` usando **Similitud Coseno**.

**Algoritmo de clasificación:**

1. **Pre-procesamiento** (método `_prepare`):
   - Para cada intent, combina sus keywords y trigger_phrases en un "documento de referencia"
   - Tokeniza y normaliza el documento
   - Calcula el vector TF (Term Frequency): `TF(término) = freq_término / total_términos`
   - Almacena el vector de referencia para cada intent

2. **Clasificación** (método `classify`):
   - Tokeniza y vectoriza la consulta del usuario (vector TF)
   - Calcula similitud coseno entre el vector de la consulta y cada vector de referencia:
     ```
     similitud(Q, D) = (Σ Q_i * D_i) / (√(Σ Q_i²) * √(Σ D_i²))
     ```
   - Retorna el intent con mayor similitud si supera el umbral (threshold=0.5)
   - Si ninguno supera el umbral → retorna `(None, score)`

**Propiedades de la similitud coseno:**
- Rango: [0.0, 1.0]
- 0.0 = vectores ortogonales (sin términos comunes)
- 1.0 = vectores idénticos (misma dirección)
- Invariante a la longitud del documento (normalización automática)

### `response_generator.py`
Construye en `__init__` un índice plano `intent → qa_entry` recorriendo todos los `qa_entries` de los archivos de datos. Lookup O(1) en tiempo de respuesta.

### `chatbot.py`
Clase orquestadora `ChatbotEPIIS`. Expone:
- `ask(pregunta) → str` — para uso en producción / notebook
- `ask_debug(pregunta) → dict` — para tests y diagnóstico

### `utils.py`
Funciones de normalización y análisis vectorial:
- `normalize_text()` — minúsculas + sin tildes + sin puntuación
- `tokenize()` — lista de tokens normalizados
- `compute_tf_vector(tokens)` — calcula vector TF (Term Frequency)
- `cosine_similarity(vec1, vec2)` — similitud coseno entre dos vectores TF

---

## Flujo de clasificación

```
texto_usuario
    │
    ▼
normalize_text() + tokenize()
    │
    ▼
compute_tf_vector(tokens_usuario)
    │              vector Q
    ▼
Para cada intent:
    ├── Recuperar vector_referencia (pre-calculado)
    │              vector D
    ▼
    cosine_similarity(Q, D)
          │
          ▼
   mejor intent → ¿similitud >= threshold?
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
| CLA | `inicio_clases.json` |
| SIL | `silabos.json` |

**Total:** 11 archivos de datos, 108 qa_entries

---

## Ventajas de la similitud coseno

1. **Semántica básica**: Captura relaciones de co-ocurrencia de términos
2. **Invariante a longitud**: Un documento largo y uno corto con los mismos términos tienen alta similitud
3. **Eficiente**: Pre-cálculo de vectores en `__init__`, clasificación O(n × m) donde n=num_intents, m=dim_vocabulario
4. **Interpretable**: Score entre 0 y 1, fácil de visualizar y diagnosticar

---

## Extensión futura

Para agregar un nuevo dominio:
1. Crear `data/nuevo_modulo.json` con `qa_entries`.
2. Agregar el prefijo en `_INTENT_PREFIX_TO_FILE` (en `knowledge_loader.py` y `response_generator.py`).
3. Agregar los intents en `knowledge_base/intents.json`.
4. Agregar los keywords y trigger_phrases en `knowledge_base/keywords.json`.
5. Agregar casos de test en `tests/test_chatbot.py`.

### Mejoras del clasificador

Para mejorar la precisión:
- **TF-IDF** en lugar de TF simple (penalizar términos muy comunes)
- **Expansión de sinónimos** para aumentar el vocabulario de referencia
- **n-gramas** (bigramas, trigramas) para capturar frases completas
- **Pesos personalizados** por categoría de intent (prioridad alta → mayor peso)
