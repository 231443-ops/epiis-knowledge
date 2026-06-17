# Repositorio de Conocimiento — EPIIS UNSAAC

Repositorio de conocimientos de la **Escuela Profesional de Ingeniería Informática y de Sistemas** de la Universidad Nacional de San Antonio Abad del Cusco (UNSAAC).

Este repositorio almacena, en formato JSON estructurado, el conocimiento institucional de la EPIIS para alimentar un **chatbot de atención académica** a estudiantes y docentes. Forma parte del Proyecto Semestral del curso **IF651 Inteligencia Artificial** (2026-1).

## 📂 Estructura del repositorio

```
epiis-knowledge/
├── README.md
├── CLAUDE.md                     # Guía para Claude Code
├── data/                         # 11 archivos de conocimiento (108 qa_entries)
│   ├── tutorias.json            # Tutoría académica (20 entradas)
│   ├── matricula.json           # Matrícula y procesos (10 entradas)
│   ├── servicios_academicos.json # Servicios académicos (10 entradas)
│   ├── practicas.json           # Prácticas pre-profesionales (10 entradas)
│   ├── bienestar.json           # Bienestar universitario (10 entradas)
│   ├── movilidad.json           # Movilidad estudiantil (10 entradas)
│   ├── titulacion.json          # Grados y títulos (10 entradas)
│   ├── malla_semestralizada.json # Cursos por semestre (10 entradas)
│   ├── plan_estudios_resumen.json # Áreas curriculares (10 entradas)
│   ├── inicio_clases.json       # Inicio de clases (4 entradas)
│   └── silabos.json             # Sílabos académicos (4 entradas)
├── knowledge_base/
│   ├── intents.json             # 109 intents con prioridades
│   └── keywords.json            # Keywords y trigger_phrases por intent
├── src/                         # Código fuente del chatbot (Python)
│   ├── chatbot.py               # Clase orquestadora ChatbotEPIIS
│   ├── intent_classifier.py     # Clasificador con similitud coseno
│   ├── knowledge_loader.py      # Cargador de datos JSON
│   ├── response_generator.py    # Generador de respuestas
│   └── utils.py                 # Funciones de normalización y vectorización
├── tests/                       # Tests unitarios (pytest)
│   ├── test_chatbot.py
│   └── test_knowledge_loader.py
├── notebooks/
│   └── chatbot_epiis.ipynb      # Demo interactiva y evaluación
├── corpus/
│   └── corpus_consultas.json    # 80 consultas de prueba
├── docs/
│   ├── arquitectura.md          # Documentación técnica
│   └── modelo_datos.md          # Esquema de datos JSON
└── sources/
    └── README.md                # Referencias documentales
```

## 🎯 Características del Chatbot

### Arquitectura basada en POO
- **ChatbotEPIIS**: Clase orquestadora principal
- **IntentClassifier**: Clasificación de intenciones con similitud coseno
- **KnowledgeLoader**: Carga centralizada de conocimiento
- **ResponseGenerator**: Generación de respuestas contextualizadas

### Motor de clasificación: Similitud Coseno
El chatbot utiliza **similitud coseno** sobre representaciones vectoriales TF (Term Frequency) para clasificar las consultas del usuario:

```
similitud(Q, D) = (Σ Q_i × D_i) / (√(Σ Q_i²) × √(Σ D_i²))
```

- **Q**: Vector TF de la consulta del usuario
- **D**: Vector TF del intent (keywords + trigger_phrases)
- **Resultado**: Score entre 0.0 (ortogonal) y 1.0 (idéntico)

### Características técnicas
- ✅ **Zero dependencias de NLP**: Solo Python stdlib + pytest
- ✅ **Procesamiento local**: Sin llamadas a APIs externas
- ✅ **Determinista**: Resultados reproducibles
- ✅ **Extensible**: Arquitectura modular para agregar dominios

## 📊 Corpus de Conocimiento

### Cobertura actual
- **11 categorías temáticas**
- **108 pares pregunta-respuesta** (qa_entries)
- **109 intents únicos** definidos

### Distribución por categoría

| Categoría | Archivo | Entradas | Descripción |
|-----------|---------|----------|-------------|
| Tutorías | `tutorias.json` | 20 | Sistema de tutoría académica UNSAAC |
| Matrícula | `matricula.json` | 10 | Proceso de matrícula y requisitos |
| Servicios Académicos | `servicios_academicos.json` | 10 | Constancias, certificados, trámites |
| Prácticas PPP | `practicas.json` | 10 | Prácticas pre-profesionales |
| Bienestar | `bienestar.json` | 10 | Servicios de bienestar universitario |
| Movilidad | `movilidad.json` | 10 | Movilidad estudiantil e intercambios |
| Titulación | `titulacion.json` | 10 | Grados académicos y títulos |
| Cursos | `malla_semestralizada.json` | 10 | Plan de estudios semestralizado |
| Especialidades | `plan_estudios_resumen.json` | 10 | Áreas curriculares y especialidades |
| Inicio de Clases | `inicio_clases.json` | 4 | Calendario y modalidades |
| Sílabos | `silabos.json` | 4 | Estructura de sílabos y evaluación |

## 🛠️ Uso del Chatbot

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/usuario/epiis-knowledge.git
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

Abre `notebooks/chatbot_epiis.ipynb` para una demo interactiva completa.

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

### Formato de qa_entry

```json
{
  "id": "TUT-001",
  "intent": "consulta_tutoria_definicion",
  "pregunta": "¿Qué es la tutoría académica?",
  "respuesta": "La tutoría académica es un servicio...",
  "fuente": "Art. 5 del Reglamento de Tutorías UNSAAC"
}
```

### Formato de keywords_mapping

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

## 🎯 Plan Curricular Vigente

- **Nombre:** Plan Curricular 2024
- **Aprobado por:** Resolución CU-031-2025-UNSAAC (13 de enero de 2025)
- **Implementación:** Desde el Año Académico 2025
- **Modelo educativo:** Formación basada en competencias
- **Total:** 220 créditos en 10 semestres (59 cursos)

## 🏛️ Datos Institucionales

- **Universidad:** Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)
- **Facultad:** Ingeniería Eléctrica, Electrónica, Informática y Mecánica (FIEEIM)
- **Escuela:** Ingeniería Informática y de Sistemas (EPIIS)
- **Web oficial:** https://in.unsaac.edu.pe/

## 📚 Documentación Adicional

- [Arquitectura del Sistema](docs/arquitectura.md) - Detalles técnicos del chatbot
- [Modelo de Datos](docs/modelo_datos.md) - Esquema de archivos JSON
- [CLAUDE.md](CLAUDE.md) - Guía para Claude Code

## 🤝 Contribución

Para agregar nuevos dominios de conocimiento:

1. Crear `data/nuevo_modulo.json` siguiendo el formato estándar
2. Agregar intents en `knowledge_base/intents.json`
3. Agregar keywords y trigger_phrases en `knowledge_base/keywords.json`
4. Actualizar el mapeo de prefijos en `src/knowledge_loader.py`
5. Agregar tests en `tests/test_chatbot.py`

## 📄 Licencia

Este proyecto es parte del curso IF651 Inteligencia Artificial de la UNSAAC (2026-1).

---

**Proyecto desarrollado por:** [Nombre del equipo/estudiante]
**Curso:** IF651 Inteligencia Artificial (2026-1)
**Institución:** EPIIS - UNSAAC
