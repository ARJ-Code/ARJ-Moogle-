from news_crawler.crawler import crawler
from news_crawler.analyze import analyze

article = crawler(
    'https://www.washingtonpost.com/national-security/2024/02/12/trump-immunity-supreme-court-appeal-jan-6/')
analyze(article)

print(article.summary+'\n')
print(article.description+'\n')
print(article.named_entities)
# print(article.text)
# print()
# print(article.summary)
