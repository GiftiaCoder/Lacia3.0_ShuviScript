import shuvi.graph
from shuvi.method.method import Method
from base.logger import logger

import tensorflow as tf

script_text = 'input = (output)()input_method()' \
              + 'output = (output)(offset)output_method(input.output)'

class InputMethod(Method):
    def __init__(self, inputs, inputnodes, confs, conf, logger):
        super().__init__(inputs, inputnodes, confs, conf, logger)

        self.output = tf.sqrt(tf.Variable([2, 3, 5, 7, 11, 13, 17, 19], dtype=tf.float32))
        self.register_output('output', self.output)


class OutputMethod(Method):
    def __init__(self, inputs, inputnodes, confs, conf, logger):
        super().__init__(inputs, inputnodes, confs, conf, logger)

        self.offset = tf.placeholder(dtype=tf.float32)
        self.register_placeholder('offset', self.offset)

        self.output = inputs[0] * tf.sin(inputs[0]) + self.offset
        self.register_output('output', self.output)

    def feed_dict(self, feeddict):
        feeddict[self.offset] = 3.141


graph = shuvi.graph.Graph(script_text, {
    'input_method': InputMethod,
    'output_method': OutputMethod,
}, logger=logger)

with tf.Session() as sess:
    graph.init(sess, tf.global_variables_initializer())
    print(graph.run(sess, 'input.output'))
    print(graph.run(sess, 'output.output'))

