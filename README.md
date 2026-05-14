# Repositorio de Conocimiento — EPIIS UNSAAC

Repositorio de conocimientos de la **Escuela Profesional de Ingeniería Informática y de Sistemas** de la Universidad Nacional de San Antonio Abad del Cusco (UNSAAC).

Este repositorio almacena, en formato JSON estructurado, el conocimiento institucional de la EPIIS para alimentar un **chatbot de atención académica** a estudiantes y docentes. Forma parte del Proyecto Semestral del curso **IF651 Inteligencia Artificial** (2026-1).

## 📂 Estructura del repositorio

```
repo-epiis/
├── README.md
└── data/
    ├── escuela.json                 # Info general, autoridades, contacto
    ├── plan_estudios_resumen.json   # Áreas curriculares y estructura
    ├── cursos.json                  # Catálogo de 78 cursos con sumillas
    ├── malla_semestralizada.json    # Cursos organizados por semestre (1-10)
    └── equivalencias.json           # Equivalencias plan 2018 → 2024
```

## 📑 Contenido del repositorio

### `escuela.json`
Información institucional general:
- Datos de la escuela, facultad y universidad
- Carrera, grado académico y título profesional
- Autoridades vigentes (rector, decano, directora de escuela, etc.)
- Plan curricular vigente y marco legal
- Enlaces oficiales
- Competencias genéricas

### `plan_estudios_resumen.json`
Estructura curricular general:
- 5 áreas curriculares (Estudios Generales, Específicos, Especialidad, Extracurriculares, Prácticas)
- Total: **59 cursos** y **220 créditos** en **10 semestres**
- Distribución porcentual por área
- Rasgos del perfil del egresado

### `cursos.json`
Catálogo completo de cursos con:
- Código y nombre
- Área curricular y tipo (obligatorio/electivo)
- Créditos, horas teóricas y prácticas
- Prerrequisitos (códigos y créditos requeridos)
- Sumilla y ejes temáticos
- Competencia genérica vinculada

### `malla_semestralizada.json`
Plan de estudios organizado por semestre (1-10), tal como debe llevarlo el estudiante en condiciones regulares.

### `equivalencias.json`
Tabla de equivalencias entre el **Plan Curricular 2018** y el **Plan Curricular 2024** vigente. Útil para estudiantes en proceso de transición o convalidación.

## 🎯 Plan Curricular Vigente

- **Nombre:** Plan Curricular 2024
- **Aprobado por:** Resolución CU-031-2025-UNSAAC (13 de enero de 2025)
- **Implementación:** Desde el Año Académico 2025
- **Modelo educativo:** Formación basada en competencias

## 🏛️ Datos institucionales

- **Universidad:** Universidad Nacional de San Antonio Abad del Cusco (UNSAAC)
- **Facultad:** Ingeniería Eléctrica, Electrónica, Informática y Mecánica (FIEEIM)
- **Escuela:** Ingeniería Informática y de Sistemas (EPIIS)
- **Web oficial:** https://in.unsaac.edu.pe/

## 🛠️ Uso del repositorio

Los archivos JSON están diseñados para ser consumidos por:
- Chatbots de atención académica (proyecto del curso IF651)
- Sistemas de recomendación de cursos
- Aplicaciones de consulta de información institucional
- Herramientas de planificación académica

### Ejemplo de consumo en Python

```python
import json

with open('data/cursos.json', 'r', encoding='utf-8') as f:
    cursos = json.load(f)['cursos']

# Buscar curso por código
ia = next(c for c in cursos if c['codigo'] == 'IFI14')
print(ia['nombre'], '-', ia['creditos'], 'créditos')
# > Inteligencia Artificial - 4 créditos
```

## 📌 Próximos módulos (en desarrollo)

- `tutorias.json` — Reglamento y proceso de tutorías
- `servicios.json` — Bienestar universitario, movilidad estudiantil
- `practicas.json` — Detalle de prácticas pre profesionales
- `faq.json` — Preguntas frecuentes de estudiantes

## 📜 Licencia

Información pública institucional de la UNSAAC. Uso académico para el curso IF651 - Inteligencia Artificial 2026-1.

## 👥 Autoría

Proyecto académico del curso IF651 Inteligencia Artificial, EPIIS-UNSAAC, Semestre 2026-1.
