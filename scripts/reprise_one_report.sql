UPDATE extraschool_one_report
SET show_quarter = CASE WHEN quarter = '1' THEN '1er'
			WHEN quarter = '2' THEN '2eme'
			WHEN quarter = '3' THEN '3eme'
			ELSE '4eme'
		   END;
UPDATE extraschool_one_report
SET is_created = TRUE;