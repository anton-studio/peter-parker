import scrapy
import re

class QuotesSpider(scrapy.Spider):
    name = "ebay"

    def start_requests(self):
        site = self.site
        keyword = self.keyword
        category_entry = self.category_entry
        computed_entry = f'{site}/sch/i.html?_nkw={keyword}&_pgn=1'
        if category_entry != '':
            computed_entry = f'{category_entry}?_pgn=1'
        urls = [
            computed_entry,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("pgn=")[1]
        print('handling search result page ', page)

        next_page_url = response.css("nav > a.pagination__next::attr(href)").extract_first()
        if self.category_entry != '':
            next_page_url = response.css(".ebayui-pagination__control:last-child::attr(href)").extract_first()
        if (next_page_url is not None) and (next_page_url is not '#'):
            yield scrapy.Request(response.urljoin(next_page_url))

        products = response.css("#srp-river-results > ul > li > div > div.s-item__info.clearfix > a::attr(href)")
        if self.category_entry != '':
            products = response.css(".srp-results > li > div > div.s-item__info.clearfix > a::attr(href)")
        for product in products:
            productLink = product.get()
            if (productLink is not None):
                yield scrapy.Request(url=productLink, callback=self.parseProduct)


    def parseProduct(self, response):
        # print('parsing product ', response.url)
        autherLink = response.css("#RightSummaryPanel .mbg > a::attr(href)").extract_first()
        if autherLink == None:
            autherLink = response.css(".seller-details a:nth-child(1)::attr(href)").extract_first()
        if autherLink == None:
            link_search = re.search('https?:\/\/.{1,20}\.ebay\..{1,5}\/usr\/[a-z0-9?_=\.]+', response.text, re.IGNORECASE)
            if link_search:
                autherLink = link_search.group()
        if autherLink == None:
            print("can't parse seller info : ", response.url)
        else:
            yield scrapy.Request(url=autherLink, callback=self.parseSeller)


    def parseSeller(self, response):
        print('parsing author ', response.url)
        if len(response.css('#businessinfooverlay')) is not 0:
            print('#########')
            print(' ### found one seller with email ###')
            print('#########')
            yield {
                'business': response.css('#business_name + span::text').extract_first(),
                'first_name': response.css('#first_name + span::text').extract_first(),
                'last-name': response.css('#last_name + span::text').extract_first(),
                'address': '##'.join(response.css('#address + span *::text').extract()),
                'phone': response.css('#phone_number + span::text').extract_first(),
                'email': response.css('#email + span::text').extract_first(),
                'keyword': self.keyword,
                'site': self.site,
                'category_entry': self.category_entry,
                'seller_url': response.url
            }
