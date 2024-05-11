from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Form(StatesGroup):
    ism_familya = State()
    yosh = State()
    texnalogiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    murojat_vaqti = State()
    maqsad = State()
    idora_nomi = State()
    masul_ism = State()
    ish_vaqti = State()
    maosh = State()
    qoshimcha_malumot = State()
    type = State()



