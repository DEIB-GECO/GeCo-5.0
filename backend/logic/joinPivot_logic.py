import pandas as pd

class JoinPivotLogic:
    def __init__(self, op):
        self.op = op
        self.table_1 = self.op.depends_on.result.ds
        self.dict_1 = self.op.depends_on.result.dict_for_join
        self.table_2 = self.op.depends_on_2.result.ds
        self.dict_2 = self.op.depends_on_2.result.dict_for_join
        self.run()

    def run(self):
        print(self.table_1.head())
        print(self.table_2.head())
        self.df1 = pd.DataFrame().from_dict(self.dict_1).T
        self.df2 = pd.DataFrame().from_dict(self.dict_2).T
        print('df')
        print('df1 col' , self.df1.columns)
        print('df2 col', self.df2.columns)
        print('df1 ind', self.df1.index)
        print('df2 ind', self.df2.index)
        if any(i in list(self.table_1.index) for i in list(self.table_2.index)):
            print('index')
            self.table_1= self.table_1.merge(self.df1, left_index=True, right_index=True)
            print(self.table_1.head())
            self.table_2= self.table_2.merge(self.df2, left_index=True, right_index=True)
            print(self.table_2.head())
            res = self.table_1.merge(self.table_2, left_on=['donor','is_healthy'],right_on=['donor','is_healthy'])
        else:
            print('col')
            self.table_1 = self.table_1.T.merge(self.df1, left_index=True, right_index=True)
            print('tb1 col', self.table_1.columns)
            print('tb1 ind', self.table_1.index)
            print('tb1 info', self.table_1.info())
            self.table_2 = self.table_2.T.merge(self.df2, left_index=True, right_index=True)
            print('tb2 col', self.table_2.columns)
            print('tb2 ind', self.table_2.index)
            print('tb2 info', self.table_1.info())
            res = self.table_1.merge(self.table_2, left_on='donor', right_on='donor').T

        print(res.head())
        #if self.op.joinby!=None:
        #    res = self.table_1.join(self.table_2, on=self.op.joinby.name)
        #else:
        #res = self.table_1.join(self.table_2)
        aa
        self.op.executed = True
        self.op.result = res