# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MaoyanPipeline:
    def process_item(self, item, spider):
        movie_info = "{}\t{}\t{}\n".format(
            item["title"], item["category"], item["release"]
        )
        with open("./movies.txt", "a+", encoding="utf-8") as movie:
            movie.write(movie_info)
        return item
