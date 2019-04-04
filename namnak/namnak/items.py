from scrapy.item import Item, Field

class NamnakItem(Item):
    category = Field()
    group = Field()
    title = Field()
    link = Field()
    summary = Field()
    text = Field()
    images = Field()