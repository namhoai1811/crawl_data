# from pymysql import NULL
import scrapy
import math
from ..items import TgddPhoneItem
from scrapy_splash import SplashRequest


# Spider này dùng để crawl những điện thoại
# mà có từ 2 option trở lên
# do dev không pass qua được cái điều kiện của scrapy
# là không được request cùng 1 trang web

class PhoneSpider(scrapy.Spider):
    name = 'hoangha'
    i = 1
    # allowed_domains = ['https://viettelstore.vn']
    # start_urls = ['http://www.thegioididong.com/dtdd#c=42&o=9&pi=1/']
    base_url = "https://viettelstore.vn/dien-thoai"

    render_script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(4))
            assert(splash:runjs("$('#div_Danh_Sach_San_Pham_loadMore_btn > a')[0].click();"))
            assert(splash:wait(4))
            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

    def start_requests(self):
        start_urls = [
            "https://hoanghamobile.com/laptop?p=12#page_12"
        ]
        for url in start_urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(
                url,
                self.parse,
                endpoint='render.html',
                args={
                    'wait': 5,
                    'lua_source': self.render_script,
                }
            )

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
        phoneItem = response.css('.item > div> a::attr(href)').extract()
        print(phoneItem)
        for phone in phoneItem:
            # yield scrapy.Request(response.urljoin(phone), callback=self.parse_info_phone, dont_filter=True)

            yield SplashRequest(
                'https://hoanghamobile.com'+str(phone),
                self.parse_info_phone,
                endpoint='render.html',
                args={
                    'wait': 5,
                    'lua_source': self.render_script,
                },
                meta={'original_url': 'https://hoanghamobile.com'+str(phone)}
            )

        # if self.i < 5:
        #     self.i += 1
        #     path_next = self.base_url +str(self.i)
        #     yield response.follow(path_next, callback=self.parse)

    # Request tới từng option memory

    # Bat dau boc tach du lieu nhoe!
    def parse_info_phone(self, response):
        print(response.request.url)
        phone = TgddPhoneItem()
        phone['category'] = response.css('body > section:nth-child(2) > div > ol > li:nth-child(2) > a > span::text').extract_first()
        phone['company'] = response.css('body > section:nth-child(2) > div > ol > li:nth-child(3) > a > span::text').extract_first()
        # phone['color'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div > div.color > a.box03__item ::text').extract()
        name = ''
        phone['name'] = response.css('body > section:nth-child(3) > div > div > div.top-product > h1::text').extract()

        # # phone['name'] = phone['name'][11:len(phone['name'])]
        # phone['memory'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(7) > div > span ::text').extract_first()
        #

        phone['originPrice'] = response.css('body > section:nth-child(3) > div > div > div.product-details-container > div.product-center > p.price.current-product-price > i:nth-child(2) > strike::text').extract_first()
        if phone['originPrice'] == None:
            phone['originPrice'] = response.css('body > section:nth-child(3) > div > div > div.product-details-container > div.product-center > p.price.current-product-price > strong::text').extract_first()
            phone['discountPrice'] = None
            phone['discountRate'] = None
        else:
            phone['discountPrice'] = response.css('body > section:nth-child(3) > div > div > div.product-details-container > div.product-center > p.price.current-product-price > strong::text').extract_first()
            phone['discountRate'] = None


        # screenInfo = ''
        # for info in response.css(
        #         'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(1) > div > span ::text').extract():
        #     screenInfo = screenInfo + info + ', '
        # screenInfo = screenInfo[0:len(screenInfo) - 2]
        #
        # phone['screen'] = screenInfo.replace('"', '')
   #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(3) > div > span ::text').extract_first()
        # phone['chip'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(5) > div > span ::text').extract_first()
        phone['ram'] = response.css('body > section:nth-child(4) > div > div > div.product-right > div > div.specs-special > ol:nth-child(3) > li > span ::text').extract_first()

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
        divImage = response.css('.p > div > img::attr(src)').extract_first()
        phone['url'] = response.meta['original_url']

        phone['imageUrl'] = divImage

        yield phone