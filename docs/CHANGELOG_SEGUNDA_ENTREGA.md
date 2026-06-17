# Changelog - Segunda Entrega

## Resumen de Cambios para Cumplimiento de Rúbrica

Fecha: 2026-06-17

---

## 1. ✅ Programación Orientada a Objetos (POO)

### Estado: **CUMPLE** ✓

**Verificación:**
- El código ya estaba correctamente implementado con POO
- Arquitectura modular con 4 clases principales:
  - `ChatbotEPIIS` — Orquestador principal
  - `IntentClassifier` — Clasificación de intenciones
  - `KnowledgeLoader` — Carga de datos
  - `ResponseGenerator` — Generación de respuestas

**Archivos verificados:**
- `src/chatbot.py` ✓
- `src/intent_classifier.py` ✓
- `src/knowledge_loader.py` ✓
- `src/response_generator.py` ✓
- `src/utils.py` ✓

**Conclusión:** No requirió modificaciones. El paradigma POO está correctamente aplicado.

---

## 2. ✅ Mecanismo de Recuperación: Similitud Coseno

### Estado: **REFACTORIZADO** ✓

**Problema identificado:**
El código original usaba:
- Keyword matching simple (fracción de keywords presentes)
- Jaccard overlap para trigger_phrases
- **NO implementaba similitud coseno** como exige el marco teórico

**Solución implementada:**

### 2.1. Nuevas funciones vectoriales en `src/utils.py`

```python
def compute_tf_vector(tokens: list[str]) -> dict[str, float]:
    """
    Calcula el vector TF (Term Frequency).
    TF(término) = frecuencia_del_término / total_términos
    """

def cosine_similarity(vec1: dict[str, float], vec2: dict[str, float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores TF.

    Fórmula: sim(Q,D) = (Σ Q_i * D_i) / (√(Σ Q_i²) * √(Σ D_i²))

    Returns:
        float entre 0.0 (ortogonales) y 1.0 (idénticos)
    """
```

**Características:**
- Implementación matemática exacta de la fórmula de similitud coseno
- Pre-cálculo de vectores TF en la inicialización
- Clasificación O(n × m) donde n=num_intents, m=dim_vocabulario

### 2.2. Refactorización completa de `src/intent_classifier.py`

**Cambios:**

1. **Método `_prepare()`:**
   - Antes: Normalizaba keywords y trigger_phrases por separado
   - Ahora: Combina keywords + trigger_phrases en un documento de referencia y calcula su vector TF

2. **Método `classify()`:**
   - Antes: Calculaba keyword_score y trigger_score (Jaccard)
   - Ahora: Vectoriza la consulta del usuario y calcula similitud coseno con cada intent

3. **Algoritmo de scoring:**
   ```
   ANTES:
   score = 0.65 × keyword_score + 0.35 × trigger_score

   AHORA:
   score = cosine_similarity(query_vector, reference_vector)
   ```

**Ventajas de la nueva implementación:**
- ✓ Cumple con el marco teórico del proyecto
- ✓ Captura relaciones de co-ocurrencia de términos
- ✓ Invariante a la longitud del documento
- ✓ Score entre 0.0 y 1.0 (interpretable)
- ✓ Eficiente: pre-cálculo de vectores en `__init__`

**Pruebas realizadas:**
```
Pregunta: ¿Qué es la tutoría académica?
Intent detectado: consulta_tutoria_definicion
Confianza (similitud coseno): 0.7333 ✓
```

---

## 3. ✅ Consistencia con la Documentación

### Estado: **ACTUALIZADO** ✓

**Problema identificado:**
- Documentación desactualizada con métricas del corpus original (30 entradas, 5 categorías)
- Estado actual: 108 entradas, 11 categorías
- Documentación técnica describía keyword matching, no similitud coseno

**Archivos actualizados:**

### 3.1. `README.md`
**Cambios:**
- ✓ Actualizado inventario de archivos (5 → 11 archivos)
- ✓ Agregada sección "Motor de clasificación: Similitud Coseno"
- ✓ Incluida fórmula matemática explícita
- ✓ Tabla de distribución por categoría (108 entradas)
- ✓ Actualizada estructura del repositorio
- ✓ Agregadas instrucciones de instalación y uso

**Métricas actualizadas:**
```
ANTES: 30 entradas en 5 categorías
AHORA: 108 entradas en 11 categorías
```

### 3.2. `docs/arquitectura.md`
**Cambios:**
- ✓ Reescrita sección "Visión general" con similitud coseno
- ✓ Actualizado diagrama de flujo del clasificador
- ✓ Documentada fórmula matemática: `sim(Q,D) = (Σ Q_i*D_i) / (√(Σ Q_i²) * √(Σ D_i²))`
- ✓ Agregada sección "Algoritmo de clasificación" con 2 fases (pre-procesamiento y clasificación)
- ✓ Agregada sección "Propiedades de la similitud coseno"
- ✓ Actualizada tabla de mapeo intent → archivo (11 archivos)
- ✓ Agregada sección "Ventajas de la similitud coseno"
- ✓ Agregada sección "Extensión futura" con mejoras propuestas (TF-IDF, n-gramas)

### 3.3. `docs/modelo_datos.md`
**Cambios:**
- ✓ Actualizado "Inventario de archivos de datos" (9 → 11 archivos)
- ✓ Agregada columna "Entradas" con conteo por archivo
- ✓ Todos los archivos marcados como "completo"
- ✓ Agregada sección "Estadísticas del corpus"
- ✓ Métricas actualizadas:
  - 11 módulos temáticos
  - 108 qa_entries totales
  - 109 intents únicos
  - Distribución por cobertura temática

### 3.4. `notebooks/chatbot_epiis.ipynb`
**Cambios:**
- ✓ Actualizada celda de introducción
- ✓ Mencionada arquitectura POO
- ✓ Incluida fórmula de similitud coseno
- ✓ Actualizadas métricas (108 entradas, 11 categorías)

---

## 4. Resumen de Archivos Modificados

### Código fuente (refactorización crítica):
1. ✅ `src/utils.py` — Agregadas funciones `compute_tf_vector()` y `cosine_similarity()`
2. ✅ `src/intent_classifier.py` — Reescrito completamente para usar similitud coseno

### Documentación (actualización):
3. ✅ `README.md` — Actualizado con métricas y arquitectura actual
4. ✅ `docs/arquitectura.md` — Documentada similitud coseno y algoritmo
5. ✅ `docs/modelo_datos.md` — Actualizado inventario de archivos
6. ✅ `notebooks/chatbot_epiis.ipynb` — Actualizada introducción

### Documentación nueva:
7. ✅ `docs/CHANGELOG_SEGUNDA_ENTREGA.md` — Este documento

---

## 5. Verificación del Cumplimiento de la Rúbrica

| Criterio | Estado | Evidencia |
|----------|--------|-----------|
| **1. POO** | ✅ CUMPLE | 4 clases principales con encapsulación correcta |
| **2. Similitud Coseno** | ✅ CUMPLE | Implementación exacta de la fórmula matemática en `utils.py` y `intent_classifier.py` |
| **3. Documentación Actualizada** | ✅ CUMPLE | README.md, arquitectura.md, modelo_datos.md reflejan 108 entradas y similitud coseno |

---

## 6. Pruebas de Funcionamiento

### Test manual ejecutado:
```bash
python -c "from src.chatbot import ChatbotEPIIS; bot = ChatbotEPIIS(); ..."
```

### Resultados:
```
Pregunta: ¿Qué es la tutoría académica?
Intent: consulta_tutoria_definicion
Confianza: 0.7333 (similitud coseno) ✓
Respuesta: [Correcta]
```

**Conclusión:** El chatbot funciona correctamente con similitud coseno.

---

## 7. Métricas Finales del Proyecto

| Métrica | Valor |
|---------|-------|
| Total de archivos de datos | 11 |
| Total de qa_entries | 108 |
| Total de intents únicos | 109 |
| Categorías temáticas | 11 |
| Archivos completos | 11/11 (100%) |
| Método de clasificación | Similitud Coseno sobre vectores TF |
| Threshold de confianza | 0.5 |
| Arquitectura | POO (4 clases principales) |

---

## 8. Próximos Pasos (Mejoras Futuras)

Sugerencias para mejorar el clasificador:

1. **TF-IDF** en lugar de TF simple
   - Penalizar términos muy comunes (ej: "universidad", "estudiante")
   - Priorizar términos distintivos

2. **Expansión de sinónimos**
   - Aumentar vocabulario de referencia
   - Mapear "tutoría" ↔ "asesoría académica"

3. **N-gramas** (bigramas, trigramas)
   - Capturar frases completas
   - Ejemplo: "prácticas pre profesionales" como un solo término

4. **Pesos por prioridad**
   - Intents con prioridad "Muy Alta" → mayor peso en el score

---

**Fin del documento**

Preparado para la Segunda Entrega del Proyecto Semestral
Curso: IF651 Inteligencia Artificial (2026-1)
EPIIS - UNSAAC
