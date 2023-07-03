import logging
import asyncio
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ChatActions
from aiogram.utils import exceptions
from aiogram.utils.markdown import bold, code, italic

import config

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик удаления сообщений
@dp.message_handler(content_types=types.ContentType.ANY, func=lambda message: message.delete_for_all)
async def on_message_deleted(message: Message):
    try:
        # Отправляем уведомление в чат админов
        text = config.DELETED_MESSAGE_TEXT.format(
            message=message.text or '',
            author=message.from_user.get_mention(as_html=True),
            time=message.date.strftime('%Y-%m-%d %H:%M:%S')
        )
        if message.photo:
            # Сохраняем фото и отправляем его с описанием
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            await bot.send_photo(chat_id=config.CHAT_ID, photo=file.download(), caption=text)
        elif message.document:
            # Сохраняем документ и отправляем его с описанием
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            await bot.send_document(chat_id=config.CHAT_ID, document=file.download(), caption=text)
        elif message.video:
            # Сохраняем видео и отправляем его с описанием
            file_id = message.video.file_id
            file = await bot.get_file(file_id)
            await bot.send_video(chat_id=config.CHAT_ID, video=file.download(), caption=text)
        elif message.audio:
            # Сохраняем аудио и отправляем его с описанием
            file_id = message.audio.file_id
            file = await bot.get_file(file_id)
            await bot.send_audio(chat_id=config.CHAT_ID, audio=file.download(), caption=text)
        elif message.voice:
            # Сохраняем голосовое сообщение и отправляем его с описанием
            file_id = message.voice.file_id
            file = await bot.get_file(file_id)
            await bot.send_voice(chat_id=config.CHAT_ID, voice=file.download(), caption=text)
        elif message.sticker:
            # Сохраняем стикер и отправляем его с описанием
            file_id = message.sticker.file_id
            file = await bot.get_file(file_id)
            await bot.send_sticker(chat_id=config.CHAT_ID, sticker=file.download(), caption=text)
        elif message.animation:
            # Сохраняем анимацию и отправляем ее с описанием
            file_id = message.animation.file_id
            file = await bot.get_file(file_id)
            await bot.send_animation(chat_id=config.CHAT_ID, animation=file.download(), caption=text)
        else:
            # Отправляем текстовое сообщение
            await bot.send_message(chat_id=config.CHAT_ID, text=text)
    except exceptions.ChatNotFound:
        logging.warning('Чат не найден.')

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    # Отправляем приветственное сообщение
    await message.answer("Привет! Я DeLogger.")

if __name__ == '__main__':
    # Запускаем бота
    asyncio.run(dp.start_polling())