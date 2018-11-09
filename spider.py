from cli import get_data, change_ips, db_en_cache, db_en_olbase, logger
from queue import Queue
from lxml import etree
import re
from threading import Thread
from parse import parses, filter_ele
import pickle
import os
import time


charts = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def fix_url(url):
    return "http:"+url

class Spider:

    def __init__(self, size):
        self.queue = Queue(size)
        self.chart = 'a'
        self.isRun = False


    def parse_index_page(self, content):
        """
        解析每页的url
        :param content:
        :return:
        """
        self.content = content
        eles = etree.HTML(content)
        # hrefs = eles.xpath('//table[@class="caslist_box"]/tbody/tr/td/a/@href')
        hrefs = eles.xpath('//table[@class="caslist_box"]/tr/td/a/@href')
        for href in hrefs:
            # if db_en_cache.find_one({'url': href}):
            #     continue
            # self.queue.put(fix_url(href), True)
            try:
                db_en_cache.insert({'url': fix_url(href)})
            except Exception as e:
                print(e, fix_url(href))
        next = eles.xpath('//div[@class="pagination pagination-centered"]/ul/li/a/@href')[-1]
        flag = re.match('.*html', next)
        print(fix_url(next))
        logger.info(fix_url(next))
        if flag:
            # resp = get_data(fix_url(next))
            # self.parse_index_page(resp.content.decode())
            return fix_url(next)

    def get_chart_page(self, chart):
        url = 'http://www.molbase.com/en/chemical-products_%s.html'%chart.upper()
        flag = self.query_url_data(url)
        while flag:
            flag = self.query_url_data(self.url)

    def query_url_data(self, url):
        """
        获取每页的数据
        :param url:
        :return:
        """
        if not url:
            return
        # resp = get_data(url)
        # url = self.parse_index_page(resp.content.decode())
        # while url:
        #     self.url = url
        #     self.down()
        #     resp = get_data(url)
        #     url = self.parse_index_page(resp.content.decode())
        try:
            resp = get_data(url)
            url = self.parse_index_page(resp.content.decode())
            while url:
                self.url = url
                self.down()
                # time.sleep(1)
                resp = get_data(url)
                url = self.parse_index_page(resp.content.decode())
        except Exception as e:
            print(e)
            # print('*',self.url)
            logger.error(self.url)
            logger.exception(e)
            change_ips()
            return True

    def run(self):
        # self.isRun = True
        if os.path.exists('log'):
            with open('log', 'rb') as f:
                data = f.read()
                data = pickle.loads(data)
                self.chart = data['chart']
                self.content = data['content']
                self.url = data['url']
            flag = self.query_url_data(self.url)
            while flag:
                flag = self.query_url_data(self.url)
            for chart in charts[charts.index(self.chart) + 1:]:
                self.chart = chart
                self.get_chart_page(chart.upper())
            self.start()
            return
        for chart in charts[charts.index(self.chart):]:
            self.chart = chart
            self.get_chart_page(chart.upper())

    def parse(self, url):
        content = get_data(url).content.decode()
        dt = {'url': url}
        for func in parses:
            res = func(content)
            if isinstance(res, dict):
                dt[func.__name__] = filter_ele(res)
            else:
                dt[func.__name__] = res
        self.pipline(dt)
        # try:
        #     for func in parses:
        #         res = func(content)
        #         if isinstance(res, dict):
        #             dt[func.__name__] = filter_ele(res)
        #         else:
        #             dt[func.__name__] = res
        #     self.pipline(dt)
        # except Exception as e:
        #     self.queue.put(url, True)

    def pipline(self, item):
        props = {}
        val_list = []
        for key, val in item.items():
            if isinstance(val, str):
                props[key] = val
                val_list.append(val)
            else:
                for k, v in val.items():
                    props[k] = v
                    val_list.append(v)
        print(props)
        db_en_olbase.insert(props)
        db_en_cache.remove({'url': item['url']})
        self.local(val_list)
        # for name, value in props.items():
        #     pass

    def local(self, vals):
        with open('data.csv', 'a+') as f:
            for val in vals:
                f.write(val+',')
            f.write('\n')

    def engin(self):
        while self.isRun:
            try:
                # url = self.queue.get(True, timeout=3)
                # t = Thread(target=self.parse, args=(url, ))
                # t.start()
                if db_en_cache.find().count():
                    url = db_en_cache.find().next()['url']
                    t = Thread(target=self.parse, args=(url,))
                    t.start()
            except:
                pass

    def stop(self):
        self.isRun = False

    def resume(self):
        pass

    def start(self):
        # if self.url:
            # self.repeat = True
            # self.query_url_data(self.url)
            # self.repeat = False
        self.isRun = True
        self.thread = Thread(target=self.engin)
        self.thread.start()


    def down(self):
        content = self.content if self.content else ""
        url = self.url if self.url else ""
        data = {'content': content, 'chart': self.chart, 'url': url}
        data = pickle.dumps(data)
        with open('log', "wb") as f:
            f.write(data)
        # self.isRun = False



if __name__ == '__main__':
    spider = Spider(5)
    spider.run()