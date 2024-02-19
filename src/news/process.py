from newsplease import NewsPlease
import logging
import spacy
from .utils import Article
from .recomendation import recomendation
from .recomendation import tokenize_doc, cosine_similarity
import gensim
from .utils import Article
import numpy as np
import networkx as nx


def analyze(article: Article, cant_sentences: int = 3):
    """
    Función que analiza un artículo para obtener un resumen y las entidades nombradas más importantes
    article: Objeto de la clase Article que contiene la información del artículo
    cant_sentences: Cantidad de oraciones que se quieren en el resumen
    """
    
    # Cargamos el modelo de spacy para el idioma correspondiente
    nlp = spacy.load('en_core_web_sm') if article.language == 'en'else spacy.load(
        'es_core_news_sm')

    # Procesamos el texto del artículo
    doc = nlp(article.text)

    # Obtenemos las oraciones del artículo
    sents = [sent for sent in doc.sents]
    tokenized_sents = [tokenize_doc(sent.text) for sent in doc.sents]

    # Creamos el diccionario y el corpus para el modelo tf-idf
    dictionary = gensim.corpora.Dictionary(tokenized_sents)
    corpus = [dictionary.doc2bow(doc) for doc in tokenized_sents]

    # Creamos el modelo tf-idf
    tfidf = gensim.models.TfidfModel(corpus)

    # Calculamos la matriz de similitud entre las oraciones
    sim_mat = np.zeros([len(sents), len(sents)])
    for i in range(len(sents)):
        for j in range(len(sents)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(
                    tfidf[corpus[i]], tfidf[corpus[j]], dictionary)

    # Aplicamos el algoritmo de PageRank para obtener las oraciones más importantes
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    # Ordenamos las oraciones según su importancia
    ranked_sents = [s.text for _, s in sorted(((scores[i], s)
                                               for i, s in enumerate(sents)), reverse=True)]

    # Obtenemos el resumen del artículo
    article.summary = '. '.join(ranked_sents[:cant_sentences])

    # Obtenemos las entidades nombradas del artículo
    interested_labels = ["GPE", "LOC", "ORG", "PERSON"]

    # Filtramos las entidades nombradas para quedarnos solo con las de interés
    article.named_entities = list(set([(x.text, x.label_)
                                       for x in doc.ents if x.label_ in interested_labels]))


def process(url: str, cant_sentences: int = 3, cant_recomendation: int = 3):
    """
    Función que procesa un artículo a partir de su url
    url: Url del artículo
    cant_sentences: Cantidad de oraciones que se quieren en el resumen
    cant_recomendation: Cantidad de recomendaciones que se quieren
    """

    logging.info(f'Processing html data from url:{url}')
    article_new = NewsPlease.from_url(url)

    logging.info('Processing article')
    article = Article(article_new)

    analyze(article, cant_sentences)
    if (article.language == 'en'):
        recomendation(article, cant_recomendation)

    return article
