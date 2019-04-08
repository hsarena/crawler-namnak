# -*- coding: utf-8 -*-
import scrapy
import os
import requests
from namnak.items import NamnakItem
from newspaper import Article, Config
from bs4 import BeautifulSoup


class SportSpider(scrapy.Spider):
    name = 'sport-article'
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

    def download_image(self, url, path):

        request = requests.get(url)
        with open(path, 'wb') as file:
            file.write(request.content)

    def parse(self, response):
        print(response.request.url)

        items = []
        path = "/tmp/namnak/sport/"
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
            item['category'] = 'ورزش و تناسب اندام'
            item['group'] = group
            item['title'] = article.xpath('div/header/h2/a/text()').get()
            item['link'] = 'http://namnak.com' + article.xpath('div/header/h2/a/@href').get()
            item['summary'] = article.xpath('div/text()').get()
            url = item['link']
            post = Article(url)
            post.download()
            key = "images"
            item.setdefault(key, [])
            soup = BeautifulSoup(post.html, features="lxml")
            art = soup.find('article')
            for img in art.findAll('img'):
                jpg_name = img['src'].split('/')[-1]
                tmp = 'http://localhost/' + jpg_name + ' ' + 'height=' + img['height'] + ' width=' + img['width']
                img.insert_after(tmp)


                #print(tmp)
            html_str = str(soup)
            post.download(input_html=html_str)
            post.parse()
            item['title'] = post.title
            item['movies'] = post.movies
            item['text'] = post.text
            items.append(item)

            print('Beginning file download ...')
            for i in item['images']:
                jpg_name = i.split('/')[-1]
                self.download_image(i, '{}/{}'.format(path, jpg_name))


        print(items[1].text)
        return items
            #print('Beginning file download ...')
            #for i in item['images']:
            #    jpg_name = i.split('/')[-1]
            #    self.download_image(i, '{}/{}'.format(path, jpg_name))



