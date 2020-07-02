from http.cookies import SimpleCookie

import pymysql
import scrapy
from maoyan.items import MaoyanItem
from maoyan.settings import DB_SETTINGS
from scrapy.selector import Selector


class Top10Spider(scrapy.Spider):
    name = "top10"
    allowed_domains = ["maoyan.com"]
    start_urls = ["https://maoyan.com/films?showType=3"]

    def __init__(self):
        self.connection = pymysql.connect(**DB_SETTINGS)
        self.cursor = self.connection.cursor()

    def insert(self, query, params):
        try:
            self.cursor.execute(query, params)
            self.logger.info(self.cursor.fetchone())
            self.connection.commit()
        except Exception as e:
            self.logger.info(e)
            self.connection.rollback()

    def __del__(self):
        self.connection.close()

    def request(self, url, callback):
        cookie_text = 'uuid_n_v=v1; uuid=9EB2A080B96A11EA9F28E30FF5FFF73CB5154A84C7A94D1DAB10BB8C2D31FEB8; _csrf=448d5750ef63e51bf723695e9008d2c176352dad7c0fc460f422f517baa014ba; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593367820; _lxsdk_cuid=172fc1f7724c8-098b7ae06bfb5b-39647b09-1fa400-172fc1f7724c8; _lxsdk=9EB2A080B96A11EA9F28E30FF5FFF73CB5154A84C7A94D1DAB10BB8C2D31FEB8; mojo-uuid=005c478c1b1c76a729dcde705c8ea14b; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593500815; __mta=147693064.1593367823108.1593500797746.1593500814850.16; _lxsdk_s=173065bd698-1d5-a44-de2%7C%7C1'
        cookie = SimpleCookie(cookie_text)
        cookie_dict = {cookie.key: cookie.value for cookie in cookie.values()}
        request = scrapy.Request(url=url, callback=callback)
        request.cookies = cookie_dict
        return request

    def start_requests(self):
        yield self.request(self.start_urls[0], self.parse)

    def parse(self, response):
        movie_infos = Selector(response=response).xpath(
            '//div[@class="movie-hover-info"]'
        )
        print(movie_infos)
        for movie_info in movie_infos[:10]:
            movie_item = MaoyanItem()
            if "title" not in movie_item:
                movie_item["title"] = movie_info.xpath(
                    './div[@class="movie-hover-title"]/@title'
                ).extract_first()
            movie_item["category"] = (
                movie_info.xpath(
                    './div[contains(@class, "movie-hover-title") and contains(.//span, "类型:")]/text()'
                )
                .extract()[-1]
                .strip()
            )
            movie_item["release"] = (
                movie_info.xpath(
                    './div[contains(@class, "movie-hover-title") and contains(.//span, "上映时间:")]/text()'
                )
                .extract()[-1]
                .strip()
            )
            yield movie_item
