import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC
import matplotlib as mpl

class UnaryOperation(ABC):
    def __init__(self, op):
        self.executed = False
        self.result = None
        self.depends_on = op

class BinaryOperation(UnaryOperation):
    def __init__(self, op, op2):
        super().__init__(op)
        self.depends_on_2 = op2

class Workflow(list):
    def __init__(self):
        super().__init__()

    def add(self, operation):
        self.append(operation)
        self.draw_workflow()
        self.visualize()

    def run(self):
        #run logic
        pass

    def draw_workflow(self):
        graph = nx.DiGraph()

        list_op=[]
        for i in range(len(self)):
            if self[i].__class__.__name__=='Select':
                graph.add_node(self[i].depends_on)
            graph.add_node(self[i])
            graph.add_edge(self[i],self[i].depends_on)
            if hasattr(self[i], 'depends_on_2'):
                graph.add_edge(self[i],self[i].depends_on_2)

        nodes= list(graph.nodes)
        mapping = {nodes[i]: nodes[i].__class__.__name__+str(i) for i in range(len(nodes))}
        #graph = nx.relabel_nodes(graph, mapping)
        pos = nx.layout.spring_layout(graph)
        options = {"node_size": 500, "alpha": 0.8, "node_shape": 'd', 'label':graph.nodes}
        node_sizes = [3 + 10 * i for i in range(len(graph))]
        M = graph.number_of_edges()

        nx.draw_networkx_nodes(graph, pos, node_color="none", **options)
        edges = nx.draw_networkx_edges(graph, pos, node_size=node_sizes, arrowstyle="->", arrowsize=10, edge_color='skyblue',width=2)
        nx.draw_networkx_labels(graph, pos, labels=mapping, font_size=16)
        #nx.draw(graph, with_labels=True, node_shape="s", node_color="none",bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))

        ax = plt.gca()
        ax.set_axis_off()
        plt.show()



    def visualize(self):
        for i in range(len(self)):
            name = self[i].__class__.__name__
            print(i)
            print(name)
            print('--parameters--')
            for x,v in self[i].__dict__.items():
                if (x=='depends_on') or (x=='depends_on_2'):
                    print(x+':'+str(v.__class__.__name__))
                    if str(v.__class__.__name__)=='DataSet':
                        for q,w in v.__dict__.items():
                            print(q+':'+str(w))
                else:
                    print(x+':'+str(v))
            print('-------')


