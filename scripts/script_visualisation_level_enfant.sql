SELECT c.lastname, c.firstname, l.name, c.isdisabled
FROM extraschool_child AS c
INNER JOIN extraschool_level AS l
ON c.levelid = l.id
ORDER BY c.lastname, l.name;