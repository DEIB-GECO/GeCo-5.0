import pandas as pd


class JoinPivotLogic:
    def __init__(self, op, sid):
        self.op = op
        self.table_1 = self.op.depends_on.result.ds
        self.dict_1 = self.op.depends_on.result.dict_for_join
        self.table_2 = self.op.depends_on_2.result.ds
        self.dict_2 = self.op.depends_on_2.result.dict_for_join
        self.run(sid)

    def run(self,sid):
        self.df1 = pd.DataFrame.from_dict(self.dict_1).T
        self.df2 = pd.DataFrame.from_dict(self.dict_2).T
        if self.table_1.index.name=='item_id' and self.table_2.index.name=='item_id':
            self.table_1 = self.table_1.merge(self.df1, left_index=True, right_index=True)
            self.table_1 = self.table_1.drop('disease', axis=1)
            self.table_2 = self.table_2.merge(self.df2, left_index=True, right_index=True)
            self.table_2 = self.table_2.drop('disease', axis=1)
            res = self.table_1.merge(self.table_2, left_on=['donor', 'is_healthy'],
                                     right_on=['donor', 'is_healthy']).set_index(['donor', 'is_healthy'])
            # res = res.drop('disease', axis=1)
        else:
            self.table_1 = self.table_1.T.merge(self.df1, left_index=True, right_index=True)
            self.table_1 = self.table_1.drop('disease', axis=1)
            self.table_2 = self.table_2.T.merge(self.df2, left_index=True, right_index=True)
            self.table_2 = self.table_2.drop('disease', axis=1)
            res = self.table_1.merge(self.table_2, left_on=['donor', 'is_healthy'],
                                     right_on=['donor', 'is_healthy']).set_index(['donor', 'is_healthy']).T
            # res = res.drop('disease',axis=0)

        # if self.op.joinby!=None:
        #    res = self.table_1.join(self.table_2, on=self.op.joinby.name)
        # else:
        # res = self.table_1.join(self.table_2)

        self.op.executed = True
        self.op.result = res
