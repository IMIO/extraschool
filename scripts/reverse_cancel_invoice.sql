-- Delete the refound line first
DELETE FROM extraschool_refound_line
WHERE invoiceid in (	SELECT id
		FROM extraschool_invoice
		WHERE no_value != 0
	    )

-- Get the invoices that were canceled (they now have value in no_value).
UPDATE extraschool_invoice
SET balance = no_value,
    no_value = 0
WHERE id in (	SELECT id
		FROM extraschool_invoice
		WHERE no_value != 0
	    )


    
