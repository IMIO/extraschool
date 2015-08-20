insert into extraschool_prestation_times_of_the_day
(date_of_the_day, child_id, verified)
select prestation_date, childid, False as verified
from extraschool_pdaprestationtimes
group by childid, prestation_date, verified;

update extraschool_prestationtimes 
	set prestation_times_of_the_day_id = (select id from extraschool_prestation_times_of_the_day where child_id = childid and date_of_the_day = prestation_date);
update extraschool_pdaprestationtimes 
	set prestation_times_of_the_day_id = (select id from extraschool_prestation_times_of_the_day where child_id = childid and date_of_the_day = prestation_date);
