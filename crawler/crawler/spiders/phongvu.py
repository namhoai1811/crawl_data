import scrapy
from scrapy.selector import Selector
from ..items import TgddPhoneItem
from scrapy_splash import SplashRequest
class PhongVuSpider(scrapy.Spider):
    i=1
    name = "pvlaptop"
    base_url="https://phongvu.vn/c/laptop?page="

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
        start_urls=[
            "https://phongvu.vn/c/laptop?page=1"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        products = response.css('.product-card')
        for product in products:
            link_detail = product.css('a::attr(href)').extract_first()
            yield response.follow(link_detail, self.parse_detail)

        if self.i < 13:
            self.i += 1
            path_next = self.base_url +str(self.i)
            # yield response.follow(path_next, callback=self.parse)
            yield SplashRequest(
                path_next,
                self.parse,
                endpoint='render.html',
                args={
                    'wait': 20,
                    'lua_source': self.render_script,
                }
            )

    def parse_detail(self, response):
        item = TgddPhoneItem()
        item['name'] = response.css('.css-4kh4rf ::text').extract_first()
        item['pin'] = response.css('#__next > div > div > div > div > div:nth-child(4) > div > div > div:nth-child(4) > div > div.teko-col.teko-col-4.css-gr7r8o > div.css-1h28ttq > div:nth-child(1) > div:nth-child(2)::text').extract_first()
        # item['producer'] = response.css('.css-6b3ezu > div > div > div > a > span ::text').extract_first()
        # item['price'] = response.css('.att-product-detail-latest-price ::text').extract_first()
        # item['price_sale'] = response.css('.att-product-detail-retail-price::text').extract_first()
        item['originPrice'] = response.css('.att-product-detail-latest-price ::text').extract_first()
        item['discountPrice'] = response.css('.att-product-detail-retail-price::text').extract_first()
        item['discountRate'] = response.css('#__next > div > div > div > div > div:nth-child(7) > div > div > div:nth-child(4) > div.css-1hwtax5 > div > div > div.css-6b3ezu > div.css-1q5zfcu > div.css-3mjppt > div.css-1p6etnp::text').extract_first()
        item['imageUrl'] = response.css('.productDetailPreview > div > img ::attr(src)').extract_first()
        item['category'] = response.css(".css-6b3ezu > div > div > div > a > span::text").extract_first()
        item['url'] = response.request.url


        yield item


