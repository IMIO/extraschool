update extraschool_prestationtimes 
	set prestation_times_of_the_day_id = (select id from extraschool_prestation_times_of_the_day where child_id = childid and date_of_the_day = prestation_date);
update pdaextraschool_prestationtimes 
	set prestation_times_of_the_day_id = (select id from extraschool_prestation_times_of_the_day where child_id = childid and date_of_the_day = prestation_date);
