from pathlib import Path

from .knowledge_loader import KnowledgeLoader
from .intent_classifier import IntentClassifier
from .response_generator import ResponseGenerator

_LOW_CONFIDENCE_MSG = (
    "No estoy seguro de entender tu consulta. ¿Puedes reformularla? "
    "Puedo ayudarte sobre tutorías, cursos, prácticas pre-profesionales, "
    "bienestar, movilidad, matrícula y titulación."
)


class ChatbotEPIIS:
    """Orquestador del chatbot académico EPIIS-UNSAAC."""

    def __init__(self, base_dir: str | Path | None = None):
        loader = KnowledgeLoader(base_dir)
        knowledge = loader.load_all()

        self._classifier = IntentClassifier(
            keywords_mapping=knowledge["keywords_mapping"],
            intents_config=knowledge["intents"],
        )
        self._generator = ResponseGenerator(
            data_files=knowledge["data_files"],
        )

    def ask(self, question: str) -> str:
        """Procesa una pregunta y retorna la respuesta en texto."""
        if not question or not question.strip():
            return "Por favor, escribe tu consulta."

        intent, confidence = self._classifier.classify(question)
        return self._generator.generate(intent, confidence)

    def ask_debug(self, question: str) -> dict:
        """Como ask(), pero retorna también el intent y la confianza."""
        intent, confidence = self._classifier.classify(question)
        response = self._generator.generate(intent, confidence)
        return {
            "question": question,
            "intent": intent,
            "confidence": confidence,
            "response": response,
        }
