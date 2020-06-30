# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MaoyanPipeline:
    def process_item(self, item, spider):
        query = """INSERT INTO top10 (title, category, release_time) VALUES (%s, %s, %s)"""
        params = (item["title"], item["category"], item["release"])
        spider.insert(query, params)
        return item
