update extraschool_prestationtimes set activity_category_id = (select min(id) from extraschool_activitycategory);
