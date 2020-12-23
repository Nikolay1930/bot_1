import logging
import asyncio
from message import MESSAGES

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '1484954369:AAEF7O4vZvohDYL8AfH9LfMbrpda7xpdbmI'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

URL = 'https://yoomoney.ru/quickpay/shop-widget?writer=buyer&targets=%D0%B8%D0%BD%D1%81%D1%82%D0%B0%20%D1%84%D0%B5%' \
      'D0%BC%D0%B5%D0%BB%D0%B8&targets-hint=%D0%A3%D0%BA%D0%B0%D0%B6%D0%B8%D1%82%D0%B5%20%D1%81%D0%B2%D0%BE%D0%B9%' \
      '20%D0%BD%D0%B8%D0%BA%20%D0%98%D0%BD%D1%81%D1%82%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%20%40' \
      'nik_tam&default-sum=999&button-text=14&hint=&successURL=&quickpay=shop&account=4100115721797759'


def registration():
    inline_btn_1 = types.InlineKeyboardButton('Оплата', url=URL)
    inline_btn_2 = types.InlineKeyboardButton('Подствердить оплату', callback_data='button')
    inline_kb = types.InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)
    return inline_kb


def pay():
    inline_btn_1 = types.InlineKeyboardButton('Да🔥', callback_data='button1')
    inline_btn_2 = types.InlineKeyboardButton('Еще нет🐣', callback_data='button2')
    inline_kb = types.InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
    return inline_kb


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(MESSAGES['start'], reply_markup=registration())


@dp.callback_query_handler(lambda c: c.data == 'button')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы успешно оплатили подписку?', reply_markup=pay())


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, MESSAGES['pay'])
    await asyncio.sleep(3)
    await bot.send_message(callback_query.from_user.id, 'В ближайшее время куратор проверит оплату и свяжется с вами!')


@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Дерзай😉', reply_markup=registration())


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Введите команду /start для начала работы")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
