SELECT DISTINCT(pay.parent_id), par.lastname AS Nom, par.firstname AS Prénom, pay.structcom AS Communication_structurée
FROM extraschool_payment AS pay
INNER JOIN extraschool_parent as par
ON pay.parent_id = par.id
WHERE pay.structcom IS NOT NULL
ORDER BY par.lastname,par.firstname;
