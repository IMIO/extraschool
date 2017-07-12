UPDATE extraschool_parent
SET invoicesendmethod = 'onlybymail', remindersendmethod = 'onlybymail'
WHERE email IS NULL OR email = '';