from cli.cli import get_data, change_ips
from db.db import  db_en_cache, db_en_olbase
from lxml import etree
import re
from threading import Thread
import pickle
import os
from cli.log import get_log

log = get_log('link_list')


def process(queue):
    pass

def run(size):
    url_pool = []
    db = db_en_cache.find()
    count = 0
    while True:
        try:
            if len(url_pool) < size:
                url = db.next()['url']
                count += 1
                # if url not in self.url_pool:
                res = db_en_olbase.find_one({'url': url})
                if not res:
                    url_pool.append(url)
            else:
                process(url_pool)
        except StopIteration:
            log.error("can not find data in db_en_olbase_url")
        except Exception as e:
            log.exception(e)
            db = db_en_cache.find()[count:]

def fix_url(url):
    return "http:"+url

class Spider:

    def __init__(self, size, chart):
        # self.queue = Queue(size)
        self.size = size
        self.chart = chart
        self.isRun = False
        self.log = get_log(chart)


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
                # db_en_olbase_url.insert({'url': fix_url(href)})
            except Exception as e:
                print(e, fix_url(href))
        next = eles.xpath('//div[@class="pagination pagination-centered"]/ul/li/a/@href')[-1]
        flag = re.match('.*html', next)
        print(fix_url(next))
        self.log.info(fix_url(next))
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
            self.log.error(self.url)
            # self.log.exception(e)
            change_ips()
            return True

    def run(self):
        # self.isRun = True
        if os.path.exists('cache/log_%s.plk'%self.chart):
            with open('cache/log_%s.plk'%self.chart, 'rb') as f:
                data = f.read()
                data = pickle.loads(data)
                self.chart = data['chart']
                self.content = data['content']
                self.url = data['url']
            flag = self.query_url_data(self.url)
            while flag:
                flag = self.query_url_data(self.url)
        # self.get_chart_page(self.chart.upper())
            # for chart in charts[charts.index(self.chart) + 1:]:
            #     self.chart = chart
            #     self.get_chart_page(chart.upper())
            # self.start()
            # return
        # for chart in charts[charts.index(self.chart):]:
        #     self.chart = chart
        #     self.get_chart_page(chart.upper())


    def local(self, vals):
        """
        本地化
        :param vals:
        :return:
        """
        with open('data.csv', 'a+') as f:
            for val in vals:
                f.write(val+',')
            f.write('\n')

    def engin(self):
        self.url_pool = []
        self.db = db_en_cache.find()
        count = 0
        while self.isRun:
            try:
                if len(self.url_pool) < self.size:
                    url = self.db.next()['url']
                    count += 1
                    # if url not in self.url_pool:
                    res = db_en_olbase.find_one({'url': url})
                    if not res:
                        self.url_pool.append(url)
                else:
                    process(self.url_pool)
            except StopIteration:
                log.error("can not find data in db_en_olbase_url")
            except Exception as e:
                log.exception(e)
                self.db = db_en_cache.find()[count:]


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
        with open('cache/log_%s.plk'%self.chart, "wb") as f:
            f.write(data)
        # self.isRun = False

# =====================================================================

if __name__ == '__main__':
    run(10)