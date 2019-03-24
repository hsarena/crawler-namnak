# -*- coding: utf-8 -*-
import scrapy
from namnak.items import NamnakItem

class SportSpider(scrapy.Spider):
    name = 'sport'
    allowed_domains = ['namnak.com']

    groups = ['c117-رژیم-و-تغذیه', 'c118-کنترل-وزن', 'c119-تمرینات-ورزشی',
              'c13-تناسب-اندام', 'c9-رشته-های-ورزشی', 'c104-بیوگرافی-ورزشکاران',
              'c38-ورزش-درمانی', 'c39-گوناگون']

    start_urls = ['http://namnak.com/{0}'.format(group) for group in groups]

    custom_settings = {
        'DEPTH_LIMIT': '1',
    }

    def grp (self, argument):
        switcher = {
            'http://namnak.com/c117-%D8%B1%DA%98%DB%8C%D9%85-%D9%88-%D8%AA%D8%BA%D8%B0%DB%8C%D9%87': 'رژیم و تغذیه',
            'http://namnak.com/c118-%DA%A9%D9%86%D8%AA%D8%B1%D9%84-%D9%88%D8%B2%D9%86': 'کنترل وزن',
            'http://namnak.com/c119-%D8%AA%D9%85%D8%B1%DB%8C%D9%86%D8%A7%D8%AA-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C': 'تمرینات ورزشی',
            'http://namnak.com/c13-%D8%AA%D9%86%D8%A7%D8%B3%D8%A8-%D8%A7%D9%86%D8%AF%D8%A7%D9%85': 'تناسب اندام',
            'http://namnak.com/c9-%D8%B1%D8%B4%D8%AA%D9%87-%D9%87%D8%A7%DB%8C-%D9%88%D8%B1%D8%B2%D8%B4%DB%8C': 'رشته های ورزشی',
            'http://namnak.com/c104-%D8%A8%DB%8C%D9%88%DA%AF%D8%B1%D8%A7%D9%81%DB%8C-%D9%88%D8%B1%D8%B2%D8%B4%DA%A9%D8%A7%D8%B1%D8%A7%D9%86': 'بیوگرافی ورزشکاران',
            'http://namnak.com/c38-%D9%88%D8%B1%D8%B2%D8%B4-%D8%AF%D8%B1%D9%85%D8%A7%D9%86%DB%8C': 'ورزش درمانی',
            'http://namnak.com/c39-%DA%AF%D9%88%D9%86%D8%A7%DA%AF%D9%88%D9%86': 'گوناگون'
        }
        return switcher.get(argument,"Invalid Group")


    def parse(self, response):
        print(response.request.url)

        items = []

        group = self.grp(response.request.url)
        articles = response.xpath('//*[@id="maintbl"]/div/div/article')
        for article in articles:
            item = NamnakItem()
            item['category'] = 'ورزش و تناسب اندام'
            item['group'] = group
            item['title'] = article.xpath('div/header/h2/a/text()').get()
            item['link'] = 'http://namnak.com' + article.xpath('div/header/h2/a/@href').get()
            item['summary'] = article.xpath('div/text()').get()
            items.append(item)
        print(items)
        return items