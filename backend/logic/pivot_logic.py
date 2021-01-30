import pandas as pd
from tqdm import tqdm
class PivotRes:
    def __init__(self, pivot, labels):
        self.ds = pivot
        self.labels = labels

class PivotLogic:
    def __init__(self, op):
        self.op = op
        self.ds = self.op.depends_on.result
        self.run()


    def run(self):
        # if (self.op.meta_col != None) and (self.op.meta_row != None):
        #     temp_meta = pd.DataFrame(index=list(self.ds.meta['item_id']).sort(), columns=self.op.meta_col)
        #     self.ds.meta.index = self.ds.meta['item_id']
        #     self.ds.meta = self.ds.meta.drop('item_id', axis=1)
        #     self.ds.meta = self.ds.meta.sort_index()
        #     for i in self.op.meta_col:
        #         temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
        #     for i in self.op.meta_row:
        #         temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']

        if self.op.meta_col != None:
            items = list(self.ds.meta['item_id'])
            items.sort()
            temp_meta = pd.DataFrame(index=items, columns=self.op.meta_col)
            for i in self.op.meta_col:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
        else:
            items = list(self.ds.meta['item_id'])
            items.sort()
            temp_meta = pd.DataFrame(items, columns=self.op.meta_row)
            for i in self.op.meta_row:
                temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']

        temp_reg = self.ds.region.merge(temp_meta, left_on='item_id', right_index=True)
        items_reg = pd.DataFrame(index=list(set(temp_reg['item_id'])))

        #if (self.op.region_col!=None) and (self.op.meta_col!=None):
        #    col = self.op.region_col.append(self.op.meta_col)
        if self.op.region_col!=None:
            col = self.op.region_col
        else:
            col = self.op.meta_col
        if (self.op.region_row!=None) and (self.op.meta_row!=None):
            row = self.op.region_row.append(self.op.meta_row)
        elif self.op.region_row!=None:
            row = self.op.region_row
        else:
            row = self.op.meta_row

        pivot = temp_reg.pivot_table(index=row, columns=col, values=self.op.value)
        pivot.columns = pivot.columns.droplevel(0)

        if self.op.other_meta!=None:
            items = list(set(self.ds.meta['item_id']))
            #items = list(temp_reg['item_id'])

            items.sort()
            #print(items)
            labels_meta = pd.DataFrame(items, columns=self.op.other_meta)

            labels_meta.index= items

            for i in self.op.other_meta:
                labels_meta[i] = self.ds.meta.loc[self.ds.meta['key'] == i]['value']

            #print('temp_reg',list(temp_reg['item_id']))

            temp_labels_meta = pd.merge(labels_meta,items_reg, right_index=True, left_index=True)


        if self.op.other_region!=None:
            labels_reg = temp_reg[self.op.other_region]

        if (self.op.meta_col != None):
            if self.op.other_meta!=None:
                pivot = pivot.T
                for i in self.op.other_meta:
                    pivot[i]= list(temp_labels_meta[i])

                pivot = pivot.T

            elif self.op.other_region!=None:
                for i in self.op.other_region:
                    pivot[i] = list(labels_reg[i])
        else:
            if self.op.other_meta!=None:
                for i in self.op.other_meta:
                    pivot[i] = list(temp_labels_meta[i])
            elif self.op.other_region!=None:
                pivot = pivot.T
                for i in self.op.other_region:
                    pivot[i] = list(labels_reg[i])
                pivot = pivot.T
        #pivot.index= pivot.index.droplevel(0)
        print('pivot!')
        print(pivot.head())
        pivot.to_csv('pivot.csv')
        self.op.result = pivot
        self.op.executed = True
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

        with open('python_script.py', 'a') as f:
            f.write('import pandas as pd\n'+
                    'table = pd.read_csv("pivot.csv")')
        f.close()