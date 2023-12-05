from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

reception_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='11:00 a.m')],
    [KeyboardButton(text='02:00 p.m')]
], resize_keyboard=True)

end_reception_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='sign up')],
    [KeyboardButton(text='cancel')]
], resize_keyboard=True)

end_cancel_reception_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='yes')],
    [KeyboardButton(text='no')]
], resize_keyboard=True)