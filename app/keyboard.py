from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Начать 🎮'), KeyboardButton(text='Помощь 🆘')],
    [KeyboardButton(text='Добавить 🤖 в чат')]
],
                                resize_keyboard=True,
                                input_field_placeholder='Меню')

startinline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить бота в чат', url='https://t.me/PencilGame_Bot?startgroup=start')]
])