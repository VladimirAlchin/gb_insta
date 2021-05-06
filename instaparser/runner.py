from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instaparser.spiders.instagram import InstagramSpider
from instaparser import settings
import time

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    answer = []
    hash_list = [0, 1]
    i = 1
    # vladimiralchin valentinchenchik
    while i == 1:
        ans = input('Введите имя пользователя для сбора данных и нажмите ввод. Для прекращения, введите 0: ')
        if len(ans) > 1:
            answer.append(ans)
        else:
            i = 0
    for i in answer:
        for j in hash_list:
            process.crawl(InstagramSpider, i, j)

    process.start()