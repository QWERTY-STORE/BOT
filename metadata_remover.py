from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image

SELECT_IMAGE = range(1)

async def remove_metadata(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Пожалуйста, отправьте фотографии для удаления метаданных.")
    return SELECT_IMAGE

async def select_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['images'] = []
    for photo in update.message.photo:
        file = await photo.get_file()
        file_path = await file.download_to_drive(custom_path=f"{file.file_id}.jpg")
        context.user_data['images'].append(file_path)
    await update.message.reply_text(f"{len(context.user_data['images'])} изображения выбраны. Удаление метаданных...")
    remove_metadata_from_images(context.user_data['images'])
    await update.message.reply_text("Метаданные удалены. Отправка изображений обратно...")
    for image_path in context.user_data['images']:
        with open(image_path, 'rb') as image_file:
            await update.message.reply_photo(photo=image_file)
    return ConversationHandler.END

def remove_metadata_from_images(image_paths):
    for image_path in image_paths:
        img = Image.open(image_path)
        data = img.getdata()
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(data)
        new_img.save(image_path)
