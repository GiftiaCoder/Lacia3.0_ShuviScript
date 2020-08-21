import shuvi.graph
from shuvi.method.method import Method
from base.logger import logger

import tensorflow
logger.info('tensorflow.__version__ = %s' % tensorflow.__version__)
if tensorflow.__version__.split('.')[0] == '1':
    import tensorflow as tf
else:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

script_text = '''
input = (output)()input_method()

{{
# this is a python script which used like javascript in html
input_name = 'input.output'
print('out1 = (output)(offset)output_method(%s)' % input_name)
}}

out2 = (output)(offset)output_method(out1.output)
'''


class InputMethod(Method):
    def __init__(self, graph, inputs, inputnodes, confs, conf, logger):
        super().__init__(graph, inputs, inputnodes, confs, conf, logger)

        self.output = tf.Variable([2, 3, 5, 7, 11, 13], dtype=tf.float32)
        self.register_output('output', self.output)


class OutputMethod(Method):
    def __init__(self, graph, inputs, inputnodes, confs, conf, logger):
        super().__init__(graph, inputs, inputnodes, confs, conf, logger)

        self.val_offset = conf['offset']

        self.offset = tf.placeholder(dtype=tf.float32)
        self.register_placeholder('offset', self.offset)

        self.output = inputs[0] + self.offset
        self.register_output('output', self.output)

    def feed_dict(self, feeddict):
        feeddict[self.offset] = self.val_offset

    def conf(self, confs, conf):
        self.val_offset = conf['offset']

    def list_conf_name(self):
        return [('offset', 0)]


graph = shuvi.graph.Graph(script_text, {
    'input_method': InputMethod,
    'output_method': OutputMethod,
}, logger=logger, conf_paths=[
    'sample.json.conf'
])
graph.gen_conf('./sample.gen.conf')

with tf.Session() as sess:
    graph.init(sess, tf.global_variables_initializer())
    graph.conf()
    print(graph.run(sess, 'input.output'))
    print(graph.run(sess, 'out1.output'))
    print(graph.run(sess, 'out2.output'))
