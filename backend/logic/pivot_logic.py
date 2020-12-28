import pandas as pd
from tqdm import tqdm
class PivotLogic:
    def __init__(self, op):
        self.op = op
        self.ds = self.op.depends_on.result
        self.run()


    def run(self):
        print('meta')
        print(self.ds.meta)
        print('region')
        print(self.ds.region)
        if (self.op.meta_col != None) and (self.op.meta_row != None):
            temp_meta = pd.DataFrame(index=list(self.ds.meta['item_id']).sort(), columns=self.op.meta_col)
            self.ds.meta.index = self.ds.meta['item_id']
            self.ds.meta = self.ds.meta.drop('item_id', axis=1)
            self.ds.meta = self.ds.meta.sort_index()
            for i in self.op.meta_col:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
            for i in self.op.meta_row:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']

        elif self.op.meta_col != None:
            items = list(self.ds.meta['item_id'])
            items.sort()
            temp_meta = pd.DataFrame(index=items, columns=self.op.meta_col)
            for i in self.op.meta_col:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
            print('TEMP META 1')
            print(temp_meta)
        else:
            items = list(self.ds.meta['item_id'])
            items.sort()
            temp_meta = pd.DataFrame(items, columns=self.op.meta_row)
            for i in self.op.meta_row:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
            print('TEMP META 2')
            print(temp_meta)

        temp_reg = self.ds.region.merge(temp_meta, left_on='item_id', right_index=True)
        print('TEMP REG')
        print(temp_reg)

        if (self.op.region_col!=None) and (self.op.meta_col!=None):
            col = self.op.region_col.append(self.op.meta_col)
        elif self.op.region_col!=None:
            col = self.op.region_col
        else:
            col = self.op.meta_col
        if (self.op.region_row!=None) and (self.op.meta_row!=None):
            row = self.op.region_row.append(self.op.meta_row)
        elif self.op.region_row!=None:
            row = self.op.region_row
        else:
            row = self.op.meta_row

        print('row',row)
        print('col',col)
        pivot = temp_reg.pivot_table(index=row, columns=col,  values=self.op.value)
        print('pivot')
        print(pivot)
        pivot.to_csv('pivot.csv')
        self.op.result = pivot
        self.op.executed = True
        print(pivot)
        self.write()


    def write(self):
        with open('jupyter_notebook.ipynb', 'a') as f:
            f.write('{ "cell_type": "code",'+
                    '"execution_count": 0,'+
                    '"metadata": {},'+
                    '"outputs": [],'+
                    '"source": ['+
                    'import pandas as pd\n'+
                    'table = pd.read_csv("pivot.csv")'+
                    ']},')
        f.close()