import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        # Loop through every quote on the page
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:  # If next button exists
            yield response.follow(next_page, callback=self.parse)