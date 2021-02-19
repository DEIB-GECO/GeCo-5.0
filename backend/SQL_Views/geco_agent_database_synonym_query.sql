SELECT distinct 'tissue' as label_type, pref_label, label
FROM biosample 
JOIN vocabulary  ON tissue_tid = tid
NATURAL JOIN synonym 

UNION ALL

SELECT distinct 'disease' as label_type, pref_label, label
FROM biosample 
JOIN vocabulary  ON disease_tid = tid
NATURAL JOIN synonym 

UNION ALL

SELECT distinct 'cell' as label_type, pref_label, label
FROM biosample 
JOIN vocabulary  ON cell_tid = tid
NATURAL JOIN synonym 

UNION ALL

SELECT distinct 'content_type' as label_type, pref_label, label
FROM item 
JOIN vocabulary  ON content_type_tid = tid
NATURAL JOIN synonym 


UNION ALL

SELECT distinct 'target' as label_type, pref_label, label
FROM experiment_type 
JOIN vocabulary  ON target_tid = tid
NATURAL JOIN synonym 


UNION ALL

SELECT distinct 'data_type' as label_type, pref_label, synonym
FROM dw.data_type_synonym

ORDER BY label_type, pref_label, label

-- limit 10

