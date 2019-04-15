from base.logger import logger

class ShuviMethod(object):
    def __init__(self, name, graph, inputs):
        self.output_map = {}
        self.placeholder_map = {}
        self.name = name
        self.graph = graph

        self.inputs = inputs

    def init(self, sess):
        pass
    def update_conf(self, conf, confs):
        pass

    def get_name(self):
        return self.name
    def get_graph(self):
        return self.graph
    def get_inputs(self):
        return self.inputs

    def register_output(self, name, tensor):
        if name not in self.output_map:
            self.output_map[name] = tensor
        else:
            logger.error('output tensor of name %s has exist' % name)
    def register_placeholder(self, name, tensor):
        if name not in self.placeholder_map:
            self.placeholder_map[name] = tensor
        else:
            logger.error('placeholder tensor of name %s has exist' % name)

    def get_output(self, name):
        if name in self.output_map:
            return self.output_map[name]
        logger.error('output %s not found' % name)
        return None
    def get_placeholder(self, name):
        if name in self.placeholder_map:
            return self.placeholder_map[name]
        logger.error('output %s not found' % name)
        return None