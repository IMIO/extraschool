SELECT i.id
FROM extraschool_invoice AS i
INNER JOIN extraschool_parent AS p
ON i.parentid = p .id
WHERE i.id IN (
		SELECT i.id
		FROM extraschool_reminder AS r
		INNER JOIN extraschool_reminder_invoice_rel AS ri
		ON r.id = ri.reminder_id
		INNER JOIN extraschool_invoice AS i
		ON ri.invoice_id = i.id
		INNER JOIN extraschool_parent AS p
		ON r.parentid = p.id
		WHERE r.reminders_journal_id = 6 AND i.balance > 0
		)




