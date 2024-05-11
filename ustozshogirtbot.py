import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton
from aiogram.utils.i18n import gettext as _, lazy_gettext as __, I18n, FSMI18nMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from redis_dict import RedisDict
from sqlalchemy import Select, Delete

from base import Unversal, engine
from forms import Form
from funksiyalar import menu_button, button_ha_yoq, insert_into, text_filter, text

TOKEN = "6686631791:AAFWVmn_1tF64N5qZBlkEA4dBL0H7-zLVB0"
database = RedisDict()
admin_list = [5760868166]
dp = Dispatcher()
name = ''
'''
-1002107185115 @praktikaa_0007_bot
'''


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    rkm = ReplyKeyboardBuilder()
    rkm.add(
        KeyboardButton(text=_('Sherik kerak')), KeyboardButton(text=_('Ish joy kerak')),
        KeyboardButton(text=_('Hodim kerak')), KeyboardButton(text=_('Ustoz kerak')),
        KeyboardButton(text=_('Shogird kerak'))
    )
    rkm.adjust(2, 2, 1)
    await message.answer(
        f"Assalom alaykum {html.bold(message.from_user.full_name)} \nUstozShogird kanalining rasmiy botiga xush kelibsiz! \n\n/help yordam buyrugi orqali nimalarga qodir ekanligimni bilib oling",
        reply_markup=rkm.as_markup())


@dp.message(Command('news'), F.from_user.id.in_(admin_list))
async def command_news(message: Message):
    with engine.connect() as conn:
        res = conn.execute(Select(Unversal).limit(1))
        _id = 0
        _name = ''
        for i in res:
            r = i
            _id += int(i[0])
            _name = i[-1]
        conn.execute(Delete(Unversal).where(Unversal.id == _id))
        conn.commit()
    tex = await text(data=r, name=_name, message=message)
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='Jonatish', callback_data='send'),
            InlineKeyboardButton(text='Bekor qilish', callback_data='cancel'))
    await message.answer(tex, reply_markup=ikb.as_markup())


@dp.message(F.text == __('Ha'))
async def ha(message: Message, state: FSMContext):
    data = await state.get_data()
    global name
    print(*data.values())
    await insert_into(name=name, data=data)
    text = "📪 So`rovingiz tekshirish uchun adminga jo`natildi! \n\nE'lon 24-48 soat ichida kanalda chiqariladi."
    await menu_button(text, message)


@dp.message(F.text == "Yo'q")
async def ha(message: Message):
    text = "Qabul qilinmadi"
    await menu_button(text, message)


@dp.message(F.text.endswith("kerak"))
async def sherik(message: Message, state: FSMContext):
    global name
    name = message.text
    if name.split()[0] in ['Ustoz', 'Shogird', 'Ish', 'Sherik']:
        await state.set_state(Form.ism_familya)
        await message.answer(
            f"{name.split()[0]} topish uchun ariza berish\n\nHozir sizga birnecha savollar beriladi.\nHar biriga javob bering.\nOxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.")
        await message.answer('Ism, familiyangizni kiriting?')
    elif name.startswith('Hodim'):
        await state.set_state(Form.idora_nomi)
        await message.answer(
            f"{name.split()[0]} topish uchun ariza berish\n\nHozir sizga birnecha savollar beriladi.\nHar biriga javob bering.\nOxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.")
        await message.answer(
            "🎓 Idora nomi?")


@dp.message(Form.ism_familya)
async def ism(message: Message, state: FSMContext):
    await state.update_data(ism_familya=message.text)
    global name
    if name.split()[0] in ['Ustoz', 'Shogird', 'Ish']:
        await state.set_state(Form.yosh)
        await message.answer("🕑 Yosh: \n\nYoshingizni kiriting?\nMasalan, 19")
    else:
        await state.set_state(Form.texnalogiya)
        await message.answer(
            "📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan, \n\nJava, C++, C#")


@dp.message(Form.idora_nomi)
async def hodim_1(message: Message, state: FSMContext):
    await state.update_data(idora_nomi=message.text)
    await state.set_state(Form.texnalogiya)
    await message.answer(
        "📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan,\n\nJava, C++, C#")


@dp.message(Form.masul_ism)
async def hodim_1(message: Message, state: FSMContext):
    await state.update_data(masul_ism=message.text)
    await state.set_state(Form.murojat_vaqti)
    await message.answer("🕰 Murojaat qilish vaqti: \n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")


@dp.message(Form.ish_vaqti)
async def hodim_1(message: Message, state: FSMContext):
    await state.update_data(ish_vaqti=message.text)
    await state.set_state(Form.maosh)
    await message.answer("💰 Maoshni kiriting?")


@dp.message(Form.maosh)
async def hodim_1(message: Message, state: FSMContext):
    await state.update_data(maosh=message.text)
    await state.set_state(Form.qoshimcha_malumot)
    await message.answer("‼️ Qo`shimcha ma`lumotlar?")


@dp.message(Form.qoshimcha_malumot)
async def hodim_1(message: Message, state: FSMContext):
    global name
    await state.update_data(qoshimcha_malumot=message.text)
    await state.update_data(type=name)
    data = await state.get_data()
    text = f"""Xodim kerak:

🏢 Idora: {data['idora_nomi']}
📚 Texnologiya: {data['texnalogiya']}
🇺🇿 Telegram: @{message.from_user.username}
📞 Aloqa: {data['aloqa']}
🌐 Hudud: {data['hudud']}
✍️ Mas'ul: {data['masul_ism']}
🕰 Murojaat vaqti: {data['murojat_vaqti']}
🕰 Ish vaqti: {data['ish_vaqti']}
💰 Maosh: {data['maosh']}
‼️ Qo`shimcha: {data['qoshimcha_malumot']}

#xodim"""
    await button_ha_yoq(text, message)


@dp.message(Form.yosh)
async def process_yosh(message: Message, state: FSMContext):
    await state.update_data(yosh=message.text)
    await state.set_state(Form.texnalogiya)
    await message.answer(
        "📚 Texnologiya:\n\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan, \n\nJava, C++, C#")


@dp.message(Form.texnalogiya)
async def process_yosh(message: Message, state: FSMContext):
    await state.update_data(texnalogiya=message.text)
    await state.set_state(Form.aloqa)
    await message.answer("📞 Aloqa:\n\nBog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67")


@dp.message(Form.aloqa)
async def process_yosh(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(Form.hudud)
    await message.answer("🌐 Hudud:\n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")


@dp.message(Form.hudud)
async def process_yosh(message: Message, state: FSMContext):
    global name
    if name == 'Hodim kerak':
        await state.update_data(hudud=message.text)
        await state.set_state(Form.masul_ism)
        await message.answer("✍️Mas'ul ism sharifi?")
    else:
        await state.update_data(hudud=message.text)
        await state.set_state(Form.narxi)
        await message.answer("💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?")


@dp.message(Form.narxi)
async def process_yosh(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await state.set_state(Form.kasbi)
    await message.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba")


@dp.message(Form.kasbi)
async def process_yosh(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await state.set_state(Form.murojat_vaqti)
    await message.answer("🕰 Murojaat qilish vaqti: \n\nQaysi vaqtda murojaat qilish mumkin?\nMasalan, 9:00 - 18:00")


@dp.message(Form.murojat_vaqti)
async def process_yosh(message: Message, state: FSMContext):
    global name
    await state.update_data(murojat_vaqti=message.text)
    if name == 'Hodim kerak':
        await state.set_state(Form.ish_vaqti)
        await message.answer("🕰 Ish vaqtini kiriting?")
    else:
        await state.set_state(Form.maqsad)
        await message.answer("🔎 Maqsad: \n\nMaqsadingizni qisqacha yozib bering.")


@dp.message(Form.maqsad)
async def process_yosh(message: Message, state: FSMContext):
    global name
    await state.update_data(maqsad=message.text)
    await state.update_data(type=name)
    data = await state.get_data()
    text = text_filter(data=data, name=name, message=message)
    await button_ha_yoq(text, message)


@dp.callback_query(F.data == 'send')
async def callback_data(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=-1002107185115, text=callback.message.text)
    await command_news(callback.message)


@dp.callback_query(F.data == 'cancel')
async def callback_data(callback: CallbackQuery):
    await command_news(callback.message)


@dp.message(F.text == '')
async def main() -> None:
    i18n = I18n(path="locales")
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    await dp.start_polling(Bot(TOKEN))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
