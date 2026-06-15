import pytest
from pathlib import Path
from src.knowledge_loader import KnowledgeLoader

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def loader():
    return KnowledgeLoader(BASE_DIR)


def test_load_intents_returns_list(loader):
    intents = loader.load_intents()
    assert isinstance(intents, list)
    assert len(intents) > 0


def test_intents_have_required_fields(loader):
    for intent in loader.load_intents():
        assert "id" in intent
        assert "intent" in intent
        assert "confianza_minima" in intent
        assert 0.0 <= intent["confianza_minima"] <= 1.0


def test_load_keywords_mapping_returns_list(loader):
    mapping = loader.load_keywords_mapping()
    assert isinstance(mapping, list)
    assert len(mapping) > 0


def test_keywords_mapping_have_required_fields(loader):
    for entry in loader.load_keywords_mapping():
        assert "intent" in entry
        assert "keywords" in entry
        assert "trigger_phrases" in entry
        assert isinstance(entry["keywords"], list)
        assert isinstance(entry["trigger_phrases"], list)


def test_load_data_files_returns_all_files(loader):
    data_files = loader.load_data_files()
    expected = {
        "tutorias.json",
        "malla_semestralizada.json",
        "plan_estudios_resumen.json",
        "practicas.json",
        "bienestar.json",
        "movilidad.json",
        "matricula.json",
        "titulacion.json",
        "servicios_academicos.json",
    }
    assert expected == set(data_files.keys())


def test_data_files_have_categoria_id(loader):
    for name, data in loader.load_data_files().items():
        assert "categoria_id" in data, f"{name} no tiene categoria_id"


def test_intents_and_keywords_are_consistent(loader):
    """Todos los intents en keywords_mapping deben existir en intents.json."""
    intent_names = {e["intent"] for e in loader.load_intents()}
    for entry in loader.load_keywords_mapping():
        assert entry["intent"] in intent_names, (
            f"Intent '{entry['intent']}' en keywords.json no existe en intents.json"
        )
