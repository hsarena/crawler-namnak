# -*- coding: utf-8 -*-
import scrapy
import os
import requests
from namnak.items import NamnakItem
from newspaper import Article, Config
from bs4 import BeautifulSoup
from scrapy import Selector


class SportSpider(scrapy.Spider):
    name = 'life-style-article'
    allowed_domains = ['namnak.com']

    groups = ['c21-روابط-عاطفی', 'c107-روانشناسی', 'c23-موفقیت',
              'c60-خانه-داری', 'c29-کودک', 'c108-بارداری-و-نوزاد',
              'c12-کار-و-زندگی', 'c116-گردشگری']

    start_urls = ['http://namnak.com/{0}'.format(group) for group in groups]

    custom_settings = {
        'DEPTH_LIMIT': '1',
    }

    def grp (self, argument):
        switcher = {
            'http://namnak.com/c21-%D8%B1%D9%88%D8%A7%D8%A8%D8%B7-%D8%B9%D8%A7%D8%B7%D9%81%DB%8C': 'روابط عاطفی',
            'http://namnak.com/c107-%D8%B1%D9%88%D8%A7%D9%86%D8%B4%D9%86%D8%A7%D8%B3%DB%8C': 'روانشناسی',
            'http://namnak.com/c23-%D9%85%D9%88%D9%81%D9%82%DB%8C%D8%AA': 'موفقیت',
            'http://namnak.com/c60-%D8%AE%D8%A7%D9%86%D9%87-%D8%AF%D8%A7%D8%B1%DB%8C': 'خانه داری',
            'http://namnak.com/c29-%DA%A9%D9%88%D8%AF%DA%A9': 'کودک',
            'http://namnak.com/c108-%D8%A8%D8%A7%D8%B1%D8%AF%D8%A7%D8%B1%DB%8C-%D9%88-%D9%86%D9%88%D8%B2%D8%A7%D8%AF': 'بارداری و نوزاد',
            'http://namnak.com/c12-%DA%A9%D8%A7%D8%B1-%D9%88-%D8%B2%D9%86%D8%AF%DA%AF%DB%8C': 'کار و زندگی',
            'http://namnak.com/c116-%DA%AF%D8%B1%D8%AF%D8%B4%DA%AF%D8%B1%DB%8C': 'گردشگری'
        }
        return switcher.get(argument,"Invalid Group")

    def download_image(self, url, path):

        request = requests.get(url)
        with open(path, 'wb') as file:
            file.write(request.content)

    def parse(self, response):
        print(response.request.url)

        items = []
        path = "/tmp/namnak/life-style/"
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        group = self.grp(response.request.url)
        articles = response.xpath('//*[@id="maintbl"]/div/div/article')
        for article in articles:
            item = NamnakItem()
            item['category'] = 'سبک زندگی'
            item['group'] = group
            item['thumbnail'] = article.xpath('div/span/img/@src').get()
            item['link'] = 'http://namnak.com' + article.xpath('div/header/h2/a/@href').get()
            item['summary'] = article.xpath('div/text()').get()
            url = item['link']
            post = Article(url)
            post.download()
            item['source'] = Selector(text=post.html).xpath('//*[@id="maintbl"]/div/div/div[1]').get()
            key = "images"
            item.setdefault(key, [])
            soup = BeautifulSoup(post.html, features="lxml")
            art = soup.find('article')
            item['html'] = art
            for img in art.findAll('img'):
                jpg_name = img['src'].split('/')[-1]
                src_str = 'http://localhost/{}'.format(jpg_name)
                item['images'].append(src_str)
                tmp = src_str + ' height= ' + img['height'] + ' width= ' + img['width']
                img.insert_after(tmp)
            for header in art.findAll('h3'):
                for h in header.stripped_strings:
                    tmp = ' -- Header: ' + header.text
                header.insert_after(tmp)
            html_str = str(soup)
            post.download(input_html=html_str)
            post.parse()
            item['title'] = post.title
            item['movies'] = post.movies
            item['text'] = post.text
            items.append(item)
        print(items)
        return items
        #     print('Beginning file download ...')
        #     for i in item['images']:
        #         jpg_name = i.split('/')[-1]
        #         self.download_image(i, '{}/{}'.format(path, jpg_name))
        #
        #
        # print(items)
        # return items
