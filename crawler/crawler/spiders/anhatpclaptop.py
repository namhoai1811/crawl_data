# from pymysql import NULL
import scrapy
import math
from ..items import TgddPhoneItem
# from scrapy_splash import SplashRequest

class PhoneSpider(scrapy.Spider):
    name = '1'
    i = 1
    # allowed_domains = ['www.thegioididong.com/dtdd']
    # start_urls = ['http://www.thegioididong.com/dtdd#c=42&o=9&pi=1/']
    base_url = "https://www.ankhang.vn/laptop.html?page="

    render_script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(5))

            return {
                html = splash:html(),
                url = splash:url(),
            }
        ends
        """

    def start_requests(self):
        start_urls = [
            "https://www.ankhang.vn/laptop.html"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # yield SplashRequest(
            #     url,
            #     self.parse,
            #     endpoint='render.html',
            #     args={
            #         'wait': 20,
            #         # 'lua_source': self.render_script,
            #     }
            # )

    # Do trang tgdđ nó load bằng javascript. Nên cần delay 1 chút
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(
    #             url,
    #             self.parse,
    #             endpoint='render.html',
    #             args={
    #                 'wait': 20,
    #                 'lua_source': self.render_script,
    #             }
    #         )

    def parse(self, response):
        phoneItem = response.css('.p-item-2021 > div > a::attr(href)').extract()
        for phone in phoneItem:
            yield response.follow('https://www.ankhang.vn'+str(phone), self.parse_info_phone)

        if self.i < 52:
            self.i += 1
            path_next = self.base_url +str(self.i)
            yield response.follow(path_next, callback=self.parse)

    def parse_info_phone(self, response):
        phone = TgddPhoneItem()
        phone['category'] = response.css('#breadcrumb > ol > li:nth-child(2) > a > span::text').extract_first()
        # phone['category'] = str(phone['category']).replace(' ','')
        # phone['company'] = response.css('body > section.detail > ul > li:nth-child(2) > a ::text').extract_first()
        # phone['company'] = phone['company'][11:len(phone['company'])]
        # phone['color'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div > div.color > a.box03__item ::text').extract()
        phone['name'] = response.css('#overview-left > h1::text').extract_first()
        # phone['name'] = phone['name'][11:len(phone['name'])]
        # phone['memory'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(7) > div > span ::text').extract_first()
        #
        phone['originPrice'] = response.css('#overview-left > table > tbody > tr > td:nth-child(2) > span.pro-oldprice::text').extract_first()
        phone['originPrice'] = str(phone['originPrice']).replace(' VNĐ', '₫')
        phone['discountPrice'] = response.css('#overview-left > table > tbody > tr:nth-child(2) > td:nth-child(2) > span.pro-price::text').extract_first()
        phone['discountPrice'] = str(phone['discountPrice']).replace(' VNĐ', '₫')
        # if phone['originPrice'] == None:
        #     phone['originPrice'] = response.css(".box-price-present::text").extract_first()
        #     phone['discountPrice'] = None
        #     phone['discountRate'] = None
        # else:
        #     phone['discountPrice'] = response.css(".box-price-present::text").extract_first()
        #     phone['discountRate'] = response.css(".box-price-percent::text").extract_first()
        #
        # screenInfo = ''
        # for info in response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(1) > div > span ::text').extract():
        #     screenInfo = screenInfo + info + ', '
        # screenInfo = screenInfo[0:len(screenInfo) - 2]
        #
        # phone['screen'] = screenInfo.replace('"', '')
        # phone['operatingSystem'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(2) > div > span ::text').extract_first()
        # phone['frontCamera'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(4) > div > span ::text').extract_first()
        # phone['behindCamera'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(3) > div > span ::text').extract_first()
        # phone['chip'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(5) > div > span ::text').extract_first()
        # phone['ram'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(6) > div > span ::text').extract_first()
        #
        # simInfo = ''
        # for info in response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(8) > div > span ::text').extract():
        #     simInfo = simInfo + info + ', '
        # simInfo = simInfo[0:len(simInfo) - 2]
        # phone['sim'] = simInfo
        #
        # pinInfo = ''
        # for info in response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(9) > div > span ::text').extract():
        #     pinInfo = pinInfo + info + ', '
        # pinInfo = pinInfo[0:len(pinInfo) - 2]
        # phone['pin'] = pinInfo
        # phone['rate'] = response.css(".point::text").extract_first()
        # phone['point'] = response.css(".rating-total::text").extract_first()
        phone['url'] = response.request.url
        # divImage = response.css("body > div.product-detail-container > div.product_details > div > div > div.img_product_detail > div.list_img_product_smaill > div.item_img.js-product-img-item.active > a > img::attr(data-src)").extract_first()
        divImage = response.css('.img_product_big >a::attr(href)').extract_first()
        phone['imageUrl'] = divImage

        yield phone