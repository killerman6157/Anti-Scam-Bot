from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.db import add_scammer

class ReportScammer(StatesGroup):
    waiting_for_phone = State()
    waiting_for_reason = State()

async def start_report(message: types.Message):
    await message.answer("📞 Shigar da lambar WhatsApp scammer (misali: +2348012345678):")
    await ReportScammer.waiting_for_phone.set()

async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("✍️ Me wannan mutumin ya aikata? (gajeren bayani)")
    await ReportScammer.waiting_for_reason.set()

async def process_reason(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    phone = user_data['phone']
    reason = message.text

    add_scammer(phone, reason)

    report_template = f"""📢 WhatsApp SCAMMER REPORT

Lamba: {phone}
Dalili: {reason}

📝 Zaka iya turawa WhatsApp Support a: wa.me/wa_support
