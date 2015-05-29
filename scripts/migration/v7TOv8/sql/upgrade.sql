
DROP TABLE extraschool_activity_child_rel;

DROP TABLE extraschool_prestations_wizard;

DROP TABLE extraschool_statsone_wizard;

ALTER TABLE extraschool_activity
	ADD COLUMN parent_id integer,
	ADD COLUMN price_list_id integer,
	ADD COLUMN root_id integer,
	ADD COLUMN default_from_to character varying,
	ALTER COLUMN name TYPE character varying(100),
	ALTER COLUMN name SET NOT NULL;
DELETE FROM extraschool_activity;

ALTER TABLE extraschool_activitychildregistration
	ADD COLUMN place_id integer NOT NULL,
	ALTER COLUMN child_id SET NOT NULL,
	ALTER COLUMN registration_from SET NOT NULL,
	ALTER COLUMN registration_to SET NOT NULL;
DELETE FROM extraschool_activitychildregistration;

ALTER TABLE extraschool_activityexclusiondates
	DROP COLUMN name;
DELETE FROM extraschool_activityexclusiondates;

ALTER TABLE extraschool_biller
	ALTER COLUMN name TYPE character varying(100);

ALTER TABLE extraschool_child
	DROP COLUMN name,
	DROP COLUMN toto;

ALTER TABLE extraschool_childposition
	ALTER COLUMN name SET NOT NULL,
	ALTER COLUMN "position" SET NOT NULL;

ALTER TABLE extraschool_childtype
	ALTER COLUMN name SET NOT NULL;

ALTER TABLE extraschool_class
	ALTER COLUMN name SET NOT NULL;

ALTER TABLE extraschool_guardian
	DROP COLUMN name;

ALTER TABLE extraschool_guardianprestationtimes
	RENAME COLUMN "ES" TO "es";

ALTER TABLE extraschool_invoice
	ADD COLUMN payment_term date,
	ADD COLUMN period_to date,
	ADD COLUMN period_from date,
	ADD COLUMN activitycategoryid integer;

ALTER TABLE extraschool_parent
	ADD COLUMN one_subvention_type character varying NOT NULL default 'sf';

ALTER TABLE extraschool_payment
	DROP COLUMN addr1,
	DROP COLUMN addr2;

ALTER TABLE extraschool_pdaprestationtimes
	ADD COLUMN prestation_times_of_the_day_id integer;
ALTER TABLE extraschool_pdaprestationtimes
	RENAME COLUMN "ES" TO "es";

ALTER TABLE extraschool_prestationscheck_wizard
	DROP COLUMN childid,
	DROP COLUMN currentdate,
	DROP COLUMN prestation_time,
	DROP COLUMN es,
	ALTER COLUMN period_to DROP NOT NULL,
	ALTER COLUMN period_from DROP NOT NULL;

ALTER TABLE extraschool_prestationtimes
	DROP COLUMN activityid,
	DROP COLUMN activitycategoryid,
	ADD COLUMN prestation_times_of_the_day_id integer,
	ADD COLUMN error_msg character varying(255),
	ADD COLUMN exit_all boolean,
	ADD COLUMN activity_occurrence_id integer;
ALTER TABLE extraschool_prestationtimes
	RENAME COLUMN "ES" TO "es";

ALTER TABLE extraschool_reject
	DROP COLUMN addr1,
	DROP COLUMN addr2;

ALTER TABLE extraschool_reminder
	ADD COLUMN term date,
	ADD COLUMN activitycategoryid integer,
	ADD COLUMN transmissiondate date;

ALTER TABLE extraschool_schoolimplantation
	ALTER COLUMN name TYPE character varying(100) /* TYPE change - table: extraschool_schoolimplantation original: character varying(50) new: character varying(100) */,
	ALTER COLUMN street TYPE character varying(100) /* TYPE change - table: extraschool_schoolimplantation original: character varying(50) new: character varying(100) */;




