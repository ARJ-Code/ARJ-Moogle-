from newsplease import NewsPlease
import spacy
from collections import Counter
from heapq import nlargest
from .utils import Article
from .recomendation import recomendation


def analyze(article: Article, cant_sentences: int = 3):
    # Cargamos el modelo de lenguaje español pequeño
    nlp = spacy.load('en_core_web_sm') if article.language == 'en'else spacy.load(
        'es_core_news_sm')

    # Analizamos el texto del artículo con spaCy
    doc = nlp(article.text)

    # Inicializamos listas y diccionarios para almacenar palabras clave y frecuencias
    keyword = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    freq_word = Counter()
    sent_strength = {}

    # Procesamos cada token en el documento
    for token in doc:
        # Si el token es una palabra de parada o signo de puntuación, lo saltamos
        if token.is_stop or not token.is_alpha:
            continue
        # Si el token es un nombre propio, adjetivo, sustantivo o verbo, lo añadimos a las palabras clave
        if token.pos_ in pos_tag:
            keyword.append(token.lemma_.lower())

    # Contamos la frecuencia de cada palabra clave y normalizamos las frecuencias
    freq_word = Counter(keyword)
    max_freq = freq_word.most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = freq_word[word] / max_freq

    # Calculamos la fuerza de cada frase sumando los pesos relativos de las palabras clave
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in freq_word.keys():
                if sent in sent_strength:
                    sent_strength[sent] += freq_word[word.lemma_.lower()]
                else:
                    sent_strength[sent] = freq_word[word.lemma_.lower()]

    # Seleccionamos las 'cant_sentences' frases más fuertes
    summarized_sentences = nlargest(
        cant_sentences, sent_strength, key=sent_strength.get)

    # Extraemos las frases seleccionadas y las unimos para formar el resumen
    final_sentences = [w.text for w in summarized_sentences]
    article.summary = ' '.join(final_sentences)

    # Lista de etiquetas de entidad que nos interesan
    interested_labels = ["GPE", "LOC", "ORG", "PERSON"]

    # Filtramos las entidades nombradas para quedarnos solo con las de interés
    article.named_entities = list(set([(x.text, x.label_)
                                       for x in doc.ents if x.label_ in interested_labels]))


def crawler(url: str, cant_sentences: int = 3, cant_recomendation: int = 3):
    print(f'Processing html data from url:{url}')
    article_new = NewsPlease.from_url(url)

    print('Processing article')
    article = Article(article_new)

    analyze(article, cant_sentences)
    if(article.language=='en'):
        recomendation(article, cant_recomendation)

    return article
