SELECT distinct label_type, lower(pref_label), lower(label)
FROM (
         SELECT distinct 'tissue' as label_type, pref_label, label
         FROM biosample
         JOIN vocabulary ON tissue_tid = tid
         NATURAL JOIN synonym

		UNION

		 SELECT distinct 'tissue' as label_type, tissue as pref_label, tissue as label
         FROM biosample


         UNION

         SELECT distinct 'disease' as label_type, pref_label, label
         FROM biosample
         JOIN vocabulary ON disease_tid = tid
         NATURAL JOIN synonym

			UNION

		 SELECT distinct 'disease' as label_type, disease as pref_label, disease as label
         FROM biosample

         UNION

         SELECT distinct 'cell' as label_type, pref_label, label
         FROM biosample
                  JOIN vocabulary ON cell_tid = tid
                  NATURAL JOIN synonym


		UNION

		 SELECT distinct 'cell' as label_type, cell as pref_label, cell as label
         FROM biosample

         UNION

         SELECT distinct 'content_type' as label_type, pref_label, label
         FROM item
                  JOIN vocabulary ON content_type_tid = tid
                  NATURAL JOIN synonym


		UNION

		 SELECT distinct 'content_type' as label_type, content_type as pref_label, content_type as label
         FROM item


         UNION

         SELECT distinct 'target' as label_type, pref_label, label
         FROM experiment_type
                  JOIN vocabulary ON target_tid = tid
                  NATURAL JOIN synonym


		UNION

		 SELECT distinct 'target' as label_type, target as pref_label, target as label
         FROM experiment_type


         UNION

         SELECT distinct 'data_type' as label_type, pref_label, synonym
         FROM dw.data_type_synonym

			UNION

		 SELECT distinct 'data_type' as label_type, data_type as pref_label, data_type as label
         FROM dataset
		 WHERE lower(data_type) not in (SELECT lower(synonym) from dw.data_type_synonym)


) as inn
ORDER BY label_type, lower(pref_label), lower(label)
-- limit 10

