from news_crawler.crawler import crawler
import telebot
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardRemove

article = None

bot = telebot.TeleBot("6876084200:AAHTQM2vDcBYZunoFqKFaNzDPdXwZ3y4vd8")

@bot.message_handler(commands=["help", "start"])
def saludar(message):
    bot.reply_to(
        message, "Hello, send us the url of a news item and we will analyze it for you")


@bot.message_handler(func=lambda message: message.text.lower() not in ["summary", "descripcion", "autor", "date", "title", "text",
                                                                       "language", "entidades nombradas", "recomendation", "restart"])
def analyze(message):
    try:
        global article
        article = crawler(message.text)

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("summary", "descripcion", "autor", "date", "title", "text",
                   "language", "entidades nombradas", "recomendation", "restart")
        bot.reply_to(
            message, "Select what you want to know about the news", reply_markup=markup)

    except Exception:
        bot.reply_to(
            message, "No se pudo procesar la URL. Por favor, intenta de nuevo.")

@bot.message_handler(func=lambda message: message.text.lower() == "summary")
def get_summary(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return    
    bot.reply_to(message,article.summary)


@bot.message_handler(func=lambda message: message.text.lower() == "descripcion")
def get_description(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.description)


@bot.message_handler(func=lambda message: message.text.lower() == "autor")
def obtener_autor(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.authors)


@bot.message_handler(func=lambda message: message.text.lower() == "date")
def obtener_fecha(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.date_publish)


@bot.message_handler(func=lambda message: message.text.lower() == "title")
def obtener_titulo(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.title)


@bot.message_handler(func=lambda message: message.text.lower() == "text")
def obtener_texto(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.text)


@bot.message_handler(func=lambda message: message.text.lower() == "language")
def obtener_idioma(message):
    bot.reply_to(message, article.language)


@bot.message_handler(func=lambda message: message.text.lower() == "entidades nombradas")
def obtener_entidades(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, article.named_entities[0])


@bot.message_handler(func=lambda message: message.text.lower() == "recomendacion")
def obtener_recomendacion(message):
    if article is None:
        bot.reply_to(message, "Plese select a news")
        return
    bot.reply_to(message, "aun no tenemos esa funcionalidad disponible")


# bot.polling()
bot.infinity_polling()
