import re
import unicodedata
import math
from collections import Counter


# Stop words (palabras vacías) en español
# Estas palabras se filtran del análisis porque no aportan significado semántico
STOP_WORDS = {
    # Artículos
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',

    # Preposiciones
    'de', 'del', 'a', 'al', 'en', 'por', 'para', 'con', 'sin', 'sobre',
    'entre', 'desde', 'hasta', 'hacia', 'mediante', 'tras',

    # Pronombres
    'yo', 'tu', 'el', 'ella', 'nosotros', 'vosotros', 'ellos', 'ellas',
    'me', 'te', 'se', 'nos', 'os', 'le', 'les', 'lo', 'mi', 'mis', 'su', 'sus',

    # Conjunciones
    'y', 'e', 'o', 'u', 'pero', 'sino', 'aunque', 'si', 'porque', 'que',

    # Verbos auxiliares comunes
    'ser', 'estar', 'haber', 'tener', 'hacer', 'poder', 'deber',
    'es', 'son', 'esta', 'estan', 'hay', 'tiene', 'pueden',

    # Interrogativos (se mantienen algunos como 'como', 'cuando' que pueden ser útiles)

    # Demostrativos
    'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
    'aquel', 'aquella', 'aquellos', 'aquellas',

    # Adverbios muy comunes
    'muy', 'mas', 'menos', 'tambien', 'tampoco', 'si', 'no',

    # Nombres institucionales genéricos (contexto UNSAAC)
    'unsaac', 'universidad', 'nacional', 'san', 'antonio', 'abad', 'cusco',

    # Palabras de cortesía/relleno
    'por', 'favor', 'gracias', 'dame', 'dime', 'explicame', 'quiero', 'necesito',
    'hola', 'buenos', 'dias', 'tardes', 'noches', 'ayuda', 'ayudame',

    # Otras palabras vacías
    'algo', 'nada', 'todo', 'cada', 'otro', 'otra', 'mismo', 'misma'
}


def normalize_text(text: str) -> str:
    """Minúsculas + sin tildes + sin puntuación."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_plural(word: str) -> str:
    """
    Normaliza plurales comunes al singular (español).

    Reglas aplicadas:
    - Palabras terminadas en 's' con más de 4 letras → remover 's' final
    - Excepciones: palabras que terminan en 'as', 'es', 'os' naturalmente singulares

    Args:
        word: Palabra normalizada (minúsculas, sin tildes)

    Returns:
        Palabra en singular (aproximado)
    """
    if not word or len(word) <= 3:
        return word

    # Si termina en 's' y tiene más de 4 letras, intentar singularizar
    if word.endswith('s') and len(word) > 4:
        # Casos especiales que no deben singularizarse
        exceptions = {
            'mas', 'menos', 'entonces', 'ademas', 'despues', 'antes',
            'mas', 'pues', 'tras', 'campus', 'bus', 'plus'
        }

        if word in exceptions:
            return word

        # Singularizar: remover 's' final
        singular = word[:-1]

        # Si termina en 'es' y tiene más de 5 letras, remover 'es'
        if word.endswith('es') and len(word) > 5:
            singular = word[:-2]

        return singular

    return word


def tokenize(text: str, remove_stop_words: bool = True) -> list[str]:
    """
    Tokeniza y normaliza el texto, manejando plurales y filtrando stop_words.

    Args:
        text: Texto a tokenizar
        remove_stop_words: Si True, filtra palabras vacías (por defecto True)

    Returns:
        Lista de tokens normalizados (singular, minúsculas, sin tildes, sin stop_words)
    """
    normalized = normalize_text(text)
    tokens = normalized.split()

    # Normalizar plurales en cada token
    tokens_singular = [normalize_plural(token) for token in tokens]

    # Filtrar stop_words si está habilitado
    if remove_stop_words:
        tokens_singular = [token for token in tokens_singular if token not in STOP_WORDS]

    return tokens_singular


def compute_tf_vector(tokens: list[str]) -> dict[str, float]:
    """
    Calcula el vector TF (Term Frequency) de una lista de tokens.
    TF(término) = frecuencia_del_término / total_términos

    Args:
        tokens: Lista de tokens normalizados

    Returns:
        dict con {término: tf_valor}
    """
    if not tokens:
        return {}

    total = len(tokens)
    freq = Counter(tokens)
    return {term: count / total for term, count in freq.items()}


def cosine_similarity(vec1: dict[str, float], vec2: dict[str, float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores TF.

    Fórmula: sim(Q,D) = (Σ Q_i * D_i) / (√(Σ Q_i²) * √(Σ D_i²))

    Args:
        vec1: Vector TF del primer texto (ej: query del usuario)
        vec2: Vector TF del segundo texto (ej: documento de referencia)

    Returns:
        float entre 0.0 (ortogonales) y 1.0 (idénticos)
    """
    if not vec1 or not vec2:
        return 0.0

    # Términos comunes entre ambos vectores
    common_terms = set(vec1.keys()) & set(vec2.keys())

    if not common_terms:
        return 0.0

    # Producto punto: Σ Q_i * D_i
    dot_product = sum(vec1[term] * vec2[term] for term in common_terms)

    # Magnitudes: √(Σ Q_i²) y √(Σ D_i²)
    magnitude_vec1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
    magnitude_vec2 = math.sqrt(sum(val ** 2 for val in vec2.values()))

    if magnitude_vec1 == 0.0 or magnitude_vec2 == 0.0:
        return 0.0

    # Similitud coseno
    return dot_product / (magnitude_vec1 * magnitude_vec2)
