from base.logger import logger

class ShuviMethod(object):
    def __init__(self, name, inputs, graph, conf, confs):
        self.output_map = {}
        self.placeholder_map = {}
        self.name = name

        self.inputs = inputs

    def init(self, sess):
        pass
    def update_conf(self, conf, confs):
        pass
    def run(self, sess, output_name, feed_dict):
        return sess.run(self.get_output(output_name), feed_dict)

    def get_name(self):
        return self.name
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