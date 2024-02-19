from bot.telegram_bot import TelegramBot
import logging

def main():
    logging.basicConfig(level=logging.INFO)

    bot = TelegramBot()
    bot.start()


if __name__ == "__main__":
    main()
