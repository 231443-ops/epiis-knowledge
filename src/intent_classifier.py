from .utils import normalize_text, tokenize, compute_tf_vector, cosine_similarity


class IntentClassifier:
    """
    Clasificador basado en Similitud Coseno entre la consulta del usuario
    y las representaciones vectoriales (TF) de keywords y trigger_phrases de cada intent.

    Implementa la fórmula:
        Similitud(Q,D) = (Σ Q_i * D_i) / (√(Σ Q_i²) * √(Σ D_i²))

    donde Q es el vector TF de la consulta del usuario y D es el vector TF
    del documento de referencia (keywords + trigger_phrases del intent).

    Nota: los valores confianza_minima de intents.json están calibrados para
    Dialogflow/Rasa (modelos ML). Este clasificador usa threshold=0.5 como
    umbral propio, apropiado para la escala de similitud coseno [0, 1].
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
        """
        Pre-procesa los keywords y trigger_phrases de cada intent,
        construyendo su representación vectorial (TF).
        """
        prepared = []
        for entry in mapping:
            intent = entry["intent"]

            # Combinar todos los keywords y trigger_phrases en un solo documento de referencia
            keywords = entry.get("keywords", [])
            trigger_phrases = entry.get("trigger_phrases", [])

            # Construir el "documento de referencia" del intent
            reference_text = " ".join(keywords) + " " + " ".join(trigger_phrases)
            reference_tokens = tokenize(reference_text)
            reference_vector = compute_tf_vector(reference_tokens)

            prepared.append({
                "intent": intent,
                "reference_vector": reference_vector,
            })

        return prepared

    def classify(self, text: str) -> tuple[str | None, float]:
        """
        Clasifica el texto del usuario usando similitud coseno.

        Args:
            text: Consulta del usuario en lenguaje natural

        Returns:
            tuple (intent, confianza): intent detectado y su score de similitud,
            o (None, mejor_score) si ningún intent supera el umbral mínimo.
        """
        if not text or not text.strip():
            return None, 0.0

        # Vectorizar la consulta del usuario
        query_tokens = tokenize(text)
        query_vector = compute_tf_vector(query_tokens)

        if not query_vector:
            return None, 0.0

        best_intent: str | None = None
        best_score: float = 0.0

        # Calcular similitud coseno con cada intent
        for entry in self._prepared:
            intent = entry["intent"]
            reference_vector = entry["reference_vector"]

            score = cosine_similarity(query_vector, reference_vector)

            if score > best_score:
                best_score = score
                best_intent = intent

        # Verificar si supera el umbral
        if best_intent is None or best_score < self._threshold:
            return None, round(best_score, 4)

        return best_intent, round(best_score, 4)
