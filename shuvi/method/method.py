import base.logger as logger


class ShuviMethod(object):

    def __init__(self, nodename, namespace, inputs, graph, conf, confs):
        self.nodename = nodename
        self.namespace = namespace
        self.inputs = inputs
        self.graph = graph

        # edge output
        self.output_map = {}
        self.placeholder_map = {}

    def init(self, sess):
        pass

    def conf(self, conf, confs):
        pass

    def __feed_dict__(self, tensor, val):
        self.graph.feed_dict[tensor] = val

    def __get_input_edge__(self, idx):
        return self.inputs[idx]

    def __register_output__(self, name, tensor):
        self.output_map[name] = tensor

    def __register_placeholder__(self, name, tensor):
        self.placeholder_map[name] = tensor

    def get_output(self, name):
        if name in self.output_map:
            return self.output_map[name]
        else:
            logger.error('cannot find output of name[%s]' % name)

    def get_placeholder(self, name):
        if name in self.placeholder_map:
            return self.placeholder_map[name]
        else:
            logger.error('cannot find output of name[%s]' % name)
