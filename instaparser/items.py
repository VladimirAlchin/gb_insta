# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    is_private = scrapy.Field()
    is_verified = scrapy.Field()
    followed_by_viewer = scrapy.Field()
    follows_viewer = scrapy.Field()
    requested_by_viewer = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    # "username": "r7308093",
    # "full_name": "IGOR777",
    # "profile_pic_url":
    # "is_private": false,
    # "is_verified": false,
    # "followed_by_viewer": false,
    # "follows_viewer": false,
    # "requested_by_viewer": false
