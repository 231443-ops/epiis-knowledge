# Chatbot Académico EPIIS — Repositorio de Conocimiento

**Repositorio:** https://github.com/231443-ops/epiis-knowledge

Repositorio de conocimientos y código del chatbot de atención académica de la **Escuela Profesional de Ingeniería Informática y de Sistemas (EPIIS)** de la Universidad Nacional de San Antonio Abad del Cusco (UNSAAC).

Forma parte del Proyecto Semestral del curso **IF651 Inteligencia Artificial** (2026-1).

---

## 📂 Estructura del repositorio

```
epiis-knowledge/
├── README.md
├── data/                          # 9 archivos de conocimiento (116 qa_entries)
│   ├── tutorias.json              # Tutoría académica (20 entradas)
│   ├── matricula.json             # Matrícula y procesos (20 entradas)
│   ├── titulacion.json            # Grados y títulos (16 entradas)
│   ├── servicios_academicos.json  # Servicios académicos (10 entradas)
│   ├── practicas.json             # Prácticas pre-profesionales (10 entradas)
│   ├── bienestar.json             # Bienestar universitario (10 entradas)
│   ├── movilidad.json             # Movilidad estudiantil (10 entradas)
│   ├── malla_semestralizada.json  # Cursos por semestre (10 entradas)
│   └── plan_estudios_resumen.json # Áreas curriculares (10 entradas)
├── knowledge_base/
│   ├── intents.json               # 116 intents con prioridades
│   └── keywords.json              # Keywords y trigger_phrases por intent
├── src/                           # Código fuente del chatbot (Python)
│   ├── chatbot.py                 # Clase orquestadora ChatbotEPIIS
│   ├── intent_classifier.py       # Clasificador con similitud coseno
│   ├── knowledge_loader.py        # Cargador de datos JSON
│   ├── response_generator.py      # Generador de respuestas
│   └── utils.py                   # Normalización y vectorización (TF)
├── tests/                         # Tests unitarios (pytest)
├── notebooks/
│   └── chatbot_epiis.ipynb        # Demo interactiva y evaluación
├── corpus/
│   └── corpus_consultas.json      # 84 consultas de prueba
├── docs/                          # Documentación técnica
└── sources/                       # PDFs normativos que respaldan la data
```

## 🏗️ Arquitectura del Chatbot

Arquitectura modular basada en POO, **sin dependencias de NLP externas** (solo Python estándar). Cada consulta atraviesa el siguiente pipeline:

```
Pregunta del usuario
   │
   ▼
normalize_text()      → minúsculas, sin tildes, sin puntuación
   │
   ▼
tokenize()            → tokens + singularización de plurales + filtrado de stop-words
   │
   ▼
compute_tfidf_vector() → vector TF-IDF de la consulta
   │
   ▼
IntentClassifier      → similitud coseno contra cada intent
   │                    (fallback por substring/trigramas si el score es muy bajo)
   ▼
¿score ≥ umbral (0.3)?
   │            │
  sí           no ──► respuesta de fallback ("no encontré información…")
   │
   ▼
ResponseGenerator     → busca la respuesta del intent (índice O(1)) + cita la fuente
   │
   ▼
Respuesta al usuario
```

### Componentes (`src/`)

| Componente | Responsabilidad |
|---|---|
| **`ChatbotEPIIS`** (`chatbot.py`) | Orquestador. Expone `ask()` y `ask_debug()`. Sin estado entre consultas. |
| **`KnowledgeLoader`** (`knowledge_loader.py`) | Carga los JSON de `data/` y `knowledge_base/`. |
| **`IntentClassifier`** (`intent_classifier.py`) | Clasifica la consulta por similitud coseno; fallback por substring/trigramas. Umbral 0.3. |
| **`ResponseGenerator`** (`response_generator.py`) | Índice `intent → qa_entry` para lookup O(1); añade la cita de la `fuente`. |
| **`utils.py`** | Normalización de texto, singularización de plurales, stop-words, vectores TF-IDF y similitud coseno. |

### Motor de clasificación: Similitud Coseno sobre TF-IDF

Cada intent tiene un "documento de referencia" (sus `keywords` + `trigger_phrases`) representado como vector TF-IDF. La consulta se proyecta sobre ese mismo espacio vectorial y se compara mediante similitud coseno:

```
similitud(Q, D) = (Σ Q_i × D_i) / (√(Σ Q_i²) × √(Σ D_i²))
```

- **Q**: vector TF-IDF de la consulta del usuario
- **D**: vector TF-IDF del intent (keywords + trigger_phrases)
- **Resultado**: score entre 0.0 (ortogonal) y 1.0 (idéntico)

El peso **IDF** realza los términos discriminantes (`convalidacion`, `bachiller`) frente a los que aparecen en muchas intenciones (`tramite`, `solicitar`). Se aplica **atenuado** (raíz cuadrada): como los documentos de referencia son cortos y curados a mano, la palabra que nombra el dominio (`titulacion`, `tutoria`) aparece a propósito en varias intenciones de su categoría, y un IDF sin atenuar acabaría penalizando justo esa señal temática.

Si ningún intent supera el umbral por similitud coseno, se aplica un **fallback** basado en coincidencia de subcadenas y trigramas de caracteres, que ayuda con variantes léxicas y errores ortográficos menores.

### Características técnicas

- ✅ **Zero dependencias de NLP**: solo Python stdlib (+ pytest para tests)
- ✅ **Procesamiento local**: sin llamadas a APIs externas
- ✅ **Determinista**: resultados reproducibles
- ✅ **Extensible**: arquitectura modular para agregar dominios

## 📊 Corpus de Conocimiento

### Cobertura actual
- **9 categorías temáticas**
- **116 pares pregunta-respuesta** (qa_entries)
- **116 intents únicos** definidos

### Distribución por categoría

| Categoría | Archivo | Entradas | Descripción |
|-----------|---------|----------|-------------|
| Tutorías | `tutorias.json` | 20 | Sistema de tutoría académica UNSAAC |
| Matrícula | `matricula.json` | 20 | Proceso de matrícula y requisitos |
| Titulación | `titulacion.json` | 16 | Grados académicos y títulos |
| Servicios Académicos | `servicios_academicos.json` | 10 | Constancias, certificados, trámites |
| Prácticas PPP | `practicas.json` | 10 | Prácticas pre-profesionales |
| Bienestar | `bienestar.json` | 10 | Servicios de bienestar universitario |
| Movilidad | `movilidad.json` | 10 | Movilidad estudiantil e intercambios |
| Cursos | `malla_semestralizada.json` | 10 | Plan de estudios semestralizado |
| Especialidades | `plan_estudios_resumen.json` | 10 | Áreas curriculares y especialidades |

### Fuentes

El contenido de `data/` se respalda en los documentos normativos oficiales de la UNSAAC ubicados en [`sources/`](sources/): Reglamento Académico, Reglamento de Tutoría Académica y el Plan de Estudios / Malla Curricular. Cada `respuesta` cita el artículo o documento del que proviene.

## 🛠️ Uso del Chatbot

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/231443-ops/epiis-knowledge.git
cd epiis-knowledge

# Instalar dependencias (solo pytest para desarrollo)
pip install pytest
```

### Uso desde Python

```python
from src.chatbot import ChatbotEPIIS

# Inicializar el chatbot
bot = ChatbotEPIIS()

# Hacer una consulta
respuesta = bot.ask("¿Qué es la tutoría académica?")
print(respuesta)

# Modo debug (con intent y confianza)
debug = bot.ask_debug("¿Cuántos créditos llevo por semestre?")
print(f"Intent: {debug['intent']}")
print(f"Confianza: {debug['confidence']}")
print(f"Respuesta: {debug['response']}")
```

### Uso desde Jupyter Notebook

Abre `notebooks/chatbot_epiis.ipynb` para una demo interactiva completa y la evaluación sobre el corpus.

### Ejecución de tests

```bash
# Ejecutar todos los tests
python -m pytest

# Tests con salida detallada
python -m pytest -v

# Test específico
python -m pytest tests/test_chatbot.py::test_classify_known_queries
```

## 📑 Estructura de Datos

### Formato de qa_entry (`data/*.json`)

```json
{
  "id": "TUT-001",
  "intent": "consulta_tutoria_definicion",
  "pregunta": "¿Qué es la tutoría académica?",
  "respuesta": "La tutoría académica es un servicio...",
  "fuente": "Art. 5 del Reglamento de Tutorías UNSAAC"
}
```

### Formato de keywords_mapping (`knowledge_base/keywords.json`)

```json
{
  "intent": "consulta_tutoria_definicion",
  "keywords": ["tutoria", "tutoría", "que es tutoria"],
  "trigger_phrases": [
    "qué es la tutoría",
    "en qué consiste la tutoría",
    "explicame la tutoria"
  ]
}
```

## 🤝 Contribución

Para agregar nuevos dominios de conocimiento:

1. Crear `data/nuevo_modulo.json` siguiendo el formato estándar
2. Agregar intents en `knowledge_base/intents.json`
3. Agregar keywords y trigger_phrases en `knowledge_base/keywords.json`
4. Actualizar el mapeo de prefijos en `src/knowledge_loader.py`
5. Agregar tests en `tests/test_chatbot.py`

## 📚 Documentación Adicional

- [Arquitectura del Sistema](docs/arquitectura.md) — Detalles técnicos del chatbot
- [Modelo de Datos](docs/modelo_datos.md) — Esquema de archivos JSON
