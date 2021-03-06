import requests
from cli.log import get_log
from cli.proxy import IpPool
import json
import datetime
from lxml import etree

logger = get_log('http')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    # 'cookie': "my_mbcookie=9381740248; gr_user_id=aadb4e55-834c-4b15-9629-0ad5b46be83f; grwng_uid=8afb463c-2554-482a-b175-584868f76b76; _ga=GA1.2.1853337866.1539237768; deny_ip=UWMHa1ViACtWYFBoVGAHLgBvAzJReAg0VmUGMw%3D%3D; g_step_tmp=1; _pk_ref.2.9731=%5B%22%22%2C%22%22%2C1541396804%2C%22http%3A%2F%2Fwww.molbase.com%2Fen%2F488-93-7-moldata-179475.html%22%5D; _pk_ses.2.9731=*; ad747e1972c640de_gr_session_id=7e1a2bb0-a122-4b3f-a364-e2ecd53690c0; _gid=GA1.2.1927091434.1541396804; ad747e1972c640de_gr_session_id_7e1a2bb0-a122-4b3f-a364-e2ecd53690c0=true; current_user_key=689615e92a91e9b63ff65108985e2782; count_views_key=113c494d84d1f9713d661963f783d079; ECM_ID=rf5ko34u1lcn6vn2vd67s0t061; ECM_ID=rf5ko34u1lcn6vn2vd67s0t061; Hm_lvt_16ee3e47bd5e54a79fa2659fe457ff1e=1539237692,1539323463,1541127887,1541396811; _pk_id.2.9731=b06a2f06be918374.1539237692.7.1541399717.1541396804.; Hm_lpvt_16ee3e47bd5e54a79fa2659fe457ff1e=1541399717; lighting=eyJpdiI6IjFJNnJQUTNuUjh0TzQ3WFZcL1ZlOG13PT0iLCJ2YWx1ZSI6IlhYK1UyVW50ekx6SzVnTWlScXkxbzUwTEJCOW1Eb1BtdEIxTXRaWnE1SzR6RTNrM1JJMXRcL0tpRCtKSmgxaHptNTB2VTdTTnl5OFZqOTZ6V05INDJSZz09IiwibWFjIjoiMTIxYTRhZWJiZjJlYjAyYzg1MmFjNzUzZmZiODg1OTJlOTE1NGI2YzZkMzYxNmY1MGRlMTU4NTg5Y2ViZmQwZiJ9",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Host': 'www.molbase.com',
    'Accept-Encoding': 'gzip, deflate'
    }

ips = '52.79.116.117:3128'


def get_proxy_ips():
    # global ips
    # if ips:
    #     resp = requests.get('http://10.9.60.13:5010/delete/?proxy=%s' % ips, headers)
    # resp = requests.get('http://10.9.60.13:5010/get', headers)
    while True:
        try:
            resp = requests.get('http://123.207.35.36:5010/get', headers)
            # resp = requests.get('http://localhost:5010/get', headers)
            print(resp.text)
            logger.info(resp.text)
            return resp.text
        except:
            pass

# 代理
# def get_proxy_ips():
#     resp = requests.get(
#         # 5
#         'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
#         # 20
#         # 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=&city=0&yys=0&port=1&time=2'
#     )
#     res = json.loads(resp.content.decode())
#     print(res)
#     print(datetime.datetime.now().strftime("%H:%M:%S"))
#     logger.info(resp.content.decode())
#     if res['success']:
#         res = res['data'][0]
#         ips = res['ip'] + ":" + str(res['port'])
#         return ips

def change_ips():
    global ips
    # print('change: %s'%ips)
    # resp = requests.get('http://10.9.60.13:5010/delete/?proxy=%s'%ips, headers)
    # print(resp.content.decode())
    ips = get_proxy_ips()

def get_data(url):
    success = False
    retry = 3
    global ips
    if not ips:
        ips = get_proxy_ips()
    while not success:
        retry -= 1
        try:
            resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=6)
            if resp.status_code == 200:
                success = True
                return resp
            # if retry <0:
            #    change_ips()
        except Exception as e:
            print(e)
            logger.error(str(e)+"*_*"+url)
            # if retry <0:
            #    change_ips()
            # ips = get_proxy_ips()


# def verify(content):
#     # eles = etree.HTML(content)
#     # ele = eles.xpath('//input[@name="checkcode"]')
#     # if len(ele) < 1:
#     #     return True
#     return True
#
# ip_pool = IpPool(1, verify)
#
# def get_data(url):
#     return ip_pool.get(url)

# def get_local_data(url):
#     success = False
#     while not success:
#         try:
#             resp = requests.get(url, headers=headers, proxies={'http': ips}, timeout=3)
#             if resp.status_code == 200:
#                 success = True
#                 return resp
#             else:
#                 print(resp.status_code)
#         except Exception as e:
#             print(e)

# get_data = get_local_data

if __name__ == '__main__':
    pass