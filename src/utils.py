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
    # Nota: 'necesito'/'quiero' NO están aquí a propósito: "qué necesito para X"
    # es la forma más común de preguntar por requisitos, filtrarla vacía la consulta.
    'por', 'favor', 'gracias', 'dame', 'dime', 'explicame',
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


# Sufijos que en español casi siempre vienen de una raíz terminada en
# consonante + "-es" (profesor -> profesores, obligación -> obligaciones).
# Se usan para decidir si hay que quitar "es" completo o solo la "s" final,
# ya que ambos patrones de plural ("papel"->"papeles" y "semestre"->"semestres")
# terminan igual en la superficie y no se pueden distinguir letra por letra.
_SUFIJOS_PLURAL_CONSONANTE = (
    'ciones', 'siones', 'dades', 'tades', 'ores', 'ones', 'ales', 'iles', 'eles', 'enes',
)


def normalize_plural(word: str) -> str:
    """
    Normaliza plurales comunes al singular (español).

    Reglas aplicadas:
    - Palabras terminadas en 's' con más de 4 letras → remover 's' final
      (cubre plurales de palabras que terminan en vocal: "semestre" -> "semestres")
    - Si además terminan en uno de los sufijos típicos de raíz consonántica
      + "es" (ver _SUFIJOS_PLURAL_CONSONANTE) → remover "es" completo
      ("profesor" -> "profesores", "obligación" -> "obligaciones")
    - Excepciones: palabras que terminan naturalmente en 's' en singular

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

        # Singularizar: remover 's' final (caso general, raíz en vocal)
        singular = word[:-1]

        # Solo si el sufijo calza con un patrón conocido de raíz consonántica
        # removemos también la 'e' (evita romper "semestre", "docente",
        # "estudiante", "clase", "parte", que ya terminan en vocal)
        if len(word) > 6 and word.endswith(_SUFIJOS_PLURAL_CONSONANTE):
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


def compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """
    Calcula el peso IDF (Inverse Document Frequency) atenuado de cada termino
    sobre una coleccion de documentos ya tokenizados.

        IDF(t) = √( ln( N / (1 + df(t)) ) + 1 )

    Se parte de la variante suavizada (smooth IDF): el "+1" en el denominador
    evita la division por cero para terminos ausentes y el "+1" exterior
    garantiza que ningun termino reciba peso nulo, de modo que un termino
    presente en todos los documentos aun contribuye minimamente al vector.

    La raiz cuadrada **atenua** ese peso, y es una decision deliberada para
    este dominio. Los "documentos" aqui no son textos naturales sino los
    catalogos de keywords/trigger_phrases de cada intencion: son cortos
    (~13 tokens) y estan curados a mano. En ellos, la palabra que nombra el
    dominio ("titulacion", "tutoria", "matricula") aparece a proposito en
    varias intenciones de esa misma categoria, porque es la senal que indica
    el tema. El IDF sin atenuar interpreta esa repeticion como "ruido" y
    penaliza justo el termino mas informativo para enrutar la consulta; la
    raiz comprime el rango de pesos y evita ese efecto contraproducente.

    Args:
        documents: lista de documentos, cada uno como lista de tokens.

    Returns:
        dict {termino: peso_idf}
    """
    n_docs = len(documents)
    if n_docs == 0:
        return {}

    df: Counter = Counter()
    for tokens in documents:
        df.update(set(tokens))

    return {
        term: math.sqrt(math.log(n_docs / (1 + freq)) + 1.0)
        for term, freq in df.items()
    }


def compute_tfidf_vector(
    tokens: list[str],
    idf: dict[str, float],
    default_idf: float | None = None,
) -> dict[str, float]:
    """
    Calcula el vector TF-IDF de una lista de tokens.

        TF-IDF(t, d) = TF(t, d) * IDF(t)

    Los terminos que no aparecen en el vocabulario de la coleccion (por
    ejemplo, palabras nuevas en una consulta del usuario) reciben
    ``default_idf``; de este modo el vector de consulta nunca se vacia.
    Si no se indica, se usa el IDF maximo observado: un termino nunca visto
    es, por definicion, al menos tan raro como el mas raro conocido, y darle
    un peso bajo lo haria contar menos que las palabras mas comunes.

    Args:
        tokens: lista de tokens normalizados.
        idf: pesos IDF calculados con compute_idf().
        default_idf: peso asignado a terminos fuera de vocabulario.
            Por defecto (None), el maximo peso IDF de la coleccion.

    Returns:
        dict {termino: peso_tfidf}
    """
    if default_idf is None:
        default_idf = max(idf.values()) if idf else 1.0

    tf = compute_tf_vector(tokens)
    return {term: value * idf.get(term, default_idf) for term, value in tf.items()}


def cosine_similarity(vec1: dict[str, float], vec2: dict[str, float]) -> float:
    """
    Calcula la similitud coseno entre dos vectores dispersos (TF o TF-IDF).

    Fórmula: sim(Q,D) = (Σ Q_i * D_i) / (√(Σ Q_i²) * √(Σ D_i²))

    Args:
        vec1: Vector del primer texto (ej: query del usuario)
        vec2: Vector del segundo texto (ej: documento de referencia)

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