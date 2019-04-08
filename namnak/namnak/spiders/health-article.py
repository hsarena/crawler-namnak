# -*- coding: utf-8 -*-
import scrapy
import os
import requests
from namnak.items import NamnakItem
from newspaper import Article, Config
from bs4 import BeautifulSoup
from scrapy import Selector


class SportSpider(scrapy.Spider):
    name = 'health-article'
    allowed_domains = ['namnak.com']

    groups = ['c49-تازه-های-سلامت', 'c16-دهان-و-دندان', 'c20-پوست-و-مو',
              'c17-تغذیه', 'c45-پیشگیری-و-بیماریها', 'c46-سلامت-جنسی',
              'c52-متخصصین', 'c47-سلامت-روان', 'c50-سلامت-خانواده']

    start_urls = ['http://namnak.com/{0}'.format(group) for group in groups]

    custom_settings = {
        'DEPTH_LIMIT': '1',
    }

    def grp (self, argument):
        switcher = {
            'http://namnak.com/c49-%D8%AA%D8%A7%D8%B2%D9%87-%D9%87%D8%A7%DB%8C-%D8%B3%D9%84%D8%A7%D9%85%D8%AA': 'تازه های سلامت',
            'http://namnak.com/c16-%D8%AF%D9%87%D8%A7%D9%86-%D9%88-%D8%AF%D9%86%D8%AF%D8%A7%D9%86': 'دهان و دندان',
            'http://namnak.com/c20-%D9%BE%D9%88%D8%B3%D8%AA-%D9%88-%D9%85%D9%88': 'پوست و مو',
            'http://namnak.com/c17-%D8%AA%D8%BA%D8%B0%DB%8C%D9%87': 'تغذیه',
            'http://namnak.com/c45-%D9%BE%DB%8C%D8%B4%DA%AF%DB%8C%D8%B1%DB%8C-%D9%88-%D8%A8%DB%8C%D9%85%D8%A7%D8%B1%DB%8C%D9%87%D8%A7': 'پیشگیری و بیماریها',
            'http://namnak.com/c46-%D8%B3%D9%84%D8%A7%D9%85%D8%AA-%D8%AC%D9%86%D8%B3%DB%8C': 'سلامت جنسی',
            'http://namnak.com/c52-%D9%85%D8%AA%D8%AE%D8%B5%D8%B5%DB%8C%D9%86': 'متخصصین',
            'http://namnak.com/c47-%D8%B3%D9%84%D8%A7%D9%85%D8%AA-%D8%B1%D9%88%D8%A7%D9%86': 'سلامت روان',
            'http://namnak.com/c50-%D8%B3%D9%84%D8%A7%D9%85%D8%AA-%D8%AE%D8%A7%D9%86%D9%88%D8%A7%D8%AF%D9%87': 'سلامت خانواده'
        }
        return switcher.get(argument,"Invalid Group")

    def download_image(self, url, path):

        request = requests.get(url)
        with open(path, 'wb') as file:
            file.write(request.content)

    def parse(self, response):
        print(response.request.url)

        items = []
        path = "/tmp/namnak/health/"
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
            item['category'] = 'بهداشت و سلامت'
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
                pg_name = img['src'].split('/')[-1]
                src_str = 'http://localhost/{}'.format(jpg_name)
                item['images'].append(src_str)
                tmp = src_str + ' height= ' + img['height'] + ' width= ' + img['width']
                img.insert_after(tmp)
            for header in art.findAll('h3'):
                for h in header.stripped_strings:
                    tmp = ' -- Header: ' + header.text
                header.insert_after(tmp)
            html_str = str(soup)
            # print(html_str)
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
        # print(items[1].text)
        # return items
