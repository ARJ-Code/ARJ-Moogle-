import telebot
import logging
from telebot.types import ReplyKeyboardMarkup
from news.process import process

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot("6876084200:AAHTQM2vDcBYZunoFqKFaNzDPdXwZ3y4vd8")

    def start(self):

        @self.bot.message_handler(commands=["help", "start"])
        def start(message):
            self.bot.reply_to(
                message, "Hello, send us the url of a news item and we will analyze it for you")


        @self.bot.message_handler(func=lambda message: message.text.lower() not in ["summary", "description", "autors", "date", "title",
                                                                            "language", "named entities", "recomendation"])
        def analyze(message):
            try:
                global article
                article = process(message.text)

                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add("summary", "description", "autors", "date", "title",
                        "language", "named entities", "recomendation")
                self.bot.reply_to(
                    message, "Select what you want to know about the news", reply_markup=markup)

            except:
                self.bot.reply_to(
                    message, "The URL could not be processed. Please try again.")


        @self.bot.message_handler(func=lambda message: message.text.lower() == "summary")
        def get_summary(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return
            self.bot.reply_to(message, article.summary)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "description")
        def get_description(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return
            if article.description == "":
                self.bot.reply_to(message, "Property not found")
                return
            self.bot.reply_to(message, article.description)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "autors")
        def get_autors(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return

            text = build_text(article.authors)

            if text == "":
                self.bot.reply_to(message, "Property not found")
                return

            self.bot.reply_to(message, text)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "date")
        def get_date(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return
            self.bot.reply_to(message, article.date_publish)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "title")
        def get_title(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return

            if article.title == "":
                self.bot.reply_to(message, "Property not found")
                return

            self.bot.reply_to(message, article.title)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "language")
        def get_language(message):
            self.bot.reply_to(message, article.language)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "named entities")
        def get_entities(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return

            text = build_text([f'{i}: {j}' for i, j in article.named_entities])
            if text == "":
                self.bot.reply_to(message, "Property not found")
                return

            self.bot.reply_to(message, text)


        @self.bot.message_handler(func=lambda message: message.text.lower() == "recomendation")
        def get_recomendtion(message):
            if article is None:
                self.bot.reply_to(message, "Plese select a news")
                return

            text = build_text([doc['link'] for doc in article.recomendations])

            if text == "":
                self.bot.reply_to(message, "Property not found")
                return

            self.bot.reply_to(message, text)


        def build_text(texts):
            return '\n'.join(['- '+x for x in texts])


        logging.info("Running...")
        self.bot.infinity_polling()
