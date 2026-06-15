from .utils import normalize_text, tokenize


class IntentClassifier:
    """
    Clasificador basado en coincidencia de keywords y solapamiento de palabras
    con trigger_phrases. No requiere modelo externo ni dependencias de NLP.

    Nota: los valores confianza_minima de intents.json están calibrados para
    Dialogflow/Rasa (modelos ML). Este clasificador de keywords usa threshold=0.5
    como umbral propio, que es apropiado para la escala de puntuación que produce.
    """

    def __init__(
        self,
        keywords_mapping: list[dict],
        intents_config: list[dict],
        threshold: float = 0.5,
    ):
        self._threshold = threshold
        # Guardamos confianza_minima como metadato para futura integración ML
        self._min_conf_ml: dict[str, float] = {
            e["intent"]: e["confianza_minima"] for e in intents_config
        }
        self._prepared = self._prepare(keywords_mapping)

    def _prepare(self, mapping: list[dict]) -> list[dict]:
        prepared = []
        for entry in mapping:
            norm_keywords = [normalize_text(k) for k in entry.get("keywords", [])]
            norm_triggers: list[set[str]] = [
                set(tokenize(tp)) for tp in entry.get("trigger_phrases", [])
            ]
            prepared.append({
                "intent": entry["intent"],
                "keywords": norm_keywords,
                "trigger_tokens": norm_triggers,
            })
        return prepared

    def classify(self, text: str) -> tuple[str | None, float]:
        """
        Retorna (intent, confianza). Retorna (None, 0.0) si no supera
        el umbral mínimo de ningún intent.
        """
        norm = normalize_text(text)
        tokens = set(tokenize(text))

        best_intent: str | None = None
        best_score: float = 0.0

        for entry in self._prepared:
            intent = entry["intent"]
            score = self._score(norm, tokens, entry)
            if score > best_score:
                best_score = score
                best_intent = intent

        if best_intent is None or best_score < self._threshold:
            return None, round(best_score, 4)

        return best_intent, round(best_score, 4)

    def _score(self, norm_text: str, tokens: set[str], entry: dict) -> float:
        """
        Combina dos señales:
        - keyword_score: fracción de keywords del intent presentes en el texto
        - trigger_score: mejor solapamiento de Jaccard con algún trigger_phrase
        """
        keywords = entry["keywords"]
        keyword_score = 0.0
        if keywords:
            hits = sum(1 for kw in keywords if kw in norm_text)
            keyword_score = hits / len(keywords)

        trigger_score = 0.0
        for trig_tokens in entry["trigger_tokens"]:
            if not trig_tokens:
                continue
            overlap = len(tokens & trig_tokens) / len(tokens | trig_tokens)
            if overlap > trigger_score:
                trigger_score = overlap

        # Ponderación: keywords tienen más peso que trigger_phrases
        return 0.65 * keyword_score + 0.35 * trigger_score
