import telebot
from news_crawler.crawler import crawler
from news_crawler.analyze import analyze
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardRemove

new = "https://www.washingtonpost.com/national-security/2024/02/12/trump-immunity-supreme-court-appeal-jan-6/"

article = crawler(new)
analyze(article)




bot = telebot.TeleBot("6876084200:AAHTQM2vDcBYZunoFqKFaNzDPdXwZ3y4vd8")

@bot.message_handler(commands=["help", "start", ])

def saludar(message):
    markup=ReplyKeyboardRemove()
    bot.reply_to(message, "Hola, envianos el url de una noticia y la analizaremos por ti")

@bot.message_handler(func=lambda message: message.text.startswith("http"))   

def analizar(message):
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("descripcion", "autor", "fecha", "titulo", "texto", "idioma", "entidades nombradas", "recomendacion", "restart")
    bot.reply_to(message, "selecciona que quieres saber sobre la noticia ", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == "descripcion")
def obtener_descripcion(message):
    bot.reply_to(message, article.description)

@bot.message_handler(func=lambda message: message.text.lower() == "autor")
def obtener_autor(message):
    bot.reply_to(message, article.authors)

@bot.message_handler(func=lambda message: message.text.lower() == "fecha")
def obtener_fecha(message):
    bot.reply_to(message, article.date_publish)

@bot.message_handler(func=lambda message: message.text.lower() == "titulo")
def obtener_titulo(message):
    bot.reply_to(message, article.title)

@bot.message_handler(func=lambda message: message.text.lower() == "texto")
def obtener_texto(message):
    bot.reply_to(message, article.text)

@bot.message_handler(func=lambda message: message.text.lower() == "idioma")
def obtener_idioma(message):
    bot.reply_to(message, article.language)

@bot.message_handler(func=lambda message: message.text.lower() == "entidades nombradas")
def obtener_entidades(message):
    bot.reply_to(message, article.named_entities[0])

@bot.message_handler(func=lambda message: message.text.lower() == "recomendacion")
def obtener_recomendacion(message):
    bot.reply_to(message, "aun no tenemos esa funcionalidad disponible")

bot.polling()
