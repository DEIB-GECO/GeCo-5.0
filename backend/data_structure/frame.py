from enum import Enum


class PivotIndexes(Enum):
    FEATURES = 0
    SAMPLES = 1

class Frame:
    def __init__(self):
        self.datasets = []
        self.row = None
        self.column = None

    def has_ds(self):
        if len(self.datasets)==0:
            return False
        else:
            return True

    def has_rows_col(self):
        if self.row==None and self.column==None:
            return False
        else:
            return True

    def add_ds(self,ds_list):
        self.datasets = ds_list

    def is_filled(self):
        # To add checks on every attribute of the frame
        if self.has_ds() and self.has_rows_col():
            return True
        elif not self.has_ds():
            from dialogue_manager import CheckDataset
            return [CheckDataset]
        else:
            from dialogue_manager import AskRowCol
            return [AskRowCol]

    def attributes(self):
        attributes = {}
        for i in self.__dict__:
            attributes[i] = getattr(self, i)
            if i=='row':
                attributes[i] = self.row.name
            if i=='column':
                attributes[i] = self.column.name
        return attributes

    def define_frame(self, intent):
        if intent == 'clustering_row_feature':
            self.row = PivotIndexes.FEATURES
            self.column = PivotIndexes.SAMPLES
        elif intent == 'clustering_row_sample':
            self.row = PivotIndexes.SAMPLES
            self.column = PivotIndexes.FEATURES

    def update_frame(self, entities):
        for e in entities.keys():
            if hasattr(self, e) and getattr(self, e)==None:
                setattr(self, e, entities[e])
            elif e=='dataset_name':
                self.add_ds(entities[e])
                print(self.datasets)
            if e=='row' and getattr(self, e)==None:
                if entities[e]=='features':
                    self.row = PivotIndexes.FEATURES
                    self.column = PivotIndexes.SAMPLES
                else:
                    self.row = PivotIndexes.SAMPLES
                    self.column = PivotIndexes.FEATURES
            if e=='column'and getattr(self, e)==None:
                if entities[e]=='features':
                    self.column = PivotIndexes.FEATURES
                    self.row = PivotIndexes.SAMPLES
                else:
                    self.column = PivotIndexes.SAMPLES
                    self.row = PivotIndexes.FEATURES