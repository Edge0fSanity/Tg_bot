from aiogram import F, Router, types, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import kb
import text


#обработка форм:
import logging
from typing import Any, Dict

class Form(StatesGroup):
    name = State()
    activity = State()
    age = State()
    height = State()
    sex = State()
    weight = State()

form_router = Router()


#стартуем машину состояний

@form_router.callback_query(F.data == "make_user")
async def form_start(clbck: CallbackQuery, state: FSMContext) -> None:
    await clbck.message.answer(
        text.make_user, 
        reply_markup=ReplyKeyboardRemove()
    ) #приветствуем пользователя и сообщаем о возможности отмены
    await clbck.message.answer("На любом из шагов напиши 'Отмена' и мы отложим этот разговор")
    await state.set_state(Form.name)


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "А начиналось так красиво...",
        reply_markup=ReplyKeyboardRemove(),
    )


@form_router.message(Form.name)
async def process_name(message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        f"Привет, {html.quote(message.text)}!",
            resize_keyboard=True, 
            reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.activity)
    await message.answer("Как бы ты оценил свой уровень активности ?",
    reply_markup=kb.activity
    )
    
@form_router.callback_query(Form.activity)
async def process_activity(clbck: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(activity = F.data)
    await state.set_state(Form.age)
    await clbck.message.answer(
        "Сколько тебе лет ?",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Form.age)
async def process_age(clbck: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(age = F.text)
    await state.set_state(Form.height)
    await clbck.answer(
        "Какого ты пола ?",
        reply_markup=kb.sex,
    )
    await clbck.answer()

@form_router.callback_query(Form.height)
async def process_age(clbck: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(sex = F.data)
    await state.set_state(Form.weight)
    await clbck.message.answer(
        "Укажи свой вес в кг",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.message(Form.height)
async def process_age(clbck: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(weight = F.text)
    await state.clear()
    
    await show_summary(message=clbck.message, data=state.data.get(), positive=False) #реализуем эту функцию, когда пользователь полностью пройдет опрос



async def show_summary(clbck: CallbackQuery, data: Dict[str, Any], positive: bool = True) -> None:
    text = f"Итак данные вышли такими:\n Пользователь: {data["name"]}\n"
    text += f"Пол: {data["sex"]}\n"
    text += f"Активность: {data["activity"]}\n"
    text += f"Возраст: {data["age"]}\n"
    text += f"Рост: {data["height"]}\n"
    text += f"Вес: {data["weight"]}\n"+"Спасибо за прохождение анкетирования !"
    
    await clbck.answer(text=text, reply_markup=ReplyKeyboardRemove())


router = Router()


@router.message(Command('help'))
async def process_help_command(msg: Message):
    await msg.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню") #F - это элемент библиотеки magick-filters, поставляемой с aiogram
@router.message(F.text == "Выйти в меню") # lambda message: message.text == 'Выйти в меню'
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, clbck: CallbackQuery):
    await msg.answer(text.menu, reply_markup=kb.menu)
    await clbck.answer()

@router.callback_query(F.data == "help") #Попытка обработки нажатия кнопки помощи
async def input_text_prompt(clbck: CallbackQuery):
    await clbck.message.answer("Сам не ебу, бро", reply_markup=kb.exit_kb) 
    await clbck.answer()

@router.callback_query(F.data == "exercise_start") #Попытка обработки нажатия начать упражнение
async def input_text_prompt(clbck: CallbackQuery):
    await clbck.message.answer("Сначала заполни информацию о себе, долбоеб", reply_markup=kb.exit_kb) 
    await clbck.answer()

@router.callback_query(F.data == "send_meal") #Попытка обработки нажатия получить блюдо
async def input_text_prompt(clbck: CallbackQuery):
    await clbck.message.answer("Сначала заполни информацию о себе, долбоеб", reply_markup=kb.exit_kb) 
    await clbck.answer()