# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**EPIIS Knowledge Repository** — Academic chatbot for the School of Computer Science and Information Systems (EPIIS) at Universidad Nacional de San Antonio Abad del Cusco (UNSAAC).

This is a keyword-based intent classification chatbot that answers student questions about academic processes. It uses **zero external dependencies** for NLP — classification is based on keyword matching and Jaccard overlap with trigger phrases.

Part of course **IF651 Inteligencia Artificial** (2026-1).

## Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_chatbot.py

# Run with verbose output
python -m pytest -v

# Run specific test
python -m pytest tests/test_chatbot.py::test_classify_known_queries
```

## Running the Chatbot

### From Python REPL
```python
from src.chatbot import ChatbotEPIIS

bot = ChatbotEPIIS()
response = bot.ask("¿Qué es la tutoría académica?")
print(response)

# Debug mode shows intent and confidence
debug_info = bot.ask_debug("¿Cuántos semestres dura la carrera?")
print(debug_info)  # {'question': ..., 'intent': ..., 'confidence': ..., 'response': ...}
```

### From Jupyter Notebook
Use `notebooks/chatbot_epiis.ipynb` for interactive demos and evaluation.

## Architecture

### Core Components (src/)

1. **ChatbotEPIIS** (`chatbot.py`) — Main orchestrator
   - Initializes all components
   - Provides `ask()` and `ask_debug()` methods
   - No state between queries

2. **IntentClassifier** (`intent_classifier.py`) — Intent detection
   - **No ML models** — uses keyword matching + Jaccard overlap
   - Scoring: `0.65 * keyword_score + 0.35 * trigger_score`
   - Default threshold: 0.5 (configured in constructor)
   - Returns `(intent, confidence)` or `(None, score)` if below threshold
   - Note: `confianza_minima` values in `intents.json` are calibrated for ML engines (Dialogflow/Rasa), not used by this keyword classifier

3. **ResponseGenerator** (`response_generator.py`) — Response builder
   - Builds O(1) lookup index: `intent → qa_entry`
   - Appends `fuente` citation if present in qa_entry
   - Returns fallback message for None/unknown intents

4. **KnowledgeLoader** (`knowledge_loader.py`) — Data loader
   - Loads all JSON files from `data/` and `knowledge_base/`
   - Intent prefix mapping: `TUT` → `tutorias.json`, `PPP` → `practicas.json`, etc.
   - Returns dict with `intents`, `keywords_mapping`, `data_files`, `intent_prefix_map`

5. **utils.py** — Text normalization
   - `normalize_text()`: lowercasing, accent removal, Unicode normalization
   - `tokenize()`: whitespace-based word splitting

### Data Structure

```
data/                          # Domain-specific Q&A responses
├── bienestar.json             # Student welfare services
├── malla_semestralizada.json  # Curriculum by semester
├── matricula.json             # Enrollment processes
├── movilidad.json             # Student mobility/exchange
├── plan_estudios_resumen.json # Curriculum summary
├── practicas.json             # Internships (PPP)
├── servicios_academicos.json  # Academic services
├── titulacion.json            # Graduation requirements
└── tutorias.json              # Tutoring system

knowledge_base/                # Classification config
├── intents.json               # Intent catalog (109 intents)
└── keywords.json              # Intent → keywords/trigger_phrases mapping

corpus/                        # Evaluation dataset
└── corpus_consultas.json      # Test queries with expected intents
```

### Intent Naming Convention

Intents follow pattern: `{PREFIX}-{NUMBER}` → `{action}_{domain}_{detail}`

Examples:
- `TUT-001` → `consulta_tutoria_definicion`
- `PPP-001` → `consulta_ppp_requisitos_inicio`
- `MAT-002` → `consulta_mat_proceso_serunsa`

Prefixes map to data files via `_INTENT_PREFIX_TO_FILE` in `knowledge_loader.py`.

### QA Entry Structure (in data/*.json files)

```json
{
  "qa_entries": [
    {
      "intent": "consulta_tutoria_definicion",
      "pregunta_representativa": "¿Qué es la tutoría académica?",
      "respuesta": "...",
      "fuente": "Art. 5 del Reglamento de Tutorías UNSAAC"
    }
  ]
}
```

### Keywords Mapping Structure (knowledge_base/keywords.json)

```json
{
  "keywords_mapping": [
    {
      "intent": "consulta_tutoria_definicion",
      "keywords": ["tutoria", "tutoría", "que es tutoria"],
      "trigger_phrases": [
        "qué es la tutoría",
        "en qué consiste la tutoría",
        "explicame la tutoria"
      ]
    }
  ]
}
```

## Key Design Decisions

1. **Zero ML Dependencies** — Deliberately uses simple keyword matching instead of ML models for ease of deployment and interpretability

2. **Threshold Mismatch** — `confianza_minima` in `intents.json` (0.70-0.90) is metadata for future ML integration. Current keyword classifier uses `threshold=0.5` which is appropriate for its scoring scale.

3. **Stateless** — No conversation history; each query is independent

4. **Spanish-only** — All normalization and responses are in Spanish

5. **O(1) Response Lookup** — `ResponseGenerator` pre-builds intent → qa_entry index for fast lookups

## Modifying the Knowledge Base

### Adding a new intent

1. Add entry to `knowledge_base/intents.json`:
```json
{"id": "TUT-011", "intent": "consulta_tutoria_nueva", "prioridad": "Media", "confianza_minima": 0.75}
```

2. Add keywords to `knowledge_base/keywords.json`:
```json
{
  "intent": "consulta_tutoria_nueva",
  "keywords": ["palabra1", "palabra2"],
  "trigger_phrases": ["frase ejemplo 1", "frase ejemplo 2"]
}
```

3. Add Q&A response to appropriate `data/*.json` file:
```json
{
  "intent": "consulta_tutoria_nueva",
  "pregunta_representativa": "...",
  "respuesta": "...",
  "fuente": "..."
}
```

4. Add test cases to `tests/test_chatbot.py` parametrized tests

5. Optionally add to `corpus/corpus_consultas.json` for evaluation

### Modifying classifier behavior

- Adjust keyword vs. trigger weighting in `IntentClassifier._score()` (currently 0.65/0.35)
- Change classification threshold via constructor parameter (default 0.5)
- Modify text normalization in `utils.normalize_text()`

## File Encoding

All JSON files use **UTF-8 encoding**. When reading files in Python, always use `encoding='utf-8'`.

## Testing Strategy

Tests are organized by component:
- `test_chatbot.py` — Integration tests for end-to-end flow
- `test_knowledge_loader.py` — Data loading validation

Test categories:
- **Happy path** — Known queries should classify to expected intent
- **Response validation** — Responses should include content and sources
- **Edge cases** — Empty input, whitespace, gibberish
- **Debug mode** — Verify all keys returned in debug dict

Parametrized tests use actual examples from the corpus to ensure consistency.
