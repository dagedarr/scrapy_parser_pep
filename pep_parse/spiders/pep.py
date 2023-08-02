from re import sub
from urllib.parse import urljoin


import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    """
    Паук для парсинга PEP с веб-сайта peps.python.org.
    """
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response: scrapy.http.Response):
        """
        Парсит главную страницу для получения URL всех PEP и следует
        за ними для дальнейшего парсинга.

        Параметры:
            response (scrapy.http.Response): Объект ответа, представляющий
                                             главную страницу.

        Возвращает:
            Iterator[scrapy.http.Request]: Итератор запросов scrapy для
                                           следования по URL PEP.
        """
        sections = response.css('section[id="index-by-category"]')
        for section in sections.css('tr'):
            url = section.css(
                'a[class="pep reference internal"]::attr(href)').get()
            if url is not None:
                full_url = urljoin(self.start_urls[0], url)
                yield response.follow(full_url, callback=self.parse_pep)
            continue

    def parse_pep(self, response):
        """
        Парсит индивидуальную страницу PEP и возвращает объект PepParseItem
        с деталями PEP.

        Параметры:
            response (scrapy.http.Response): Объект ответа, представляющий
                                             страницу PEP.

        Возвращает:
            Iterator[PepParseItem]: Итератор объектов PepParseItem с деталями
                                    PEP.
        """
        raw_page_title = response.css('.page-title *::text').getall()
        page_title = ''.join(raw_page_title).strip()

        # pep_number = ''.join(
        #     [chr for chr in page_title.split(' – ')[0] if chr.isdigit()]
        # )
        pep_number = sub(r'[^0-9]', '', page_title.split(' – ')[0])

        name = page_title.split(' – ')[1]
        status = response.css('abbr::text').get()
        data = {
            'number': pep_number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data.copy())
