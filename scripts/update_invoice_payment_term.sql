update extraschool_invoice i
set payment_term = b.payment_term
from extraschool_biller b 
where b.id = i.biller_id
