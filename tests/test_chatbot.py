import pytest
from pathlib import Path
from src.chatbot import ChatbotEPIIS

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def bot():
    return ChatbotEPIIS(BASE_DIR)


# ---------------------------------------------------------------------------
# Casos felices: preguntas que deben clasificarse correctamente
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("question, expected_intent", [
    ("¿Qué es la tutoría académica?",           "consulta_tutoria_definicion"),
    ("¿Cuántas veces al semestre es la tutoría?", "consulta_tutoria_frecuencia"),
    ("la tutoria es obligatoria o puedo faltar", "consulta_tutoria_obligatoriedad"),
    ("¿Puedo cambiarme de tutor?",               "consulta_tutoria_cambio_tutor"),
    ("¿Cuántos semestres dura la carrera?",      "consulta_cursos_duracion_carrera"),
    ("¿Qué requisitos necesito para iniciar prácticas?", "consulta_ppp_requisitos_inicio"),
    ("cuantas horas de practicas me piden",      "consulta_ppp_horas_acumuladas"),
    ("¿A qué países puedo ir de intercambio?",   "consulta_mov_programas_disponibles"),
    ("hay psicólogo gratis en la universidad",   "consulta_bie_atencion_psicologica"),
])
def test_classify_known_queries(bot, question, expected_intent):
    result = bot.ask_debug(question)
    assert result["intent"] == expected_intent, (
        f"Para '{question}' se esperaba '{expected_intent}' "
        f"pero se obtuvo '{result['intent']}' (conf={result['confidence']})"
    )


# ---------------------------------------------------------------------------
# Respuesta no vacía para intents conocidos
# ---------------------------------------------------------------------------

def test_response_is_not_empty(bot):
    response = bot.ask("¿Qué es la tutoría académica?")
    assert isinstance(response, str)
    assert len(response.strip()) > 0


def test_response_includes_source(bot):
    response = bot.ask("¿Qué es la tutoría académica?")
    assert "Fuente" in response or "Art." in response


# ---------------------------------------------------------------------------
# Casos de borde
# ---------------------------------------------------------------------------

def test_empty_question_returns_prompt(bot):
    response = bot.ask("")
    assert "consulta" in response.lower() or "escribe" in response.lower()


def test_whitespace_only_returns_prompt(bot):
    response = bot.ask("   ")
    assert len(response) > 0


def test_gibberish_returns_fallback(bot):
    result = bot.ask_debug("asdfghjkl qwerty xyz")
    assert result["intent"] is None


def test_ask_debug_returns_all_keys(bot):
    result = bot.ask_debug("¿Qué es la tutoría?")
    assert {"question", "intent", "confidence", "response"} == set(result.keys())


def test_confidence_in_valid_range(bot):
    result = bot.ask_debug("¿Qué es la tutoría académica?")
    assert 0.0 <= result["confidence"] <= 1.0
