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
    def __init__(self, context):
        self.context = context
        self.datasets = []
        self.row = None
        self.column = None
        self.region_value = None
        self.tuning = None

    def has_ds(self):
        from dialogue_manager import CheckDataset, AskBinary
        if len(self.datasets)==0:
            return [CheckDataset]
        elif len(self.datasets)==2 and not hasattr(self, 'pivot_binary_operation') and not hasattr(self, 'gmql_binary_operation'):
            return [AskBinary]
        else:
            return True

    def has_binary(self):
        from dialogue_manager import CheckDataset, AskBinary
        if len(self.datasets) == 2 and hasattr(self, 'pivot_binary_operation'):
            setattr(self.pivot_binary_operation, 'ds1', self.datasets[0])
            setattr(self.pivot_binary_operation, 'ds2', self.datasets[1])
        elif len(self.datasets)==2 and hasattr(self, 'gmql_binary_operation'):
            setattr(self.gmql_binary_operation.ds1, 'ds1', self.datasets[0])
            setattr(self.gmql_binary_operation.ds2, 'ds2', self.datasets[1])
        elif len(self.datasets)<2:
            return True

    def has_rows_col(self):
        from dialogue_manager import AskRowCol
        if self.row==None and self.column==None:
            return [AskRowCol]
        else:
            return True

    def has_region_value(self):
        from dialogue_manager import AskRegionValue
        if self.region_value == None:
            return [AskRegionValue]
        else:
            return True

    def has_tuning(self):
        from dialogue_manager import AskTuning
        if self.tuning==None:
            return [AskTuning]
        else:
            if self.tuning == True:
                return True
            elif self.tuning == False:
                from dialogue_manager import AskParametersClustering
                if hasattr(self,'parameters') and self.data_analysis_operation == Clustering:
                    if self.parameters==None:
                        return [AskParametersClustering]
                elif hasattr(self,'num_clusters') and self.data_analysis_operation == Clustering:
                    if self.num_clusters!=None:
                        return True
                    else:
                        return [AskParametersClustering]
            else:
                return True

    def has_par_binary_action(self):
        if hasattr(self, 'gmql_binary_operation'):
            from dialogue_manager import UnionAction, JoinAction, MapAction
            if not isinstance(self.gmql_binary_operation, UnionAction):
                return [self.gmql_binary_operation]
        return True

    def add_ds(self,ds_list):
        self.datasets = ds_list

    def is_filled(self):
        # To add checks on every attribute of the frame
        methods = [a for a in dir(self) if (a.startswith('has_'))]
        next_call= True
        for a in methods:
            next_call = getattr(self, a)()
            if not next_call == True:
                break
        return next_call

    def attributes(self):
        attributes = {}
        for i in self.__dict__:
            if is_jsonable(getattr(self, i)):
                attributes[i] = getattr(self, i)
            else:
                if i == 'row':
                    attributes[i] = self.row.name
                elif i == 'column':
                    attributes[i] = self.column.name
                #else:
               #     attributes[i] = str(getattr(self, i).__name__)

        return attributes

    def define_frame(self, intent):
        from dialogue_manager import JoinPivotAction, ConcatPivotAction
        if intent == 'clustering_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.data_analysis_operation = Clustering
        elif intent == 'clustering_row_sample':
            self.row = PivotIndexes.SAMPLES
            self.column = PivotIndexes.FEATURES
            self.data_analysis_operation = Clustering
        elif intent == 'clustering_row_feature_tuning':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.tuning = True
            self.data_analysis_operation = Clustering
        elif intent == 'clustering_row_sample_tuning':
            self.row = PivotIndexes.SAMPLES
            self.column = PivotIndexes.FEATURES
            self.tuning = True
            self.data_analysis_operation = Clustering
        elif intent == 'clustering_concatpivot_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.pivot_binary_operation = ConcatPivotAction
            self.data_analysis_operation = Clustering
        elif intent == 'clustering_joinpivot_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
            self.pivot_binary_operation = JoinPivotAction
            self.data_analysis_operation = Clustering

    def update_frame(self, entities, gcm_filter):
        for e in entities.keys():
            if hasattr(self, e) and getattr(self, e)==None:
                setattr(self, e, entities[e])
            elif e=='dataset_name':
                ds_name = entities[e][0]
                regions = self.context.payload.database.retrieve_region(ds_name)
                self.add_ds([DataSet(gcm_filter,ds_name, regions)])

    def create_workflow(self):
        workflow = Workflow()
        list_select = []
        for i in self.datasets:
            list_select.append(Select(i))
        workflow.extend(list_select)
        list_pivot = []
        if hasattr(self, 'gmql_binary_operation'):
            from dialogue_manager import UnionAction, JoinAction, MapAction
            if isinstance(self.gmql_binary_operation, UnionAction):
                binary = Union(list_select[0], list_select[1])
                workflow.append(binary)
            elif isinstance(self.gmql_binary_operation, JoinAction):
                binary = Join(list_select[0], list_select[1], self.gmql_binary_operation.joinby)
                workflow.append(binary)
            elif isinstance(self.gmql_binary_operation, MapAction):
                binary = Map(list_select[0], list_select[1], self.gmql_binary_operation.joinby, self.gmql_binary_operation.aggregate,  self.gmql_binary_operation.name_agg)
                workflow.append(binary)
            if self.row == PivotIndexes.SAMPLES:
                list_pivot.append(Pivot(i, metadata_row='biospecimen__bio__bcr_sample_barcode', region_column='gene_symbol',
                          region_value=self.region_value))

            else:
                list_pivot.append(Pivot(i, metadata_column='biospecimen__bio__bcr_sample_barcode', region_row='gene_symbol',
                          region_value=self.region_value))

            workflow.extend(list_pivot)

        elif hasattr(self, 'pivot_binary_operation'):
            for i in list_select:
                if self.row==PivotIndexes.SAMPLES:
                    list_pivot.append(Pivot(i,metadata_row='biospecimen__bio__bcr_sample_barcode', region_column='gene_symbol', region_value=self.region_value))
                else:
                    list_pivot.append(
                        Pivot(i,metadata_column='biospecimen__bio__bcr_sample_barcode', region_row='gene_symbol',
                              region_value=self.region_value))
            binary = self.pivot_binary_operation(list_pivot[0], list_pivot[1])
            workflow.extend(list_pivot)
            workflow.append(binary)
        else:
            if self.row == PivotIndexes.SAMPLES:
                list_pivot.append(Pivot(i, metadata_row='biospecimen__bio__bcr_sample_barcode', region_column='gene_symbol',
                          region_value=self.region_value))
            else:
                list_pivot.append(Pivot(i, metadata_column='biospecimen__bio__bcr_sample_barcode', region_row='gene_symbol',
                          region_value=self.region_value))
            workflow.extend(list_pivot)
        #if self.tuning:
         #   workflow.append(Clustering(list_pivot[0],self.tuning))

        #else:
         #   workflow.append(
          #      Clustering(list_pivot[0],self.clust_num))

        return workflow
