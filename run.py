from core.spider import Spider
from multiprocessing import Process
from engin.engin import run as crawl
from engin.inspect import run as inspect

charts = ['a', 'b', 'c', 'd', 'e',
          'f', 'g', 'h', 'i', 'j',
          'k', 'l', 'm', 'n', 'o',
          'p', 'q', 'r', 's', 't',
          'u', 'v', 'w', 'x', 'y',
          'z', '1', '2', '3', '4',
          '5', '6', '7', '8', '9']

def get_url(chart):
    spider = Spider(1, chart)
    spider.run()

def run():
    p_list = []
    for chart in charts:
        p = Process(target=get_url, args=(chart, ))
        p.daemon = True
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()


if __name__ == '__main__':
    inspect(2)