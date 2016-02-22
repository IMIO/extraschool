update extraschool_invoice ii
set structcom = 
(select 
'+++' || LPAD(ac.invoicecomstructprefix, 3, '0') 
                        || '/' || substring(LPAD(i.number::TEXT,7,'0') from 1 for 4) || '/' || substring(LPAD(i.number::TEXT,7,'0') from 5 for 3)
                        || case when LPAD(((LPAD(ac.invoicecomstructprefix, 3, '0') || LPAD(i.number::TEXT,7,'0'))::bigint % 97)::TEXT,2,'0') = '00' then '97' 
                        else LPAD(((LPAD(ac.invoicecomstructprefix, 3, '0') || LPAD(i.number::TEXT,7,'0'))::bigint % 97)::TEXT,2,'0') end
                        || '+++' as com_struct 
 from extraschool_invoice i
 left join extraschool_biller b on b.id = i.biller_id
 left join extraschool_activitycategory ac on ac.id = b.activitycategoryid
 where i.id = ii.id)