# from pymysql import NULL
import scrapy
import math
from ..items import TgddLaptopItem
from scrapy_splash import SplashRequest


# Spider này dùng để crawl những điện thoại
# mà có từ 2 option trở lên
# do dev không pass qua được cái điều kiện của scrapy
# là không được request cùng 1 trang web

class PhoneSpider(scrapy.Spider):
    name = 'fpt'
    i = 1
    # allowed_domains = ['https://viettelstore.vn']
    # start_urls = ['http://www.thegioididong.com/dtdd#c=42&o=9&pi=1/']
    base_url = "https://viettelstore.vn/dien-thoai"

    render_script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            splash:set_viewport_full()
            # local element = splash:select('#div_Danh_Sach_San_Pham_loadMore_btn > a')
            # local bounds = element:bounds()
            # assert(element:mouse_click{x=bounds.width/2, y=bounds.height/2})
                # assert(splash:runjs("$('#div_Danh_Sach_San_Pham_loadMore_btn > a')[0].click();"))
            assert(splash:wait(10))

            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

    def start_requests(self):
        start_urls = [
            "https://fptshop.com.vn/may-tinh-xach-tay?sort=ban-chay-nhat&trang=9"
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
        # listItem = response.css('.p-item > a::attr(href)').extract()
        listItem = response.css('.cdt-product')
        for item in listItem:
            laptop = TgddLaptopItem()
            laptop['category'] = 'Laptop'
            laptop['name'] = item.css('.cdt-product__info > h3 ::text').extract_first()
            laptop['discountPrice'] = item.css('.cdt-product__info > .cdt-product__show-promo > .progress::text').extract_first()
            laptop['originPrice'] = item.css('.cdt-product__info > .cdt-product__show-promo > .strike-price > strike::text').extract_first()
            laptop['screen'] = item.css('.cdt-product__config > div.cdt-product__config__param > span:nth-child(1) ::text').extract_first()
            laptop['cpu'] = item.css('.cdt-product__config > div.cdt-product__config__param > span:nth-child(2) ::text').extract_first()
            laptop['ram'] = item.css('.cdt-product__config > div.cdt-product__config__param > span:nth-child(3) ::text').extract_first()
            laptop['memory'] = item.css('.cdt-product__config > div.cdt-product__config__param > span:nth-child(4) ::text').extract_first()
            laptop['card'] = item.css('.cdt-product__config > div.cdt-product__config__param > span:nth-child(5) ::text').extract_first()
            laptop['imageUrl'] = 'https://fptshop.com.vn/' + str(item.css('.cdt-product__img > a > img ::attr(src)').extract_first())
            laptop['url'] = 'https://fptshop.com.vn/' + str(item.css('.cdt-product__img > a::attr(href)').extract_first())

            if ((laptop['discountPrice'] == None) & (laptop['discountPrice'] == None)):
                laptop['originPrice'] = item.css('.cdt-product__info > .cdt-product__price > .tcdm text-left > .price::text').extract_first()
            else:
                yield laptop


    # Bat dau boc tach du lieu nhoe!
    def parse_info_phone(self, response):
        print(response.request.url)
        phone = TgddLaptopItem()
        phone['category'] = response.css('#_price_new436::text').extract()
        phone['company'] = response.css('.owl-wrapper-outer > div > div > div > img').extract_first()
        # phone['color'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div > div.color > a.box03__item ::text').extract()
        # phone['name'] = response.css('body > section.detail > h1 ::text').extract_first()
        # # phone['name'] = phone['name'][11:len(phone['name'])]
        # phone['memory'] = response.css(
        #     'body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(7) > div > span ::text').extract_first()
        #
        # phone['originPrice'] = response.css(".box-price-old::text").extract_first()
        # if phone['originPrice'] == None:
        #     phone['originPrice'] = response.css(".box-price-present::text").extract_first()
        #     phone['discountPrice'] = None
        #     phone['discountRate'] = None
        # else:
        #     phone['discountPrice'] = response.css(".box-price-present::text").extract_first()
        #     phone['discountRate'] = response.css(".box-price-percent::text").extract_first()
        # # originPrice = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-old').extract()
        # # if len(originPrice) > 0:
        # #     phone['originPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-old ::text').extract_first()
        # #     phone['discountRate'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-percent ::text').extract_first()
        # #     phone['discountPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal > div.price-one > div > p.box-price-present ::text').extract_first()
        # # else:
        # #     phone['originPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.box_normal >div.price-one > div > p.box-price-present ::text').extract_first()
        # #     if phone['originPrice'] == None:
        # #         phone['originPrice'] = response.css('body > section.detail > div.box_main > div.box_right > div.box04.notselling > div.price-one > div > p ::text').extract_first()
        # #     phone['discountRate'] = None
        # #     phone['discountPrice'] = None
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
        # divImage = response.css(".item-border >img::attr(data-src)").extract_first()
        # phone['url'] = response.request.url
        #
        # phone['imageUrl'] = divImage

        yield phone