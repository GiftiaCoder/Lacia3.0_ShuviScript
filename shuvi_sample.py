import shuvi.graph as graph
import shuvi.script.rule as rule
import shuvi.method.method as method
import tensorflow as tf


class InputMethod2(method.ShuviMethod):

    def __init__(self, name, namespace, inputs, graph, conf, confs):
        super().__init__(name, namespace, inputs, graph, conf, confs)
        self.__register_output__('output', tf.Variable(tf.random_uniform([4], -1.0, 1.0)))


class InputMethod(method.ShuviMethod):

    def __init__(self, name, namespace, inputs, graph, conf, confs):
        super().__init__(name, namespace, inputs, graph, conf, confs)
        input = self.__get_input_edge__(0)
        self.__register_output__('output', input + 100.0)


class OutputMethod(method.ShuviMethod):

    def __init__(self, name, namespace, inputs, graph, conf, confs):
        super().__init__(name, namespace, inputs, graph, conf, confs)

        offset = tf.placeholder(tf.float32)
        self.__register_placeholder__('offset', offset)

        input = self.__get_input_edge__(0)
        output = input + offset
        self.__register_output__('output', output)

graph = graph.ShuviGraph('script', {
    'input_method': InputMethod,
    'input_method2' : InputMethod2,
    'output_method': OutputMethod,
}, rule, rule)

with tf.Session() as sess:
    graph.init(sess)

    graph.conf()
    print(graph.run(sess, 'script.data_input'))
    print(graph.run(sess, 'script.input.output'))
    print(graph.run(sess, 'script.output1.output', {
        'script.output1.offset': 1
    }))
    print(graph.run(sess, 'script.output2.output', {
        'script.output1.offset': 1,
        'script.output2.offset': 10
    }))
