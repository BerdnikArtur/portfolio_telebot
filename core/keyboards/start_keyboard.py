from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import Optional

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Sign up a reception', callback_data='reception')],
    [InlineKeyboardButton(text='Cancel a reception', callback_data='cancel_reception')],
    [InlineKeyboardButton(text='All recordings', callback_data='all_recordings')]
])

