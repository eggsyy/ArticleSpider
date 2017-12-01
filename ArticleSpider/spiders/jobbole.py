# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import urlparse
import sys
import re
from ArticleSpider.items import JobboleArticleItem

reload(sys)
sys.setdefaultencoding('utf-8')


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后进行解析
        2. 获取下一页的url交给scrapy进行下载，下载完后交给parse
        """

        # 解析列表页中的所有文章url交给scrapy下载后进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=urlparse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        next_urls = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_urls:
            yield Request(url=urlparse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobboleArticleItem()


        # 提取文章的具体字段
        # title = response.xpath('//*[@id="post-113158"]/div[1]/h1/text()').extract_first("")
        # create_date = response.xpath('//*[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace("·", "").strip()
        # praise_nums = response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        # fav_nums = response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        # match_re = re.match(r".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        # match_re = re.match(r".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        # content = response.xpath('//div[@class="entry"]').extract()[0]
        # tag_list = response.xpath('//*[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith(u"评论")]
        # tags = ",".join(tag_list)


        # 通过css选择器提取
        front_image_url = response.meta.get("front_image_url", "")    # 文章封面图
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css("span.vote-post-up h10::text").extract()[0]
        fav_nums = response.css("span.bookmark-btn::text").extract()[0]
        match_re = re.match(r".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(r".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css("div.entry").extract()[0]
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith(u"评论")]
        tags = ",".join(tag_list)

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content

        yield article_item
