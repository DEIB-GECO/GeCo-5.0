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
        gmql_operation = ['Select', 'ProjectMetadata', 'ProjectRegion', 'Cover', 'Join', 'Union', 'Map', 'Difference']
        pivot_operation = ['Pivot', 'JoinPivot', 'ConcatenatePivot']
        gmql_ops = []
        pivot_ops = []
        for i in range(len(self.workflow), 0):
            elem = self.workflow[i]
            if elem.executed == True:
                break
            elif elem.__class__.__name__ in gmql_operation:
                gmql_ops.append(elem)
            elif elem.__class__.__name__ in pivot_operation:
                pivot_ops.append(elem)
        if gmql_ops != []:
            GMQL_Logic(self.workflow, gmql_ops)
        if pivot_ops != []:
            Pivot_Logic(self.workflow, pivot_ops)
        #run logic
        pass

    def draw_workflow(self):
        graph = nx.DiGraph()

        for i in range(len(self)):
            if self[i].__class__.__name__=='Select':
                graph.add_node(self[i].depends_on)
            graph.add_node(self[i])
            graph.add_edge(self[i],self[i].depends_on)
            if hasattr(self[i], 'depends_on_2'):
                graph.add_edge(self[i],self[i].depends_on_2)

        nodes= list(graph.nodes)
        mapping = {nodes[i]: nodes[i].__class__.__name__+str(i) for i in range(len(nodes))}
        graph = nx.relabel_nodes(graph, mapping)

        #nx.draw_networkx_nodes(graph, pos, node_color="none", **options)
        #edges = nx.draw_networkx_edges(graph, pos, node_size=node_sizes, arrowstyle="->", arrowsize=10, edge_color='skyblue',width=2)
        #nx.draw_networkx_labels(graph, pos, labels=mapping, font_size=16)
        nx.draw(graph, with_labels=True, node_shape="s", node_color="none",bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round,pad=0.2'))

        plt.savefig('workflow.png')
        #plt.show()



    def visualize(self):
        with open('workflow.txt', 'w') as file:
            for i in range(len(self)):
                name = self[i].__class__.__name__
                file.write(str(i)+'\n')
                file.write(name+'\n')
                file.write('--parameters--\n')
                for x,v in self[i].__dict__.items():
                    if (x=='depends_on') or (x=='depends_on_2'):
                        file.write(x+':'+str(v.__class__.__name__)+'\n')
                        if str(v.__class__.__name__)=='DataSet':
                            for q,w in v.__dict__.items():
                                file.write(q+':'+str(w)+'\n')
                    else:
                        file.write(x+':'+str(v)+'\n')
                file.write('-------'+'\n')


