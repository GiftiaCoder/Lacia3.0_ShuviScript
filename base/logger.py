import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('lacia.log')
formatter = logging.Formatter(
    '[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)