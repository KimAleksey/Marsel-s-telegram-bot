from dotenv import load_dotenv
from os import getenv
import telebot
from telebot import types
from enum import Enum
from random import randint

# Getting token
load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


class Buttons(Enum):
    GREETING = "👋 О чем тут речь?!"
    ABOUT = "📖 Обо мне"
    HOBBIES = "🍣 Мои увлечения"
    PHOTO = "📸 Мои фото"


class GetInfo:
    @staticmethod
    def get_history_text() -> str:
        with open('./data/history.txt', 'r', encoding='utf-8') as f:
            return ''.join(f.readlines())

    @staticmethod
    def get_hobbies_text() -> str:
        with open('./data/hobbies.txt', 'r', encoding='utf-8') as f:
            return ''.join(f.readlines())


class SendImage:
    PATH = './data/'

    def __init__(self, bot: telebot.TeleBot):
        self._bot = bot
        self._number = randint(1, 7)

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, value=None) -> None:
        if value is None:
            value = randint(1, 7)
        self._number = value

    def image_path(self):
        return SendImage.PATH + f"{self._number}.JPG"

    def send_image(self, chat_id) -> None:
        with open(self.image_path(), 'rb') as img:
            self._bot.send_photo(chat_id, photo=img)


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(Buttons.GREETING.value)
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я Марсель, давай, дружить!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    # Инициализация класса для отправки изображений
    image_sender = SendImage(bot)

    # Handler
    if message.text == Buttons.GREETING.value:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # создание новых кнопок
        btn1 = types.KeyboardButton(Buttons.ABOUT.value)
        btn2 = types.KeyboardButton(Buttons.HOBBIES.value)
        btn3 = types.KeyboardButton(Buttons.PHOTO.value)
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, '❓ Что вам интересно?', reply_markup=markup) # ответ бота


    elif message.text == Buttons.ABOUT.value:
        bot.send_message(message.from_user.id, GetInfo.get_history_text(), parse_mode='Markdown')

    elif message.text == Buttons.HOBBIES.value:
        bot.send_message(message.from_user.id, GetInfo.get_hobbies_text(), parse_mode='Markdown')

    elif message.text == Buttons.PHOTO.value:
        buff = image_sender.number
        while buff == image_sender.number:
            image_sender.number = randint(1, 7)
        image_sender.send_image(message.chat.id)


bot.polling(none_stop=True, interval=0) # обязательная для работы бота часть