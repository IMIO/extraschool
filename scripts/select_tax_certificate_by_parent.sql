SELECT p.lastname AS "Parent Lastname", p.firstname, c.lastname AS "Child Lastname", c.firstname, inv.number AS "Invoice Number", 
to_char(prest.prestation_date, 'DD mon YYYY') AS "Prestation Date", act.short_name AS "Activity Name", to_char(to_timestamp((prest.prestation_time) * 60), 'MI:SS') AS "Time of Scan", 
prest.es AS "Entry/Exit", to_char(total_price, '999.99') AS "Amount"
FROM extraschool_prestationtimes AS prest
INNER JOIN extraschool_invoicedprestations AS inv_prest
ON prest.invoiced_prestation_id = inv_prest.id
INNER JOIN extraschool_invoice AS inv
ON inv.id = inv_prest.invoiceid
INNER JOIN extraschool_parent AS p
ON p.id = prest.parent_id
INNER JOIN extraschool_child AS c
ON c.id = prest.childid
INNER JOIN extraschool_activity AS act
ON act.id = inv_prest.activity_activity_id
WHERE inv_prest.invoiceid IN (	SELECT DISTINCT(inv.id) AS id
				FROM extraschool_payment_reconciliation AS pay_rec
				LEFT JOIN extraschool_invoice AS inv 
				ON inv.id = pay_rec.invoice_id
				LEFT JOIN extraschool_payment AS pay 
				ON pay.id = pay_rec.payment_id
				WHERE pay_rec.paymentdate BETWEEN '2017-01-01' AND '2017-12-31' AND parentid = 485
				AND inv.balance = 0 AND inv.last_reminder_id IS NULL) AND act.on_tax_certificate = TRUE
ORDER BY c.firstname, inv.number, prest.prestation_date, act.short_name, prest.prestation_time