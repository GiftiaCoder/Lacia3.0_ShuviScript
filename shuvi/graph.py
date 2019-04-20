from base.logger import logger
import tensorflow as tf
import json
import shuvi.method.context as context
import shuvi.script.lexical as lexical
import shuvi.script.syntax as syntax

class ShuviGraph(object):
    def __init__(self, script, method_registry, *conf_paths):
        self.node_map = {}
        self.conf_map = {}
        self.script = script
        self.method_registry = method_registry

        self.conf_paths = list(conf_paths)
        self.update_conf(False)

    def build(self):
        ctx = context.ShuviContext(self.method_registry)
        lexana = lexical.LexicalAnalyzer()
        synana = syntax.SyntaxAnalyzer(ctx)

        token_list = lexana.lexical_analyze(self.script)
        if not token_list:
            logger.error('lexcal analyzation failed')
            return False
        if not synana.analyze(token_list):
            logger.error('syntax analyzation failed')
            return False
        if not ctx.build_graph(self):
            logger.error('build graph failed')
            return False

        return True

    def get_node_names(self):
        return set(self.node_map)
    def append_node(self, node, outputs):
        self.node_map[node.get_name()] = (node, outputs)

    def get_node(self, name):
        if name in self.node_map:
            return self.node_map[name][0]
        logger.error('node of name %s not found' % name)
        return None
    def get_output(self, edge_name):
        lst = edge_name.split('.')
        if len(lst) != 2:
            logger.error('invalid node edge: %s' % edge_name)
            return None
        node = self.get_node(lst[0])
        if node == None:
            return None
        edge = node.get_output(lst[1])
        if edge == None:
            logger.error('output of name %s not found in node %s of method %s' % (lst[1], lst[0], str(type(node))))
            return None
        return edge
    def get_placeholder(self, edge_name):
        lst = edge_name.split('.')
        if len(lst) != 2:
            logger.error('invalid node edge: %s' % edge_name)
            return None
        node = self.get_node(lst[0])
        if not node:
            return None
        edge = node.get_placeholder(lst[1])
        if edge == None:
            logger.error('placeholder of name %s not found in node %s of method %s' % (lst[1], lst[0], str(type(node))))
            return None
        return edge

    def init(self, sess):
        sess.run(tf.global_variables_initializer())
        for node in self.node_map:
            self.node_map[node][0].init(sess)

    def run(self, sess, node_edge, placeholder_map = None):
        feeddict = {}
        if placeholder_map:
            for key in placeholder_map:
                placeholder = self.get_placeholder(key)
                feeddict[placeholder] = placeholder_map[key]

        lst = node_edge.split('.')
        if len(lst) != 2:
            logger.error('invalid node edge: %s' % node_edge)
            return None
        node = self.get_node(lst[0])
        if node == None:
            return None
        node.fill_placeholders(lst[1], feeddict)
        return node.run(sess, lst[1], feeddict)

    def update_conf(self, update_nodes = True):
        update_success = True
        for path in self.conf_paths:
            with open(path) as file:
                try:
                    js = json.loads(file.read())
                    for name in js:
                        self.conf_map[name] = js[name]
                except Exception as e:
                    update_success = False
                    logger.error('exception: %s' % str(e))
        if update_success and update_nodes:
            for node, _ in self.node_map.values():
                node.conf(self.get_conf(node.get_name()),
                                 self.get_conf_map())
    def get_conf(self, name):
        if name in self.conf_map:
            return self.conf_map[name]
        logger.warning('conf of name %s not fount' % name)
        return None
    def get_conf_map(self):
        return self.conf_map
