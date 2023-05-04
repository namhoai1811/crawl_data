# from pymysql import NULL
import scrapy
import math
from ..items import TgddLaptopItem
# from scrapy_splash import SplashRequest

class PhoneSpider(scrapy.Spider):
    name = 'laptop88'
    i = 1
    # allowed_domains = ['www.thegioididong.com/dtdd']
    # start_urls = ['http://www.thegioididong.com/dtdd#c=42&o=9&pi=1/']
    base_url = "https://laptop88.vn/may-tinh-xach-tay.html?page="

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
            "https://laptop88.vn/may-tinh-xach-tay.html?page=1"
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


    def parse(self, response):
        # listItem = response.css('.p-item > a::attr(href)').extract()
        listItem = response.css('.product-item')
        for item in listItem:
            laptop = TgddLaptopItem()
            laptop['category'] = 'Laptop'
            laptop['name'] = item.css('div.product-info > div.product-title >a::text').extract_first()
            laptop['originPrice'] = item.css('div.product-info > div.product-price > div > del.old-price::text').extract_first()

            laptop['discountPrice'] = item.css('div.product-info > div.product-price > div > span.item-price::text').extract_first()
            if(str(laptop['discountPrice'])=='Liên Hệ'):
                laptop['discountPrice'] = item.css('div.product-info > div.product-price > div > del.old-price::text').extract_first()
            laptop['discountRate'] = item.css('div.product-info > div.product-price > div > p.price-saleoff::text').extract_first()
            laptop['cpu'] = item.css('div.product-info > div.product-promotion > table > tbody > tr:nth-child(1) > td:nth-child(2)::text').extract_first()
            laptop['ram'] = item.css('div.product-info > div.product-promotion > table > tbody > tr:nth-child(2) > td:nth-child(2)::text').extract_first()
            laptop['memory'] = item.css('div.product-info > div.product-promotion > table > tbody > tr:nth-child(3) > td:nth-child(2)::text').extract_first()
            laptop['card'] = item.css('div.product-info > div.product-promotion > table > tbody > tr:nth-child(4) > td:nth-child(2)::text').extract_first()
            laptop['screen'] = item.css('div.product-info > div.product-promotion > table > tbody > tr:nth-child(5) > td:nth-child(2)::text').extract_first()
            laptop['imageUrl'] = 'https://laptop88.vn' +str(item.css('div.product-img > a > img::attr(src)').extract_first())
            laptop['url'] = 'https://laptop88.vn' +str(item.css('div.product-img > a::attr(href)').extract_first())
            if((laptop['discountPrice']==None) & (laptop['discountPrice'] == None)):
                laptop['originPrice'] = item.css(
                    'div.product-info > div.product-price > div > del.jjgjhhkold-price::text').extract_first()
            else: yield laptop


        if self.i < 23:
            self.i += 1
            path_next = self.base_url +str(self.i)
            yield response.follow(path_next, callback=self.parse)
    #
    # def parse_info_phone(self, response):
    #     phone = TgddPhoneItem()
    #     phone['category'] = response.css('#breadcrumb > ol > li:nth-child(2) > a > span::text').extract_first()
    #     # phone['category'] = str(phone['category']).replace(' ','')
    #     # phone['company'] = response.css('body > section.detail > ul > li:nth-child(2) > a ::text').extract_first()
    #     # phone['company'] = phone['company'][11:len(phone['company'])]
    #     # phone['color'] = response.css(
    #     #     'body > section.detail > div.box_main > div.box_right > div > div.color > a.box03__item ::text').extract()
    #     phone['name'] = response.css('#overview-left > h1::text').extract_first()
    #     # phone['name'] = phone['name'][11:len(phone['name'])]
    #
    #     phone['originPrice'] = response.css('#overview-left > table > tbody > tr > td:nth-child(2) > span.pro-oldprice::text').extract_first()
    #     phone['originPrice'] = str(phone['originPrice']).replace(' VNĐ', '₫')
    #     phone['discountPrice'] = response.css('#overview-left > table > tbody > tr:nth-child(2) > td:nth-child(2) > span.pro-price::text').extract_first()
    #     phone['discountPrice'] = str(phone['discountPrice']).replace(' VNĐ', '₫')
    #
    #     # phone['url'] = response.request.url
    #     phone['url'] = response.css('.product-item > div.product-img >a::attr(href)').extract()
    #     # divImage = response.css("body > div.product-detail-container > div.product_details > div > div > div.img_product_detail > div.list_img_product_smaill > div.item_img.js-product-img-item.active > a > img::attr(data-src)").extract_first()
    #     divImage = response.css('.img_product_big >a::attr(href)').extract_first()
    #     phone['imageUrl'] = divImage
    #
    #     yield phone