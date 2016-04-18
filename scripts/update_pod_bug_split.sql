update extraschool_pdaprestationtimes
set prestation_times_of_the_day_id = (select min(id) from extraschool_prestation_times_of_the_day where child_id = childid and date_of_the_day=prestation_date)
where prestation_date > '2016-04-10';
update extraschool_prestationtimes
set prestation_times_of_the_day_id = (select min(id) from extraschool_prestation_times_of_the_day where child_id = childid and date_of_the_day=prestation_date)
where prestation_date > '2016-04-10';
delete from extraschool_prestation_times_of_the_day pod
where id in (select id 
	     from extraschool_prestation_times_of_the_day 
	     where date_of_the_day > '2016-04-10'
		   and (select count(*) from extraschool_prestationtimes where prestation_times_of_the_day_id = pod.id) = 0
	     )