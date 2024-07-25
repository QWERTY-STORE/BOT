from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, ContextTypes
from metadata_remover import remove_metadata, select_image, SELECT_IMAGE
from participant_parser import start_parser, get_group_link, get_file_name, GROUP_LINK, FILE_NAME

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Главное меню", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Пожалуйста, перейдите в главное меню.', reply_markup=reply_markup)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Софты", callback_data='softs')],
        [InlineKeyboardButton("Товары", callback_data='goods')],
        [InlineKeyboardButton("Кабинет", callback_data='cabinet')],
        [InlineKeyboardButton("Правила", callback_data='rules')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите категорию:", reply_markup=reply_markup)

async def softs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Удалить метаданные", callback_data='remove_metadata')],
        [InlineKeyboardButton("Парсер чатов", callback_data='chat_parser')],
        [InlineKeyboardButton("Главное меню", callback_data='main_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите опцию:", reply_markup=reply_markup)

conv_handler_metadata = ConversationHandler(
    entry_points=[CallbackQueryHandler(remove_metadata, pattern='remove_metadata')],
    states={SELECT_IMAGE: [MessageHandler(filters.PHOTO, select_image)]},
    fallbacks=[],
    per_chat=True,
    per_user=True
)

conv_handler_parser = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_parser, pattern='chat_parser')],
    states={
        GROUP_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_group_link)],
        FILE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_file_name)]
    },
    fallbacks=[],
    per_chat=True,
    per_user=True
)

start = CommandHandler('start', start)
main_menu = CallbackQueryHandler(main_menu, pattern='main_menu')
softs_menu = CallbackQueryHandler(softs_menu, pattern='softs')
