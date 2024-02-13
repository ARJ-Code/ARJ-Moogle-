from newsplease import NewsPlease
from .utils import Article


def crawler(url: str):
    article = NewsPlease.from_url(url)
    return Article(article)
