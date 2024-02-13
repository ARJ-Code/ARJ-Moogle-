from news_crawler.crawler import crawler

article = crawler(
    'http://www.cubadebate.cu/especiales/2024/02/13/etica-donde-se-inventan-variedades-mejores-de-cana-de-azucar/')


print(article.summary+'\n')
# print(article.text)
# print(article.description+'\n')
# print(article.named_entities)
print(article.language)
