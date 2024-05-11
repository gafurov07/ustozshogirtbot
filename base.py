from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/tel", echo=True)


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(self):
        result = self.__name__[0].lower()
        for i in self.__name__[1:]:
            if i.isupper():
                result += f'_{i.lower()}'
                continue
            result += i
        return result


class Unversal(Base):
    id = Column(Integer, primary_key=True)
    ism_familya = Column(String(255), nullable=True)
    yosh = Column(String(255), nullable=True)
    texnalogiya = Column(String(255))
    aloqa = Column(String(255))
    hudud = Column(String(255))
    narxi = Column(String(255), nullable=True)
    kasbi = Column(String(255), nullable=True)
    murojat_vaqti = Column(String(255))
    maqsad = Column(Text, nullable=True)
    idora_nomi = Column(String(255), nullable=True)
    masul_ism = Column(String(255), nullable=True)
    ish_vaqti = Column(String(255), nullable=True)
    maosh = Column(String(255), nullable=True)
    qoshimcha_malumot = Column(Text, nullable=True)
    type = Column(String(255))


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
