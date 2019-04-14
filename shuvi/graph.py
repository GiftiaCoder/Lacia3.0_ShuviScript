from base.logger import logger
import tensorflow as tf
import json
import method.context as context
import script.lexical as lexical
import script.syntax as syntax

class ShuviGraph(object):
    def __init__(self, script, method_registry, *conf_paths):
        self.node_map = {}
        self.conf_map = {}
        self.script = script
        self.method_registry = method_registry

        self.conf_paths = list(conf_paths)
        self.update_conf()

    def build_self(self):
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
    def append_node(self, name, graph_node, outputs):
        self.node_map[name] = (graph_node, outputs)

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
        if not node:
            return None
        edge = node.get_output(lst[1])
        if not edge:
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
        if not edge:
            logger.error('placeholder of name %s not found in node %s of method %s' % (lst[1], lst[0], str(type(node))))
            return None
        return edge

    def init(self, sess):
        sess.run(tf.global_variables_initializer())
        for node in self.node_map:
            self.node_map[node][0].init(sess)

    def run(self, sess, node_edge, placeholder_map):
        output = self.get_output(node_edge)
        feeddict = {}
        for key in placeholder_map:
            placeholder = self.get_placeholder(key)
            feeddict[placeholder] = placeholder_map[key]
        sess.run(output, feed_dict=feeddict)
        return
    def update_conf(self):
        for path in self.conf_paths:
            with open(path) as file:
                try:
                    js = json.loads(file.read())
                    self.conf_map[js['name']] = js
                except Exception as e:
                    logger.error('exception: %s' % str(e))

    def get_conf(self, name):
        if name in self.conf_map:
            return self.conf_map[name]
        logger.error('cannot find conf of name: %s' % name)
        return None
