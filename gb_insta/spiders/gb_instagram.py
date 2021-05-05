import re
import scrapy
from scrapy.http import HtmlResponse


class GbInstagramSpider(scrapy.Spider):
    name = 'gb_instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    enc_password = '#PWD_INSTAGRAM_BROWSER:10:1620237030:AdNQABjhpEtT3uUVpIJF7onWxAjq9VDyWiCYTOcd7Vtduwl67XDMwRYij0ITPdmIuP1hUuvg4TXE75xpgPBt7VhBio8b+6bvu6KJnkEnOJYmVLbaOh/4s5KPDM5X25FE0HgD/WQi63YpmuN4m7sceYE='
    user_name = 'learn.vsgb'
    user_to_parse_url = 'https://www.instagram.com/vladimiralchin/'

    def parse(self, response: HtmlResponse):
        csrf_token = self.get_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.user_login,
            formdata={
                "username": self.user_name,
                "enc_password": self.enc_password
            },
            headers={'x-csrftoken': csrf_token}
        )

    def user_login(self, response: HtmlResponse):
        print("111")

        data = response.json()

        if data['authenticated']:
            yield response.follow(
                self.user_to_parse_url,
                callback=self.user_data_parse
            )

    def user_data_parse(self, response: HtmlResponse):


        pass

    # получение csrf токена
    def get_csrf_token(self, text):
        matched = re.search('\"csrf_token\":"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')
