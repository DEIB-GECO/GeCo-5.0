from enum import Enum
from data_structure.dataset import DataSet
from workflow import *
import json

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False

class PivotIndexes(Enum):
    FEATURES = 0
    SAMPLES = 1


class Frame:
    def __init__(self):
        self.datasets = []
        self.row = None
        self.column = None
        self.tuning = None

    def has_ds(self):
        from dialogue_manager import CheckDataset, AskBinary
        if len(self.datasets)==0:
            return [CheckDataset]
        elif len(self.datasets)>1 and not hasattr(self, 'pivot_binary_operation') and not hasattr(self, 'gmql_binary_operation'):
            return [AskBinary]
        else:
            return True

    def has_rows_col(self):
        from dialogue_manager import AskRowCol
        if self.row==None and self.column==None:
            return [AskRowCol]
        else:
            return True

    def has_tuning(self):
        from dialogue_manager import AskTuning
        if self.tuning==None:
            return [AskTuning]
        else:
            return True

    def add_ds(self,ds_list):
        self.datasets = ds_list

    def is_filled(self):
        # To add checks on every attribute of the frame
        print(dir(self))
        methods = [a for a in dir(self) if (a.startswith('has_'))]
        print('methods', methods)
        next_call=True
        for a in methods:
            next_call = getattr(self, a)()
            if not next_call ==True:
                break
        if next_call == True:
            self.create_workflow()
        return next_call

    def attributes(self):
        attributes = {}
        for i in self.__dict__:
            if is_jsonable(getattr(self, i)):
                attributes[i] = getattr(self, i)
            else:
                print('i', i)
                if i == 'row':
                    attributes[i] = self.row.name
                elif i == 'column':
                    attributes[i] = self.column.name
                else:
                    attributes[i] = str(getattr(self, i).__name__)
                print(attributes[i])

        print('here', attributes)
        return attributes

    def define_frame(self, intent):
        from dialogue_manager import JoinPivot, ConcatPivot
        if intent == 'clustering_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
        elif intent == 'clustering_row_sample':
            self.row = PivotIndexes.SAMPLES
            self.column = PivotIndexes.FEATURES
        elif intent == 'clustering_row_feature_tuning':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.tuning = True
        elif intent == 'clustering_row_sample_tuning':
            self.row = PivotIndexes.SAMPLES
            self.column = PivotIndexes.FEATURES
            self.tuning = True
        elif intent == 'clustering_concatpivot_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.pivot_binary_operation = ConcatPivot
        elif intent == 'clustering_joinpivot_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.pivot_binary_operation = JoinPivot

    def update_frame(self, entities):
        for e in entities.keys():
            if hasattr(self, e) and getattr(self, e)==None:
                setattr(self, e, entities[e])
            elif e=='dataset_name':
                self.add_ds(entities[e])
                print(self.datasets)

    def create_workflow(self):
        list_select = []
        for i in self.datasets:
            list_select.append(Select(i))
        list_pivot = []
        if hasattr(self, 'gmql_binary_operation'):
            binary = self.gmql_binary_operation(list_select[0], list_select[1])
            if self.row == PivotIndexes.SAMPLES:
                list_pivot.append(Pivot(i, metadata_row='biospecimen__bio__bcr_sample_barcode', region_column='gene_symbol',
                          region_value=self.region_value))
            else:
                list_pivot.append(Pivot(i, metadata_column='biospecimen__bio__bcr_sample_barcode', region_row='gene_symbol',
                          region_value=self.region_value))

        elif hasattr(self, 'pivot_binary_operation'):
            for i in list_select:
                if self.row==PivotIndexes.SAMPLES:
                    list_pivot.append(Pivot(i,metadata_row='biospecimen__bio__bcr_sample_barcode', region_column='gene_symbol', region_value=self.region_value))
                else:
                    list_pivot.append(
                        Pivot(i,metadata_column='biospecimen__bio__bcr_sample_barcode', region_row='gene_symbol',
                              region_value=self.region_value))
        else:
            if self.row == PivotIndexes.SAMPLES:
                list_pivot.append(Pivot(i, metadata_row='biospecimen__bio__bcr_sample_barcode', region_column='gene_symbol',
                          region_value=self.region_value))
            else:
                list_pivot.append(Pivot(i, metadata_column='biospecimen__bio__bcr_sample_barcode', region_row='gene_symbol',
                          region_value=self.region_value))

        if self.tuning:
            Clustering(list_pivot[0],self.tuning)
        else:
            Clustering(list_pivot[0],self.clust_num)
