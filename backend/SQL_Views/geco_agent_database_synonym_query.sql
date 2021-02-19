SELECT distinct is_annotation, label_type, lower(pref_label) as pref_label, lower(label) as label
FROM (
         SELECT distinct is_annotation, 'tissue' as label_type, pref_label, label
         FROM biosample
                  JOIN vocabulary ON tissue_tid = tid
                  NATURAL JOIN synonym
                  NATURAL JOIN replicate
                  NATURAL JOIN replicate2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset

         UNION

         SELECT distinct is_annotation, 'tissue' as label_type, tissue as pref_label, tissue as label
         FROM biosample
                  NATURAL JOIN replicate
                  NATURAL JOIN replicate2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset

         UNION

         SELECT distinct is_annotation, 'disease' as label_type, pref_label, label
         FROM biosample
                  JOIN vocabulary ON disease_tid = tid
                  NATURAL JOIN synonym
                  NATURAL JOIN replicate
                  NATURAL JOIN replicate2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset
         UNION

         SELECT distinct is_annotation, 'disease' as label_type, disease as pref_label, disease as label
         FROM biosample
                  NATURAL JOIN replicate
                  NATURAL JOIN replicate2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset

         UNION

         SELECT distinct is_annotation, 'cell' as label_type, pref_label, label
         FROM biosample
                  JOIN vocabulary ON cell_tid = tid
                  NATURAL JOIN synonym
                  NATURAL JOIN replicate
                  NATURAL JOIN replicate2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset


         UNION

         SELECT distinct is_annotation, 'cell' as label_type, cell as pref_label, cell as label
         FROM biosample
                  NATURAL JOIN replicate
                  NATURAL JOIN replicate2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset

         UNION

         SELECT distinct is_annotation, 'content_type' as label_type, pref_label, label
         FROM item
                  JOIN vocabulary ON content_type_tid = tid
                  NATURAL JOIN synonym
                  NATURAL JOIN dataset


         UNION

         SELECT distinct is_annotation, 'content_type' as label_type, content_type as pref_label, content_type as label
         FROM item
                  NATURAL JOIN dataset


         UNION

         SELECT distinct is_annotation, 'target' as label_type, pref_label, label
         FROM experiment_type
                  JOIN vocabulary ON target_tid = tid
                  NATURAL JOIN synonym
                  NATURAL JOIN item
                  NATURAL JOIN dataset


         UNION

         SELECT distinct is_annotation, 'target' as label_type, target as pref_label, target as label
         FROM experiment_type
                  NATURAL JOIN item
                  NATURAL JOIN dataset

         UNION

         SELECT distinct False, 'data_type' as label_type, pref_label, synonym
         FROM dw.data_type_synonym

         UNION

         SELECT distinct is_annotation, 'data_type' as label_type, data_type as pref_label, data_type as label
         FROM dataset
         WHERE lower(data_type) not in (SELECT lower(synonym) from dw.data_type_synonym)


         UNION

         SELECT distinct is_annotation, 'source' as label_type, source as pref_label, source as label
         FROM project
                  NATURAL JOIN case_study
                  NATURAL JOIN case2item
                  NATURAL JOIN item
                  NATURAL JOIN dataset


         UNION

         SELECT distinct is_annotation, 'assembly' as label_type, assembly as pref_label, assembly as label
         FROM dataset
     ) as inn
WHERE pref_label is not null
ORDER BY is_annotation, label_type, lower(pref_label), lower(label)
-- limit 10



