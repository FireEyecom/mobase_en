from cli.cli import get_data
from db.db import db_en_cache, en_olbase_err, mongo, db_en_olbase
from core.parse import parses, filter_ele
import uuid
from multiprocessing import Process, Queue
import random
from queue import Empty
from cli.log import get_log

log = get_log('engin')


def run(size):
    queues = [Queue() for i in range(size)]
    p_list = [Process(target=process, args=(queue,)) for queue in queues]
    for p in p_list:
        p.start()
    db = db_en_cache.find()
    count = 0
    while True:
        try:
            url = db.next()['url']
            count += 1
            # if url not in self.url_pool:
            res = db_en_olbase.find_one({'url': url})
            if not res:
                queue = random.choice(queues)
                queue.put(url)
        except StopIteration:
            log.error("can not find data in db_en_olbase_url")
        except Exception as e:
            log.exception(e)
            db = db_en_cache.find()[count:]

def process(queue):
    while True:
        try:
            url = queue.get(True, timeout=3)
            parse(url)
        except Empty:
            pass
        except Exception as e:
            log.exception(e)

def parse(url):
    try:
        content = get_data(url).content.decode()
        dt = {'url': url}
        for func in parses:
            res = func(content)
            if isinstance(res, dict):
                dt[func.__name__] = filter_ele(res)
            else:
                dt[func.__name__] = res
        pipline(dt)
    except Exception as e:
        en_olbase_err().insert({'url': url, 'msg': str(e)})
        log.exception(e)

def pipline(item):
    item['NMR']['nmr_13c_img'] = save_Img(item['NMR']['nmr_13c_url'])
    item['NMR']['nmr_h1_img'] = save_Img(item['NMR']['nmr_h1_url'])
    item['info']['structure_img'] = save_img(item['info']['structure_img_url'])
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
    props['item'] = item
    print(props)
    # self.url_pool.remove(item['url'])
    mongo().insert(props)
    # db_en_cache.remove({'url':item['url']})
    # db_en_olbase_url.remove({'url': item['url']})
    # self.local(val_list)

def save_Img(url):
    """
    存图片
    :param url:
    :return:
    """
    if not url:
        return ""
    resp = get_data(url)
    name = str(uuid.uuid4()) + '.png'
    with open('imgs/%s' % name, 'wb') as f:
        f.write(resp.content)
    return name

def save_img(url):
    if not url:
        return ""
    resp = get_data(url)
    name = str(uuid.uuid4()) + '.png'
    with open('base_img/%s' % name, 'wb') as f:
        f.write(resp.content)
    return name

if __name__ == '__main__':
    run(10)