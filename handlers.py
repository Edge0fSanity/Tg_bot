from aiogram import F, Router, types, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.handlers import CallbackQueryHandler
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import kb
import text


#обработка форм:
import logging
import sys
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
async def form_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer(
        text.make_user + "\nНа любом из шагов напиши 'Отмена' и мы отложим этот разговор",
        reply_markup=ReplyKeyboardRemove(),
    )


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





router = Router()


@router.message(Command('help'))
async def process_help_command(msg: types.Message):
    await msg.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню") #F - это элемент библиотеки magick-filters, поставляемой с aiogram
@router.message(F.text == "Выйти в меню") # lambda message: message.text == 'Выйти в меню'
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "help") #Попытка обработки нажатия кнопки помощи
async def input_text_prompt(clbck: CallbackQueryHandler):
    await clbck.message.answer("Сам не ебу, бро", reply_markup=kb.exit_kb) 
    await clbck.answer()

@router.callback_query(F.data == "exercise_start") #Попытка обработки нажатия начать упражнение
async def input_text_prompt(clbck: CallbackQueryHandler):
    await clbck.message.answer("Сначала заполни информацию о себе, долбоеб", reply_markup=kb.exit_kb) 
    await clbck.answer()

@router.callback_query(F.data == "send_meal") #Попытка обработки нажатия получить блюдо
async def input_text_prompt(clbck: CallbackQueryHandler):
    await clbck.message.answer("Сначала заполни информацию о себе, долбоеб", reply_markup=kb.exit_kb) 
    await clbck.answer()