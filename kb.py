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

activity = [
    [InlineKeyboardButton(text="Сидячий образ жизни, никаких упражнений", callback_data="no_activity"),
    InlineKeyboardButton(text="Легкая активность(небольшие упраженения 1-3 раза в неделю)", callback_data="low_activity")],
    [InlineKeyboardButton(text="Высокая активность(тренируюсь 5-6 раз в неделю)", callback_data="high_activity")],
    [InlineKeyboardButton(text="Каждый день занимаюсь спортом, либо физически активная работа", callback_data="veryhigh_activity")]
]
activity = InlineKeyboardMarkup(inline_keyboard=activity)