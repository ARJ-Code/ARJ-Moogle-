from news_crawler.crawler import crawler
from news_crawler.summary import summary

article = crawler(
    'https://www.nytimes.com/2017/02/23/us/politics/cpac-stephen-bannon-reince-priebus.html?hp')
summary(article)
print(article.text)
print()
print(article.summary)
