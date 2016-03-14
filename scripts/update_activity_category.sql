update extraschool_pdaprestationtimes
set activitycategoryid = (select min(id) from extraschool_activity);
update extraschool_prestationtimes
set activity_category_id = (select min(id) from extraschool_activity);
update extraschool_prestation_times_of_the_day
set activity_category_id = (select min(id) from extraschool_activity);
