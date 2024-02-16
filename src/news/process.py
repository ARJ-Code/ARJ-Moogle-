from newsplease import NewsPlease
import spacy
from .utils import Article
from .recomendation import recomendation
from .recomendation import tokenize_doc, cosine_similarity
import gensim
from .utils import Article
import numpy as np
import networkx as nx


def analyze(article: Article, cant_sentences: int = 3):
    nlp = spacy.load('en_core_web_sm') if article.language == 'en'else spacy.load(
        'es_core_news_sm')

    doc = nlp(article.text)

    sents = [sent for sent in doc.sents]
    tokenized_sents = [tokenize_doc(sent.text) for sent in doc.sents]

    dictionary = gensim.corpora.Dictionary(tokenized_sents)

    corpus = [dictionary.doc2bow(doc) for doc in tokenized_sents]

    tfidf = gensim.models.TfidfModel(corpus)

    sim_mat = np.zeros([len(sents), len(sents)])

    for i in range(len(sents)):
        for j in range(len(sents)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(
                    tfidf[corpus[i]], tfidf[corpus[j]], dictionary)

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    ranked_sents = [s.text for _, s in sorted(((scores[i], s)
                                               for i, s in enumerate(sents)), reverse=True)]

    article.summary = ' '.join(ranked_sents[:cant_sentences])

    interested_labels = ["GPE", "LOC", "ORG", "PERSON"]

    # Filtramos las entidades nombradas para quedarnos solo con las de interés
    article.named_entities = list(set([(x.text, x.label_)
                                       for x in doc.ents if x.label_ in interested_labels]))


def process(url: str, cant_sentences: int = 3, cant_recomendation: int = 3):
    print(f'Processing html data from url:{url}')
    article_new = NewsPlease.from_url(url)

    print('Processing article')
    article = Article(article_new)

    analyze(article, cant_sentences)
    if (article.language == 'en'):
        recomendation(article, cant_recomendation)

    return article
