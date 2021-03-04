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
        if any(i in list(self.table_1.index) for i in list(self.table_2.index)):
            self.table_1= self.table_1.merge(self.df1, left_index=True, right_index=True)
            print(self.table_1.head())
            self.table_2= self.table_2.merge(self.df2, left_index=True, right_index=True)
            print(self.table_2.head())
            res = self.table_1.merge(self.table_2, left_on=['donor','is_healthy'],right_on=['donors','is_healthy'])
        else:
            self.table_1 = self.table_1.T.merge(self.df1.T, left_index=True, right_index=True)
            print(self.table_1.head())
            self.table_2 = self.table_2.T.merge(self.df2.t, left_index=True, right_index=True)
            print(self.table_2.head())
            res = self.table_1.merge(self.table_2, left_on=['donor', 'is_healthy'], right_on=['donors', 'is_healthy']).T

        print(res.head())
        #if self.op.joinby!=None:
        #    res = self.table_1.join(self.table_2, on=self.op.joinby.name)
        #else:
        #res = self.table_1.join(self.table_2)
        self.op.executed = True
        self.op.result = res