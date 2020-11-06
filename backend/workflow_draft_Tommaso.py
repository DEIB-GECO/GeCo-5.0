from workflow.workflow_class import Workflow
from data_structure.dataset import Dataset, Field
from workflow.gmql import Select, Cover, ProjectRegion, ProjectMetadata, Union, Join, Difference
from data_structure.operations import ArithmeticOperation

#Create the workflow
w = Workflow()
#Create the first dataset
ds_0 = Dataset({"source":["tcga"],"data_type":["gene quantification"],"disease":["breast invasive carcinoma"]}, 'Genes_DS')
#Add a select to the workflow
w.add(Select(ds_0))
#Add two projects to the workflow
operation = ArithmeticOperation.DIVISION.parameters(Field('age'), 365)
w.add(ProjectMetadata(w[-1], change_dict={'age_years': operation}))
operation = ArithmeticOperation.SUBTRACT.parameters(Field('start'), Field('stop'))
w.add(ProjectRegion(w[-1], change_dict={'length':operation}, keep_list=[Field('lenght'),Field('gene_symbol'),Field('rpkm')]))
#Create a second dataset
ds_1 = Dataset({"source":["tcga"],"assembly":["hg19"],"data_type":["cnv"],"disease":["breast invasive carcinoma"]},'CNV_DS')
#Add a select and a cover to the workflow
w.add(Select(ds_1))
w.add(Cover(w[-1],min=2, max='ANY'))
#Add a Union
w.add(Union(w[2], w[-1]))
#Run from the union
w.run(w[-1])
