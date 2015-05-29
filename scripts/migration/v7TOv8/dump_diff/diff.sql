
ALTER TABLE extraschool_activity_childposition_rel
	DROP CONSTRAINT extraschool_activity_childposition_rel_activity_id_fkey;

ALTER TABLE extraschool_child
	DROP CONSTRAINT extraschool_child_parentid_fkey;

ALTER TABLE extraschool_childsworkbook_wizard
	DROP CONSTRAINT extraschool_childsworkbook_wizard_child_id_fkey;

ALTER TABLE extraschool_childsworkbook_wizard
	DROP CONSTRAINT extraschool_childsworkbook_wizard_placeid_fkey;

ALTER TABLE extraschool_guardianprestationtimes_wizard
	DROP CONSTRAINT extraschool_guardianprestationtimes_wizard_guardianid_fkey;

ALTER TABLE extraschool_invoice_wizard
	DROP CONSTRAINT extraschool_invoice_wizard_activitycategory_fkey;

ALTER TABLE extraschool_prestationscheck_wizard
	DROP CONSTRAINT extraschool_prestationscheck_wizard_activitycategory_fkey;

ALTER TABLE extraschool_prestationscheck_wizard
	DROP CONSTRAINT extraschool_prestationscheck_wizard_childid_fkey;

ALTER TABLE extraschool_prestationtimes
	DROP CONSTRAINT extraschool_prestationtimes_activitycategoryid_fkey;

ALTER TABLE extraschool_prestationtimes
	DROP CONSTRAINT extraschool_prestationtimes_activityid_fkey;

ALTER TABLE extraschool_prestationtimes
	DROP CONSTRAINT extraschool_prestationtimes_childid_fkey;

ALTER TABLE extraschool_taxcertificates_wizard
	DROP CONSTRAINT extraschool_taxcertificates_wizard_activitycategory_fkey;

ALTER TABLE extraschool_taxcertificates_wizard
	DROP CONSTRAINT extraschool_taxcertificates_wizard_parentid_fkey;

DROP INDEX "extraschool_prestationtimes_ES_index";

DROP TABLE extraschool_activity_child_rel;

DROP TABLE extraschool_prestations_wizard;

DROP TABLE extraschool_statsone_wizard;

DROP SEQUENCE extraschool_prestations_wizard_id_seq;

DROP SEQUENCE extraschool_statsone_wizard_id_seq;

CREATE SEQUENCE extraschool_activityoccurrence_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_one_report_day_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_one_report_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_prestation_times_encodage_manuel_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_prestation_times_manuel_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_prestation_times_of_the_day_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_price_list_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_price_list_version_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE TABLE extraschool_activityoccurrence (
	id integer DEFAULT nextval('extraschool_activityoccurrence_id_seq'::regclass) NOT NULL,
	create_uid integer,
	date_stop timestamp without time zone,
	date_start timestamp without time zone,
	create_date timestamp without time zone,
	name character varying(50),
	place_id integer,
	activityid integer,
	write_uid integer,
	prest_to double precision,
	write_date timestamp without time zone,
	occurrence_date date,
	prest_from double precision
);

COMMENT ON TABLE extraschool_activityoccurrence IS 'activity occurrence';

COMMENT ON COLUMN extraschool_activityoccurrence.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activityoccurrence.date_stop IS 'Date stop';

COMMENT ON COLUMN extraschool_activityoccurrence.date_start IS 'Date start';

COMMENT ON COLUMN extraschool_activityoccurrence.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activityoccurrence.name IS 'Name';

COMMENT ON COLUMN extraschool_activityoccurrence.place_id IS 'Place';

COMMENT ON COLUMN extraschool_activityoccurrence.activityid IS 'Activity';

COMMENT ON COLUMN extraschool_activityoccurrence.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activityoccurrence.prest_to IS 'prest_to';

COMMENT ON COLUMN extraschool_activityoccurrence.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_activityoccurrence.occurrence_date IS 'Date';

COMMENT ON COLUMN extraschool_activityoccurrence.prest_from IS 'prest_from';

CREATE TABLE extraschool_activityoccurrence_cild_rel (
	activityoccurrence_id integer NOT NULL,
	child_id integer NOT NULL
);

COMMENT ON TABLE extraschool_activityoccurrence_cild_rel IS 'RELATION BETWEEN extraschool_activityoccurrence AND extraschool_child';

CREATE TABLE extraschool_invoice_wizard_schoolimplantation_rel (
	invoice_wizard_id integer NOT NULL,
	schoolimplantation_id integer NOT NULL
);

COMMENT ON TABLE extraschool_invoice_wizard_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_invoice_wizard AND extraschool_schoolimplantation';

CREATE TABLE extraschool_one_report (
	id integer DEFAULT nextval('extraschool_one_report_id_seq'::regclass) NOT NULL,
	create_uid integer,
	create_date timestamp without time zone,
	transmissiondate date NOT NULL,
	placeid integer,
	write_uid integer,
	activitycategory integer,
	nb_m_childs integer,
	write_date timestamp without time zone,
	"year" integer NOT NULL,
	quarter character varying NOT NULL,
	nb_p_childs integer
);

COMMENT ON TABLE extraschool_one_report IS 'extraschool.one_report';

COMMENT ON COLUMN extraschool_one_report.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_one_report.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_one_report.transmissiondate IS 'Transmissiondate';

COMMENT ON COLUMN extraschool_one_report.placeid IS 'Placeid';

COMMENT ON COLUMN extraschool_one_report.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_one_report.activitycategory IS 'Activitycategory';

COMMENT ON COLUMN extraschool_one_report.nb_m_childs IS 'Nb m childs';

COMMENT ON COLUMN extraschool_one_report.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_one_report."year" IS 'Year';

COMMENT ON COLUMN extraschool_one_report.quarter IS 'Quarter';

COMMENT ON COLUMN extraschool_one_report.nb_p_childs IS 'Nb p childs';

CREATE TABLE extraschool_one_report_day (
	id integer DEFAULT nextval('extraschool_one_report_day_id_seq'::regclass) NOT NULL,
	create_uid integer,
	create_date timestamp without time zone,
	subvention_type character varying,
	write_uid integer,
	day_date date,
	one_report_id integer,
	nb_m_childs integer,
	write_date timestamp without time zone,
	nb_p_childs integer
);

COMMENT ON TABLE extraschool_one_report_day IS 'extraschool.one_report_day';

COMMENT ON COLUMN extraschool_one_report_day.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_one_report_day.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_one_report_day.subvention_type IS 'Subvention type';

COMMENT ON COLUMN extraschool_one_report_day.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_one_report_day.day_date IS 'Day date';

COMMENT ON COLUMN extraschool_one_report_day.one_report_id IS 'One report id';

COMMENT ON COLUMN extraschool_one_report_day.nb_m_childs IS 'Nb m childs';

COMMENT ON COLUMN extraschool_one_report_day.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_one_report_day.nb_p_childs IS 'Nb p childs';

CREATE TABLE extraschool_one_report_day_child_rel (
	one_report_day_id integer NOT NULL,
	child_id integer NOT NULL
);

COMMENT ON TABLE extraschool_one_report_day_child_rel IS 'RELATION BETWEEN extraschool_one_report_day AND extraschool_child';

CREATE TABLE extraschool_prestation_times_encodage_manuel (
	id integer DEFAULT nextval('extraschool_prestation_times_encodage_manuel_id_seq'::regclass) NOT NULL,
	comment text,
	create_uid integer,
	create_date timestamp without time zone,
	place_id integer NOT NULL,
	write_uid integer,
	write_date timestamp without time zone,
	date_of_the_day date NOT NULL
);

COMMENT ON TABLE extraschool_prestation_times_encodage_manuel IS 'extraschool.prestation_times_encodage_manuel';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.comment IS 'Comment';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.place_id IS 'Place id';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.date_of_the_day IS 'Date of the day';

CREATE TABLE extraschool_prestation_times_manuel (
	id integer DEFAULT nextval('extraschool_prestation_times_manuel_id_seq'::regclass) NOT NULL,
	comment text,
	create_uid integer,
	create_date timestamp without time zone,
	prestation_time_entry double precision,
	write_uid integer,
	prestation_times_encodage_manuel_id integer,
	write_date timestamp without time zone,
	child_id integer NOT NULL,
	prestation_time_exit double precision
);

COMMENT ON TABLE extraschool_prestation_times_manuel IS 'extraschool.prestation_times_manuel';

COMMENT ON COLUMN extraschool_prestation_times_manuel.comment IS 'Comment';

COMMENT ON COLUMN extraschool_prestation_times_manuel.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestation_times_manuel.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestation_times_manuel.prestation_time_entry IS 'Entry Time';

COMMENT ON COLUMN extraschool_prestation_times_manuel.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestation_times_manuel.prestation_times_encodage_manuel_id IS 'encodage manuel';

COMMENT ON COLUMN extraschool_prestation_times_manuel.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_prestation_times_manuel.child_id IS 'Child id';

COMMENT ON COLUMN extraschool_prestation_times_manuel.prestation_time_exit IS 'Exit Time';

CREATE TABLE extraschool_prestation_times_of_the_day (
	id integer DEFAULT nextval('extraschool_prestation_times_of_the_day_id_seq'::regclass) NOT NULL,
	comment text,
	create_uid integer,
	create_date timestamp without time zone,
	write_uid integer,
	write_date timestamp without time zone,
	date_of_the_day date NOT NULL,
	verified boolean,
	child_id integer NOT NULL
);

COMMENT ON TABLE extraschool_prestation_times_of_the_day IS 'extraschool.prestation_times_of_the_day';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.comment IS 'Comment';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.date_of_the_day IS 'Date of the day';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.verified IS 'Verified';

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.child_id IS 'Child id';

CREATE TABLE extraschool_prestationscheck_wizard_place_rel (
	prestationscheck_wizard_id integer NOT NULL,
	place_id integer NOT NULL
);

COMMENT ON TABLE extraschool_prestationscheck_wizard_place_rel IS 'RELATION BETWEEN extraschool_prestationscheck_wizard AND extraschool_place';

CREATE TABLE extraschool_price_list (
	id integer DEFAULT nextval('extraschool_price_list_id_seq'::regclass) NOT NULL,
	create_uid integer,
	create_date timestamp without time zone,
	name character varying(50),
	write_uid integer,
	write_date timestamp without time zone
);

COMMENT ON TABLE extraschool_price_list IS 'Activities price list';

COMMENT ON COLUMN extraschool_price_list.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_price_list.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_price_list.name IS 'Name';

COMMENT ON COLUMN extraschool_price_list.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_price_list.write_date IS 'Last Updated on';

CREATE TABLE extraschool_price_list_version (
	id integer DEFAULT nextval('extraschool_price_list_version_id_seq'::regclass) NOT NULL,
	validity_to date,
	create_uid integer,
	price_list_id integer,
	create_date timestamp without time zone,
	name character varying(50),
	price numeric,
	validity_from date,
	write_date timestamp without time zone,
	write_uid integer,
	period_duration integer
);

COMMENT ON TABLE extraschool_price_list_version IS 'Activities price list version';

COMMENT ON COLUMN extraschool_price_list_version.validity_to IS 'Validity to';

COMMENT ON COLUMN extraschool_price_list_version.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_price_list_version.price_list_id IS 'Price list';

COMMENT ON COLUMN extraschool_price_list_version.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_price_list_version.name IS 'Name';

COMMENT ON COLUMN extraschool_price_list_version.price IS 'Price';

COMMENT ON COLUMN extraschool_price_list_version.validity_from IS 'Validity from';

COMMENT ON COLUMN extraschool_price_list_version.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_price_list_version.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_price_list_version.period_duration IS 'Period Duration';

CREATE TABLE extraschool_timecorrection_wizard_place_rel (
	prestationscheck_wizard_id integer NOT NULL,
	place_id integer NOT NULL
);

COMMENT ON TABLE extraschool_timecorrection_wizard_place_rel IS 'RELATION BETWEEN extraschool_timecorrection_wizard AND extraschool_place';

ALTER TABLE extraschool_activity
	ADD COLUMN parent_id integer,
	ADD COLUMN price_list_id integer,
	ADD COLUMN root_id integer,
	ADD COLUMN default_from_to character varying,
	ALTER COLUMN name TYPE character varying(100) /* TYPE change - table: extraschool_activity original: character varying(50) new: character varying(100) */,
	ALTER COLUMN name SET NOT NULL;

COMMENT ON COLUMN extraschool_activity.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activity.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activity.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activity.parent_id IS 'Parent';

COMMENT ON COLUMN extraschool_activity.price_list_id IS 'Price List';

COMMENT ON COLUMN extraschool_activity.root_id IS 'Root';

COMMENT ON COLUMN extraschool_activity.default_from_to IS 'Default From To';

COMMENT ON COLUMN extraschool_activity.write_date IS 'Last Updated on';

COMMENT ON TABLE extraschool_activity_childposition_rel IS 'RELATION BETWEEN extraschool_discount AND extraschool_childposition';

COMMENT ON COLUMN extraschool_activitycategory.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activitycategory.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activitycategory.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activitycategory.write_date IS 'Last Updated on';

ALTER TABLE extraschool_activitychildregistration
	ADD COLUMN place_id integer NOT NULL,
	ALTER COLUMN child_id SET NOT NULL,
	ALTER COLUMN registration_from SET NOT NULL,
	ALTER COLUMN registration_to SET NOT NULL;

COMMENT ON COLUMN extraschool_activitychildregistration.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activitychildregistration.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activitychildregistration.place_id IS 'Place';

COMMENT ON COLUMN extraschool_activitychildregistration.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activitychildregistration.write_date IS 'Last Updated on';

ALTER TABLE extraschool_activityexclusiondates
	DROP COLUMN name;

COMMENT ON COLUMN extraschool_activityexclusiondates.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activityexclusiondates.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activityexclusiondates.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activityexclusiondates.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_activityplanneddate.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activityplanneddate.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activityplanneddate.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activityplanneddate.write_date IS 'Last Updated on';

ALTER TABLE extraschool_biller
	ALTER COLUMN name TYPE character varying(100) /* TYPE change - table: extraschool_biller original: character varying(20) new: character varying(100) */;

COMMENT ON COLUMN extraschool_biller.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_biller.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_biller.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_biller.write_date IS 'Last Updated on';

ALTER TABLE extraschool_child
	DROP COLUMN name,
	DROP COLUMN toto;

COMMENT ON COLUMN extraschool_child.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_child.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_child.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_child.write_date IS 'Last Updated on';

ALTER TABLE extraschool_childposition
	ALTER COLUMN name SET NOT NULL,
	ALTER COLUMN "position" SET NOT NULL;

COMMENT ON COLUMN extraschool_childposition.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_childposition.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_childposition.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_childposition.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_childsimport.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_childsimport.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_childsimport.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_childsimport.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_childsimportfilter.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_childsimportfilter.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_childsimportfilter.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_childsimportfilter.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_childsworkbook_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_childsworkbook_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_childsworkbook_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_childsworkbook_wizard.write_date IS 'Last Updated on';

ALTER TABLE extraschool_childtype
	ALTER COLUMN name SET NOT NULL;

COMMENT ON COLUMN extraschool_childtype.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_childtype.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_childtype.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_childtype.write_date IS 'Last Updated on';

ALTER TABLE extraschool_class
	ALTER COLUMN name SET NOT NULL;

COMMENT ON COLUMN extraschool_class.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_class.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_class.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_class.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_coda.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_coda.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_coda.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_coda.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_discount.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_discount.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_discount.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_discount.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_discountrule.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_discountrule.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_discountrule.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_discountrule.write_date IS 'Last Updated on';

ALTER TABLE extraschool_guardian
	DROP COLUMN name;

COMMENT ON COLUMN extraschool_guardian.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_guardian.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_guardian.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_guardian.write_date IS 'Last Updated on';

ALTER TABLE extraschool_guardianprestationtimes
	DROP COLUMN "ES",
	ADD COLUMN es character varying;

COMMENT ON COLUMN extraschool_guardianprestationtimes.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_guardianprestationtimes.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_guardianprestationtimes.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_guardianprestationtimes.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_guardianprestationtimes.es IS 'ES';

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_importlevelrule.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_importlevelrule.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_importlevelrule.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_importlevelrule.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_importreject.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_importreject.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_importreject.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_importreject.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_initupdate_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_initupdate_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_initupdate_wizard.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_initupdate_wizard.write_uid IS 'Last Updated by';

ALTER TABLE extraschool_invoice
	ADD COLUMN payment_term date,
	ADD COLUMN period_to date,
	ADD COLUMN period_from date,
	ADD COLUMN activitycategoryid integer;

COMMENT ON COLUMN extraschool_invoice.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_invoice.payment_term IS 'biller_id.payment_term';

COMMENT ON COLUMN extraschool_invoice.period_to IS 'biller_id.period_to';

COMMENT ON COLUMN extraschool_invoice.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_invoice.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_invoice.period_from IS 'biller_id.period_from';

COMMENT ON COLUMN extraschool_invoice.activitycategoryid IS 'Activity Category';

COMMENT ON COLUMN extraschool_invoice.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_invoice_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_invoice_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_invoice_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_invoice_wizard.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_invoicedprestations.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_invoicedprestations.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_invoicedprestations.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_invoicedprestations.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_level.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_level.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_level.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_level.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_level.leveltype IS 'Level type';

COMMENT ON COLUMN extraschool_mainsettings.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_mainsettings.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_mainsettings.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_mainsettings.write_date IS 'Last Updated on';

ALTER TABLE extraschool_parent
	ADD COLUMN one_subvention_type character varying NOT NULL;

COMMENT ON COLUMN extraschool_parent.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_parent.one_subvention_type IS 'One subvention type';

COMMENT ON COLUMN extraschool_parent.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_parent.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_parent.write_date IS 'Last Updated on';

ALTER TABLE extraschool_payment
	DROP COLUMN addr1,
	DROP COLUMN addr2;

COMMENT ON COLUMN extraschool_payment.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_payment.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_payment.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_payment.write_date IS 'Last Updated on';

ALTER TABLE extraschool_pdaprestationtimes
	DROP COLUMN "ES",
	ADD COLUMN prestation_times_of_the_day_id integer,
	ADD COLUMN es character varying;

COMMENT ON COLUMN extraschool_pdaprestationtimes.prestation_times_of_the_day_id IS 'Prestation of the day';

COMMENT ON COLUMN extraschool_pdaprestationtimes.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_pdaprestationtimes.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_pdaprestationtimes.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_pdaprestationtimes.es IS 'ES';

COMMENT ON COLUMN extraschool_pdaprestationtimes.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_place.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_place.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_place.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_place.write_date IS 'Last Updated on';

ALTER TABLE extraschool_prestationscheck_wizard
	DROP COLUMN childid,
	DROP COLUMN currentdate,
	DROP COLUMN prestation_time,
	DROP COLUMN es,
	ALTER COLUMN period_to DROP NOT NULL,
	ALTER COLUMN period_from DROP NOT NULL;

COMMENT ON COLUMN extraschool_prestationscheck_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.activitycategory IS 'Activitycategory';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.write_date IS 'Last Updated on';

ALTER TABLE extraschool_prestationtimes
	DROP COLUMN activityid,
	DROP COLUMN activitycategoryid,
	DROP COLUMN "ES",
	ADD COLUMN prestation_times_of_the_day_id integer,
	ADD COLUMN error_msg character varying(255),
	ADD COLUMN exit_all boolean,
	ADD COLUMN activity_occurrence_id integer,
	ADD COLUMN es character varying;

COMMENT ON COLUMN extraschool_prestationtimes.prestation_times_of_the_day_id IS 'Prestation of the day';

COMMENT ON COLUMN extraschool_prestationtimes.error_msg IS 'Error';

COMMENT ON COLUMN extraschool_prestationtimes.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestationtimes.exit_all IS 'Exit all';

COMMENT ON COLUMN extraschool_prestationtimes.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestationtimes.activity_occurrence_id IS 'Activity occurrence';

COMMENT ON COLUMN extraschool_prestationtimes.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_prestationtimes.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestationtimes.es IS 'es';

COMMENT ON COLUMN extraschool_qrcodes_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_qrcodes_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_qrcodes_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_qrcodes_wizard.write_date IS 'Last Updated on';

ALTER TABLE extraschool_reject
	DROP COLUMN addr1,
	DROP COLUMN addr2;

COMMENT ON COLUMN extraschool_reject.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_reject.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_reject.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_reject.write_date IS 'Last Updated on';

ALTER TABLE extraschool_reminder
	ADD COLUMN term date,
	ADD COLUMN activitycategoryid integer,
	ADD COLUMN transmissiondate date;

COMMENT ON COLUMN extraschool_reminder.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_reminder.term IS 'remindersjournalid.term';

COMMENT ON COLUMN extraschool_reminder.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_reminder.activitycategoryid IS 'Activity Category';

COMMENT ON COLUMN extraschool_reminder.transmissiondate IS 'remindersjournalid.transmissiondate';

COMMENT ON COLUMN extraschool_reminder.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_reminder.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_remindersjournal.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_remindersjournal.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_remindersjournal.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_remindersjournal.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_remindertype.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_remindertype.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_remindertype.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_remindertype.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_scheduledtasks.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_scheduledtasks.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_scheduledtasks.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_scheduledtasks.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_school.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_school.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_school.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_school.write_date IS 'Last Updated on';

ALTER TABLE extraschool_schoolimplantation
	ALTER COLUMN name TYPE character varying(100) /* TYPE change - table: extraschool_schoolimplantation original: character varying(50) new: character varying(100) */,
	ALTER COLUMN street TYPE character varying(100) /* TYPE change - table: extraschool_schoolimplantation original: character varying(50) new: character varying(100) */;

COMMENT ON COLUMN extraschool_schoolimplantation.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_schoolimplantation.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_schoolimplantation.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_schoolimplantation.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_smartphone.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_smartphone.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_smartphone.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_smartphone.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_timecorrection_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_timecorrection_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_timecorrection_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_timecorrection_wizard.write_date IS 'Last Updated on';

ALTER SEQUENCE extraschool_activityoccurrence_id_seq
	OWNED BY extraschool_activityoccurrence.id;

ALTER SEQUENCE extraschool_one_report_day_id_seq
	OWNED BY extraschool_one_report_day.id;

ALTER SEQUENCE extraschool_one_report_id_seq
	OWNED BY extraschool_one_report.id;

ALTER SEQUENCE extraschool_prestation_times_encodage_manuel_id_seq
	OWNED BY extraschool_prestation_times_encodage_manuel.id;

ALTER SEQUENCE extraschool_prestation_times_manuel_id_seq
	OWNED BY extraschool_prestation_times_manuel.id;

ALTER SEQUENCE extraschool_prestation_times_of_the_day_id_seq
	OWNED BY extraschool_prestation_times_of_the_day.id;

ALTER SEQUENCE extraschool_price_list_id_seq
	OWNED BY extraschool_price_list.id;

ALTER SEQUENCE extraschool_price_list_version_id_seq
	OWNED BY extraschool_price_list_version.id;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_one_report
	ADD CONSTRAINT extraschool_one_report_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_one_report_day
	ADD CONSTRAINT extraschool_one_report_day_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_prestation_times_encodage_manuel
	ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_prestation_times_manuel
	ADD CONSTRAINT extraschool_prestation_times_manuel_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_prestation_times_of_the_day
	ADD CONSTRAINT extraschool_prestation_times_of_the_day_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_price_list
	ADD CONSTRAINT extraschool_price_list_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_activity
	ADD CONSTRAINT extraschool_activity_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activity
	ADD CONSTRAINT extraschool_activity_price_list_id_fkey FOREIGN KEY (price_list_id) REFERENCES extraschool_price_list(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activity
	ADD CONSTRAINT extraschool_activity_root_id_fkey FOREIGN KEY (root_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activity_childposition_rel
	ADD CONSTRAINT extraschool_activity_childposition_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_discount(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activitychildregistration
	ADD CONSTRAINT extraschool_activitychildregistration_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_activityid_fkey FOREIGN KEY (activityid) REFERENCES extraschool_activity(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activityoccurrence_cild_rel
	ADD CONSTRAINT extraschool_activityoccurrenc_activityoccurrence_id_child_i_key UNIQUE (activityoccurrence_id, child_id);

ALTER TABLE extraschool_activityoccurrence_cild_rel
	ADD CONSTRAINT extraschool_activityoccurrence_cild__activityoccurrence_id_fkey FOREIGN KEY (activityoccurrence_id) REFERENCES extraschool_activityoccurrence(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activityoccurrence_cild_rel
	ADD CONSTRAINT extraschool_activityoccurrence_cild_rel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE CASCADE;

ALTER TABLE extraschool_child
	ADD CONSTRAINT extraschool_child_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE RESTRICT;

ALTER TABLE extraschool_childsworkbook_wizard
	ADD CONSTRAINT extraschool_childsworkbook_wizard_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;

ALTER TABLE extraschool_childsworkbook_wizard
	ADD CONSTRAINT extraschool_childsworkbook_wizard_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_guardianprestationtimes_wizard
	ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_guardianid_fkey FOREIGN KEY (guardianid) REFERENCES extraschool_guardian(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoice_wizard
	ADD CONSTRAINT extraschool_invoice_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoice_wizard_schoolimplantation_rel
	ADD CONSTRAINT extraschool_invoice_wizard_sc_invoice_wizard_id_schoolimpla_key UNIQUE (invoice_wizard_id, schoolimplantation_id);

ALTER TABLE extraschool_invoice_wizard_schoolimplantation_rel
	ADD CONSTRAINT extraschool_invoice_wizard_schoolimp_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;

ALTER TABLE extraschool_invoice_wizard_schoolimplantation_rel
	ADD CONSTRAINT extraschool_invoice_wizard_schoolimplant_invoice_wizard_id_fkey FOREIGN KEY (invoice_wizard_id) REFERENCES extraschool_invoice_wizard(id) ON DELETE CASCADE;

ALTER TABLE extraschool_one_report
	ADD CONSTRAINT extraschool_one_report_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

ALTER TABLE extraschool_one_report
	ADD CONSTRAINT extraschool_one_report_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_one_report
	ADD CONSTRAINT extraschool_one_report_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_one_report
	ADD CONSTRAINT extraschool_one_report_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_one_report_day
	ADD CONSTRAINT extraschool_one_report_day_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_one_report_day
	ADD CONSTRAINT extraschool_one_report_day_one_report_id_fkey FOREIGN KEY (one_report_id) REFERENCES extraschool_one_report(id) ON DELETE CASCADE;

ALTER TABLE extraschool_one_report_day
	ADD CONSTRAINT extraschool_one_report_day_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_one_report_day_child_rel
	ADD CONSTRAINT extraschool_one_report_day_child_one_report_day_id_child_id_key UNIQUE (one_report_day_id, child_id);

ALTER TABLE extraschool_one_report_day_child_rel
	ADD CONSTRAINT extraschool_one_report_day_child_rel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE CASCADE;

ALTER TABLE extraschool_one_report_day_child_rel
	ADD CONSTRAINT extraschool_one_report_day_child_rel_one_report_day_id_fkey FOREIGN KEY (one_report_day_id) REFERENCES extraschool_one_report_day(id) ON DELETE CASCADE;

ALTER TABLE extraschool_pdaprestationtimes
	ADD CONSTRAINT extraschool_pdaprestationtime_prestation_times_of_the_day__fkey FOREIGN KEY (prestation_times_of_the_day_id) REFERENCES extraschool_prestation_times_of_the_day(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_encodage_manuel
	ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_encodage_manuel
	ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_encodage_manuel
	ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_manuel
	ADD CONSTRAINT extraschool_prestation_times__prestation_times_encodage_ma_fkey FOREIGN KEY (prestation_times_encodage_manuel_id) REFERENCES extraschool_prestation_times_encodage_manuel(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_manuel
	ADD CONSTRAINT extraschool_prestation_times_manuel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_manuel
	ADD CONSTRAINT extraschool_prestation_times_manuel_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_manuel
	ADD CONSTRAINT extraschool_prestation_times_manuel_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_of_the_day
	ADD CONSTRAINT extraschool_prestation_times_of_the_day_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_of_the_day
	ADD CONSTRAINT extraschool_prestation_times_of_the_day_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestation_times_of_the_day
	ADD CONSTRAINT extraschool_prestation_times_of_the_day_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestationscheck_wizard
	ADD CONSTRAINT extraschool_prestationscheck_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestationscheck_wizard_place_rel
	ADD CONSTRAINT extraschool_prestationscheck__prestationscheck_wizard_id_pl_key UNIQUE (prestationscheck_wizard_id, place_id);

ALTER TABLE extraschool_prestationscheck_wizard_place_rel
	ADD CONSTRAINT extraschool_prestationscheck_wi_prestationscheck_wizard_id_fkey FOREIGN KEY (prestationscheck_wizard_id) REFERENCES extraschool_prestationscheck_wizard(id) ON DELETE CASCADE;

ALTER TABLE extraschool_prestationscheck_wizard_place_rel
	ADD CONSTRAINT extraschool_prestationscheck_wizard_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_activity_occurrence_id_fkey FOREIGN KEY (activity_occurrence_id) REFERENCES extraschool_activityoccurrence(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE RESTRICT;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_prestation_times_of_the_day_id_fkey FOREIGN KEY (prestation_times_of_the_day_id) REFERENCES extraschool_prestation_times_of_the_day(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list
	ADD CONSTRAINT extraschool_price_list_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list
	ADD CONSTRAINT extraschool_price_list_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_price_list_id_fkey FOREIGN KEY (price_list_id) REFERENCES extraschool_price_list(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_taxcertificates_wizard
	ADD CONSTRAINT extraschool_taxcertificates_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

ALTER TABLE extraschool_taxcertificates_wizard
	ADD CONSTRAINT extraschool_taxcertificates_wizard_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE SET NULL;

ALTER TABLE extraschool_timecorrection_wizard_place_rel
	ADD CONSTRAINT extraschool_timecorrection_wi_prestationscheck_wizard_id_pl_key UNIQUE (prestationscheck_wizard_id, place_id);

ALTER TABLE extraschool_timecorrection_wizard_place_rel
	ADD CONSTRAINT extraschool_timecorrection_wiza_prestationscheck_wizard_id_fkey FOREIGN KEY (prestationscheck_wizard_id) REFERENCES extraschool_timecorrection_wizard(id) ON DELETE CASCADE;

ALTER TABLE extraschool_timecorrection_wizard_place_rel
	ADD CONSTRAINT extraschool_timecorrection_wizard_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;

CREATE INDEX extraschool_activityoccurrence_cild_rel_activityoccurrence_id_i ON extraschool_activityoccurrence_cild_rel USING btree (activityoccurrence_id);

CREATE INDEX extraschool_activityoccurrence_cild_rel_child_id_index ON extraschool_activityoccurrence_cild_rel USING btree (child_id);

CREATE INDEX extraschool_invoice_wizard_schoolimplantation_rel_invoice_wizar ON extraschool_invoice_wizard_schoolimplantation_rel USING btree (invoice_wizard_id);

CREATE INDEX extraschool_invoice_wizard_schoolimplantation_rel_schoolimplant ON extraschool_invoice_wizard_schoolimplantation_rel USING btree (schoolimplantation_id);

CREATE INDEX extraschool_one_report_day_child_rel_child_id_index ON extraschool_one_report_day_child_rel USING btree (child_id);

CREATE INDEX extraschool_one_report_day_child_rel_one_report_day_id_index ON extraschool_one_report_day_child_rel USING btree (one_report_day_id);

CREATE INDEX extraschool_prestationscheck_wizard_place_rel_place_id_index ON extraschool_prestationscheck_wizard_place_rel USING btree (place_id);

CREATE INDEX extraschool_prestationscheck_wizard_place_rel_prestationscheck_ ON extraschool_prestationscheck_wizard_place_rel USING btree (prestationscheck_wizard_id);

CREATE INDEX extraschool_prestationtimes_es_index ON extraschool_prestationtimes USING btree (es);

CREATE INDEX extraschool_timecorrection_wizard_place_rel_place_id_index ON extraschool_timecorrection_wizard_place_rel USING btree (place_id);

CREATE INDEX extraschool_timecorrection_wizard_place_rel_prestationscheck_wi ON extraschool_timecorrection_wizard_place_rel USING btree (prestationscheck_wizard_id);
