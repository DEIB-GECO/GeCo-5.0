import networkx as nx
import matplotlib.pyplot as plt
from abc import ABC
import importlib
from logic.select_logic import SelectLogic

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

        #self.draw_workflow()
        #self.visualize()

    def run(self, last_op):
        if last_op.executed == True:
            return
        elif last_op.__class__.__name__ == 'Select':
            SelectLogic(last_op)
        else:
            package = importlib.import_module('logic')
            logic_class = getattr(package, last_op.__class__.__name__ + 'Logic')
            if hasattr(last_op, 'depends_on_2'):
                if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
                    self.run(last_op.depends_on_2)
                elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
                    self.run(last_op.depends_on)
                else:
                    self.run(last_op.depends_on)
                    self.run(last_op.depends_on_2)
            else:
                if last_op.depends_on.executed == False:
                    self.run(last_op.depends_on)
            logic_class(last_op)
        self.draw_workflow()
        self.write_workflow()


    # def run(self, last_op):
    #     if last_op.executed == True:
    #         return
    #     elif last_op.__class__.__name__ == 'Select':
    #         SelectLogic(last_op)
    #     elif last_op.__class__.__name__ == 'ProjectMetadata':
    #         if last_op.depends_on.executed == False:
    #             self.run(last_op.depends_on)
    #         ProjectMetadataLogic(last_op)
    #     elif last_op.__class__.__name__ == 'ProjectRegion':
    #         if last_op.depends_on.executed == False:
    #             self.run(last_op.depends_on)
    #         ProjectRegionLogic(last_op)
    #     elif last_op.__class__.__name__ == 'Cover':
    #         if last_op.depends_on.executed == False:
    #             self.run(last_op.depends_on)
    #         CoverLogic(last_op)
    #     elif last_op.__class__.__name__ == 'Join':
    #         if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
    #             self.run(last_op.depends_on_2)
    #         elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
    #             self.run(last_op.depends_on)
    #         else:
    #             self.run(last_op.depends_on)
    #             self.run(last_op.depends_on_2)
    #         JoinLogic(last_op)
    #     elif last_op.__class__.__name__ == 'Map':
    #         if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
    #             self.run(last_op.depends_on_2)
    #         elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
    #             self.run(last_op.depends_on)
    #         else:
    #             self.run(last_op.depends_on)
    #             self.run(last_op.depends_on_2)
    #         MapLogic(last_op)
    #     elif last_op.__class__.__name__ == 'Union':
    #         if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
    #             self.run(last_op.depends_on_2)
    #         elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
    #             self.run(last_op.depends_on)
    #         else:
    #             self.run(last_op.depends_on)
    #             self.run(last_op.depends_on_2)
    #         UnionLogic(last_op)
    #     elif last_op.__class__.__name__ == 'Difference':
    #         if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
    #             self.run(last_op.depends_on_2)
    #         elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
    #             self.run(last_op.depends_on)
    #         else:
    #             self.run(last_op.depends_on)
    #             self.run(last_op.depends_on_2)
    #         DifferenceLogic(last_op)
    #     elif last_op.__class__.__name__ == 'Pivot':
    #         if last_op.depends_on.executed == False:
    #             self.run(last_op.depends_on)
    #         PivotLogic(last_op)
    #     elif last_op.__class__.__name__ == 'JoinPivot':
    #         if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
    #             self.run(last_op.depends_on_2)
    #         elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
    #             self.run(last_op.depends_on)
    #         else:
    #             self.run(last_op.depends_on)
    #             self.run(last_op.depends_on_2)
    #         JoinPivotLogic(last_op)
    #     elif last_op.__class__.__name__ == 'ConcatenatePivot':
    #         if last_op.depends_on.executed == True and last_op.depends_on_2.executed == False:
    #             self.run(last_op.depends_on_2)
    #         elif last_op.depends_on.executed == False and last_op.depends_on_2.executed == True:
    #             self.run(last_op.depends_on)
    #         else:
    #             self.run(last_op.depends_on)
    #             self.run(last_op.depends_on_2)
    #         ConcatenatePivotLogic(last_op)



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

        plt.savefig('workflow1.png')
        #plt.show()


    def write_workflow(self):
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


