import scrapy
import re
from scrapy.selector import Selector
from ..items import TgddPhoneItem

class PhongVuSpider(scrapy.Spider):
    i=1
    name = "tgdd"
    base_url="https://www.thegioididong.com/dtdd#c=42&o=17&pi="
    def start_requests(self):
        start_urls=[
            "https://www.thegioididong.com/dtdd#c=42&o=17&pi=1"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('.item')
        for product in products:
            link_detail = product.css('a::attr(href)').extract_first()
            yield response.follow('https://www.thegioididong.com'+str(link_detail), self.parse_detail)
            # yield scrapy.Request(response.urljoin(link_detail), callback=self.parse_detail, dont_filter=True)

        if self.i < 5:
            self.i += 1
            path_next = self.base_url +str(self.i)
            yield response.follow(path_next, callback=self.parse)

    def parse_detail(self, response):
        phone = TgddPhoneItem()
        phone['company'] = response.css('body > section.detail > ul > li:nth-child(2) > a ::text').extract_first()
        phone['company'] = phone['company'][11:len(phone['company'])]
        phone['color'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div > div.color > a.box03__item ::text').extract()
        phone['name'] = response.css('body > section.detail > h1 ::text').extract_first()
        phone['name'] = phone['name'][11:len(phone['name'])]
        phone['memory'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(7) > div > span ::text').extract_first()

        phone['originPrice'] = response.css(".box-price-old::text").extract_first()
        if phone['originPrice'] == None:
            phone['originPrice'] = response.css(".box-price-present::text").extract_first()
            phone['discountPrice'] = None
            phone['discountRate'] = None
        else:
            phone['discountPrice'] = response.css(".box-price-present::text").extract_first()
            phone['discountRate'] = response.css(".box-price-percent::text").extract_first()


        # originPrice = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-old').extract()
        # if len(originPrice) > 0:
        #     phone['originPrice'] = response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-old ::text').extract_first()
        #     phone['discountRate'] = response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-percent ::text').extract_first()
        #     phone['discountPrice'] = response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-present ::text').extract_first()
        # else:
        #     phone['originPrice'] = response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.box04.box_normal >div.price-one > div > p.box-price-present ::text').extract_first()
        #     if phone['originPrice'] == None:
        #         phone['originPrice'] = response.css(
        #             'body > section.detail > div.box_main > div.box_right > div.box04.notselling > div.price-one > div > p ::text').extract_first()
        #     phone['discountRate'] = None
        #     phone['discountPrice'] = None

        screenInfo = ''
        for info in response.css(
                'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(1) > div > span ::text').extract():
            screenInfo = screenInfo + info + ', '
        screenInfo = screenInfo[0:len(screenInfo) - 2]

        phone['screen'] = screenInfo.replace('"', '')
        phone['operatingSystem'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(2) > div > span ::text').extract_first()
        phone['frontCamera'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(4) > div > span ::text').extract_first()
        phone['behindCamera'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(3) > div > span ::text').extract_first()
        phone['chip'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(5) > div > span ::text').extract_first()
        phone['ram'] = response.css(
            'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(6) > div > span ::text').extract_first()

        simInfo = ''
        for info in response.css(
                'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(8) > div > span ::text').extract():
            simInfo = simInfo + info + ', '
        simInfo = simInfo[0:len(simInfo) - 2]
        phone['sim'] = simInfo

        pinInfo = ''
        for info in response.css(
                'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(9) > div > span ::text').extract():
            pinInfo = pinInfo + info + ', '
        pinInfo = pinInfo[0:len(pinInfo) - 2]
        phone['pin'] = pinInfo

        phone['rate'] = response.css(".point::text").extract_first()
        phone['point'] = response.css(".rating-total::text").extract_first()

        # point = response.css(".rating-total::text").extract_first()
        # phone['point'] = re.search('[0-9][0-9][0-9]', str(point))
        divImage = response.css(".item-border >img::attr(data-src)").extract_first()
        phone['imageUrl'] = divImage


        yield phone



