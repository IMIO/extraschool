SELECT i.balance, i.amount_total, i.amount_total - i.amount_received AS prepaid, p.lastname, p.firstname
FROM extraschool_invoice AS i
INNER JOIN extraschool_parent AS p
ON i.parentid = p.id
WHERE i.amount_total - i.amount_received BETWEEN 0.0001 AND 0.03
ORDER BY prepaid
