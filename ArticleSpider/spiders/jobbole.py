# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/112614/']

    def parse(self, response):
        title = response.xpath('//*[@id="post-112614"]/div[1]/h1')
        pass
