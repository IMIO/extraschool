SELECT count(street), lastname, firstname
FROM extraschool_parent
GROUP BY lastname, firstname
HAVING count(street) > 1