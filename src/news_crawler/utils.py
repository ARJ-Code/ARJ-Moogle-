class Article:
    def __init__(self, article) -> None:
        self.title = article.title
        self.authors = article.authors
        self.date_publish = article.date_publish
        self.description = article.description
        self.text = article.maintext
        self.language = article.language
        self.summary=''
