#
# Basé sur un script créé à l'aide de apgdiff http://apgdiff.com/how_it_works.php
#
# Migration de la V7 - La Bruyère vers la V1 - Imio
#
# Input : Nom du fichier de dump en V7
#	  Nom de la DB V8
#

fichier_source=dump/recreagiquelb6.backup
fichier_upgrade=sql/v8_upgrade.sql
fichier_update_presta_of_the_day=sql/update_presta_of_the_day.sql
db_user=openerp
db_tmp=extraschool_tmp
db_new=extraschool_mig
odoo_v8_path=/srv/buildoutaes/bin/start_openerp

part_init=1
part_restore=1
rm tmp/*
if [ "$part_init" = "1" ]
then
	echo "---------------START----------------" > migration.log
	echo "---------------START----------------" 
	#drop and create DB
	echo "---------------CREATION DB----------------" >> migration.log
	echo "---------------CREATION DB----------------"
	psql -U openerp -d template1 -c "DROP DATABASE $db_tmp;" >> migration.log
	psql -U openerp -d template1 -c "CREATE DATABASE $db_tmp;" >> migration.log
	echo "---------------RESTORE SOURCE----------------" >> migration.log
	echo "---------------RESTORE SOURCE----------------"
	#restore source dump
	pg_restore -O --schema=public -U $db_user -d $db_tmp $fichier_source >> migration.log
	echo "---------------RENAME TO EXTRASCHOOL----------------" >> migration.log
	echo "---------------RENAME TO EXTRASCHOOL----------------"
	#rename2extraschool
	pg_dump -U $db_user -t lbschool* $db_tmp > tmp/data_tmp.sql
	#rename2extraschool->lbschoolcare
	sed -i 's/lbschoolcare/extraschool/g' tmp/data_tmp.sql
	#rename2extraschool->lbschool
	sed -i 's/lbschool/extraschool/g' tmp/data_tmp.sql
	echo "---------------RESTORE TABLES EXTRASCHOOL----------------" >> migration.log
	echo "---------------RESTORE TABLES EXTRASCHOOL----------------"
	psql -U $db_user -d $db_tmp < tmp/data_tmp.sql >> migration.log

	#upgrade
	echo "---------------UPGRADE----------------" >> migration.log
	echo "---------------UPGRADE----------------"
	psql -U openerp -d $db_tmp < $fichier_upgrade >> migration.log
fi
if [ "$part_restore" = "1" ]
then
	echo "---------------CREATION NOUV DB----------------" >> migration.log
	echo "---------------CREATION NOUV DB----------------"
	psql -U openerp -d template1 -c "DROP DATABASE $db_new;" >> migration.log
	psql -U openerp -d template1 -c "CREATE DATABASE $db_new;">> migration.log
#dump updated data
	echo "---------------DUMP USERS + EXTRASCHOOL----------------" >> migration.log
	echo "---------------DUMP USERS + EXTRASCHOOL----------------"
	pg_dump -c -U $db_user -t res_users $db_tmp > tmp/data_tmp_users.sql
	pg_dump -c -U $db_user -t extraschool_* $db_tmp > tmp/data_tmp.sql
	#create v8 DB
	echo "---------------CREATION DB ODOOV8----------------" >> migration.log
	echo "---------------CREATION DB ODOOV8----------------"
	$odoo_v8_path -d $db_new -i extraschool -l fr_BE --load-language=fr_BE --without-demo=WITHOUT_DEMO --stop-after-init
	echo "---------------RESTORE DONNEES MIGREES----------------" >> migration.log
	echo "---------------RESTORE DONNEES MIGREES----------------"
	#restore updated data
#	pg_restore -O --schema=public --disable-triggers -S $db_user -U $db_user -d $db_new tmp/data_tmp.dump
	psql -U $db_user -d $db_new -c "delete from res_users where id > 1;" >> migration.log
	psql -U $db_user -d $db_tmp -c "COPY (select id, active, login, password, company_id, 1 as partner_id, create_uid, create_date, login_date, write_uid, write_date, signature, action_id, password as password_crypt from res_users where id > 1) TO STDOUT;" > tmp/data_tmp_users.sql	
	psql -U $db_user -d $db_new -c "COPY res_users FROM STDIN;" < ./tmp/data_tmp_users.sql >> migration.log

	psql -U $db_user -d $db_new < tmp/data_tmp.sql >> migration.log
	#start odoo with update
	echo "---------------START ODOO AVEC UPDATE----------------" >> migration.log
	$odoo_v8_path -d $db_new -u $db_user --stop-after-init
	#update presta_of_the_day 
	echo "---------------UPDATE PRESTA OF THE DAY----------------" >> migration.log
	echo "---------------UPDATE PRESTA OF THE DAY----------------"
	psql -U $db_user -d $db_new < $fichier_update_presta_of_the_day
	#start odoo with update
	echo "---------------FINI DEMARRAGE ODOO----------------" >> migration.log
	echo "---------------FINI DEMARRAGE ODOO----------------"
	$odoo_v8_path -d $db_new -u extraschool
fi


