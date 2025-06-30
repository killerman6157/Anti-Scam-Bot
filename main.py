from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import report_handler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.db import init_db, get_all_scammers
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

init_db()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("👋 Sannu! Wannan bot yana taimaka maka wajen report ɗin WhatsApp scammers. Yi amfani da /report don farawa.")

@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("/report - Report WhatsApp scammer\n/scammers - Duba jerin lambobin da aka report")

@dp.message_handler(commands=["report"])
async def cmd_report(message: types.Message):
    await report_handler.start_report(message)

@dp.message_handler(state=report_handler.ReportScammer.waiting_for_phone)
async def phone_input(message: types.Message, state: FSMContext):
    await report_handler.process_phone(message, state)

@dp.message_handler(state=report_handler.ReportScammer.waiting_for_reason)
async def reason_input(message: types.Message, state: FSMContext):
    await report_handler.process_reason(message, state)

@dp.message_handler(commands=["scammers"])
async def cmd_scammers(message: types.Message):
    scammers = get_all_scammers()
    if not scammers:
        await message.answer("❌ Babu wanda aka report tukuna.")
    else:
        text = "\n".join([f"{p} - {r}" for p, r in scammers])
        await message.answer(f"🕵️ Jerin scammers:\n{text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
