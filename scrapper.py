import scrapy

class WikiSpider(scrapy.Spider):
    name = 'wikispider'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_law_enforcement_agencies_in_Kansas']

    def parse(self, response, depth=0):
        if depth >= 2:
            return

        for next_page in response.css('.multicol li > a , h2+ ul li > a'):
            yield {'from': response.css("#firstHeading::text").get(),
                   'to': next_page.attrib['title']}

            next_class = next_page.xpath("@class").extract()
            if not (next_class and 'new' in next_class):
                yield response.follow(next_page, self.parse, cb_kwargs={"depth": depth + 1})
