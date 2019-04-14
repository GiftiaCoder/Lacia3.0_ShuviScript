import re
from base.logger import logger

from .common import __pattern_type_map__
from .common import __ignored_type_name__

class LexicalAnalyzer(object):
    def __init__(self):
        pattern_list = []

        self.__total_pattern_list__ = []
        for type, pattern in __pattern_type_map__:
            pattern_list.append('(' + pattern + ')')
            self.__total_pattern_list__.append((type, re.compile(pattern)))

        self.__total_token_pattern__ = re.compile('|'.join(pattern_list))

    def lexical_analyze(self, text):
        token_list = []

        offset = 0
        while offset < len(text):
            group = self.__total_token_pattern__.match(text, offset)
            if group:
                token = group.group()
                for type, pattern in self.__total_pattern_list__:
                    if pattern.match(token):
                        if type not in __ignored_type_name__:
                            token_list.append((type, token))
                            break
                offset += len(token)
            else:
                logger.error('compile failed at line: %s, loc: %d' % (text, offset))
                return None
        return token_list
