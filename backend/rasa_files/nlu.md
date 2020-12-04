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
- clustering of [grch38 tcga gene expression]{"entity": "dataset_name", "value": "grch38_tcga_gene_expression_2019_10"}
- evaluate the cluster analysis made on [breast](tissue) cancer data
- I want to do clustering on data of [copy number segment](data_type)
- cluster
- clustering

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
- cluster all the features for [bladder urothelial carcinoma](disease)



## synonym:breast
- mammary part of chest
- mammary region
## synonym:bronchus and lung
- lung/bronchus
## synonym:kidney
- renal
## synonym:brain
- fetal brain
## synonym:ovary
- ovum-producing ovary
- reproductive system of female organism gonad
- reproductive system of female organism gonada
## synonym:prostate gland
- prostatic
## synonym:corpus uteri
- uterine body
- uterine corpus
## synonym:skin
- skin region
- skin zone
- zone of skin
## synonym:colon
- colon crypt
- colonic
- gi colon
- large bowel
## synonym:liver and intrahepatic bile ducts
- organ system, hepatic
## synonym:bladder
- urinary bladder
## synonym:cervix uteri
- neck of uterus
- uterine cervix
## synonym:adrenal gland
- fetal adrenal gland
- glandula adrenalis
- glandula suprarenalis
## synonym:esophagus
- gi esophagus
- gullet
- oesophagus
## synonym:pancreas
- pancreatic
## synonym:testis
## synonym:other and unspecified parts of tongue
- other and unspecified parts of tongue icd-o-3
## synonym:connective, subcutaneous and other soft tissues
- soft tissue
## synonym:heart, mediastinum, and pleura
- pleura
- pleural tissue
## synonym:thymus
- thymus gland
- thymus organ
## synonym:hematopoietic and reticuloendothelial systems
- re system
- reticuloendothelial system
## synonym:eye and adnexa
- ocular
- optic
## synonym:rectum
- terminal portion of intestine
## synonym:blood
- portion of blood
- vertebrate blood
## synonym:rectosigmoid junction
## synonym:floor of mouth
- floor of oval cavity
- floor of the oval cavity
- mouth floor
## synonym:base of tongue
- pars posterior dorsi linguae
- pars posterior (dorsum linguae)
- pars posterior linguae
- pars postsulcalis (dorsum linguae)
- pharyngeal part of tongue
- pharyngeal portion of dorsum of tongue
- posterior part of dorsum of tongue
- posterior part of tongue
- postsulcal part of dorsum of tongue
## synonym:spleen
- splenic
## synonym:lung
- pulmo
- pulmonary
## synonym:gastrocnemius medialis
- medial head of gastrocnemius
- medial head of gastrocnemius muscle
## synonym:gum
- gums
- gum tissue
## synonym:muscle
- muscle structure
- musculus
## synonym:hypopharynx
- laryngeal pharynx
- laryngopharynx
## synonym:esophagus muscularis mucosa
- esophagus muscularis mucosae
- lamina muscularis mucosae (oesphagus)
- lamina muscularis of esophageal mucous membrane
- muscularis mucosae of esophagus
## synonym:body of pancreas
- pancreas body
- pancreatic body
## synonym:tibial nerve
## synonym:heart
- vertebrate heart
## synonym:esophagus squamous epithelium
- gastroesophageal sphincter
- gastroesophageal sphincter muscle
- inferior esophageal sphincter
## synonym:gastroesophageal sphincter
- gastroesophageal sphincter muscle
- inferior esophageal sphincter
## synonym:gi stomach
- stomach
## synonym:uterus
- uterus nos
- uterus, nos
## synonym:gi colon
- large bowel
## synonym:gi rectum
- rectal
- rectum
- terminal portion of intestine
## synonym:cervix
- cervix uteri
- neck of uterus
- uterine cervix
## synonym:gi esophagus
- gullet
- oesophagus
## synonym:adrenal
- adrenal gland
- fetal adrenal gland
- glandula adrenalis
- glandula suprarenalis
## synonym:eye
- eye and adnexa
- ocular
- optic
## synonym:thyroid
- thyroid gland
## synonym:cervical
- cervical canal of uterus
- cervix
- cervix uteri
- neck of uterus
- uterine cervix

## synonym:breast invasive carcinoma
- infiltrating breast cancer
- infiltrating breast carcinoma
- infiltrating carcinoma of breast
- infiltrating carcinoma of the breast
- invasive breast cancer
- invasive breast carcinoma
- invasive carcinoma of breast
- invasive carcinoma of the breast
- invasive mammary carcinoma
- brca
## synonym:kidney renal clear cell carcinoma
- kirc
## synonym:lung adenocarcinoma
- luad
## synonym:head and neck squamous cell carcinoma
- hnsc
- head and neck squamous cell carcinoma, nos
- scchn
- squamous cell carcinoma of head and neck
- squamous cell carcinoma of the head and neck
## synonym:ovarian serous cystadenocarcinoma
- ov
## synonym:lung squamous cell carcinoma
- lusc
- squamous cell carcinoma of lung
- squamous cell carcinoma of the lung
- squamous cell lung cancer
- squamous cell lung carcinoma
## synonym:thyroid carcinoma
- thca
- thyroid gland cancer
- thyroid gland carcinoma
## synonym:uterine corpus endometrial carcinoma
- ucec
## synonym:prostate adenocarcinoma
- prad
## synonym:brain lower grade glioma
- lower grade glioma
- lgg
## synonym:colon adenocarcinoma
- colonic adenocarcinoma
- coad
## synonym:skin cutaneous melanoma
- skcm
- skin melanoma
- skin, melanoma
## synonym:bladder urothelial carcinoma
- transitional cell carcinoma of the urinary bladder
- urinary bladder transitional cell carcinoma
- urinary bladder urothelial carcinoma
- urothelial carcinoma of the urinary bladder
- blca
## synonym:liver hepatocellular carcinoma
- lihc
- primary carcinoma of liver cells
- primary carcinoma of the liver cells
## synonym:stomach adenocarcinoma
- stad
## synonym:glioblastoma multiforme
- gbm
- grade iv astrocytic neoplasm
- grade iv astrocytic tumor
- grade iv astrocytoma
- malignant glioblastoma
- spongioblastoma multiforme
- who grade iv glioma
## synonym:kidney renal papillary cell carcinoma
- kirp
- papillary (chromophil) renal cell carcinoma
- papillary renal cell cancer
- papillary renal cell carcinoma
- prcc
## synonym:cervical squamous cell carcinoma and endocervical adenocarcinoma
- cesc
- cervix cancer
- cervix carcinoma
- cervix uteri carcinoma
- uterine cervix cancer
- uterine cervix carcinoma
## synonym:sarcoma
- sarc
- sarcoma, malignant
- sarcoma of soft tissue and bone
- sarcoma of the soft tissue and bone
## synonym:acute myeloid leukemia
- lalm
- acute myeloid leukemia (aml)
- acute nonlymphocytic leukemia
- aml
- aml - acute myeloid leukemia
- anll
- hematopoeitic - acute myleogenous leukemia (aml)
## synonym:esophageal carcinoma
- esophagus carcinoma
- esca
## synonym:pancreatic adenocarcinoma
- paad
## synonym:hepatocellular carcinoma
- hepatoma
- liver cell cancer (hepatocellular carcinoma)
- liver cell carcinoma
- liver hepatocellular carcinoma
- primary carcinoma of liver cells
- primary carcinoma of the liver cells
## synonym:testicular germ cell tumors
- tgct
## synonym:pheochromocytoma and paraganglioma
- pcpg
## synonym:rectum adenocarcinoma
- read
## synonym:thymoma
- thym
## synonym:adrenocortical carcinoma
- acc
- adrenocortical carcinoma, nos
- cancer of the adrenal cortex
- carcinoma, adrenocortical, malignant
- carcinoma of adrenal cortex
- carcinoma of the adrenal cortex
- cortical cell carcinoma
## synonym:mesothelioma
- meso
## synonym:uveal melanoma
- uvm
## synonym:kidney chromophobe
- renal cell carcinoma, chromophobe type
- kich
## synonym:breast cancer (adenocarcinoma)
- mammary adenocarcinoma
## synonym:uterine carcinosarcoma
- ucs
- uterine malignant mixed mesodermal (mullerian) tumor
- uterine malignant mixed mesodermal (müllerian) tumor
## synonym:lymphoid neoplasm diffuse large b-cell lymphoma
- dlbc
## synonym:cholangiocarcinoma
- chol
- cholangiocarcinoma, intrahepatic and extrahepatic bile ducts (adenocarcinoma)
- cholangiocarcinoma, malignant
- cholangiocar.- intra/extrahepatic
- cholangiocellular carcinoma
- cholangiosarcoma
- intrahepatic bile duct cancer (cholangiocarcinoma)
## synonym:cervical adenocarcinoma
- cervical adenocarcinoma, nos
- cervical adenocarcinoma, not otherwise specified
- cervix adenocarcinoma
- cervix uteri adenocarcinoma
- uterine cervix adenocarcinoma
## synonym:b cell lymphoma
- b-cell lymphoma
- b-cell non-hodgkin lymphoma
- b-cell non hodgkin's lymphoma
- b-cell non-hodgkin's lymphoma
- lymphomas non-hodgkin's b-cell
- non-hodgkin's b-cell lymphoma
- non-hodgkin's lymphoma b-cell
## synonym:colorectal carcinoma
- colorectal (colon or rectal) cancer
- crc
- large bowel cancer
- large bowel carcinoma
- large intestine cancer
- large intestine carcinoma
## synonym:immunoglobulin a lambda myeloma
- immunoglobulin lambda gene
- immunoglobulin lambda locus
- lambda light chain gene
## synonym:apparently healthy
- healthy
## synonym:endometrial adenocarcinoma
- immunoblastic lymphoma
- lymphoma, immunoblastic, malignant
- refractory immunoblastic b cell lymphoma progressed from follicular centroblastic/centrocytic lymphoma
## synonym:t-cell acute lymphoblastic leukemia cell line atcc crl-2629
- t-cell acute lymphocytic leukemia
- t-cell all
- t-cell type acute leukemia
## synonym:human b cell non-hodgkin's lymphoma
- large b-cell lymphoma
- large cell lymphoma
- large-cell lymphoma
- large cell lymphoma, diffuse
- large-cell lymphoma, diffuse
- large cell lymphoma; diffuse mixed histiocytic and lymphocytic lymphoma; follicular b cell lymphoma
- large-cell lymphomas
- large-cell lymphomas, diffuse
- large lymphoid lymphoma, diffuse
- large lymphoma
- large lymphoma diffuse
- lymphoma, diffuse histiocytic
- lymphoma diffuse large
- lymphoma, diffuse large cell
- lymphoma, diffuse large-cell
- lymphoma, histiocytic
- lymphoma, histiocytic, diffuse
- lymphoma large
- lymphoma, large b-cell, diffuse
- lymphoma, large cell
- lymphoma, large-cell
- lymphoma, large cell, diffuse
- lymphoma, large-cell, diffuse
- lymphoma large diffuse
- lymphoma, large lymphoid, diffuse
- lymphomas, diffuse histiocytic
- lymphomas, diffuse large-cell
- lymphomas, histiocytic
- lymphomas, large-cell
## synonym:t-acute lymphoblastic leukemia (t-all; type iii cortical)
- t-all
- t-cell acute lymphoblastic leukemia
- t-cell acute lymphoblastic leukemia cell line atcc crl-2629
- t-cell acute lymphocytic leukemia
- t-cell all
- t-cell type acute leukemia
## synonym:large cell lymphoma; diffuse mixed histiocytic and lymphocytic lymphoma; follicular b cell lymphoma
- large-cell lymphomas
- large-cell lymphomas, diffuse
- large lymphoid lymphoma, diffuse
- large lymphoma
- large lymphoma diffuse
- lymphoma, diffuse histiocytic
- lymphoma diffuse large
- lymphoma, diffuse large cell
- lymphoma, diffuse large-cell
- lymphoma, histiocytic
- lymphoma, histiocytic, diffuse
- lymphoma large
- lymphoma, large b-cell, diffuse
- lymphoma, large cell
- lymphoma, large-cell
- lymphoma, large cell, diffuse
- lymphoma, large-cell, diffuse
- lymphoma large diffuse
- lymphoma, large lymphoid, diffuse
- lymphomas, diffuse histiocytic
- lymphomas, diffuse large-cell
- lymphomas, histiocytic
- lymphomas, large-cell
## synonym:acute t cell leukemia
- acute t-cell leukemia
- acute t cell lymphoblastic leukemia
- acute t-cell lymphoblastic leukemia
- acute t cell lymphocytic leukemia
- acute t-cell lymphocytic leukemia
- precursor t-lymphoblastic leukemia
- precursor t-lymphoblastic leukemia (t-cell all)
- t acute lymphoblastic leukemia
- t-acute lymphoblastic leukemia (t-all; type iii cortical)
- t-all
- t-cell acute lymphoblastic leukemia
- t-cell acute lymphoblastic leukemia cell line atcc crl-2629
- t-cell acute lymphocytic leukemia
- t-cell all
- t-cell type acute leukemia
## synonym:hepatocellular adenocarcinoma
- hepatocellular cancer
- hepatocellular carcinoma
- hepatoma
- liver cell cancer (hepatocellular carcinoma)
- liver cell carcinoma
- liver hepatocellular carcinoma
- primary carcinoma of liver cells
- primary carcinoma of the liver cells
## synonym:malignant glioblastoma
- spongioblastoma multiforme
- who grade iv glioma
## synonym:pheochromocythoma and paraganglioma
- pheochromocytoma
- pheochromocytoma (adrenal)
- pheochromocytoma and paraganglioma


## synonym:k562
- k-562
-  k562 cell
- k-562 cell
## synonym:hepg2
- hep-g2
- hepg2 cell
## synonym:hek293
- human embryonic kidney cell
## synonym:mcf-7
- mcf-7 cell
- mcf7 cell
- mcf7-lted
## synonym:lymphoblastoid cell line
- ms4221
## synonym:a549
- a-549
- a549 cell
- bt-549
## synonym:h1
- h1-hesc
## synonym:hct116
- hct-116 cell
- hct116 cell
## synonym:mm.1s
- mm.1 s
- mm.1-s
- mm.1s cell
## synonym:gm23248
- gm23248 cell
## synonym:imr-90
- imr90 fetal lung fibroblast cell line
## synonym:pc-3
- pc-3 cell
- pc3 cell
## synonym:cardiac muscle cell
- cardiac muscle fiber
- cardiac myocyte
- cardiocyte
- cardiomyocyte
- heart muscle cell
## synonym:skeletal muscle myoblast
- skeletal myoblast
## synonym:ishikawa
- ishikawa cell
## synonym:b cell
- b-cell
- b lymphocyte
- b-lymphocyte
## synonym:oci-ly3
- oci-ly-3
- oci-ly-3 cell
## synonym:myotube
- myotubule
## synonym:smooth muscle cell
- smooth muscle fiber
- single cell sarcomere
- smcs
## synonym:panc1
- panc-1
## synonym:karpas-422
- karpas 422 cell
## synonym:oci-ly1
- oci-ly8
## synonym:h1 cells
- h1-hesc
## synonym:a549 etoh 0.02pct lung carcinoma cell line
- bt-549
## synonym:hsmm skeletal muscle myoblasts cells
- skeletal myoblast
## synonym:ecto neural progenitor cell
- mouse neural progenitor cell
- mouse npc

## synonym:gene expression quantification
- gene expression
- gene expression data
- gene expressions
- gene expression quantifications
- rna expression
- gene quantifications

## synonym:mirna expression quantification
- mirna expressions
- mirna quantifications
- mirna expression quantifications
- mirna expression
- mirna expression data

