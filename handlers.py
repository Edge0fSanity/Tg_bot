from aiogram import F, Router, types, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


import kb
import text

from states import Form
from states import main_states
import db

usersDB = db.usersDB()

#обработка форм:
import logging
from typing import Any, Dict






router = Router()


@router.message(Command('help'))
async def process_help_command(msg: Message):
    await msg.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.delete()
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


@router.message()
async def dont_understand(msg: Message): #Если написали не по теме
    await msg.answer("Извините, я вас не понимаю. Нажмите /start, чтобы перезапустить наш диалог.")





form_router = Router()

@form_router.callback_query(F.data == "user_data")
async def user_data(clbck: CallbackQuery, state: FSMContext):
    if not(usersDB.user_exists(clbck.from_user.id)):
        await clbck.message.delete()
        await clbck.message.answer(
        text.no_user_data, 
        reply_markup=kb.user_data
        )
    else:
        data = usersDB.get_data(int(clbck.from_user.id))
        logging.info(data)
        await clbck.message.answer(
            text.user_data + '\n' + text.form_user_data(data), 
            reply_markup=kb.user_data
        )
    await state.set_state(main_states.form)

@form_router.callback_query(F.data == "Back")
async def back(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    await clbck.message.answer(text.menu, reply_markup=kb.menu)
    



@form_router.callback_query(F.data == "make_user", main_states.form)
async def form_start(clbck: CallbackQuery, state: FSMContext) -> None:
    await clbck.message.answer(
        text.make_user, 
        reply_markup=ReplyKeyboardRemove()
    ) #приветствуем пользователя и сообщаем о возможности отмены
    await clbck.message.answer("На любом из шагов напиши 'Отмена' и мы отложим этот разговор")
    await state.set_state(Form.name)
    await clbck.answer()



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
        "Отменяем...",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(text.menu, reply_markup=kb.menu)



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
    await state.update_data(activity = clbck.data)
    await state.set_state(Form.age)
    await clbck.message.delete()
    await clbck.message.answer(
        "Сколько тебе лет ?",
        reply_markup=ReplyKeyboardRemove(),
    )
    await clbck.answer()


@form_router.message(Form.age)
async def process_age(message: Message, state: FSMContext) -> None:
    await state.update_data(age = message.text)
    await state.set_state(Form.sex)
    await message.delete()
    await message.answer(
        "Какого ты пола ?",
        reply_markup=kb.sex,
    )


@form_router.callback_query(Form.sex)
async def process_age(clbck: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(sex = clbck.data)
    await state.set_state(Form.height)
    await clbck.message.delete()
    await clbck.message.answer(
        "Какой у тебя рост ?",
        reply_markup=ReplyKeyboardRemove(),
    )
    await clbck.answer()


@form_router.message(Form.height)
async def process_height(message: Message, state: FSMContext) -> None:
    await state.update_data(height = message.text)
    await state.set_state(Form.weight)
    await message.delete()
    await message.answer(
        "Теперь укажи свой вес в кг",
        reply_markup=ReplyKeyboardRemove()
    )

@form_router.message(Form.weight)
async def process_weight_summary(message: Message, state: FSMContext) -> None:
    data = await state.update_data(weight = message.text)
    await message.delete()
    await show_summary(message=message, data=data) #реализуем эту функцию, когда пользователь полностью пройдет опрос

    await message.answer("Сохранить новые данные ?", reply_markup=kb.yno)
    await state.set_state(Form.do_save)


@form_router.callback_query(Form.do_save, F.data == "yes") 
async def save_data(clbck: CallbackQuery, state: FSMContext):
    usersDB.delete_user(clbck.from_user.id)
    data = await state.get_data()
    
    usersDB.add_user(clbck.from_user.id, data["name"], data["activity"].replace(',', '.'), data["age"].replace(',', '.'), data["height"].replace(',', '.'), data["weight"].replace(',', '.'), data["sex"])
    
    logging.info(f"User {clbck.from_user.id} data changed")
    
    await clbck.message.delete()
    clbck.message.answer("Данные сохранены", reply_markup=ReplyKeyboardRemove())
    await clbck.message.answer(text.menu, reply_markup=kb.menu)
    await state.clear()
    await clbck.answer()

@form_router.callback_query(Form.do_save, F.data == "no")
async def save_data(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Оставим как было", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await clbck.answer()


async def show_summary(message: Message, data: Dict[str, Any]) -> None:
    text = f"Итак данные вышли такими:\nПользователь: {data["name"]}\n"
    text += f"Пол: {data["sex"]}\n"
    text += f"Активность: {data["activity"]}\n"
    text += f"Возраст: {data["age"]} лет\n"
    text += f"Рост: {data["height"]} см\n"
    text += f"Вес: {data["weight"]} кг"
    
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


