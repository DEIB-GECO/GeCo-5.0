class DataSet:
    def __init__(self, fields, name, region_schema=None, meta_schema = None):
        self.fields = fields
        self.name = name
        self.region_schema = region_schema
        self.meta_schema = meta_schema

    def add_meta_schema(self, schema):
        self.meta_schema = schema

    def add_region_schema(self, schema):
        self.region_schema = schema

    def add_region_table(self, df):
        self.region = df