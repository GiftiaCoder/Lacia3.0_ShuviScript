
class Method(object):

    def __init__(self, graph, inputs, inputnodes, confs, conf, logger):
        self.graph = graph
        self.inputs = inputs
        self.logger = logger

        if inputnodes:
            self.inputnodes = inputnodes
        else:
            self.inputnodes = []

        self.need_update_placeholder = False
        for node in self.inputnodes:
            if node.need_update_placeholder:
                self.need_update_placeholder = True

        # outputs
        self.output_map = {}
        self.placeholder_map = {}

    def init(self, sess):
        pass

    def conf(self, confs, conf):
        pass

    def feed_dict(self, feeddict):
        pass

    def run(self, sess, outputname):
        output = self.output_map.get(outputname, None)
        if output == None:
            self.logger.error('run undefined output[%s]' % outputname)
            return None

        if not self.need_update_placeholder:
            return sess.run(output)
        else:
            feed_dict = {}
            self.feed_dict(feed_dict)
            for node in self.inputnodes:
                if node.need_update_placeholder:
                    node.feed_dict(feed_dict)
            return sess.run(output, feed_dict=feed_dict)

    def get_output(self, name):
        if name in self.output_map:
            return self.output_map[name]
        else:
            self.logger.error('undefined output[%s]' % name)

    def get_placeholder(self, name):
        if name in self.placeholder_map:
            return self.placeholder_map[name]
        else:
            self.logger.error('undefined placeholder[%s]' % name)

    def post_construct(self):
        if len(self.placeholder_map) > 0:
            self.need_update_placeholder = True

    def get_graph(self):
        return self.graph

    # self call
    def register_output(self, name, tensor):
        self.output_map[name] = tensor

    def register_placeholder(self, name, tensor):
        self.placeholder_map[name] = tensor
