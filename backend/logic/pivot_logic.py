import pandas as pd
from tqdm import tqdm
import numpy as np
import time
from sqlalchemy import create_engine
import pandas as pd
import time

def get_db_uri():
    postgres_url = "localhost"
    postgres_user = "geco_ro"
    postgres_pw = "geco78"
    postgres_db = "gmql_meta_new16_geco_agent"
    return 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=postgres_user,
                                                                 pw=postgres_pw,
                                                                 url=postgres_url,
                                                                 db=postgres_db)

#db = SQLAlchemy()
db_string = get_db_uri()
db = create_engine(db_string)

class PivotRes:
    def __init__(self, name, pivot, labels, dict_for_join):
        self.ds_name = name
        self.ds = pivot
        self.labels = labels
        self.dict_for_join = dict_for_join

class PivotLogic:
    def __init__(self, op, sid):
        self.op = op
        self.ds = self.op.depends_on.result
        self.run(sid)


    def run(self,sid):
        print('inizio pivot')
        self.run_select()
        # if self.op.meta_col != None:
        #     items = list(self.ds.meta['item_id'])
        #     items.sort()
        #     temp_meta = pd.DataFrame(index=items, columns=self.op.meta_col)
        #     for i in self.op.meta_col:
        #         if i!='item_id':
        #             temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
        # else:
        #     items = list(self.ds.meta['item_id'])
        #     items.sort()
        #     temp_meta = pd.DataFrame(index=items, columns=self.op.meta_row)
        #     for i in self.op.meta_row:
        #         if i != 'item_id':
        #             temp_meta[i] = self.ds.meta[self.ds.meta['key'] == i]['value']
        #items = list(self.ds.meta['item_id'])
        #items.sort()
        #temp_meta = pd.DataFrame(index=items)
        #print('temp meta done')
        #print('TEMP META')
        #print(temp_meta.head())
        #temp_reg = self.ds.region.merge(temp_meta, left_on='item_id', right_index=True)
        temp_reg = self.ds.region
        #items_reg = pd.DataFrame(index=list(set(temp_reg['item_id'])))
        #if (self.op.region_col!=None) and (self.op.meta_col!=None):
        #    col = self.op.region_col.append(self.op.meta_col)
        if self.op.region_col!=None:
            col = self.op.region_col
        else:
            #donors = [d for i,d in self.ds.dict_for_join.items()]

            col = self.op.meta_col
        if (self.op.region_row!=None) and (self.op.meta_row!=None):
            row = self.op.region_row.append(self.op.meta_row)
        elif self.op.region_row!=None:
            row = self.op.region_row
        else:
            row = self.op.meta_row
        df = pd.DataFrame().from_dict(self.ds.dict_for_join).T
        print('col', col)
        print('row', row)
        print('prima pivot')
        pivot = temp_reg.pivot_table(index=row, columns=col, values=self.op.value)
        pivot.columns = pivot.columns.droplevel(0)
        pivot.sort_index()
        print('dopo pivot')
        print(pivot.head())

        if self.op.other_region!=None:
            labels_reg = temp_reg[self.op.other_region]
        labels = []
        if (self.op.meta_col != None):
            if self.op.other_meta!=None:
                pivot = pivot.T
                for i in self.op.other_meta:
                    labels.append(i)
                    pivot[i]= ""
                    temp = self.ds.meta[self.ds.meta['key'] == i]
                    for x in pivot.index:
                        pivot.at[x,i]=temp[self.ds.meta['item_id']==x]['value'].values[0]
                pivot = pivot.T
            elif self.op.other_region!=None:
                for i in self.op.other_region:
                    labels.append(i)
                    pivot[i] = list(labels_reg[i])
        else:
            if self.op.other_meta!=None:
                for i in self.op.other_meta:
                    labels.append(i)
                    temp = self.ds.meta[self.ds.meta['key'] == i]
                    for x in pivot.index:
                        pivot.at[x, i] = temp[self.ds.meta['item_id'] == x][
                            'value'].values[0]
            elif self.op.other_region!=None:
                pivot = pivot.T
                for i in self.op.other_region:
                    labels.append(i)
                    pivot[i] = list(labels_reg[i])
                pivot = pivot.T
        #pivot.index= pivot.index.droplevel(0)
        print('pivot!')
        print(pivot.head())
        pivot.to_csv(f'{self.ds.name}.csv')
        self.op.result = PivotRes(self.ds.name, pivot, labels, self.ds.dict_for_join)
        self.op.executed = True
        self.write(sid)


    def write(self,sid):
        with open(f'jupyter_notebook_{sid}.ipynb', 'a') as f:
            f.write('{ "cell_type": "code",'+
                    '"execution_count": 0,'+
                    '"metadata": {},'+
                    '"outputs": [],'+
                    '"source": ['+
                    'import pandas as pd\n'+
                    f'{self.ds.name} = pd.read_csv("{self.ds.name}.csv")\n'+
                    ']},')
        f.close()

        with open(f'python_script_{sid}.py', 'a') as f:
            f.write('import pandas as pd\n'+
                    f'{self.ds.name} = pd.read_csv("{self.ds.name}.csv")\n')
        f.close()


    def query_field(self):
        filter = ' and '.join(['{} in ({})'.format(k, ",".join(['\'{}\''.format(x) for x in v])) for (k, v) in
                                 self.op.depends_on.fields.items()if k!='metadata'])
        if self.ds.items!=[]:
            items = ','.join(str(i) for i in self.ds.items)
            if 'metadata' in self.op.depends_on.fields and self.op.depends_on.fields['metadata'] != None:
                keys = ','.join([f'\'{str(i)}\'' for i in list(self.op.depends_on.fields['metadata'].keys())])
                values = ','.join([f'\'{str(i)}\'' for k, v in self.op.depends_on.fields['metadata'].items() for i in v])
                query = "join dw.flatten_gecoagent as df on rr.item_id = df.item_id join dw.unified_pair_gecoagent as du on rr.item_id = du.item_id " \
                        "where df.item_id in ({}) and du.key in ({}) and du.value in ({})".format(items, keys, values)
            else:
                query = "join dw.flatten_gecoagent as df on rr.item_id = df.item_id " \
                        "where df.item_id in ({})".format(items)
        else:
            if 'metadata' in self.op.depends_on.fields and self.op.depends_on.fields['metadata'] != None:
                keys = ','.join([f'\'{str(i)}\'' for i in list(self.op.depends_on.fields['metadata'].keys())])
                values = ','.join([f'\'{str(i)}\'' for k, v in self.op.depends_on.fields['metadata'].items() for i in v])
                query = "join dw.flatten_gecoagent as df on rr.item_id = df.item_id join dw.unified_pair_gecoagent as du on rr.item_id = du.item_id " \
                        "where {} and du.key in ({}) and du.value in ({})".format(filter, keys, values)
            else:
                query = "join dw.flatten_gecoagent as df on rr.item_id = df.item_id " \
                        "where {}".format(filter)
        #print(query)
        #query = "select distinct(item_id) from dw.flatten_gecoagent where {} group by item_id".format(filter)
        return query


    def run_select(self):
        pre = time.time()
        regions = list(set((self.op.region_row or []) + (self.op.region_col or []) + (self.op.other_region or []) + list(self.op.value)))
        regions = ','.join(str(i) for i in regions)
        items = ','.join(str(i) for i in self.ds.items)
        #query = self.query_field()
        query =  f"select item_id, {regions}  from rr.{self.ds.fields['dataset_name'][0]} as rr where item_id in ({items})"
        print(query)
        reg = pd.read_sql(query, db.engine)
        print(reg.head())
        print('time-first select df:', time.time() - pre)
        #print(reg.head())

        self.ds.add_region_table(reg)
        #self.ds.add_region_schema(list(res.keys()))
        self.ds.add_region_schema(list(reg.columns))
        print('time-add schema:', time.time() - pre)
        if hasattr(self.ds.fields, 'metadata'):
             query2 = self.query_key()
             res = db.engine.execute(
                 "select rr.* from dw.unified_pair_gecoagent as rr {} where ({})".format(
                     query, query2))
        else:
             query_meta =  "select * from dw.unified_pair_gecoagent where item_id in ({})".format(items)
             print(query_meta)
             res = db.engine.execute(query_meta)

        print('time-second select:', time.time() - pre)
        values = res.fetchall()
        print('time-second fetchall:', time.time() - pre)
        meta = pd.DataFrame(values, columns=res.keys())
        print('time-second df:', time.time() - pre)
        del values

        self.ds.add_meta_table(meta)
        print('time-second add schema:', time.time() - pre)
        print('fine select')

