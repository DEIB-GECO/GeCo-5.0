import pandas as pd
import copy
from collections import defaultdict

templates = []
with open('template.txt', 'r') as f:
    for x in f.readlines():
        x = x.strip()
        if x != "":
            templates.append(x)

synonyms = pd.read_csv('../SQL_Views/geco_agent_database_synonym.txt', sep='\t')
manual_synonyms = pd.read_csv('../SQL_Views/synonyms.tsv', sep='\t')
manual_synonyms.columns= synonyms.columns
manual_synonyms['pref_label'] = [x.lower() for x in manual_synonyms['pref_label']]
manual_synonyms['label'] = [x.lower() for x in manual_synonyms['label']]
synonyms = pd.concat([synonyms,manual_synonyms])
ann_synonyms = synonyms[synonyms['is_annotation']==True]
exp_synonyms = synonyms[synonyms['is_annotation']==False]
ann_synonyms = ann_synonyms.drop('is_annotation', axis=1)
exp_synonyms = exp_synonyms.drop('is_annotation', axis=1)



def generate_sentences(templates, dataframe, name_file):
    syn_dict = defaultdict(lambda: defaultdict(list))

    for label_type, pref_label, syn_label in dataframe.values:
        syn_dict[label_type][pref_label].append(syn_label)
    syn_dict_copy = copy.deepcopy(syn_dict)
    list_rewritten = []
    with open(f'{name_file}.txt', 'w') as f:
        for j in range(3):
            for t in templates:
                list_t = t.split('$')
                for i in range(1, len(list_t), 2):
                    field = list_t[i]
                    inner_dict = syn_dict[field]
                    substitute = None
                    pref = None
                    if len(inner_dict) == 0:
                        inner_dict = copy.deepcopy(syn_dict_copy[field])
                        syn_dict[field] = inner_dict
                        list_rewritten.append(field)
                    for k, v in inner_dict.items():
                        if k in v:
                            substitute = k
                            v.remove(substitute)
                            if len(v) == 0:
                                del inner_dict[k]
                            break

                    if substitute == None:
                        for k, v in inner_dict.items():
                            if len(v) > 0:
                                substitute = v[0]
                                v.remove(substitute)
                                if len(v) == 0:
                                    del inner_dict[k]
                                pref = k
                                break

                    if pref == None:
                        list_t[i] = f'[{substitute}]({field})'
                    else:
                        list_t[i] = f'[{substitute}]{{"entity":"{field}","value":"{pref}"}}'

                f.write('\t- ' + ''.join(list_t) + '\n')


    for k in syn_dict_copy.keys():
        if k not in set(list_rewritten):
            with open(f'sentences_syn_db_{k}_ann.txt', 'w') as f:
                inner_dict = syn_dict[k]
                for pref, labels in inner_dict.items():
                    for label in labels:
                        if pref == label:
                            syn = f'[{label}]({k})'
                        else:
                            syn = f'[{label}]{{"entity":"{k}","value":"{pref}"}}'
                        f.write(f'\t- {syn}\n')

    with open(f'synonyms_db_ann.txt', 'w') as f:
        for k in syn_dict_copy.keys():
            inner_dict = syn_dict_copy[k]
            for pref, labels in inner_dict.items():
                f.write(f'- synonym: {pref}\n'
                        f'  examples: |\n')
                for label in labels:
                    if pref == label:
                        pass
                    else:
                        f.write(f'    - {label}\n')

#generate_sentences(templates, exp_synonyms, 'sentences_syn_db_exp')
generate_sentences(templates, ann_synonyms, 'sentences_syn_db_ann')



