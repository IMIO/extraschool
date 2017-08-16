SELECT *
FROM extraschool_child
WHERE create_date < '2017-07-01'
ORDER BY id;

SELECT *
FROM extraschool_class
WHERE id IN (
		SELECT class_id
		FROM extraschool_class_level_rel
		WHERE level_id = 39
		)
ORDER BY name;

SELECT *
FROM extraschool_class

SELECT *
FROM extraschool_class_level_rel
ORDER BY level_id



-- WHERE level_id = 39

INSERT INTO extraschool_class_level_rel
VALUES (8, 39)
