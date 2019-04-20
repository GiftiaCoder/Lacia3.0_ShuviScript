import shuvi.graph as graph
import shuvi.method.method as method
import tensorflow as tf
from base.logger import logger

class InputMethod(method.ShuviMethod):
    def __init__(self, name, inputs, graph, conf, confs):
        super().__init__(name, inputs, graph, conf, confs)
        self.register_output('output', tf.Variable(tf.random_uniform([4], -1.0, 1.0)))

class OutputMethod(method.ShuviMethod):
    def __init__(self, name, inputs, graph, conf, confs):
        super().__init__(name, inputs, graph, conf, confs)

        offset = tf.placeholder(tf.float32)
        self.register_placeholder('offset', offset)

        input = self.get_input_edge(0)
        output = input * input + offset
        self.register_output('output', output)

script = '#this is just a comment example\n' \
         'input = (output)()input_method()\n' \
         'output1 = (output)(offset)output_method(input.output)\n' \
         'output2 = (output)(offset)output_method(output1.output)'

graph = graph.ShuviGraph(script, {
    'input_method': InputMethod,
    'output_method': OutputMethod,
})
if graph.build():
    with tf.Session() as sess:
        graph.init(sess)

        graph.update_conf()
        print(graph.run(sess, 'input.output'))
        print(graph.run(sess, 'output1.output', {
            'output1.offset': 1
        }))
        print(graph.run(sess, 'output2.output', {
            'output1.offset': 1,
            'output2.offset': 10
        }))
else:
    logger.error('build graph failed')