from scrapy.item import Item, Field

class NamnakItem(Item):
    category = Field()
    group = Field()
    title = Field()
    link = Field()
    summary = Field()
    thumbnail = Field()
    text = Field()
    source = Field()
    images = Field()
    movies = Field()
    html = Field()