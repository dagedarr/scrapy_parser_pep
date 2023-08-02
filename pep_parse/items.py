import scrapy


class PepParseItem(scrapy.Item):
    """
    Класс, представляющий объект данных PEP для парсинга и хранения
    результатов.
    """
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
