from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, declared_attr

from .settings import BASE_DIR
from .utils import OutputFile


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class Pep(Base):
    """
    Класс, представляющий модель данных для таблицы Pep в базе данных.
    """
    number = Column(Integer, unique=True)
    name = Column(String(255))
    status = Column(String(32))


class PepParsePipeline:
    """
    Класс для обработки данных паука PepSpider и сохранения результатов в базе
    данных и CSV файл.
    """
    def __init__(self) -> None:
        self.__BASE_DIR = BASE_DIR
        self.__pep_list = []

    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

        # Удаляем все записи из таблицы Pep перед каждым запуском
        # Чтобы избежать дублирования
        self.session.query(Pep).delete()

    def process_item(self, item, spider):
        pep = Pep(
            number=item['number'],
            name=item['name'],
            status=item['status'],
        )
        self.__pep_list.append(pep)
        return item

    def close_spider(self, spider):
        self.bulk_create(self.session, self.__pep_list.copy())
        OutputFile.cvs_create(self.session, Pep, self.__BASE_DIR)
        self.__pep_list = []
        self.session.close()

    @staticmethod
    def bulk_create(session, pep_list):
        session.add_all(pep_list)
        session.commit()
