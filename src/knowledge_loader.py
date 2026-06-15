import json
from pathlib import Path


# Mapeo: prefijo de intent → nombre del archivo en data/
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


class KnowledgeLoader:
    def __init__(self, base_dir: str | Path | None = None):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent
        self.base_dir = Path(base_dir)

    def _load_json(self, rel_path: str) -> dict:
        path = self.base_dir / rel_path
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def load_intents(self) -> list[dict]:
        data = self._load_json("knowledge_base/intents.json")
        return data["intents"]

    def load_keywords_mapping(self) -> list[dict]:
        data = self._load_json("knowledge_base/keywords.json")
        return data["keywords_mapping"]

    def load_data_files(self) -> dict[str, dict]:
        """Devuelve un dict {nombre_archivo: contenido} para todos los archivos de data/."""
        loaded: dict[str, dict] = {}
        for filename in set(_INTENT_PREFIX_TO_FILE.values()):
            loaded[filename] = self._load_json(f"data/{filename}")
        return loaded

    def load_all(self) -> dict:
        return {
            "intents": self.load_intents(),
            "keywords_mapping": self.load_keywords_mapping(),
            "data_files": self.load_data_files(),
            "intent_prefix_map": _INTENT_PREFIX_TO_FILE,
        }
