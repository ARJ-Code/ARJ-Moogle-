from news.process import process
import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot("6876084200:AAHTQM2vDcBYZunoFqKFaNzDPdXwZ3y4vd8")

article = None


def build_text(texts):
    text = ""

    for i in texts:
        text += '- '
        text += i
        text += '\n'

    return text


@bot.message_handler(commands=["help", "start"])
def start(message):
    bot.reply_to(
        message, "Hello, send us the url of a news item and we will analyze it for you")


@bot.message_handler(func=lambda message: message.text.lower() not in ["summary", "descripcion", "autors", "date", "title",
                                                                       "language", "named entities", "recomendation"])
def analyze(message):
    try:
        global article
        article = process(message.text)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("summary", "descripcion", "autors", "date", "title",
                   "language", "named entities", "recomendation")
        bot.reply_to(
            message, "Select what you want to know about the news", reply_markup=markup)

    except:
        bot.reply_to(
            message, "The URL could not be processed. Please try again.")


@bot.message_handler(func=lambda message: message.text.lower() == "summary")
def get_summary(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.summary)


@bot.message_handler(func=lambda message: message.text.lower() == "descripcion")
def get_description(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    if article.description == "":
        bot.reply_to(message, "Property not found")
        return
    bot.reply_to(message, article.description)


@bot.message_handler(func=lambda message: message.text.lower() == "autors")
def get_autors(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return

    text = build_text(article.authors)

    if text == "":
        bot.reply_to(message, "Property not found")
        return

    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: message.text.lower() == "date")
def get_date(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.date_publish)


@bot.message_handler(func=lambda message: message.text.lower() == "title")
def get_title(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return

    if article.title == "":
        bot.reply_to(message, "Property not found")
        return

    bot.reply_to(message, article.title)


@bot.message_handler(func=lambda message: message.text.lower() == "language")
def get_language(message):
    bot.reply_to(message, article.language)


@bot.message_handler(func=lambda message: message.text.lower() == "named entities")
def get_entities(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return

    text = build_text([f'{i}: {j}' for i, j in article.named_entities])
    if text == "":
        bot.reply_to(message, "Property not found")
        return

    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: message.text.lower() == "recomendation")
def get_recomendtion(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return

    text = build_text([doc['link'] for doc in article.recomendations])

    if text == "":
        bot.reply_to(message, "Property not found")
        return

    bot.reply_to(message, text)


print("Running...")
bot.polling()
bot.infinity_polling()
