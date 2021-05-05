from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gb_insta import settings
from gb_insta.spiders.gb_instagram import GbInstagramSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(GbInstagramSpider)

    process.start()
