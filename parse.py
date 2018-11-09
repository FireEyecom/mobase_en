from lxml import etree
from cli import get_data, mongo
import re
import json


def filter(eles):
    if len(eles) > 0:
        return eles[0]
    return ''


def sds_url(url):
    eles = url.split('-moldata-')
    first = eles[0].split('_')[1]
    second = eles[1].split('.')[0]
    url = 'http://baike.molbase.cn/ajax/sds/%s/%s?callback=a' % (second, first)
    return url


def empty_item(items):
    if len(items) > 0:
        return items[0].strip()
    return ''


def trim(content):
    return re.sub('\n|\t', '', content)


def fix_url(url):
    return "http:" + url


def get_string(items):
    if len(items) > 0:
        return items[0].xpath('string(.)').strip()
    return ''


def Synonym(eles):
    synonyms = eles[2].xpath('./td/div/div/ul')
    if len(synonyms) > 0:
        return get_string(synonyms)
    else:
        synonyms = eles[2].xpath('./td/div/ul')
        return get_string(synonyms)


def price_item(eles):
    if len(eles) > 8:
        Reference_price = eles[8].xpath('./td/a[1]/b/text()')
        Reference_price = empty_item(Reference_price)
        return Reference_price
    else:
        return ''


def info(content):
    eles = etree.HTML(content)
    eles = eles.xpath('//table[@class="mb_l_mb_r_tb pinfo"]')[0]
    eles = eles.xpath('./tr')
    name = eles[0].xpath('./td/a/h1/text()')
    name = empty_item(name)
    cas = eles[1].xpath('./td/text()')
    cas = empty_item(cas)
    # Synonyms = eles[2].xpath('./td/div/div/ul')
    Synonyms = trim(Synonym(eles))
    Formula = eles[3].xpath('./td/text()')
    Formula = empty_item(Formula)
    Exact_Mass = eles[4].xpath('./td/text()')
    Exact_Mass = empty_item(Exact_Mass)
    Molecular = eles[5].xpath('./td/text()')
    Molecular = empty_item(Molecular)
    PSA = eles[6].xpath('./td/text()')
    PSA = empty_item(PSA)
    LogP = eles[7].xpath('./td/text()')
    LogP = empty_item(LogP)
    Reference_price = price_item(eles)
    return locals()


def description(content):
    eles = etree.HTML(content)
    Description = eles.xpath('//div[@class="cont_text"]/text()')
    Description = empty_item(Description)
    return Description


def Properties(content):
    eles = etree.HTML(content)
    eles = eles.xpath('//table[@id="tab_body_1"]')
    if len(eles) > 1:
        eles = eles[1]
    else:
        eles = eles[0]
    prop = {}
    for ele in eles:
        key = empty_item(ele.xpath('./th/text()'))
        value = empty_item(ele.xpath('./td/text()'))
        if key:
            prop[key[:-1]] = value
    return prop


def Safety_Info(content):
    eles = etree.HTML(content)
    eles = eles.xpath('//table[@id="tab_body_2"]')[0]
    prop = {}
    for ele in eles:
        key = empty_item(ele.xpath('./th/text()'))
        value = get_string(ele.xpath('./td'))
        if key:
            prop[key[:-1]] = value
    return prop


def SDS(content):
    eles = etree.HTML(content)
    eles = eles.xpath('//ul[@class="mbctabs fix-clear"]/li/a/@href')[-3]
    flag = re.match('.*html', eles)
    if flag:
        content = get_data(sds_url(eles)).content.decode()
        data = filter(re.findall('a\((.*)\)', content))
        if data:
            dt = json.loads(data)
            if dt['code'] == 'error':
                return ''
            return trim(dt['data'])
        return ''
    return ''


def MSDS(content):
    eles = etree.HTML(content)
    eles = eles.xpath('//ul[@class="mbctabs fix-clear"]/li/a/@href')[-2]
    flag = re.match('.*html', eles)
    if flag:
        eles = fix_url(eles)
        eles = get_data(eles).content.decode()
        msds = etree.HTML(eles).xpath('//div[@class="msds"]')
        if len(msds) > 0:
            content = etree.tostring(filter(msds), encoding='utf-8').decode()
            return trim(content)
        return ''
    return ''


def NMR(content):
    eles = etree.HTML(content)
    eles = eles.xpath('//ul[@class="mbctabs fix-clear"]/li/a/@href')[-1]
    flag = re.match('.*html', eles)
    if flag:
        eles = fix_url(eles)
        eles = get_data(eles).content.decode()
        ele = etree.HTML(eles)
        try:
            tables = ele.xpath('//div[@style="margin:9px;background-color:#fff;"]')
            nrm_h1 = tables[0].xpath('string(.)').strip()
            nrm_h1_url = filter(tables[0].xpath('./img/@src'))
            nrm_13c = tables[1].xpath('string(.)').strip()
            nrm_13c_url = filter(tables[1].xpath('./img/@src'))
            return dict(nrm_h1=nrm_h1, nrm_h1_url=nrm_h1_url, nrm_13c=nrm_13c,
                        nrm_13c_url=nrm_13c_url)
        except:
            nodata = ele.xpath('//div[@class="nodata"]')
            if len(nodata) == 0:
                print('nrm error')
                return NMR(content)
            return dict(nrm_h1='', nrm_h1_url='', nrm_13c='', nrm_13c_url='')
    return dict(nrm_h1='', nrm_h1_url='', nrm_13c='', nrm_13c_url='')





parses = [info, description, Properties, Safety_Info, SDS, MSDS, NMR]


def filter_ele(dt):
    keys = list(dt.keys())
    # dt.pop('content')
    dt.pop('eles') if keys.count('eles') > 0 else dt
    dt.pop('content') if keys.count('content') > 0 else dt
    dt.pop('flag') if keys.count('flag') > 0 else dt
    return dt


import json


def parse(url):
    content = get_data(url).content.decode()
    dt = {'url': url}
    for func in parses:
        res = func(content)
        if isinstance(res, dict):
            dt[func.__name__] = filter_ele(res)
        else:
            dt[func.__name__] = res
    dt = show(dt)
    # print(json.dumps(dt))
    return dt


def show(item):
    props = {}
    for key, val in item.items():
        if isinstance(val, str):
            props[key] = val
        else:
            for k, v in val.items():
                props[k] = v
    return props


if __name__ == '__main__':
    collection = parse('http://www.molbase.com/en/616-47-7-moldata-3094.html')
    mongo().insert(collection)
