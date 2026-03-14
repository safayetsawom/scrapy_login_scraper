import scrapy

class LoginQuotesSpider(scrapy.Spider):
    name = "login_quotes"
    start_urls = ["https://quotes.toscrape.com/login"]  # Step 1: Visit login page first

    def parse(self, response):
        # Step 2: Scrapy reads the form and auto-grabs the csrf_token
        # Then submits username + password along with it
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "username": "user",
                "password": "password"
            },
            callback=self.after_login  # Step 3: After submitting, go to after_login
        )

    def after_login(self, response):
        # After redirect, we're already on the homepage!
        if "Logout" in response.text:
            self.log("✅ Login successful!")
            # Scrape THIS response directly — no new request needed
            yield from self.scrape_quotes(response)
        else:
            self.log("❌ Login FAILED. Check credentials.")

    def scrape_quotes(self, response):
        # Step 6: Scrape exactly like before
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("a.tag::text").getall(),  # Bonus: tags only visible when logged in
            }

        # Step 7: Follow pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.scrape_quotes)
