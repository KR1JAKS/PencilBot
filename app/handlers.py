from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
import app.keyboard as k
from app.db import point_pluse, add_player, top, add_chat_id
import sqlite3 as sq
import datetime

router = Router()

@router.message(CommandStart())
async def Start(message : Message):
    user = message.from_user
    if message.chat.type in ['group', 'supergroup', 'channel']:
        await message.reply('Всем привет! Меня зовут Pencil.\n\nЧтобы начать используйте команду /pen.')
    elif message.chat.type == 'private':
        await message.reply(f'Привет, <b>{user.first_name}!</b>\nЯ работаю только в чатах.', 
                            reply_markup=k.main,
                            parse_mode='HTML')

@router.message(Command('pen'))
async def Pencil(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.first_name
    chat_id = message.chat.id

    if message.chat.type in ['group', 'supergroup', 'channel']:
        await add_player(user_id, username, chat_id)
        new_score = await point_pluse(user_id, chat_id)

        if new_score is not None:
            if new_score[0] >= 0:
                await message.reply(f'{user.first_name}, увеличил свой pencil на {new_score[0]} см, теперь он равен {new_score[1]} см!\n\nСледующая попытка будет доступна через 24 часа.',
                                 reply_markup=ReplyKeyboardRemove())
            else:
                await message.reply(f'{user.first_name}, уменьшил свой pencil на {-new_score[0]} см, теперь он равен {new_score[1]} см!\n\nСледующая попытка будет доступна через 24 часа.',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            db = sq.connect('pencils.db')
            cur = db.cursor()
            cur.execute('SELECT next_update FROM accounts WHERE id = ? AND chat_id = ?', (user_id, chat_id))
            next_update_time = cur.fetchone()[0]
            db.close()

            remaining_time = datetime.datetime.strptime(next_update_time, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
            minuts, seconds = divmod(remainder, 60)
            await message.reply(f'Вы уже использовали свою попытку.\n\nСледующая попытка будет через {int(hours)} часов {int(minuts)} минут и {int(seconds)} секунд.')

    elif message.chat.type == 'private':
        await message.reply(f'Привет, <b>{user.first_name}!</b>\nЯ работаю только в чатах.', 
                            reply_markup=k.main,
                            parse_mode='HTML')

@router.message(Command('add'))
async def addbot(message: Message):
    await message.answer('Вы уверены, что хотите добавить бота в чат?',
                         reply_markup=k.startinline)     

@router.message(Command('help'))
async def help(message: Message):
    await message.answer("""
<b>Как начать</b> 🤔
1. Добавьте бота в любой чат телеграмма.
2. Напишите команду /pen.\n
<b>Команды бота</b>
1. /pen - Увеличивает pencil от 0 до 10 см.
2. /topen - Показывает топ 10 игроков чата.\n
<b>ВНИМАНИЕ</b>
Запустить бота можно 1 раз в сутки.\n
<b>Благодарность</b>
<b>Отец бота</b> - Я.
<b>Отдельное спасибо</b> - Мне, ИИ(помогал).
<b>СБЕР:</b> 2202 2063 6416 6301 - на еду.
""", parse_mode='HTML')

@router.message(Command('topen'))
async def top_command(message: Message):
    chat_id = message.chat.id
    players = await top(chat_id)
    if message.chat.type in ['group', 'supergroup', 'channel']:
        if players:
            player_list = "\n".join([f"{index + 1}) {username} - {score} см." for index, (id, username, score) in enumerate(players)])
            await message.reply(f"Топ 15 игроков:\n{player_list}")
        else:
            await message.reply('Список пуст.')

    elif message.chat.type == 'private':
        await message.reply(f'Привет, <b>{message.from_user.first_name}!</b>\nЯ работаю только в чатах.', 
                            reply_markup=k.main,
                            parse_mode='HTML')

@router.message(F.text == 'Помощь 🆘')
async def help_btn(message: Message):
    await help(message)

@router.message(F.text == 'Начать 🎮')
async def Start_btn(message: Message):
    await Start(message)

@router.message(F.text == 'Добавить 🤖 в чат')
async def addbot_btn(message: Message):
    await addbot(message)