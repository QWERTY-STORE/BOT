from telegram.ext import ApplicationBuilder
from handlers import start, main_menu, softs_menu, conv_handler_metadata, conv_handler_parser
import os

bot_token = '7014402222:AAGJFY3kaIUNkc7EnVfwRNC8-aHT4wrluwM'

def main():
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(start)
    app.add_handler(main_menu)
    app.add_handler(softs_menu)
    app.add_handler(conv_handler_metadata)
    app.add_handler(conv_handler_parser)

    app.run_polling()

if __name__ == '__main__':
    main()
