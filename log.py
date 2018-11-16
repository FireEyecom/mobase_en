import logging

logger = logging.getLogger('spider')
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("spider.log")
handler.setLevel(logging.INFO)
# handler.setLevel(logging.ERROR)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


log = logging.getLogger('engin')
log.setLevel(level = logging.INFO)
handler = logging.FileHandler("engin.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def get_log(chart):
    logger = logging.getLogger(chart)
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler("log/log_%s.log"%chart)
    handler.setLevel(logging.INFO)
    # handler.setLevel(logging.ERROR)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger



