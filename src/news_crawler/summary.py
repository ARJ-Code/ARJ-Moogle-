import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest
from .utils import Article


def summary(article: Article, cant_sentences:int=3):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(article.text)

    keyword = []
    stop_words = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if (token.text in stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            keyword.append(token.text)

    freq_word = Counter(keyword)

    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)

    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]

    summarized_sentences = nlargest(
        cant_sentences, sent_strength, key=sent_strength.get)

    final_sentences = [w.text for w in summarized_sentences]
    article.summary = ' '.join(final_sentences)
