update extraschool_prestation_times_of_the_day set activity_category_id = (select min(id) from extraschool_activitycategory);
