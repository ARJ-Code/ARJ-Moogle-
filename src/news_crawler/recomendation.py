import json
import spacy
import gensim
from .utils import Article
import numpy as np
from gensim.matutils import corpus2dense

nlp = spacy.load('en_core_web_sm')


def tokenize_doc(doc):
    return [token.lemma_ for token in nlp(
        doc.lower()) if token.is_alpha and not token.is_stop]


def build_dataset():
    print('Load data')
    try:
        f = open('data/data.json')
        lines = f.readlines()
        f.close()

        data = [json.loads(line) for line in lines]
    except:
        data = []

    data = data[:10000]
    print('Processing data')
    tokenized_docs = [tokenize_doc(
        doc['short_description'].lower()) for doc in data]

    dictionary = gensim.corpora.Dictionary(tokenized_docs)

    corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

    tfidf = gensim.models.TfidfModel(corpus)

    print('Save data')
    tfidf.save("data/tfidf.model.news")
    dictionary.save("data/dictionary.dict.news")
    vector_repr = [tfidf[doc] for doc in corpus]

    for i in range(len(vector_repr)):
        data[i]['doc_tfidf'] = vector_repr[i]

    f = open('data/data_build.json', 'w')
    json.dump(data, f)
    f.close()


def recomendation(article: Article, cant_recomendation=3):
    # Cargar el modelo TF-IDF y el diccionario
    tfidf = gensim.models.TfidfModel.load("data/tfidf.model.news")
    dictionary = gensim.corpora.Dictionary.load("data/dictionary.dict.news")

    try:
        f = open('data/data_build.json')
        data = json.load(f)
        f.close()
    except:
        data = []

    def dense_vect(vect):
        return corpus2dense([vect], len(dictionary)).flatten()

    def cosine_similarity(vec1, vec2):
        vec1, vec2 = dense_vect(vec1), dense_vect(vec2)

        v = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        if v == 0:
            return 0

        return np.dot(vec1, vec2) / v

    # Preprocesar y tokenizar la consulta
    query_tokens = tokenize_doc(article.text)

    # Convertir la consulta en su representación BoW
    query_bow = dictionary.doc2bow(query_tokens)

    # Calcular la representación TF-IDF de la consulta
    query_tfidf = tfidf[query_bow]

    # Calcular la similitud entre la consulta y cada documento en el corpus
    similarities = [cosine_similarity(query_tfidf, doc["doc_tfidf"])
                    for doc in data]

    for i in range(len(data)):
        if not any(p for p in article.authors if data[i]['authors'].lower().find(p.lower())):
            similarities[i] *= 3/4

    # Ordenar las noticias por similitud y seleccionar las más relevantes
    top_n_indices = np.argsort(similarities)[-cant_recomendation:]

    top_n = [data[ind]
             for ind in top_n_indices if similarities[ind] != 0]
    top_n.reverse()

    article.recomendations = top_n
