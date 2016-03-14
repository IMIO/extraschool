update extraschool_prestation_times_encodage_manuel set activity_category_id = (select min(id) from extraschool_activitycategory);
