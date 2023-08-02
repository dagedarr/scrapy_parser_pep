from collections import defaultdict

from .settings import BASE_DIR
from .utils import OutputFile


class PepParsePipeline:
    """
    Класс для обработки данных паука PepSpider и сохранения результатов
    в CSV файл.
    """

    def __init__(self):
        self.__BASE_DIR = BASE_DIR
        self.__results = defaultdict(int)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.__results[item.get('status')] += 1
        return item

    def close_spider(self, spider):
        OutputFile.cvs_create(self.__results.copy(), self.__BASE_DIR)
        self.__results.clear()
