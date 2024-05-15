#kb = keyboards, тут храним клавиатуры для меню

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="Профиль", callback_data="user_data"),
    InlineKeyboardButton(text="Начать тренировку", callback_data="exercise_start")],
    [InlineKeyboardButton(text="Получить блюдо", callback_data="send_meal")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

activity = [
    [InlineKeyboardButton(text="Сидячий образ жизни, никаких упражнений", callback_data="Нет активности"),
    InlineKeyboardButton(text="Легкая активность(небольшие упраженения 1-3 раза в неделю)", callback_data="Низкая активность")],
    [InlineKeyboardButton(text="Высокая активность(тренируюсь 5-6 раз в неделю)", callback_data="Высокая активность")],
    [InlineKeyboardButton(text="Каждый день занимаюсь спортом, либо физически активная работа", callback_data="Очень высокая активность")]
]
activity = InlineKeyboardMarkup(inline_keyboard=activity)

sex = [
    [InlineKeyboardButton(text="муж", callback_data="муж"),
    InlineKeyboardButton(text="жен", callback_data="жен")],
]
sex = InlineKeyboardMarkup(inline_keyboard=sex)

yno = [[
    InlineKeyboardButton(text="Да", callback_data="yes"),
    InlineKeyboardButton(text="Нет", callback_data="no")]]
yno = InlineKeyboardMarkup(inline_keyboard=yno)

user_data = [[
    InlineKeyboardButton(text="Заполнить профиль", callback_data="make_user"),
    InlineKeyboardButton(text="Назад", callback_data="Back")]]
user_data = InlineKeyboardMarkup(inline_keyboard=user_data)

meal = [[
    InlineKeyboardButton(text="Завтрак", callback_data="breakfast"),
    InlineKeyboardButton(text="Обед", callback_data="dinner"),
    InlineKeyboardButton(text="Ужин", callback_data="supper")]]
meal = InlineKeyboardMarkup(inline_keyboard=meal)