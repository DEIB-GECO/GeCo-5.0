import pandas as pd
from tqdm import tqdm
class PivotLogic:
    def __init__(self, op):
        self.op = op
        self.ds = self.op.depends_on.result
        self.run()


    def run(self):
        if self.op.meta_col != None and self.op.meta_row != None:
            temp_meta = pd.DataFrame(index=list(self.ds.meta['item_id']).sort(), columns=self.op.meta_col)
            self.ds.meta.index = self.ds.meta['item_id']
            self.ds.meta = self.ds.meta.drop('item_id', axis=1)
            self.ds.meta = self.ds.meta.sort_index()
            for i in self.op.meta_col:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
            for i in self.op.meta_row:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
            print(temp_meta)
        elif self.op.meta_col != None:
            temp_meta = pd.DataFrame(index=list(self.ds.meta['item_id']).sort(), columns=self.op.meta_col)
            for i in self.op.meta_col:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
        else:
            temp_meta = pd.DataFrame(index=list(self.ds.meta['item_id']).sort(), columns=self.op.meta_row)
            for i in self.op.meta_row:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']

        temp_reg = self.ds.region.merge(temp_meta, left_on='item_id', right_index=True)
        print(temp_reg)

        if self.op.region_col!=None and self.op.meta_col!=None:
            col = self.op.region_col.append(self.op.meta_col)
        elif self.op.region_col!=None:
            col = self.op.region_col
        else:
            col = self.op.meta_col
        if self.op.region_row!=None and self.op.meta_row!=None:
            row = self.op.region_row.append(self.op.meta_row)
        elif self.op.region_row!=None:
            row = self.op.region_row
        else:
            row = self.op.meta_row

        pivot = temp_reg.pivot_table(index=row, columns=col,  values=self.op.value)
        self.op.result = pivot
        self.op.executed = True
        print(pivot)
        item_id = list(self.ds.meta['item_id'].values).intersection(list(self.ds.region['item_id'].values))


