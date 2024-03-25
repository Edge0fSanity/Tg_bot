from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.handlers import CallbackQueryHandler


import kb
import text

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
    await clbck.message.answer("Бля, братан, тут сам не ебу", reply_markup=kb.exit_kb) 