import psycopg

from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import Command

from core.keyboards.start_keyboard import start_keyboard
from core.settings import settings
from core.utils.commands import set_commands
from core.utils.dbconnect import UserDatabase

router = Router()

async def bot_start(bot: Bot):
    await set_commands(bot)
    await bot.send_message(chat_id=settings.bots.admin_id, text='bot is working')

@router.message(F.text == '/start', Command(commands='start'))
async def start(msg: Message, request: UserDatabase):
    image = FSInputFile(path='/home/pickle_slime/div_of_projects/python_folder/telegram-bot/assets/992446758.png', filename='start_image')
    try:
        await request.add_user(msg.from_user.full_name, msg.from_user.id)
    except psycopg.errors.UniqueViolation:
        None
    finally:
        await msg.answer_photo(photo=image, caption='welcome to the registering bot', reply_markup=start_keyboard)
    


