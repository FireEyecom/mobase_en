from cli.cli import db_en_cache, db_en_olbase_url


if __name__ == '__main__':
    for index, db in enumerate(db_en_cache.find()):
        try:
            print(index)
            db_en_olbase_url.insert({'url': db['url']})
        except Exception as e:
            print(e)


