#kb = keyboards, тут храним клавиатуры для меню

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="Заполнить информацию о себе", callback_data="make_user"),
    InlineKeyboardButton(text="Начать тренировку", callback_data="exercise_start")],
    [InlineKeyboardButton(text="Получить блюдо", callback_data="send_meal")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])