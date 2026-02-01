# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from ..items import JingdongItem
import time
from bs4 import BeautifulSoup

class JdSpider(scrapy.Spider):
    name = 'JD'
    allowed_domains = ['jingdong.com']
    start_urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&page=1&s=1&click=0']
    num = 1
    s = 1
    def parse(self, response):
        keyword = input('请输入关键词')
        bot = int(input('请输入页面起始'))
        top = int(input('请输入页面终止'))
        headers1 = {'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'}
        for i in range(bot,top):
            url = 'http://search.jd.com/Search?keyword='+ keyword + '&page=' + str(i) + '&s=1&click=0'

            page = requests.get(url, headers=headers1, timeout=10)

            soup = BeautifulSoup(page.content, 'html.parser')
            #print(soup)
            time.sleep(0.5)
            #ul_list = response.xpath("//ul[@class='gl-warp clearfix']/li")
            items = soup.find_all(class_='gl-item')
            for item111 in items:
                item = ()
                item1_name = item111.find(class_='p-name').text.strip()
                item1_price = item111.find(class_='p-price').text.strip()
                item1_link = 'http:' + item111.find(class_='p-img').find('a').get('href')
                items1_piclink = 'http:' + item111.find(class_='p-img').find('img').get('data-lazy-img')
                items1_piclink1 = re.sub("n7*", "n0", items1_piclink)

                item = JingdongItem(img_url=items1_piclink1, title=item1_name, price=item1_price,shoplink=item1_link)
                yield item
            self.s += 50
            self.num += 2
            next_url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&wq=%E6%89%8B%E6%9C%BA&page=" + str(self.num) + "&s=" + str(self.s) + "&click=0"

