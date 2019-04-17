from base.logger import logger

class ShuviNode(object):
    def __init__(self):
        self.name = ''
        self.method = ''

        self.output = []
        self.placeholder = []
        self.input = []

        self.is_finish = False

class ShuviContext(object):
    def __init__(self, method_registry):
        self.node_list = []
        self.method_registry = method_registry

    def finish_cur_node(self):
        self.node_list[-1].is_finish = True

    def node_set_name(self, name):
        self.__get_cur_node__().name = name
    def node_set_method(self, method):
        self.__get_cur_node__().method = method
    def node_get_output(self):
        return self.__get_cur_node__().output
    def node_get_placeholder(self):
        return self.__get_cur_node__().placeholder
    def node_get_input(self):
        return self.__get_cur_node__().input

    def __get_cur_node__(self):
        if len(self.node_list) == 0 or self.node_list[-1].is_finish:
            self.node_list.append(ShuviNode())
        return self.node_list[-1]

    def build_graph(self, graph):
        for node in self.node_list:
            if node.method not in self.method_registry:
                logger.error('referenced method %s not exist' % node.method)
                return False
            if node.name in graph.get_node_names():
                logger.error('multi-declared node of name: %s' % node.name)
                return False

            input_list = []
            for input in node.input:
                name, edge = input.split('.')
                if name not in graph.get_node_names():
                    logger.error('referenced an undeclered node: %s' % name)
                    return False
                input_edge = graph.get_node(name).get_output(edge)
                if input_edge == None:
                    logger.error('referenced an undeclared node output: %s' % edge)
                    return False
                input_list.append(input_edge)

            graph_node = self.method_registry[node.method](node.name,
                                                           input_list,
                                                           graph,
                                                           graph.get_conf(node.name),
                                                           graph.get_conf_map())
            graph.append_node(graph_node, set(node.output))
        return True