import ply.ply.lex as lex
import ply.ply.yacc as yacc
from .script import lexer as compile_lexer
from .script import syntax as compile_syntax
from .script import preparser

import json
import os


class Graph(object):

    def __init__(self, script_text, method_registry, logger, conf_paths=None):
        self.method_registry = method_registry
        self.logger = logger
        self.conf_paths = conf_paths
        if not self.conf_paths:
            self.conf_paths = []

        self.node_map = {}
        self.conf_map = {}
        # to record the last loading time stamp for each conf file
        self.conf_update_ts = {}
        self.__load_confs__()

        lexer = lex.lex(module=compile_lexer)
        syntax = yacc.yacc(module=compile_syntax)
        syntax.__define_node__ = self.__define_node__
        if logger:
            syntax.__logger__ = logger

        parser = preparser.Parser()
        for c in script_text:
            parser.feed(c)
        parser.close()
        self.logger.warning('final shuvi script[%s]' % parser.get_final_script())
        syntax.parse(parser.get_final_script(), lexer=lexer)

    def run(self, sess, outputpath):
        nodename, outputname = outputpath.split('.')
        node = self.node_map.get(nodename, None)
        if node == None:
            self.logger.error('node of name[%s] not found' % nodename)
            return None
        return node.run(sess, outputname)

    def init(self, sess, tf_initializer):
        sess.run(tf_initializer)
        for name, node in self.node_map.items():
            node.init(sess)

    def conf(self):
        if self.__load_confs__():
            for name, node in self.node_map.items():
                node.conf(self.conf_map, self.conf_map.get(name, None))

    def get_output(self, outputpath):
        nodename, outputname = outputpath.split('.')
        node = self.node_map.get(nodename, None)
        if node is None:
            self.logger.error('node of name[%s] not found' % nodename)
            return None
        return node.get_output(outputname)

    # private
    def __define_node__(self, nodename, methodname, outputs, placeholders, inputs):
        if methodname not in self.method_registry:
            self.logger.error('method name[%s] not registed' % methodname)
        if nodename in self.node_map:
            self.logger.error('node[%s] has already registed' % nodename)

        input_edge_list, input_node_list = [], set()
        for input_node_name, input_edge_name in inputs:
            input_node = self.node_map.get(input_node_name, None)
            if input_node is None:
                self.logger.error('undefined node[%s]' % input_node_name)
            input_edge = input_node.get_output(input_edge_name)
            if input_edge is None:
                self.logger.error('undefined edge[%s] of node[%s]' % (input_edge_name, input_node_name))
            input_node_list.add(input_node)
            input_edge_list.append(input_edge)

        node = self.method_registry[methodname](self,
                                                input_edge_list,
                                                list(input_node_list),
                                                self.conf_map,
                                                self.conf_map.get(nodename, None),
                                                self.logger)
        node.post_construct()

        self.__verify_outputs__(node, outputs)
        self.__verify_placeholders__(node, placeholders)

        self.node_map[nodename] = node

    def __load_confs__(self):
        has_updated = False
        for conf_path in self.conf_paths:
            try:
                cur_ts = os.path.getmtime(conf_path)
                if conf_path not in self.conf_update_ts or self.conf_update_ts[conf_path] != cur_ts:
                    with open(conf_path) as i_f:
                        js = json.loads(i_f.read())
                        for k in js:
                            self.conf_map[k] = js[k]
                    self.conf_update_ts[conf_path] = cur_ts
                    has_updated = True
            except Exception as e:
                self.logger.warning('catch exception when loading conf file[%s]: %s' % (conf_path, str(e)))
        return has_updated

    @staticmethod
    def __verify_outputs__(node, names):
        for name in names:
            node.get_output(name)

    @staticmethod
    def __verify_placeholders__(node, names):
        for name in names:
            node.get_placeholder(name)

