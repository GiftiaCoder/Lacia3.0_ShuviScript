
from .common import Type
from base.logger import logger

class SyntaxAnalyzer(object):
    def __init__(self, context):
        self.context = context

    def analyze(self, token_list):
        offset, syn_func = 0, self.__syn_nodename
        while offset < len(token_list):
            cur_loc = offset
            offset, syn_func = syn_func(token_list, offset)
            if not offset:
                tmp_list = []
                for token in token_list:
                    tmp_list.append(token[1])
                logger.error('invalid syntax at loc: %d' % cur_loc)
                logger.error('token list: %s' % ' '.join(tmp_list))
                return False
            if not syn_func:
                self.context.finish_cur_node()
                syn_func = self.__syn_nodename
        return True

    def __syn_nodename(self, token_list, offset):
        token_type, token_value = token_list[offset]
        if token_type == Type.NAME:
            self.context.node_set_name(token_value)
            return offset + 1, self.__syn_define
        return None, None

    def __syn_define(self, token_list, offset):
        token_type, token_value = token_list[offset]
        if token_type == Type.EQUAL:
            return offset + 1, self.__syn_outputlist
        return None, None

    def __syn_outputlist(self, token_list, offset):
        syn_func, output_list = self.__syn_parselist_start, self.context.node_get_output()
        while offset < len(token_list):
            offset, syn_func = syn_func(token_list, offset, Type.NAME, output_list)
            if offset:
                if not syn_func:
                    return offset, self.__syn_placeholderlist
            else:
                return None, None
        return None, None

    def __syn_placeholderlist(self, token_list, offset):
        syn_func, placeholder_list = self.__syn_parselist_start, self.context.node_get_placeholder()
        while offset < len(token_list):
            offset, syn_func = syn_func(token_list, offset, Type.NAME, placeholder_list)
            if offset:
                if not syn_func:
                    return offset, self.__syn_methodname
            else:
                return None, None
        return None, None

    def __syn_methodname(self, token_list, offset):
        token_type, token_value = token_list[offset]
        if token_type == Type.NAME:
            self.context.node_set_method(token_value)
            return offset + 1, self.__syn_inputlist
        return None, None

    def __syn_inputlist(self, token_list, offset):
        syn_func, input_list = self.__syn_parselist_start, self.context.node_get_input()
        while offset < len(token_list):
            offset, syn_func = syn_func(token_list, offset, Type.REF, input_list)
            if offset:
                if not syn_func:
                    return offset, None
            else:
                return None, None
        return None, None

    def __syn_parselist_start(self, token_list, offset, item_type, list_ctx):
        token_type, token_value = token_list[offset]
        if token_type == Type.BCKL:
            return offset + 1, self.__syn_parselist_item
        return None, None
    def __syn_parselist_item(self, token_list, offset, item_type, list_ctx):
        token_type, token_value = token_list[offset]
        if token_type == item_type:
            list_ctx.append(token_value)
            return offset + 1, self.__syn_parselist_split
        if token_type == Type.BCKR:
            return offset + 1, None
        return None, None
    def __syn_parselist_split(self, token_list, offset, item_type, list_ctx):
        token_type, token_value = token_list[offset]
        if token_type == Type.SPLIT:
            return offset + 1, self.__syn_parselist_item
        if token_type == Type.BCKR:
            return offset + 1, None
        return None, None