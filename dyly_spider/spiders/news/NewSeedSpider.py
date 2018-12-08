# -*- coding: utf-8 -*-

from scrapy import Request

from dyly_spider.spiders.news.NewsSpider import NewsSpider
from util import RegExUtil


class NewSeedSpider(NewsSpider):
    """
    新芽
    """

    # custom_settings = {
    #     "AUTOTHROTTLE_ENABLED": True,
    #     "DOWNLOAD_DELAY": 1
    # }

    name = "newseed_news"

    list_url = "https://news.newseed.cn/p{page}"

    def __init__(self, *a, **kw):
        super(NewSeedSpider, self).__init__(*a, **kw)

    def start_requests(self):
        yield Request(
            self.list_url.format(page=1),
            dont_filter=True
        )

    def parse(self, response):
        items = response.xpath('//*[@id="news-list"]/ul/li')
        next_page = response.xpath('//*[@id="page-news"]/div/div[2]/div/div[2]/div/a[@class="next"][last()]/@href').extract_first()
        if next_page is not None:
            yield Request(
                next_page,
                dont_filter=True
            )
        for item in items:
            yield Request(
                item.xpath("h3/a/@href").extract_first(),
                dont_filter=True,
                priority=1,
                callback=self.detail
            )

    def detail(self, response):
        self.insert_new(
            RegExUtil.find_first("/(\d+)", response.url),
            response.xpath('normalize-space(/html/body/div[2]/div/div[2]/div/span[@class="date"]/text())').extract_first(),
            response.xpath('normalize-space(//*[@id="title"]/text())').extract_first(),
            response.xpath('normalize-space(/html/body/div[2]/div/div[2]/div/span[@class="dot"]/a/text())').extract_first(),
            response.xpath('normalize-space(/html/body/div[2]/div/div[2]/div/span[@class="resfrom"]/text())').extract_first(),
            None,
            response.xpath('//*[@id="news-content"]'),
            response.url,
            36
        )