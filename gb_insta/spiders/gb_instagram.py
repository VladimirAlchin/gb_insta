import re
import scrapy
from scrapy.http import HtmlResponse
import json
from urllib.parse import quote


class GbInstagramSpider(scrapy.Spider):
    name = 'gb_instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    enc_password = '#PWD_INSTAGRAM_BROWSER:10:1620237030:AdNQABjhpEtT3uUVpIJF7onWxAjq9VDyWiCYTOcd7Vtduwl67XDMwRYij0ITPdmIuP1hUuvg4TXE75xpgPBt7VhBio8b+6bvu6KJnkEnOJYmVLbaOh/4s5KPDM5X25FE0HgD/WQi63YpmuN4m7sceYE='
    user_name = 'learn.vsgb'
    user_to_parse_url = 'https://www.instagram.com/%s/'
    user_to_parse_url_tmp = 'vladimiralchin'
    posts_hash = "32b14723a678bd4628d70c1f877b94c9"
    graphql_url = "https://www.instagram.com/graphql/query/?"

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
                self.user_to_parse_url % self.user_to_parse_url_tmp,
                callback=self.user_data_parse,
                cb_kwargs={'username': self.user_to_parse_url_tmp}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.get_user_id(response.text, username)
        variables = {
            'first': 12,
            'id': user_id,
        }
        new_code = self.encode_var(variables)


        pass
    # кодировка в строку
    def encode_var(self, variables):
        str_variables = quote(str(variables).replace(" ", "").replace("'", '"'))
        return str_variables


    # получение csrf токена
    def get_csrf_token(self, text):
        matched = re.search('\"csrf_token\":"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def get_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
