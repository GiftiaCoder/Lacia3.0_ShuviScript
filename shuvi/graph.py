import base.logger as logger
import ply.lex as lex
import ply.yacc as yacc
import os
import json
import tensorflow as tf

class ShuviGraph(object):
    def __init__(self, package_name, method_registry, lexmodule, parsermodule, *conf_paths):
        # parser
        self.lexmodule = lexmodule
        self.parsermodule = parsermodule
        self.__cur_namespace__ = ''
        # init data
        self.method_registry = method_registry

        # build graph phase
        # name => node
        self.node_map = {}
        # name => edge/placeholder
        self.edge_map = {}
        self.placeholder_map = {}
        # node_name => edge/placeholder
        self.node_edge_map = {}
        self.node_placeholder_map = {}

        # runtime phase
        # tensor => value
        self.feed_dict = {}
        # name => conf map
        self.conf_map = {}

        # just a timestamp of each conf files
        self.conf_file_version_map = {}
        for conf_path in conf_paths:
            self.conf_file_version_map[conf_path] = 0.0

        # load file
        self.__load_conf__()
        self.__import_package__(package_name)

    def init(self, sess):
        sess.run(tf.global_variables_initializer())
        for node_name in self.node_map:
            self.node_map[node_name].init(sess)

    def run(self, sess, edge_path, placeholders=None):
        if edge_path not in self.edge_map:
            logger.error('edge of path[%s] has not been defined or referenced' % edge_path)

        output_edge = self.edge_map[edge_path]
        if placeholders:
            for placeholder_path in placeholders:
                if placeholder_path in self.placeholder_map:
                    self.feed_dict[self.placeholder_map[placeholder_path]] = placeholders[placeholder_path]

        return sess.run(output_edge, feed_dict=self.feed_dict)

    def conf(self):
        if self.__load_conf__():
            for node_path in self.node_map:
                conf = None
                if node_path in self.conf_map:
                    conf = self.conf_map[node_path]
                self.node_map[node_path].conf(conf, self.conf_map)

    def __import_package__(self, package_name):
        if type(package_name) == list:
            self.__cur_pkg_file_path__ = '.'.join(package_name) + '.shv'
        else:
            self.__cur_pkg_file_path__ = './' + package_name.replace('.', '/') + '.shv'

        with open(self.__cur_pkg_file_path__) as i_f:
            orig_namespace = self.__cur_namespace__

            if type(package_name) == list:
                self.__cur_namespace__ = '.'.join(package_name)
            else:
                self.__cur_namespace__ = package_name

            lexer = lex.lex(module=self.lexmodule)
            parser = yacc.yacc(module=self.parsermodule)
            parser.__expr_import_package__ = self.__import_package__
            parser.__expr_use_edge__ = self.__set_use_edge__
            parser.__expr_use_node__ = self.__set_use_node__
            parser.__expr_create_node__ = self.__create_node__

            parser.parse(i_f.read(), lexer=lexer)

            self.__cur_namespace__ = orig_namespace

    def __set_use_edge__(self, using_edge, target_ref):
        fin_edge = self.__get_first_valid__([
            self.edge_map.get(self.__cur_namespace__ + '.' + '.'.join(using_edge), None),
            self.edge_map.get('.'.join(using_edge), None)
        ])
        if fin_edge:
            if len(target_ref) > 0:
                self.edge_map[self.__cur_namespace__ + '.' + '.'.join(target_ref)] = fin_edge
            else:
                self.edge_map[self.__cur_namespace__ + '.' + using_edge[-1]] = fin_edge
        else:
            logger.error('edge of path[%s or %s] to referenced has not been defined' %
                         ('.'.join(using_edge), self.__cur_namespace__ + '.' + '.'.join(using_edge)))

    def __set_use_node__(self, using_node, target_node):
        fin_edge_list = self.__get_first_valid__([
            (self.node_edge_map.get(self.__cur_namespace__ + '.' + '.'.join(using_node), None), self.__cur_namespace__ + '.' + '.'.join(using_node)),
            (self.node_edge_map.get('.'.join(using_node), None), '.'.join(using_node)),
        ], lambda val: val[0])
        if fin_edge_list:
            fin_node_path = fin_edge_list[1]
            if len(target_node) > 0:
                target_node_path = self.__cur_namespace__ + '.' + '.'.join(target_node)
            else:
                target_node_path = self.__cur_namespace__ + '.' + using_node[-1]
            for edge_name in fin_edge_list[0]:
                self.edge_map[target_node_path + '.' + edge_name] = self.edge_map[fin_node_path + '.' + edge_name]
        else:
            logger.error('edge of path[%s or %s] to referenced has not been defined' %
                         ('.'.join(using_node), self.__cur_namespace__ + '.' + '.'.join(using_node)))

    def __create_node__(self, node_name, method_name, inputs, placeholders, outputs):
        node_path = self.__cur_namespace__ + '.' + node_name
        edge_list, placeholder_list = [], []

        input_list = []
        for input_path in inputs:
            fin_edge = self.__get_first_valid__([
                self.edge_map.get(self.__cur_namespace__ + '.' + '.'.join(input_path), None),
                self.edge_map.get('.'.join(input_path), None),
            ])

            if fin_edge != None:
                input_list.append(fin_edge)
            else:
                logger.error('input edge of path[%s] has not been defined or referenced' % input_path)

        conf = None
        if node_path in self.conf_map:
            conf = self.conf_map[node_path]

        if method_name in self.method_registry:
            node = self.method_registry[method_name](node_name,
                                                     self.__cur_namespace__,
                                                     input_list,
                                                     self,
                                                     conf,
                                                     self.conf_map)
            self.node_map[node_path] = node

            for output in outputs:
                edge_path = node_path + '.' + output
                if edge_path not in self.edge_map:
                    edge_list.append(output)
                    self.edge_map[edge_path] = node.get_output(output)

                else:
                    logger.error('edge of path[%s] has been defined or referenced in current namespace[%s]' %
                                 (edge_path, self.__cur_namespace__))
            self.node_edge_map[node_path] = edge_list

            for placeholder in placeholders:
                placeholder_path = node_path + '.' + placeholder
                if placeholder_path not in self.placeholder_map:
                    placeholder_list.append(placeholder)
                    self.placeholder_map[placeholder_path] = node.get_placeholder(placeholder)
                else:
                    logger.error('placeholder of path[%s] has been defined or referenced in current namespace[%s]' %
                                 (placeholder_path, self.__cur_namespace__))
            self.node_placeholder_map[node_path] = placeholder_list
        else:
            logger.error('method[%s] not in registry' % method_name)

    def __load_conf__(self):
        try:
            conf_updated = False
            for conf_path in self.conf_file_version_map:
                if self.__reload_conf_if_need__(conf_path):
                    conf_updated = True
            return conf_updated
        except:
            return False

    def __reload_conf_if_need__(self, conf_path):
        last_version = self.conf_file_version_map.get(conf_path, 0.0)
        modify_version = os.path.getmtime(conf_path)
        if last_version != modify_version:
            with open(conf_path) as i_f:
                obj = json.loads(i_f.read())
                for key in obj:
                    self.conf_map[key] = obj[key]
            self.conf_file_version_map[conf_path] = modify_version

    def __get_first_valid__(self, vals, condition=None):
        for val in vals:
            if condition:
                if condition(val):
                    return val
            else:
                if val != None:
                    return val
        return None
