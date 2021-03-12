const choices: AvailableChoice[] = [
  { name: 'breast invasive carcinoma', value: 'breast invasive carcinoma' },
  {
    name: 'kidney renal clear cell carcinoma',
    value: 'kidney renal clear cell carcinoma'
  },
  { name: 'lung adenocarcinoma', value: 'lung adenocarcinoma' },
  {
    name: 'head and neck squamous cell carcinoma',
    value: 'head and neck squamous cell carcinoma'
  },
  {
    name: 'ovarian serous cystadenocarcinoma',
    value: 'ovarian serous cystadenocarcinoma'
  },
  {
    name: 'lung squamous cell carcinoma',
    value: 'lung squamous cell carcinoma'
  },
  { name: 'thyroid carcinoma', value: 'thyroid carcinoma' },
  {
    name: 'uterine corpus endometrial carcinoma',
    value: 'uterine corpus endometrial carcinoma'
  },
  { name: 'prostate adenocarcinoma', value: 'prostate adenocarcinoma' },
  { name: 'brain lower grade glioma', value: 'brain lower grade glioma' },
  { name: 'colon adenocarcinoma', value: 'colon adenocarcinoma' },
  { name: 'skin cutaneous melanoma', value: 'skin cutaneous melanoma' },
  {
    name: 'bladder urothelial carcinoma',
    value: 'bladder urothelial carcinoma'
  },
  {
    name: 'liver hepatocellular carcinoma',
    value: 'liver hepatocellular carcinoma'
  },
  { name: 'stomach adenocarcinoma', value: 'stomach adenocarcinoma' },
  { name: 'glioblastoma multiforme', value: 'glioblastoma multiforme' },
  {
    name: 'kidney renal papillary cell carcinoma',
    value: 'kidney renal papillary cell carcinoma'
  },
  {
    name: 'chronic myelogenous leukemia (cml)',
    value: 'chronic myelogenous leukemia (cml)'
  },
  {
    name: 'cervical squamous cell carcinoma and endocervical adenocarcinoma',
    value: 'cervical squamous cell carcinoma and endocervical adenocarcinoma'
  },
  { name: 'sarcoma', value: 'sarcoma' },
  { name: 'acute myeloid leukemia', value: 'acute myeloid leukemia' },
  { name: 'esophageal carcinoma', value: 'esophageal carcinoma' },
  { name: 'pancreatic adenocarcinoma', value: 'pancreatic adenocarcinoma' },
  {
    name: 'pheochromocytoma and paraganglioma',
    value: 'pheochromocytoma and paraganglioma'
  },
  { name: 'hepatocellular carcinoma', value: 'hepatocellular carcinoma' },
  {
    name: 'testicular germ cell tumors',
    value: 'testicular germ cell tumors'
  },
  { name: 'rectum adenocarcinoma', value: 'rectum adenocarcinoma' },
  { name: 'thymoma', value: 'thymoma' },
  { name: 'adrenocortical carcinoma', value: 'adrenocortical carcinoma' },
  { name: 'mesothelioma', value: 'mesothelioma' },
  { name: 'uveal melanoma', value: 'uveal melanoma' },
  { name: 'kidney chromophobe', value: 'kidney chromophobe' },
  {
    name: 'breast cancer (adenocarcinoma)',
    value: 'breast cancer (adenocarcinoma)'
  },
  { name: 'uterine carcinosarcoma', value: 'uterine carcinosarcoma' },
  {
    name: 'lymphoid neoplasm diffuse large b-cell lymphoma',
    value: 'lymphoid neoplasm diffuse large b-cell lymphoma'
  },
  { name: 'cholangiocarcinoma', value: 'cholangiocarcinoma' },
  {
    name: 'metastatic neuroblastoma from bone marrow',
    value: 'metastatic neuroblastoma from bone marrow'
  },
  { name: 'cervical adenocarcinoma', value: 'cervical adenocarcinoma' },
  { name: 'b cell lymphoma', value: 'b cell lymphoma' },
  { name: 'colorectal carcinoma', value: 'colorectal carcinoma' },
  {
    name: 'immunoglobulin a lambda myeloma',
    value: 'immunoglobulin a lambda myeloma'
  },
  { name: 'grade iv, adenocarcinoma', value: 'grade iv, adenocarcinoma' },
  { name: 'apparently healthy', value: 'apparently healthy' },
  { name: 'breast cancer', value: 'breast cancer' },
  {
    name: 'endometrial adenocarcinoma',
    value: 'endometrial adenocarcinoma'
  },
  {
    name:
      'refractory immunoblastic b cell lymphoma progressed from follicular centroblastic/centrocytic lymphoma',
    value:
      'refractory immunoblastic b cell lymphoma progressed from follicular centroblastic/centrocytic lymphoma'
  },
  {
    name: 't-cell acute lymphoblastic leukemia cell line atcc crl-2629',
    value: 't-cell acute lymphoblastic leukemia cell line atcc crl-2629'
  },
  { name: 'pancreatic carcinoma', value: 'pancreatic carcinoma' },
  {
    name: "human b cell non-hodgkin's lymphoma",
    value: "human b cell non-hodgkin's lymphoma"
  },
  {
    name: 't-acute lymphoblastic leukemia (t-all; type iii cortical)',
    value: 't-acute lymphoblastic leukemia (t-all; type iii cortical)'
  },
  { name: 'fibrocystic disease', value: 'fibrocystic disease' },
  {
    name:
      'large cell lymphoma; diffuse mixed histiocytic and lymphocytic lymphoma; follicular b cell lymphoma',
    value:
      'large cell lymphoma; diffuse mixed histiocytic and lymphocytic lymphoma; follicular b cell lymphoma'
  },
  { name: "ewing's sarcoma", value: "ewing's sarcoma" },
  {
    name: 'malignant pluripotent embryonal carcinoma',
    value: 'malignant pluripotent embryonal carcinoma'
  },
  {
    name: 'acute promyelocytic leukemia',
    value: 'acute promyelocytic leukemia'
  },
  { name: 'mammary ductal carcinoma', value: 'mammary ductal carcinoma' },
  { name: 'igak myeloma', value: 'igak myeloma' },
  { name: 'pancreatitis', value: 'pancreatitis' },
  { name: 'prostate cancer', value: 'prostate cancer' },
  { name: 'colon cancer', value: 'colon cancer' },
  { name: 'colorectal adenocarcinoma', value: 'colorectal adenocarcinoma' },
  { name: 'melanoma', value: 'melanoma' },
  { name: 'burkitt lymphoma', value: 'burkitt lymphoma' },
  { name: 'carcinoma (prostate)', value: 'carcinoma (prostate)' },
  {
    name: 'cancer, coronary artery disease, hypertension',
    value: 'cancer, coronary artery disease, hypertension'
  },
  {
    name: 'malignant primitive neuroectodermal tumor',
    value: 'malignant primitive neuroectodermal tumor'
  },
  { name: 'parathyroid adenoma', value: 'parathyroid adenoma' },
  { name: 'submaxillar tumor', value: 'submaxillar tumor' },
  { name: 'breast adenocarcinoma', value: 'breast adenocarcinoma' },
  { name: 'tonsillitis', value: 'tonsillitis' },
  { name: 'cancer', value: 'cancer' },
  {
    name: 'diffuse large b-cell lymphoma',
    value: 'diffuse large b-cell lymphoma'
  },
  {
    name: 'acute lymphocytic leukemia',
    value: 'acute lymphocytic leukemia'
  },
  { name: 'retinoblastoma', value: 'retinoblastoma' },
  { name: 'neuroblastoma', value: 'neuroblastoma' },
  { name: 'ewing sarcoma', value: 'ewing sarcoma' },
  {
    name: 'primary hyperparathyroidism',
    value: 'primary hyperparathyroidism'
  },
  {
    name: 'breast cancer, breast carcinoma',
    value: 'breast cancer, breast carcinoma'
  },
  { name: 'neuronitis', value: 'neuronitis' },
  { name: "burkitt's lymphoma", value: "burkitt's lymphoma" },
  { name: 'follicular lymphoma', value: 'follicular lymphoma' },
  { name: "parkinson's disease", value: "parkinson's disease" },
  { name: 'leukemia', value: 'leukemia' },
  { name: 'medulloblastoma', value: 'medulloblastoma' },
  { name: 'acute t cell leukemia', value: 'acute t cell leukemia' },
  { name: 'multiple myeloma', value: 'multiple myeloma' },
  {
    name: 'breast adenocarcinoma, breast cancer',
    value: 'breast adenocarcinoma, breast cancer'
  },
  {
    name: 'hereditary spherocytosis type 2',
    value: 'hereditary spherocytosis type 2'
  },
  { name: 'chronic myeloid leukemia', value: 'chronic myeloid leukemia' },
  {
    name:
      'de lange phenotype; developmental delay; profound retardation; seizures; 3 cousins are also affected; 46,xy,-22,+der (22)t(3;22)(q25.3;p12)',
    value:
      'de lange phenotype; developmental delay; profound retardation; seizures; 3 cousins are also affected; 46,xy,-22,+der (22)t(3;22)(q25.3;p12)'
  },
  {
    name: 'cancer, chronic myeloid leukemia, leukemia',
    value: 'cancer, chronic myeloid leukemia, leukemia'
  },
  { name: 'colorectal cancer', value: 'colorectal cancer' },
  { name: 'embryonal carcinoma', value: 'embryonal carcinoma' },
  {
    name: 'chronic myeloid leukemia, leukemia',
    value: 'chronic myeloid leukemia, leukemia'
  },
  {
    name: 'cornelia de lange syndrome 1; cdls1; nipped-b-like; nipbl',
    value: 'cornelia de lange syndrome 1; cdls1; nipped-b-like; nipbl'
  },
  { name: 'carcinoma', value: 'carcinoma' },
  { name: 'cervical cancer', value: 'cervical cancer' },
  { name: 'b-cell lymphoma', value: 'b-cell lymphoma' },
  { name: 'breast cancer, carcinoma', value: 'breast cancer, carcinoma' },
  { name: 'cancer, leukemia', value: 'cancer, leukemia' },
  {
    name: 'hepatocellular adenocarcinoma',
    value: 'hepatocellular adenocarcinoma'
  },
  { name: 'lung carcinoma', value: 'lung carcinoma' },
  { name: 'malignant glioblastoma', value: 'malignant glioblastoma' },
  { name: 'stomach cancer', value: 'stomach cancer' },
  {
    name: 'cancer, lung adenocarcinoma',
    value: 'cancer, lung adenocarcinoma'
  },
  { name: 'esophagitis', value: 'esophagitis' },
  { name: 'lymphoma', value: 'lymphoma' },
  {
    name: 'multiple myeloma, myeloid neoplasm',
    value: 'multiple myeloma, myeloid neoplasm'
  },
  {
    name: 'cancer, embryonal carcinoma, embryonal testis carcinoma',
    value: 'cancer, embryonal carcinoma, embryonal testis carcinoma'
  },
  { name: 'carcinoma, cervicitis', value: 'carcinoma, cervicitis' },
  { name: 'colon carcinoma', value: 'colon carcinoma' },
  {
    name: 'coronary artery disease, hypertension',
    value: 'coronary artery disease, hypertension'
  },
  { name: 'fibrosarcoma', value: 'fibrosarcoma' },
  {
    name: 'lymphoblastic leukemia, lymphoma',
    value: 'lymphoblastic leukemia, lymphoma'
  },
  { name: 'mucositis', value: 'mucositis' },
  { name: 'prostatitis', value: 'prostatitis' },
  { name: 't-cell leukemia', value: 't-cell leukemia' },
  { name: 'adenocarcinoma, cancer', value: 'adenocarcinoma, cancer' },
  {
    name: 'cancer, hepatocellular carcinoma',
    value: 'cancer, hepatocellular carcinoma'
  },
  { name: 'cancer, neuroblastoma', value: 'cancer, neuroblastoma' },
  { name: 'down syndrome', value: 'down syndrome' },
  { name: 'renal cell adenocarcinoma', value: 'renal cell adenocarcinoma' },
  {
    name: "rhabdoid tumor (wilm's tumor)",
    value: "rhabdoid tumor (wilm's tumor)"
  },
  {
    name: 'acute promyelocytic leukemia, atrichia with papular lesions',
    value: 'acute promyelocytic leukemia, atrichia with papular lesions'
  },
  {
    name: 'cancer, pancreatic carcinoma',
    value: 'cancer, pancreatic carcinoma'
  },
  {
    name: 'carcinoma; large cell lung cancer',
    value: 'carcinoma; large cell lung cancer'
  },
  { name: 'cystadenocarcinoma', value: 'cystadenocarcinoma' },
  {
    name: "dukes' type c, grade iv, colorectal adenocarcinoma",
    value: "dukes' type c, grade iv, colorectal adenocarcinoma"
  },
  { name: 'endometriosis', value: 'endometriosis' },
  { name: 'hepatitis', value: 'hepatitis' },
  { name: 'liver carcinoma', value: 'liver carcinoma' },
  { name: 'malignant melanoma', value: 'malignant melanoma' },
  { name: 'metastatic melanoma', value: 'metastatic melanoma' },
  { name: 'neuroglioma', value: 'neuroglioma' },
  { name: 'osteosarcoma', value: 'osteosarcoma' },
  { name: 'plasmacytoma; myeloma', value: 'plasmacytoma; myeloma' },
  { name: 'renal carcinoma ', value: 'renal carcinoma ' },
  { name: 'renal cell carcinoma', value: 'renal cell carcinoma' },
  {
    name: 'squamous cell carcinoma; mesothelioma',
    value: 'squamous cell carcinoma; mesothelioma'
  },
  { name: 'urinary bladder cancer', value: 'urinary bladder cancer' },
  { name: 'cancer, carcinoma', value: 'cancer, carcinoma' },
  {
    name: 'cancer, carcinoma, cervicitis',
    value: 'cancer, carcinoma, cervicitis'
  },
  {
    name: 'cancer, colorectal adenocarcinoma',
    value: 'cancer, colorectal adenocarcinoma'
  },
  { name: 'skin melanoma', value: 'skin melanoma' },
  { name: 'bone cancer, osteosarcoma', value: 'bone cancer, osteosarcoma' },
  {
    name: 'cancer, endometrial carcinoma',
    value: 'cancer, endometrial carcinoma'
  },
  { name: 'cancer, lung carcinoma', value: 'cancer, lung carcinoma' },
  { name: 'cancer, osteosarcoma', value: 'cancer, osteosarcoma' },
  {
    name: 'cancer, osteosarcoma, sarcoma',
    value: 'cancer, osteosarcoma, sarcoma'
  },
  { name: 'cervicitis', value: 'cervicitis' },
  {
    name: 'embryonal carcinoma, mediastinitis, seminoma',
    value: 'embryonal carcinoma, mediastinitis, seminoma'
  },
  {
    name: 'gastrointestinal stromal tumor',
    value: 'gastrointestinal stromal tumor'
  },
  { name: 'hepatoblastoma', value: 'hepatoblastoma' },
  { name: 'lung cancer', value: 'lung cancer' },
  {
    name: 'pheochromocythoma and paraganglioma',
    value: 'pheochromocythoma and paraganglioma'
  },
  { name: 'progeria', value: 'progeria' },
  {
    name: 'prostate carcinoma, prostatitis',
    value: 'prostate carcinoma, prostatitis'
  },
  { name: 'retinitis', value: 'retinitis' },
  { name: 'seminoma', value: 'seminoma' },
  {
    name: 'acute promyelocytic leukemia, cancer',
    value: 'acute promyelocytic leukemia, cancer'
  },
  {
    name: 'acute t cell leukemia, cancer',
    value: 'acute t cell leukemia, cancer'
  },
  {
    name: 'cancer, prostate adenocarcinoma, prostate carcinoma',
    value: 'cancer, prostate adenocarcinoma, prostate carcinoma'
  },
  { name: 'cancer, prostate cancer', value: 'cancer, prostate cancer' },
  { name: 'cancer, retinoblastoma', value: 'cancer, retinoblastoma' },
  { name: 'choroiditis', value: 'choroiditis' },
  {
    name: 'chronic leukemia, chronic myeloid leukemia',
    value: 'chronic leukemia, chronic myeloid leukemia'
  },
  {
    name: 'diffuse large b-cell lymphoma, tonsillitis',
    value: 'diffuse large b-cell lymphoma, tonsillitis'
  },
  { name: 'essential thrombocythemia', value: 'essential thrombocythemia' },
  { name: 'hepatic rhabdoid tumor', value: 'hepatic rhabdoid tumor' },
  { name: 'noonan syndrome 1', value: 'noonan syndrome 1' },
  { name: 'nut midline carcinoma', value: 'nut midline carcinoma' },
  {
    name: 'prostate cancer, prostate carcinoma',
    value: 'prostate cancer, prostate carcinoma'
  },
  { name: 'rhabdomyosarcoma', value: 'rhabdomyosarcoma' }
];

export { choices };
