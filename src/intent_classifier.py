from .utils import (
    normalize_text,
    tokenize,
    compute_idf,
    compute_tfidf_vector,
    cosine_similarity,
)


class IntentClassifier:
    """
    Clasificador basado en Similitud Coseno sobre vectores TF-IDF.

    Cada intencion se representa como un "documento de referencia" formado por
    la union de sus keywords y trigger_phrases. La coleccion de todos esos
    documentos define el vocabulario y los pesos IDF; la consulta del usuario
    se proyecta sobre ese mismo espacio vectorial y se compara por coseno:

        Similitud(Q,D) = (Σ Q_i * D_i) / (√(Σ Q_i²) * √(Σ D_i²))

    donde Q es el vector TF-IDF de la consulta y D el vector TF-IDF del
    documento de referencia de la intencion. El factor IDF penaliza los
    terminos que aparecen en muchas intenciones ("tramite", "solicitar") y
    realza los discriminantes ("convalidacion", "bachiller"). Se usa el IDF
    atenuado de compute_idf(): sin atenuar, el peso llega a penalizar la
    palabra que nombra el dominio (ver la nota en esa funcion).

    Nota: los valores confianza_minima de intents.json están calibrados para
    Dialogflow/Rasa (modelos ML). Este clasificador usa su propio umbral
    (threshold=0.3), apropiado para la escala de similitud coseno [0, 1].
    """

    def __init__(
        self,
        keywords_mapping: list[dict],
        intents_config: list[dict],
        threshold: float = 0.3,  # Bajado de 0.5 a 0.3 para mayor tolerancia a variaciones
    ):
        self._threshold = threshold
        # Guardamos confianza_minima como metadato para futura integración ML
        self._min_conf_ml: dict[str, float] = {
            e["intent"]: e["confianza_minima"] for e in intents_config
        }
        self._prepared = self._prepare(keywords_mapping)
        self._raw_keywords = keywords_mapping  # Guardar keywords originales para substring matching

    def _prepare(self, mapping: list[dict]) -> list[dict]:
        """
        Pre-procesa los keywords y trigger_phrases de cada intent: construye la
        coleccion de documentos de referencia, estima los pesos IDF sobre ella y
        vectoriza cada intencion en el espacio TF-IDF. Se ejecuta una sola vez.
        """
        # 1a pasada: tokenizar el documento de referencia de cada intencion.
        tokenized: list[tuple[str, list[str]]] = []
        for entry in mapping:
            keywords = entry.get("keywords", [])
            trigger_phrases = entry.get("trigger_phrases", [])
            reference_text = " ".join(keywords) + " " + " ".join(trigger_phrases)
            tokenized.append((entry["intent"], tokenize(reference_text)))

        # 2a pasada: los pesos IDF se estiman sobre la coleccion completa de
        # documentos de referencia, que es el "corpus" del sistema.
        self._idf = compute_idf([tokens for _, tokens in tokenized])

        # 3a pasada: vectorizar cada intencion en el espacio TF-IDF.
        prepared = [
            {"intent": intent, "reference_vector": compute_tfidf_vector(tokens, self._idf)}
            for intent, tokens in tokenized
        ]

        return prepared

    def _substring_score(self, query_tokens: list[str], keywords: list[str]) -> float:
        """
        Calcula un score basado en substring matching y n-gramas de caracteres.
        Se usa como fallback cuando la similitud coseno es muy baja.

        Args:
            query_tokens: Tokens de la consulta del usuario
            keywords: Keywords del intent a evaluar

        Returns:
            Score entre 0.0 y 1.0 basado en coincidencias de subcadenas
        """
        if not query_tokens or not keywords:
            return 0.0

        query_text = " ".join(query_tokens)
        total_matches = 0
        total_keywords = len(keywords)

        for keyword in keywords:
            keyword_normalized = normalize_text(keyword)

            # Coincidencia exacta de substring
            if keyword_normalized in query_text:
                total_matches += 1
                continue

            # Coincidencia de n-gramas de caracteres (trigramas)
            # Para manejar casos como "matriculas" vs "matricula"
            keyword_trigrams = {keyword_normalized[i:i+3]
                               for i in range(len(keyword_normalized) - 2)}
            query_trigrams = {query_text[i:i+3]
                             for i in range(len(query_text) - 2)}

            if keyword_trigrams and query_trigrams:
                overlap = len(keyword_trigrams & query_trigrams)
                total = len(keyword_trigrams | query_trigrams)
                trigram_similarity = overlap / total if total > 0 else 0.0

                # Si hay buena similitud de trigramas, contar como match parcial
                if trigram_similarity > 0.6:
                    total_matches += 0.7  # Match parcial

        return total_matches / total_keywords if total_keywords > 0 else 0.0

    def classify(self, text: str) -> tuple[str | None, float]:
        """
        Clasifica el texto del usuario por relevancia semantica vectorial:
        similitud coseno entre el vector TF-IDF de la consulta y el de cada
        intencion. Si la similitud es muy baja, se aplica un fallback lexico
        por subcadenas y trigramas de caracteres.

        Args:
            text: Consulta del usuario en lenguaje natural

        Returns:
            tuple (intent, confianza): intent detectado y su score de similitud,
            o (None, mejor_score) si ningún intent supera el umbral mínimo.
        """
        if not text or not text.strip():
            return None, 0.0

        # Proyectar la consulta sobre el mismo espacio TF-IDF de las intenciones
        query_tokens = tokenize(text)
        query_vector = compute_tfidf_vector(query_tokens, self._idf)

        if not query_vector:
            return None, 0.0

        best_intent: str | None = None
        best_score: float = 0.0

        # Relevancia semantica vectorial: coseno contra cada intencion
        for entry in self._prepared:
            intent = entry["intent"]
            reference_vector = entry["reference_vector"]

            score = cosine_similarity(query_vector, reference_vector)

            if score > best_score:
                best_score = score
                best_intent = intent

        # Si la similitud coseno es muy baja (< 0.2), intentar substring matching
        if best_score < 0.2:
            best_substring_intent: str | None = None
            best_substring_score: float = 0.0

            for entry in self._raw_keywords:
                intent = entry["intent"]
                keywords = entry.get("keywords", [])

                substring_score = self._substring_score(query_tokens, keywords)

                if substring_score > best_substring_score:
                    best_substring_score = substring_score
                    best_substring_intent = intent

            # Si el substring matching da mejor resultado, usar ese
            if best_substring_score > 0.5 and best_substring_score > best_score:
                best_score = best_substring_score
                best_intent = best_substring_intent

        # Verificar si supera el umbral
        if best_intent is None or best_score < self._threshold:
            return None, round(best_score, 4)

        return best_intent, round(best_score, 4)