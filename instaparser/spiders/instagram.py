import scrapy
from scrapy.http import HtmlResponse
import re
import json
from pprint import pprint
# from urllib.parse import urlencode
from urllib.parse import quote
from copy import deepcopy
from instaparser.items import InstaparserItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    username = "learn.vsgb"
    enc_password = "#PWD_INSTAGRAM_BROWSER:10:1620237030:AdNQABjhpEtT3uUVpIJF7onW" \
                   "xAjq9VDyWiCYTOcd7Vtduwl67XDMwRYij0ITPdmIuP1hUuvg4TXE75xpgPBt7VhBio" \
                   "8b+6bvu6KJnkEnOJYmVLbaOh/4s5KPDM5X25FE0HgD/WQi63YpmuN4m7sceYE="
    user_to_parse_url_template = "/%s"
    user_to_parse = "vladimiralchin"
    posts_hash = "32b14723a678bd4628d70c1f877b94c9"
    subscribers_hash = '5aefa9893005572d237da5068082d8d5'
    graphql_url = "https://www.instagram.com/graphql/query/?"

    # авторизуемся на странице инсты
    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.user_login,
            formdata={
                "username": self.username,
                "enc_password": self.enc_password
            },
            headers={
                'x-csrftoken': csrf_token
            }
        )

    # проверяем прошла ли авторизация, если прошла идем получать все посты
    def user_login(self, response: HtmlResponse):
        data = response.json()
        if data['authenticated']:
            yield response.follow(
                self.user_to_parse_url_template % self.user_to_parse,
                # калбэк для парсинга постов
                # callback=self.user_data_parse,
                callback=self.get_user_subscribers,
                cb_kwargs={
                    "username": self.user_to_parse,
                }
            )

    def get_user_subscribers(self, response: HtmlResponse, username):
        # итог variables={"id":"3098502418","include_reel":true,"fetch_mutual":true,"first":24}
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'first': 24,
            'id': user_id
        }
        str_variables = self.make_str_variables(variables)
        url = f"{self.graphql_url}query_hash={self.subscribers_hash}&variables={str_variables}"

        yield response.follow(
            url,
            callback='',
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                'variables': deepcopy(variables),
            }

        )

    def get_user_subscr(self, response: HtmlResponse, username, user_id, variables):
        print()

        data = response.json()



    # прокручиваем страницу по 12 постов с конца до начала
    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {
            'first': 12,
            'id': user_id
        }
        str_variables = self.make_str_variables(variables)
        # print("$$$")
        url = f"{self.graphql_url}query_hash={self.posts_hash}&variables={str_variables}"
        yield response.follow(
            url,
            callback=self.user_post_parse,
            cb_kwargs={
                "username": username,
                "user_id": user_id,
                # на будущее: изучите в чем отличие глубокого копирования
                "variables": deepcopy(variables),
            }
        )

    def user_post_parse(self, response: HtmlResponse, username, user_id, variables):
        print()

        data = response.json()
        # наиболее предпочтительный вариант
        # try:
        info = data["data"]["user"]['edge_owner_to_timeline_media']
        posts = info['edges']
        # работа с постами
        for post in posts:
            item = InstaparserItem()
            item['user_id'] = user_id
            node = post['node']
            item['photo'] = node["display_url"]
            item['likes'] = node['edge_media_preview_like']['count']
            item['post_data'] = node
            yield item

        page_info = info['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            str_variables = self.make_str_variables(variables)
            url = f"{self.graphql_url}query_hash={self.posts_hash}&variables={str_variables}"
            yield response.follow(
                url,
                callback=self.user_post_parse,
                cb_kwargs={
                    "username": username,
                    "user_id": user_id,
                    # на будущее: изучите в чем отличие глубокого копирования
                    "variables": deepcopy(variables),
                }
            )

    # создаем из словаря строку
    def make_str_variables(self, variables):
        str_variables = quote(
            str(variables).replace(" ", "").replace("'", '"')
        )
        return str_variables

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
