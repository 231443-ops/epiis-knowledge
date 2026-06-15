_INTENT_PREFIX_TO_FILE = {
    "TUT":  "tutorias.json",
    "TTUT": "tutorias.json",
    "CUR":  "malla_semestralizada.json",
    "ESP":  "plan_estudios_resumen.json",
    "PPP":  "practicas.json",
    "BIE":  "bienestar.json",
    "MOV":  "movilidad.json",
    "MAT":  "matricula.json",
    "TIT":  "titulacion.json",
    "SER":  "servicios_academicos.json",
}

_FALLBACK = (
    "Lo siento, no encontré información específica sobre eso. "
    "Te recomiendo consultar directamente en la secretaría de la EPIIS "
    "o revisar el portal SERUNSA (serunsa.unsaac.edu.pe)."
)


class ResponseGenerator:
    def __init__(self, data_files: dict[str, dict]):
        # Construye un índice plano intent → qa_entry para búsqueda O(1)
        self._index: dict[str, dict] = {}
        for file_data in data_files.values():
            for entry in file_data.get("qa_entries", []):
                self._index[entry["intent"]] = entry

    def generate(self, intent: str | None, confidence: float = 1.0) -> str:
        if intent is None:
            return _FALLBACK

        entry = self._index.get(intent)
        if entry is None:
            return _FALLBACK

        respuesta = entry.get("respuesta", _FALLBACK)
        fuente = entry.get("fuente", "")
        if fuente:
            respuesta = f"{respuesta}\n\n_Fuente: {fuente}_"
        return respuesta

    def get_entry(self, intent: str | None) -> dict | None:
        """Retorna la qa_entry completa para inspección o tests."""
        if intent is None:
            return None
        return self._index.get(intent)
