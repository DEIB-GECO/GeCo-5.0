## lookup:source
./source.txt

## lookup:assembly
./assembly.txt

## lookup:content_type
./content_type_ann.txt

## lookup:project_name
./project_name.txt

## lookup:data_type
./data_type.txt

## lookup:is_healthy
./is_healthy.txt

## lookup:disease
./disease.txt

## lookup:cell
./cell.txt

## lookup:tissue
./tissue.txt

## lookup:target
./target.txt


## intent:affirm
 - yes
 - ok
 - i agree
 - top
 - yeah
 - yep
 - sure
 - ok thanks

## intent:deny
 - no
 - never
 - no way
 - not really
 - none
 - any

## intent:back
 - go back
 - back



## intent:clustering
- I want you to clusterize the data of [thymoma](disease)
- Can you do the clustering for [hg19_tcga_rnaseq_gene](dataset_name) data?
- clustering of [grch38_tcga_gene_expression_2019_10]{"entity": "dataset_name", "value": "grch38_tcga_gene_expression_2019_10"}
- evaluate the cluster analysis made on [breast](tissue) cancer data
- I want to do clustering on data of [copy number segment](data_type)

## intent:clustering_row_feature
- Please perform the clustering of the [fpkm](region_value) data for patients affected by [sarcoma](disease)
- Clusterize the [gene expression data]{"entity": "data_type", "value": "gene expression quantification"}
- Clusterize the [gene expression data]{"entity": "data_type", "value": "gene expression quantification"}
- cluster genes extracted from [tumoral patients]{"entity":"is_healthy", "value": False} using [grch38](assembly) 
- cluster genes of [kidney renal clear cell carcinoma](disease)
- i want the clustering of cell [imr90](cell)

## intent:clustering_row_feature_tuning
- Please perform the clustering of the [fpkm](region_value) data for patients affected by [sarcoma](disease) using parameter tuning
- With parameter tuning clusterize the [gene expression data]{"entity": "data_type", "value": "gene expression quantification"}
- Clusterize the [gene expression data]{"entity": "data_type", "value": "gene expression quantification"} with parameter tuning
- cluster genes extracted from [tumoral patients]{"entity":"is_healthy", "value": False} using [grch38](assembly) with tuning of the parameters
- cluster genes of [kidney renal clear cell carcinoma](disease) by tuning the number of clusters

## intent:clustering_row_sample
- cluster the patients according to their [cnv](data_type)
- cluster samples of [tcga](source) [kidney](tissue) data
- cluster samples retrieved from [a549](cell)
- cluster patients affected by [breast cancer]{"entity": "disease", "value": "breast cancer (adenocarcinoma)"}

## intent:clustering_row_sample_tuning
- cluster the patients according to their [cnv](data_type) with parameter tuning
- cluster patients affected by [breast cancer]{"entity": "disease", "value": "breast cancer (adenocarcinoma)"} using the tuning of the parameters
- using parameter tuning I want the clustering of [tumoral]{"entity": "is_healthy", "value": "False"} samples with [uveal melanoma](disease)


## intent:clustering_concatpivot_row_feature
- cluster genes and mirnas extracted from data of [grch38_tcga_gene_expression_2019_10](dataset_name) and [grch38_tcga_mirna_expression_2019_10](dataset_name)
- cluster [genes]{"entity": "data_type", "value": "gene expression quantification"} and [mirnas]{"entity": "data_type", "value": "mirna expression quantification"} extracted from [lung](tissue) tissue


## intent:clustering_joinpivot_row_feature
- cluster [genes]{"entity": "data_type", "value": "gene expression quantification"} extracted from data of [lung adenocarcinoma](disease) and [kidney renal clear cell carcinoma](disease)
- cluster 
