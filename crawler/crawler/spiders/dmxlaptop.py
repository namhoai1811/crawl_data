import scrapy
from ..items import TgddLaptopItem
from scrapy_splash import SplashRequest



# Spider này dùng để crawl những điện thoại
# mà có từ 2 option trở lên
# do dev không pass qua được cái điều kiện của scrapy
# là không được request cùng 1 trang web

class PhoneSpider(scrapy.Spider):
    name = 'dmx'
    i = 1
    base_url = "https://www.thegioididong.com/laptop#c=44&o=17&pi="

    render_script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(20))

            return {
                html = splash:html(),
                url = splash:url(),
            }
        ends
        """

    def start_requests(self):
        start_urls = [
            "https://www.dienmayxanh.com/laptop?key=laptop&sc=new#c=44&o=17&pi=10"
        ]
        for url in start_urls:
            # yield scrapy.Request(url=url, callback=self.parse)
            yield SplashRequest(
                url,
                self.parse,
                endpoint='render.html',
                args={
                    'wait': 20,
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
        phoneItem = response.css('div.container-productbox > ul > li > a.main-contain ::attr(href)').extract()
        print(phoneItem)
        for phone in phoneItem:
            yield scrapy.Request(response.urljoin(phone), callback=self.parse_info_phone, dont_filter=True)

        # if self.i < 5:
        #     self.i += 1
        #     path_next = self.base_url +str(self.i)
        #     yield response.follow(path_next, callback=self.parse)

    # Bat dau boc tach du lieu nhoe!
    def parse_info_phone(self, response):
        phone = TgddLaptopItem()
        phone['category'] = response.css('body > section.detail > ul > li:nth-child(1) > a ::text').extract_first()
        phone['company'] = response.css('body > section.detail > ul > li:nth-child(2) > a ::text').extract_first()
        phone['company'] = phone['company'][7:len(phone['company'])]
        phone['name'] = response.css('body > section.detail > h1 ::text').extract_first()
        # phone['name'] = phone['name'][11:len(phone['name'])]
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


        phone['ram'] = response.css('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(2) > div > span ::text').extract_first()
        phone['cpu'] = response.css('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(1) > div > span::text').extract_first()
        phone['memory'] = response.css('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(3) > div > span::text').extract_first()
        phone['screen'] = response.css('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(4) > div > span::text').extract_first()
        phone['card'] = response.css('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(5) > div > span::text').extract_first()
        phone['operatingSystem'] = response.css('body > section.detail > div.box_main > div.box_right > div.parameter > ul > li:nth-child(8) > div > span::text').extract_first()

        phone['rate'] = response.css(".point::text").extract_first()
        phone['point'] = response.css(".rating-total::text").extract_first()
        divImage = response.css(".item-border >img::attr(data-src)").extract_first()
        phone['url'] = response.request.url

        phone['imageUrl'] = divImage

        yield phone