from telegram import Update
from telegram.ext import ContextTypes
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
import csv

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
session_name = 'session_name'
client = TelegramClient(session_name, api_id, api_hash)

GROUP_LINK, FILE_NAME = range(2)

async def start_parser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text='Введите ссылку на группу или канал Telegram:')
    return GROUP_LINK

async def get_group_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['group_link'] = update.message.text
    await update.message.reply_text('Введите имя файла для сохранения (без расширения):')
    return FILE_NAME

async def get_file_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    group_link = context.user_data['group_link']
    file_name = update.message.text.strip() + '.txt'
    context.user_data['file_name'] = file_name

    await update.message.reply_text('Парсинг участников, пожалуйста, подождите...')
    result = await fetch_participants(group_link, file_name)

    await update.message.reply_text(result)
    await update.message.reply_text(f"Файл сохранен как {file_name}")

    # Отправка файла пользователю
    with open(file_name, 'rb') as file:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=file)

    return ConversationHandler.END

async def fetch_participants(group_link, file_name):
    await client.start()
    try:
        entity = await client.get_entity(group_link)
        all_participants = []
        async for participant in client.iter_participants(entity):
            all_participants.append(participant)

        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            for participant in all_participants:
                username = '@' + (participant.username or '')
                writer.writerow([username])

        return f"Всего участников: {len(all_participants)}"
    except ChatAdminRequiredError:
        return "Необходимы права администратора для парсинга участников этого канала или группы."
    except Exception as e:
        return f"Произошла ошибка: {e}"
