import scrapy


class ScrapeNetKeibaItem(scrapy.Item):
    race_title = scrapy.Field()
    uma_id = scrapy.Field()
    waku_number = scrapy.Field()
    uma_number = scrapy.Field()
    uma_name = scrapy.Field()
    uma_nenrei = scrapy.Field()
    kinryo = scrapy.Field()
    jocky = scrapy.Field()
    area = scrapy.Field()
    trainer = scrapy.Field()
    # father = scrapy.Field()
    # father_father = scrapy.Field()
    # mother = scrapy.Field()
    # mother_father = scrapy.Field()
