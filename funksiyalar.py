from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy import Insert

from base import engine, Unversal


# from database import engine
# from forms import Base
#
#
# def capitalize_chars(name):
#     r = ''
#     for i in name.split():
#         r += i.capitalize()
#     return r
#

# async def first_object():
# with engine.connect() as conn:
#     res = conn.execute(Select(Unversal).limit(1))
#     _id = [int(i['id']) for i in res]
#     conn.execute(Delete(Unversal).where(Unversal.id == _id))
#     conn.commit()


async def menu_button(text, message: Message):
    rkm = ReplyKeyboardBuilder()
    rkm.row(
        KeyboardButton(text='Sherik kerak'), KeyboardButton(text='Ish joy kerak'),
    )
    rkm.row(
        KeyboardButton(text='Hodim kerak'), KeyboardButton(text='Ustoz kerak'),
    )
    rkm.row(
        KeyboardButton(text='Shogird kerak')
    )
    await message.answer(
        text,
        reply_markup=rkm.as_markup(resize_keyboard=True))


async def button_ha_yoq(text, message):
    await message.answer(text=text)
    rkm = ReplyKeyboardBuilder()
    rkm.add(KeyboardButton(text='Ha'), KeyboardButton(text="Yo'q"))
    rkm.adjust(2)
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=rkm.as_markup(resize_keyboard=True))


async def insert_into(name, data):
    with engine.connect() as conn:
        if name == 'Sherik kerak':
            query = Insert(Unversal).values(ism_familya=data['ism_familya'], texnalogiya=data['texnalogiya'],
                                            aloqa=data['aloqa'], hudud=data['hudud'], narxi=data['narxi'],
                                            kasbi=data['kasbi'], murojat_vaqti=data['murojat_vaqti'],
                                            maqsad=data['maqsad'],
                                            type=name)
        elif name in ['Ustoz kerak', 'Shogird kerak', 'Ish joy kerak']:
            query = Insert(Unversal).values(ism_familya=data['ism_familya'], yosh=data['yosh'],
                                            texnalogiya=data['texnalogiya'],
                                            aloqa=data['aloqa'], hudud=data['hudud'], narxi=data['narxi'],
                                            kasbi=data['kasbi'], murojat_vaqti=data['murojat_vaqti'],
                                            maqsad=data['maqsad'],
                                            type=name)
        elif name == 'Hodim kerak':
            query = Insert(Unversal).values(idora_nomi=data['idora_nomi'], texnalogiya=data['texnalogiya'],
                                            aloqa=data['aloqa'], hudud=data['hudud'], masul_ism=data['masul_ism'],
                                            murojat_vaqti=data['murojat_vaqti'], ish_vaqti=data['ish_vaqti'],
                                            maosh=data['maosh'], qoshimcha_malumot=data['qoshimcha_malumot'],
                                            type=data['type'])
        conn.execute(query)
        conn.commit()


def text_filter(data, name, message):
    user = 'Hodim'
    if name.startswith('Ustoz'):
        user = 'Shogird'
    elif name.startswith('Shogird'):
        user = 'Ustoz'
    text = f"""{name}:

    👨‍💼 {user}: {data['ism_familya']}
    📚 Texnologiya: {data['texnalogiya']}
    🇺🇿 Telegram: @{message.from_user.username}
    📞 Aloqa: {data['aloqa']}
    🌐 Hudud: {data['hudud']}
    💰 Narxi: {data['narxi']}
    👨🏻‍💻 Kasbi: {data['kasbi']}
    🕰 Murojaat qilish vaqti: {data['murojat_vaqti']}
    🔎 Maqsad: {data['maqsad']}

    #xodim"""
    print(name.split()[0], 123456, name)
    if name.split()[0] in ['Ustoz', 'Shogird', 'Ish']:
        text = f"""{name}:

    👨‍💼 {user}: {data['ism_familya']}
    🕑 Yosh: {data['yosh']}
    📚 Texnologiya: {data['texnalogiya']}
    🇺🇿 Telegram: @{message.from_user.username}
    📞 Aloqa: {data['aloqa']}
    🌐 Hudud: {data['hudud']}
    💰 Narxi: {data['narxi']}
    👨🏻‍💻 Kasbi: {data['kasbi']}
    🕰 Murojaat qilish vaqti: {data['murojat_vaqti']}
    🔎 Maqsad: {data['maqsad']}

    #xodim"""
    elif name == 'Hodim':
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

    #ishJoyi"""

    return text


async def text(data, name, message):
    user = 'Hodim'
    if name.startswith('Ustoz'):
        user = 'Shogird'
    elif name.startswith('Shogird'):
        user = 'Ustoz'
    print(data, 11)
    text = f"""{name}:
    
    👨‍💼 {user}: {data[1]}
    📚 Texnologiya: {data[3]}
    🇺🇿 Telegram: @{message.from_user.username}
    📞 Aloqa: {data[4]}
    🌐 Hudud: {data[5]}
    💰 Narxi: {data[6]}
    👨🏻‍💻 Kasbi: {data[8]}
    🕰 Murojaat qilish vaqti: {data[9]}
    🔎 Maqsad: {data[10]}

    #xodim"""
    if name.split()[0] in ['Ustoz', 'Shogird', 'Ish']:
        text = f"""{name}:

    👨‍💼 {user}: {data[1]}
    🕑 Yosh: {data[2]}
    📚 Texnologiya: {data[3]}
    🇺🇿 Telegram: @{message.from_user.username}
    📞 Aloqa: {data[4]}
    🌐 Hudud: {data[5]}
    💰 Narxi: {data[6]}
    👨🏻‍💻 Kasbi: {data[8]}
    🕰 Murojaat qilish vaqti: {data[9]}
    🔎 Maqsad: {data[10]}

    #xodim"""
    elif name == 'Hodim kerak':
        text = f"""Xodim kerak:

    🏢 Idora: {data[11]}
    📚 Texnologiya: {data[3]} 
    🇺🇿 Telegram: @{message.from_user.username} 
    📞 Aloqa: {data[4]}
    🌐 Hudud: {data[5]}
    ✍️ Mas'ul: {data[11]}
    🕰 Murojaat vaqti: {data[9]} 
    🕰 Ish vaqti: {data[12]} 
    💰 Maosh: {data[13]}
    ‼️ Qo`shimcha: {data[14]}

    #ishJoyi"""

    return text
