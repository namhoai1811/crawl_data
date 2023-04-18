# from pymysql import NULL
import scrapy
import math
from ..items import TgddPhoneItem
# from scrapy_splash import SplashRequest


# Spider này dùng để crawl những điện thoại
# mà có từ 2 option trở lên
# do dev không pass qua được cái điều kiện của scrapy
# là không được request cùng 1 trang web

class PhoneSpider(scrapy.Spider):
    name = 'phone'
    i = 1
    allowed_domains = ['www.thegioididong.com/dtdd']
    # start_urls = ['http://www.thegioididong.com/dtdd#c=42&o=9&pi=1/']
    base_url = "https://www.thegioididong.com/dtdd#c=42&o=17&pi="

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
            "https://www.thegioididong.com/dtdd#c=42&o=17&pi=1"
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
        phoneItem = response.css('div.container-productbox > ul > li > a.main-contain ::attr(href)').extract()
        for phone in phoneItem:
            yield scrapy.Request(response.urljoin(phone), callback=self.parse_type_phone, dont_filter=True)

        # if self.i < 5:
        #     self.i += 1
        #     path_next = self.base_url +str(self.i)
        #     yield response.follow(path_next, callback=self.parse)

    # Request tới từng option memory
    def parse_type_phone(self, response):

        url = response.request.url
        opstion = response.css(
            "body > section.detail > div.box_main > div.box_right > div.scrolling_inner > div >a::attr(href)").extract()
        if len(opstion):
            url = response.css(
                'body > section.detail > div.box_main > div.box_right > div:nth-child(1) > div > a ::attr(href)').extract()
            for i in range(len(url)):
                # if i > 0:
                yield scrapy.Request(response.urljoin(url[i]), callback=self.parse_info_phone, dont_filter=True)
        else:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_info_phone, dont_filter=True)

    # Bat dau boc tach du lieu nhoe!
    def parse_info_phone(self, response):
        phone = TgddPhoneItem()
        phone['category'] = response.css('body > section.detail > ul > li:nth-child(1) > a ::text').extract_first()
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
        #     phone['originPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-old ::text').extract_first()
        #     phone['discountRate'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-percent ::text').extract_first()
        #     phone['discountPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-present ::text').extract_first()
        # else:
        #     phone['originPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal >div.price-one > div > p.box-price-present ::text').extract_first()
        #     if phone['originPrice'] == None:
        #         phone['originPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.notselling > div.price-one > div > p ::text').extract_first()
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
        phone['url'] = response.request.url

        divImage = response.css(".item-border >img::attr(data-src)").extract_first()
        phone['imageUrl'] = divImage

        yield phone