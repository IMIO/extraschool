
ALTER TABLE extraschool_activity_activityexclusiondates_rel
	DROP CONSTRAINT extraschool_activity_activit_activity_id_activityexclusion_key;

ALTER TABLE extraschool_activity_activityexclusiondates_rel
	DROP CONSTRAINT extraschool_activity_activityex_activityexclusiondates_id_fkey;

ALTER TABLE extraschool_activity_activityexclusiondates_rel
	DROP CONSTRAINT extraschool_activity_activityexclusiondates_r_activity_id_fkey;

ALTER TABLE extraschool_activity_activityplanneddate_rel
	DROP CONSTRAINT extraschool_activity_activit_activityplanneddate_id_activi_key;

ALTER TABLE extraschool_activity_activityplanneddate_rel
	DROP CONSTRAINT extraschool_activity_activityplann_activityplanneddate_id_fkey;

ALTER TABLE extraschool_activity_childposition_rel
	DROP CONSTRAINT extraschool_activity_childpos_activity_id_childposition_id_key;

ALTER TABLE extraschool_activity_childposition_rel
	DROP CONSTRAINT extraschool_activity_childposition_rel_activity_id_fkey;

ALTER TABLE extraschool_activity_childtype_rel
	DROP CONSTRAINT extraschool_activity_childtype_re_activity_id_childtype_id_key;

ALTER TABLE extraschool_activity_schoolimplantation_rel
	DROP CONSTRAINT extraschool_activity_schooli_activity_id_schoolimplantatio_key;

ALTER TABLE extraschool_activity_schoolimplantation_rel
	DROP CONSTRAINT extraschool_activity_schoolimplanta_schoolimplantation_id_fkey;

ALTER TABLE extraschool_activitycategory_place_rel
	DROP CONSTRAINT extraschool_activitycategory__activitycategory_id_place_id_key;

ALTER TABLE extraschool_activitycategory_place_rel
	DROP CONSTRAINT extraschool_activitycategory_place_re_activitycategory_id_fkey;

ALTER TABLE extraschool_child
	DROP CONSTRAINT extraschool_child_parentid_fkey;

ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel
	DROP CONSTRAINT extraschool_childsimportfilt_childsimportfilter_id_importl_key;

ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel
	DROP CONSTRAINT extraschool_childsimportfilter_impo_childsimportfilter_id_fkey;

ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel
	DROP CONSTRAINT extraschool_childsimportfilter_importl_importlevelrule_id_fkey;

ALTER TABLE extraschool_childsworkbook_wizard
	DROP CONSTRAINT extraschool_childsworkbook_wizard_child_id_fkey;

ALTER TABLE extraschool_childsworkbook_wizard
	DROP CONSTRAINT extraschool_childsworkbook_wizard_placeid_fkey;

ALTER TABLE extraschool_childsworkbook_wizard
	DROP CONSTRAINT extraschool_childsworkbook_wizard_schoolimplantation_fkey;

ALTER TABLE extraschool_class
	DROP CONSTRAINT extraschool_class_titular_fkey;

ALTER TABLE extraschool_discount_childtype_rel
	DROP CONSTRAINT extraschool_discount_childtype_re_discount_id_childtype_id_key;

ALTER TABLE extraschool_discount_discountrule_rel
	DROP CONSTRAINT extraschool_discount_discountr_discount_id_discountrule_id_key;

ALTER TABLE extraschool_guardianprestationtimes_wizard
	DROP CONSTRAINT extraschool_guardianprestationtimes_wizard_guardianid_fkey;

ALTER TABLE extraschool_invoice_wizard
	DROP CONSTRAINT extraschool_invoice_wizard_activitycategory_fkey;

ALTER TABLE extraschool_mainsettings
	DROP CONSTRAINT extraschool_mainsettings_levelbeforedisable_fkey;

ALTER TABLE extraschool_place_schoolimplantation_rel
	DROP CONSTRAINT extraschool_place_schoolimpl_place_id_schoolimplantation_i_key;

ALTER TABLE extraschool_place_schoolimplantation_rel
	DROP CONSTRAINT extraschool_place_schoolimplantatio_schoolimplantation_id_fkey;

ALTER TABLE extraschool_prestationscheck_wizard
	DROP CONSTRAINT extraschool_prestationscheck_wizard_activitycategory_fkey;

ALTER TABLE extraschool_prestationscheck_wizard
	DROP CONSTRAINT extraschool_prestationscheck_wizard_childid_fkey;

ALTER TABLE extraschool_prestationscheck_wizard
	DROP CONSTRAINT extraschool_prestationscheck_wizard_schoolimplantationid_fkey;

ALTER TABLE extraschool_prestationtimes
	DROP CONSTRAINT extraschool_prestationtimes_activitycategoryid_fkey;

ALTER TABLE extraschool_prestationtimes
	DROP CONSTRAINT extraschool_prestationtimes_activityid_fkey;

ALTER TABLE extraschool_prestationtimes
	DROP CONSTRAINT extraschool_prestationtimes_childid_fkey;

ALTER TABLE extraschool_remindersjournal_biller_rel
	DROP CONSTRAINT extraschool_remindersjournal_remindersjournal_id_biller_id_key;

ALTER TABLE extraschool_remindersjournal_biller_rel
	DROP CONSTRAINT extraschool_remindersjournal_biller_r_remindersjournal_id_fkey;

ALTER TABLE extraschool_smartphone_activitycategory_rel
	DROP CONSTRAINT extraschool_smartphone_activ_smartphone_id_activitycategor_key;

ALTER TABLE extraschool_smartphone_activitycategory_rel
	DROP CONSTRAINT extraschool_smartphone_activitycatego_activitycategory_id_fkey;

ALTER TABLE extraschool_taxcertificates_wizard
	DROP CONSTRAINT extraschool_taxcertificates_wizard_activitycategory_fkey;

ALTER TABLE extraschool_taxcertificates_wizard
	DROP CONSTRAINT extraschool_taxcertificates_wizard_parentid_fkey;

DROP INDEX extraschool_activity_activityexclusiondates_rel_activity_id_in;

DROP INDEX extraschool_activity_activityexclusiondates_rel_activityexclus;

DROP INDEX extraschool_activity_activityplanneddate_rel_activityplannedda;

DROP INDEX extraschool_activity_schoolimplantation_rel_schoolimplantation;

DROP INDEX extraschool_activitycategory_place_rel_activitycategory_id_ind;

DROP INDEX extraschool_childsimportfilter_importlevelrule_rel_childsimpor;

DROP INDEX extraschool_childsimportfilter_importlevelrule_rel_importlevel;

DROP INDEX extraschool_invoicedprestations_quantity_index;

DROP INDEX extraschool_place_schoolimplantation_rel_schoolimplantation_id;

DROP INDEX "extraschool_prestationtimes_ES_index";

DROP INDEX extraschool_remindersjournal_biller_rel_remindersjournal_id_in;

DROP INDEX extraschool_smartphone_activitycategory_rel_activitycategory_i;

DROP INDEX extraschool_smartphone_activitycategory_rel_smartphone_id_inde;

DROP TABLE extraschool_quotaadjustment;

DROP TABLE extraschool_copierquota;

DROP TABLE extraschool_copiercode;

DROP TABLE extraschool_file_wizard;

DROP TABLE extraschool_teacher;

DROP TABLE extraschool_activity_child_rel;

DROP TABLE extraschool_activitycategory_schoolimplantation_rel;

DROP TABLE extraschool_childsimportfilter_importchildtyperule_rel;

DROP TABLE extraschool_importchildtyperule;

DROP TABLE extraschool_prestations_wizard;

DROP TABLE extraschool_reminders_wizard;

DROP TABLE extraschool_smartphone_schoolimplantation_rel;

DROP TABLE extraschool_stats_wizard;

DROP TABLE extraschool_statsone_wizard;

DROP SEQUENCE extraschool_copiercode_id_seq;

DROP SEQUENCE extraschool_copierquota_id_seq;

DROP SEQUENCE extraschool_file_wizard_id_seq;

DROP SEQUENCE extraschool_quotaadjustment_id_seq;

DROP SEQUENCE extraschool_teacher_id_seq;

DROP SEQUENCE extraschool_importchildtyperule_id_seq;

DROP SEQUENCE extraschool_prestations_wizard_id_seq;

DROP SEQUENCE extraschool_reminders_wizard_id_seq;

DROP SEQUENCE extraschool_stats_wizard_id_seq;

DROP SEQUENCE extraschool_statsone_wizard_id_seq;

CREATE SEQUENCE extraschool_activityoccurrence_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE SEQUENCE extraschool_inline_report_id_seq
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

CREATE SEQUENCE extraschool_onereport_settings_id_seq
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

CREATE SEQUENCE extraschool_report_id_seq
	START WITH 1
	INCREMENT BY 1
	NO MAXVALUE
	NO MINVALUE
	CACHE 1;

CREATE TABLE extraschool_activity_pricelist_rel (
	extraschool_price_list_version_id integer NOT NULL,
	extraschool_activity_id integer NOT NULL
);

COMMENT ON TABLE extraschool_activity_pricelist_rel IS 'RELATION BETWEEN extraschool_price_list_version AND extraschool_activity';

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
	prest_from double precision,
	activity_category_id integer
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

COMMENT ON COLUMN extraschool_activityoccurrence.activity_category_id IS 'Category';

CREATE TABLE extraschool_activityoccurrence_cild_rel (
	activityoccurrence_id integer NOT NULL,
	child_id integer NOT NULL
);

COMMENT ON TABLE extraschool_activityoccurrence_cild_rel IS 'RELATION BETWEEN extraschool_activityoccurrence AND extraschool_child';

CREATE TABLE extraschool_childposition_pricelist_rel (
	extraschool_price_list_version_id integer NOT NULL,
	extraschool_childposition_id integer NOT NULL
);

COMMENT ON TABLE extraschool_childposition_pricelist_rel IS 'RELATION BETWEEN extraschool_price_list_version AND extraschool_childposition';

CREATE TABLE extraschool_inline_report (
	id integer DEFAULT nextval('extraschool_inline_report_id_seq'::regclass) NOT NULL,
	create_uid integer,
	create_date timestamp without time zone,
	name character varying(50) NOT NULL,
	"sequence" integer,
	"section" character varying,
	visibility character varying,
	write_uid integer,
	write_date timestamp without time zone,
	inline_report_id integer NOT NULL,
	report_id integer
);

COMMENT ON TABLE extraschool_inline_report IS 'Report';

COMMENT ON COLUMN extraschool_inline_report.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_inline_report.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_inline_report.name IS 'Name';

COMMENT ON COLUMN extraschool_inline_report."sequence" IS 'Sequence';

COMMENT ON COLUMN extraschool_inline_report."section" IS 'Section';

COMMENT ON COLUMN extraschool_inline_report.visibility IS 'Visibility';

COMMENT ON COLUMN extraschool_inline_report.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_inline_report.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_inline_report.inline_report_id IS 'Report';

COMMENT ON COLUMN extraschool_inline_report.report_id IS 'Report';

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
	nb_p_childs integer,
	report bytea
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

COMMENT ON COLUMN extraschool_one_report.report IS 'Report';

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

CREATE TABLE extraschool_onereport_settings (
	id integer DEFAULT nextval('extraschool_onereport_settings_id_seq'::regclass) NOT NULL,
	create_uid integer,
	create_date timestamp without time zone,
	one_logo bytea,
	write_uid integer,
	report_template bytea,
	write_date timestamp without time zone,
	validity_to date,
	validity_from date
);

COMMENT ON TABLE extraschool_onereport_settings IS 'extraschool.onereport.settings';

COMMENT ON COLUMN extraschool_onereport_settings.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_onereport_settings.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_onereport_settings.one_logo IS 'One logo';

COMMENT ON COLUMN extraschool_onereport_settings.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_onereport_settings.report_template IS 'Report template';

COMMENT ON COLUMN extraschool_onereport_settings.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_onereport_settings.validity_to IS 'Validity to';

COMMENT ON COLUMN extraschool_onereport_settings.validity_from IS 'Validity from';

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
	parent_id integer,
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

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.parent_id IS 'Parent';

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
	price_list_id integer,
	name character varying(50),
	create_uid integer,
	price numeric,
	period_duration integer,
	validity_from date,
	write_date timestamp without time zone,
	period_tolerance integer,
	create_date timestamp without time zone,
	write_uid integer,
	validity_to date,
	child_type_id integer
);

COMMENT ON TABLE extraschool_price_list_version IS 'Activities price list version';

COMMENT ON COLUMN extraschool_price_list_version.price_list_id IS 'Price list';

COMMENT ON COLUMN extraschool_price_list_version.name IS 'Name';

COMMENT ON COLUMN extraschool_price_list_version.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_price_list_version.price IS 'Price';

COMMENT ON COLUMN extraschool_price_list_version.period_duration IS 'Period Duration';

COMMENT ON COLUMN extraschool_price_list_version.validity_from IS 'Validity from';

COMMENT ON COLUMN extraschool_price_list_version.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_price_list_version.period_tolerance IS 'Period Tolerance';

COMMENT ON COLUMN extraschool_price_list_version.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_price_list_version.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_price_list_version.validity_to IS 'Validity to';

COMMENT ON COLUMN extraschool_price_list_version.child_type_id IS 'Child type';

CREATE TABLE extraschool_report (
	id integer DEFAULT nextval('extraschool_report_id_seq'::regclass) NOT NULL,
	create_uid integer,
	create_date timestamp without time zone,
	name character varying(50) NOT NULL,
	write_uid integer,
	write_date timestamp without time zone,
	report_type_id integer NOT NULL
);

COMMENT ON TABLE extraschool_report IS 'Report';

COMMENT ON COLUMN extraschool_report.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_report.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_report.name IS 'Name';

COMMENT ON COLUMN extraschool_report.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_report.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_report.report_type_id IS 'Report type';

CREATE TABLE extraschool_timecorrection_wizard_place_rel (
	prestationscheck_wizard_id integer NOT NULL,
	place_id integer NOT NULL
);

COMMENT ON TABLE extraschool_timecorrection_wizard_place_rel IS 'RELATION BETWEEN extraschool_timecorrection_wizard AND extraschool_place';

ALTER TABLE extraschool_activity
	DROP COLUMN minamount,
	DROP COLUMN maxamount,
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

COMMENT ON COLUMN extraschool_activity.short_name IS 'Short name';

COMMENT ON COLUMN extraschool_activity.root_id IS 'Root';

COMMENT ON COLUMN extraschool_activity.default_from_to IS 'Default From To';

COMMENT ON COLUMN extraschool_activity.price IS 'Price';

COMMENT ON COLUMN extraschool_activity.write_date IS 'Last Updated on';

COMMENT ON TABLE extraschool_activity_activityplanneddate_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_activityplanneddate';

COMMENT ON TABLE extraschool_activity_childposition_rel IS 'RELATION BETWEEN extraschool_discount AND extraschool_childposition';

ALTER TABLE extraschool_activitycategory
	DROP COLUMN daydiscountforbadgeusage,
	ADD COLUMN logo bytea,
	ADD COLUMN report_id integer,
	ADD COLUMN slogan character varying(50);

COMMENT ON COLUMN extraschool_activitycategory.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_activitycategory.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_activitycategory.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_activitycategory.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_activitycategory.logo IS 'Logo';

COMMENT ON COLUMN extraschool_activitycategory.report_id IS 'Report';

COMMENT ON COLUMN extraschool_activitycategory.slogan IS 'Slogan';

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
	DROP COLUMN name;

COMMENT ON COLUMN extraschool_child.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_child.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_child.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_child.write_date IS 'Last Updated on';

ALTER TABLE extraschool_childposition
	DROP COLUMN "Position",
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

ALTER TABLE extraschool_childsimportfilter
	DROP COLUMN childtypecolumn,
	DROP COLUMN childtypecolumnname,
	DROP COLUMN majchildtype;

COMMENT ON COLUMN extraschool_childsimportfilter.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_childsimportfilter.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_childsimportfilter.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_childsimportfilter.write_date IS 'Last Updated on';

ALTER TABLE extraschool_childsworkbook_wizard
	DROP COLUMN schoolimplantation;

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
	DROP COLUMN titular,
	DROP COLUMN oldid,
	ALTER COLUMN name SET NOT NULL;

COMMENT ON COLUMN extraschool_class.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_class.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_class.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_class.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_coda.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_coda.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_coda.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_coda.create_date IS 'Created on';

ALTER TABLE extraschool_discount
	DROP COLUMN oneofactivities;

COMMENT ON COLUMN extraschool_discount.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_discount.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_discount.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_discount.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_discountrule.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_discountrule.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_discountrule.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_discountrule.write_date IS 'Last Updated on';

ALTER TABLE extraschool_guardian
	DROP COLUMN name,
	ADD COLUMN weekly_schedule double precision;

COMMENT ON COLUMN extraschool_guardian.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_guardian.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_guardian.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_guardian.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_guardian.weekly_schedule IS 'Horaire hebdomadaire';

ALTER TABLE extraschool_guardianprestationtimes RENAME COLUMN "ES" TO es;

COMMENT ON COLUMN extraschool_guardianprestationtimes.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_guardianprestationtimes.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_guardianprestationtimes.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_guardianprestationtimes.guardianid IS 'Guardian';

COMMENT ON COLUMN extraschool_guardianprestationtimes.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_guardianprestationtimes.es IS 'ES';

ALTER TABLE extraschool_guardianprestationtimes_wizard
	ALTER COLUMN guardianid DROP NOT NULL;

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

ALTER TABLE extraschool_invoicedprestations
	ADD COLUMN child_position integer,
	ADD COLUMN activity_occurrence_id integer,
	ADD COLUMN duration integer,
	ADD COLUMN unit_price numeric,
	ADD COLUMN price_list_version_id integer,
	ADD COLUMN total_price numeric,
	ADD COLUMN period_tolerance integer,
	ADD COLUMN child_position_id integer,
	ADD COLUMN period_duration integer;

COMMENT ON COLUMN extraschool_invoicedprestations.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_invoicedprestations.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_invoicedprestations.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_invoicedprestations.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_invoicedprestations.child_position IS 'Child';

COMMENT ON COLUMN extraschool_invoicedprestations.activity_occurrence_id IS 'Activity occurrence';

COMMENT ON COLUMN extraschool_invoicedprestations.duration IS 'Duration';

COMMENT ON COLUMN extraschool_invoicedprestations.unit_price IS 'Price';

COMMENT ON COLUMN extraschool_invoicedprestations.price_list_version_id IS 'Price list version id';

COMMENT ON COLUMN extraschool_invoicedprestations.total_price IS 'Price';

COMMENT ON COLUMN extraschool_invoicedprestations.period_tolerance IS 'Period Tolerance';

COMMENT ON COLUMN extraschool_invoicedprestations.child_position_id IS 'Child';

COMMENT ON COLUMN extraschool_invoicedprestations.period_duration IS 'Period Duration';

COMMENT ON COLUMN extraschool_level.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_level.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_level.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_level.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_level.leveltype IS 'Level type';

ALTER TABLE extraschool_mainsettings
	DROP COLUMN leveldeterminationbirthdate,
	DROP COLUMN levelbeforedisable;

COMMENT ON COLUMN extraschool_mainsettings.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_mainsettings.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_mainsettings.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_mainsettings.write_date IS 'Last Updated on';

ALTER TABLE extraschool_parent
	DROP COLUMN numrn,
	ADD COLUMN one_subvention_type character varying NOT NULL;

COMMENT ON COLUMN extraschool_parent.remindersendmethod IS 'Reminder send method';

COMMENT ON COLUMN extraschool_parent.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_parent.one_subvention_type IS 'One subvention type';

COMMENT ON COLUMN extraschool_parent.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_parent.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_parent.email IS 'Email';

COMMENT ON COLUMN extraschool_parent.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_payment.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_payment.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_payment.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_payment.write_date IS 'Last Updated on';

ALTER TABLE extraschool_pdaprestationtimes RENAME COLUMN "ES" TO es;
ALTER TABLE extraschool_pdaprestationtimes
	ADD COLUMN prestation_times_of_the_day_id integer;

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
	DROP COLUMN schoolimplantationid,
	DROP COLUMN prestation_time,
	DROP COLUMN es,
	ALTER COLUMN period_to DROP NOT NULL,
	ALTER COLUMN period_from DROP NOT NULL;

COMMENT ON COLUMN extraschool_prestationscheck_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.activitycategory IS 'Activitycategory';

COMMENT ON COLUMN extraschool_prestationscheck_wizard.write_date IS 'Last Updated on';

ALTER TABLE extraschool_prestationtimes RENAME COLUMN activitycategoryid TO activity_category_id;
ALTER TABLE extraschool_prestationtimes RENAME COLUMN "ES" TO es;
ALTER TABLE extraschool_prestationtimes
	DROP COLUMN activityid,
	ADD COLUMN prestation_times_of_the_day_id integer,
	ADD COLUMN error_msg character varying(255),
	ADD COLUMN exit_all boolean,
	ADD COLUMN activity_occurrence_id integer,
	ADD COLUMN parent_id integer;

COMMENT ON COLUMN extraschool_prestationtimes.prestation_times_of_the_day_id IS 'Prestation of the day';

COMMENT ON COLUMN extraschool_prestationtimes.error_msg IS 'Error';

COMMENT ON COLUMN extraschool_prestationtimes.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_prestationtimes.exit_all IS 'Exit all';

COMMENT ON COLUMN extraschool_prestationtimes.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_prestationtimes.activity_occurrence_id IS 'Activity occurrence';

COMMENT ON COLUMN extraschool_prestationtimes.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_prestationtimes.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_prestationtimes.es IS 'es';

COMMENT ON COLUMN extraschool_prestationtimes.activity_category_id IS 'Category';

COMMENT ON COLUMN extraschool_prestationtimes.parent_id IS 'Parent';

ALTER TABLE extraschool_qrcodes_wizard
	DROP COLUMN qrcodes,
	ADD COLUMN print_value boolean,
	ADD COLUMN last_id integer;

COMMENT ON COLUMN extraschool_qrcodes_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_qrcodes_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_qrcodes_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_qrcodes_wizard.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_qrcodes_wizard.print_value IS 'Print QrCode value';

COMMENT ON COLUMN extraschool_qrcodes_wizard.last_id IS 'Last id';

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

COMMENT ON COLUMN extraschool_reminder.filename IS 'filename';

COMMENT ON COLUMN extraschool_reminder.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_reminder.write_date IS 'Last Updated on';

ALTER TABLE extraschool_remindersjournal
	DROP COLUMN unpaidinvoicefrom,
	DROP COLUMN unpaidinvoiceto;

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

ALTER TABLE extraschool_smartphone
	ALTER COLUMN userpassword TYPE character varying(40) /* TYPE change - table: extraschool_smartphone original: character varying(20) new: character varying(40) */;

COMMENT ON COLUMN extraschool_smartphone.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_smartphone.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_smartphone.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_smartphone.write_date IS 'Last Updated on';

ALTER TABLE extraschool_taxcertificates_wizard
	DROP COLUMN transmissiondate;

COMMENT ON COLUMN extraschool_taxcertificates_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.name IS 'File Name';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_taxcertificates_wizard.write_date IS 'Last Updated on';

COMMENT ON COLUMN extraschool_timecorrection_wizard.create_uid IS 'Created by';

COMMENT ON COLUMN extraschool_timecorrection_wizard.create_date IS 'Created on';

COMMENT ON COLUMN extraschool_timecorrection_wizard.write_uid IS 'Last Updated by';

COMMENT ON COLUMN extraschool_timecorrection_wizard.write_date IS 'Last Updated on';

ALTER SEQUENCE extraschool_activityoccurrence_id_seq
	OWNED BY extraschool_activityoccurrence.id;

ALTER SEQUENCE extraschool_inline_report_id_seq
	OWNED BY extraschool_inline_report.id;

ALTER SEQUENCE extraschool_one_report_day_id_seq
	OWNED BY extraschool_one_report_day.id;

ALTER SEQUENCE extraschool_one_report_id_seq
	OWNED BY extraschool_one_report.id;

ALTER SEQUENCE extraschool_onereport_settings_id_seq
	OWNED BY extraschool_onereport_settings.id;

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

ALTER SEQUENCE extraschool_report_id_seq
	OWNED BY extraschool_report.id;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_inline_report
	ADD CONSTRAINT extraschool_inline_report_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_one_report
	ADD CONSTRAINT extraschool_one_report_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_one_report_day
	ADD CONSTRAINT extraschool_one_report_day_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_onereport_settings
	ADD CONSTRAINT extraschool_onereport_settings_pkey PRIMARY KEY (id);

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

ALTER TABLE extraschool_report
	ADD CONSTRAINT extraschool_report_pkey PRIMARY KEY (id);

ALTER TABLE extraschool_activity
	ADD CONSTRAINT extraschool_activity_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activity
	ADD CONSTRAINT extraschool_activity_price_list_id_fkey FOREIGN KEY (price_list_id) REFERENCES extraschool_price_list(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activity
	ADD CONSTRAINT extraschool_activity_root_id_fkey FOREIGN KEY (root_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activity_activityexclusiondates_rel
	ADD CONSTRAINT extraschool_activity_activity_activity_id_activityexclusion_key UNIQUE (activity_id, activityexclusiondates_id);

ALTER TABLE extraschool_activity_activityexclusiondates_rel
	ADD CONSTRAINT extraschool_activity_activityexc_activityexclusiondates_id_fkey FOREIGN KEY (activityexclusiondates_id) REFERENCES extraschool_activityexclusiondates(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activity_activityexclusiondates_rel
	ADD CONSTRAINT extraschool_activity_activityexclusiondates_re_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activity_activityplanneddate_rel
	ADD CONSTRAINT extraschool_activity_activity_activity_id_activityplannedda_key UNIQUE (activity_id, activityplanneddate_id);

ALTER TABLE extraschool_activity_activityplanneddate_rel
	ADD CONSTRAINT extraschool_activity_activityplanne_activityplanneddate_id_fkey FOREIGN KEY (activityplanneddate_id) REFERENCES extraschool_activityplanneddate(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activity_childposition_rel
	ADD CONSTRAINT extraschool_activity_childposi_activity_id_childposition_id_key UNIQUE (activity_id, childposition_id);

ALTER TABLE extraschool_activity_childposition_rel
	ADD CONSTRAINT extraschool_activity_childposition_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_discount(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activity_childtype_rel
	ADD CONSTRAINT extraschool_activity_childtype_rel_activity_id_childtype_id_key UNIQUE (activity_id, childtype_id);

ALTER TABLE extraschool_activity_pricelist_rel
	ADD CONSTRAINT extraschool_activity_pricelis_extraschool_price_list_versio_key UNIQUE (extraschool_price_list_version_id, extraschool_activity_id);

ALTER TABLE extraschool_activity_pricelist_rel
	ADD CONSTRAINT extraschool_activity_pricelis_extraschool_price_list_versi_fkey FOREIGN KEY (extraschool_price_list_version_id) REFERENCES extraschool_price_list_version(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activity_pricelist_rel
	ADD CONSTRAINT extraschool_activity_pricelist_rel_extraschool_activity_id_fkey FOREIGN KEY (extraschool_activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activity_schoolimplantation_rel
	ADD CONSTRAINT extraschool_activity_schoolim_activity_id_schoolimplantatio_key UNIQUE (activity_id, schoolimplantation_id);

ALTER TABLE extraschool_activity_schoolimplantation_rel
	ADD CONSTRAINT extraschool_activity_schoolimplantat_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activitycategory
	ADD CONSTRAINT extraschool_activitycategory_report_id_fkey FOREIGN KEY (report_id) REFERENCES extraschool_report(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activitycategory_place_rel
	ADD CONSTRAINT extraschool_activitycategory_p_activitycategory_id_place_id_key UNIQUE (activitycategory_id, place_id);

ALTER TABLE extraschool_activitycategory_place_rel
	ADD CONSTRAINT extraschool_activitycategory_place_rel_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;

ALTER TABLE extraschool_activitychildregistration
	ADD CONSTRAINT extraschool_activitychildregistration_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_activityoccurrence
	ADD CONSTRAINT extraschool_activityoccurrence_activity_category_id_fkey FOREIGN KEY (activity_category_id) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

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

ALTER TABLE extraschool_childposition_pricelist_rel
	ADD CONSTRAINT extraschool_childposition_pri_extraschool_price_list_versio_key UNIQUE (extraschool_price_list_version_id, extraschool_childposition_id);

ALTER TABLE extraschool_childposition_pricelist_rel
	ADD CONSTRAINT extraschool_childposition_pri_extraschool_childposition_id_fkey FOREIGN KEY (extraschool_childposition_id) REFERENCES extraschool_childposition(id) ON DELETE CASCADE;

ALTER TABLE extraschool_childposition_pricelist_rel
	ADD CONSTRAINT extraschool_childposition_pri_extraschool_price_list_versi_fkey FOREIGN KEY (extraschool_price_list_version_id) REFERENCES extraschool_price_list_version(id) ON DELETE CASCADE;

ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel
	ADD CONSTRAINT extraschool_childsimportfilte_childsimportfilter_id_importl_key UNIQUE (childsimportfilter_id, importlevelrule_id);

ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel
	ADD CONSTRAINT extraschool_childsimportfilter_impor_childsimportfilter_id_fkey FOREIGN KEY (childsimportfilter_id) REFERENCES extraschool_childsimportfilter(id) ON DELETE CASCADE;

ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel
	ADD CONSTRAINT extraschool_childsimportfilter_importle_importlevelrule_id_fkey FOREIGN KEY (importlevelrule_id) REFERENCES extraschool_importlevelrule(id) ON DELETE CASCADE;

ALTER TABLE extraschool_childsworkbook_wizard
	ADD CONSTRAINT extraschool_childsworkbook_wizard_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;

ALTER TABLE extraschool_childsworkbook_wizard
	ADD CONSTRAINT extraschool_childsworkbook_wizard_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;

ALTER TABLE extraschool_discount_childtype_rel
	ADD CONSTRAINT extraschool_discount_childtype_rel_discount_id_childtype_id_key UNIQUE (discount_id, childtype_id);

ALTER TABLE extraschool_discount_discountrule_rel
	ADD CONSTRAINT extraschool_discount_discountru_discount_id_discountrule_id_key UNIQUE (discount_id, discountrule_id);

ALTER TABLE extraschool_guardianprestationtimes_wizard
	ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_guardianid_fkey FOREIGN KEY (guardianid) REFERENCES extraschool_guardian(id) ON DELETE SET NULL;

ALTER TABLE extraschool_inline_report
	ADD CONSTRAINT extraschool_inline_report_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_inline_report
	ADD CONSTRAINT extraschool_inline_report_inline_report_id_fkey FOREIGN KEY (inline_report_id) REFERENCES ir_ui_view(id) ON DELETE SET NULL;

ALTER TABLE extraschool_inline_report
	ADD CONSTRAINT extraschool_inline_report_report_id_fkey FOREIGN KEY (report_id) REFERENCES extraschool_report(id) ON DELETE SET NULL;

ALTER TABLE extraschool_inline_report
	ADD CONSTRAINT extraschool_inline_report_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoice_wizard
	ADD CONSTRAINT extraschool_invoice_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoice_wizard_schoolimplantation_rel
	ADD CONSTRAINT extraschool_invoice_wizard_sc_invoice_wizard_id_schoolimpla_key UNIQUE (invoice_wizard_id, schoolimplantation_id);

ALTER TABLE extraschool_invoice_wizard_schoolimplantation_rel
	ADD CONSTRAINT extraschool_invoice_wizard_schoolimp_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;

ALTER TABLE extraschool_invoice_wizard_schoolimplantation_rel
	ADD CONSTRAINT extraschool_invoice_wizard_schoolimplant_invoice_wizard_id_fkey FOREIGN KEY (invoice_wizard_id) REFERENCES extraschool_invoice_wizard(id) ON DELETE CASCADE;

ALTER TABLE extraschool_invoicedprestations
	ADD CONSTRAINT extraschool_invoicedprestations_activity_occurrence_id_fkey FOREIGN KEY (activity_occurrence_id) REFERENCES extraschool_activityoccurrence(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoicedprestations
	ADD CONSTRAINT extraschool_invoicedprestations_child_position_fkey FOREIGN KEY (child_position) REFERENCES extraschool_childposition(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoicedprestations
	ADD CONSTRAINT extraschool_invoicedprestations_child_position_id_fkey FOREIGN KEY (child_position_id) REFERENCES extraschool_childposition(id) ON DELETE SET NULL;

ALTER TABLE extraschool_invoicedprestations
	ADD CONSTRAINT extraschool_invoicedprestations_price_list_version_id_fkey FOREIGN KEY (price_list_version_id) REFERENCES extraschool_price_list_version(id) ON DELETE SET NULL;

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

ALTER TABLE extraschool_onereport_settings
	ADD CONSTRAINT extraschool_onereport_settings_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_onereport_settings
	ADD CONSTRAINT extraschool_onereport_settings_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_pdaprestationtimes
	ADD CONSTRAINT extraschool_pdaprestationtime_prestation_times_of_the_day__fkey FOREIGN KEY (prestation_times_of_the_day_id) REFERENCES extraschool_prestation_times_of_the_day(id) ON DELETE SET NULL;

ALTER TABLE extraschool_place_schoolimplantation_rel
	ADD CONSTRAINT extraschool_place_schoolimpla_place_id_schoolimplantation_i_key UNIQUE (place_id, schoolimplantation_id);

ALTER TABLE extraschool_place_schoolimplantation_rel
	ADD CONSTRAINT extraschool_place_schoolimplantation_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;

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
	ADD CONSTRAINT extraschool_prestation_times_of_the_day_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES extraschool_parent(id) ON DELETE SET NULL;

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
	ADD CONSTRAINT extraschool_prestationtimes_activity_category_id_fkey FOREIGN KEY (activity_category_id) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_activity_occurrence_id_fkey FOREIGN KEY (activity_occurrence_id) REFERENCES extraschool_activityoccurrence(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE RESTRICT;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES extraschool_parent(id) ON DELETE SET NULL;

ALTER TABLE extraschool_prestationtimes
	ADD CONSTRAINT extraschool_prestationtimes_prestation_times_of_the_day_id_fkey FOREIGN KEY (prestation_times_of_the_day_id) REFERENCES extraschool_prestation_times_of_the_day(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list
	ADD CONSTRAINT extraschool_price_list_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list
	ADD CONSTRAINT extraschool_price_list_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_child_type_id_fkey FOREIGN KEY (child_type_id) REFERENCES extraschool_childtype(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_price_list_id_fkey FOREIGN KEY (price_list_id) REFERENCES extraschool_price_list(id) ON DELETE SET NULL;

ALTER TABLE extraschool_price_list_version
	ADD CONSTRAINT extraschool_price_list_version_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_remindersjournal_biller_rel
	ADD CONSTRAINT extraschool_remindersjournal__remindersjournal_id_biller_id_key UNIQUE (remindersjournal_id, biller_id);

ALTER TABLE extraschool_remindersjournal_biller_rel
	ADD CONSTRAINT extraschool_remindersjournal_biller_re_remindersjournal_id_fkey FOREIGN KEY (remindersjournal_id) REFERENCES extraschool_remindersjournal(id) ON DELETE CASCADE;

ALTER TABLE extraschool_report
	ADD CONSTRAINT extraschool_report_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_report
	ADD CONSTRAINT extraschool_report_report_type_id_fkey FOREIGN KEY (report_type_id) REFERENCES ir_act_report_xml(id) ON DELETE SET NULL;

ALTER TABLE extraschool_report
	ADD CONSTRAINT extraschool_report_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;

ALTER TABLE extraschool_smartphone_activitycategory_rel
	ADD CONSTRAINT extraschool_smartphone_activi_smartphone_id_activitycategor_key UNIQUE (smartphone_id, activitycategory_id);

ALTER TABLE extraschool_smartphone_activitycategory_rel
	ADD CONSTRAINT extraschool_smartphone_activitycategor_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;

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

CREATE INDEX extraschool_activity_activityexclusiondates_rel_activity_id_ind ON extraschool_activity_activityexclusiondates_rel USING btree (activity_id);

CREATE INDEX extraschool_activity_activityexclusiondates_rel_activityexclusi ON extraschool_activity_activityexclusiondates_rel USING btree (activityexclusiondates_id);

CREATE INDEX extraschool_activity_activityplanneddate_rel_activityplanneddat ON extraschool_activity_activityplanneddate_rel USING btree (activityplanneddate_id);

CREATE INDEX extraschool_activity_pricelist_rel_extraschool_activity_id_inde ON extraschool_activity_pricelist_rel USING btree (extraschool_activity_id);

CREATE INDEX extraschool_activity_pricelist_rel_extraschool_price_list_versi ON extraschool_activity_pricelist_rel USING btree (extraschool_price_list_version_id);

CREATE INDEX extraschool_activity_schoolimplantation_rel_schoolimplantation_ ON extraschool_activity_schoolimplantation_rel USING btree (schoolimplantation_id);

CREATE INDEX extraschool_activitycategory_place_rel_activitycategory_id_inde ON extraschool_activitycategory_place_rel USING btree (activitycategory_id);

CREATE INDEX extraschool_activityoccurrence_activity_category_id_index ON extraschool_activityoccurrence USING btree (activity_category_id);

CREATE INDEX extraschool_activityoccurrence_activityid_index ON extraschool_activityoccurrence USING btree (activityid);

CREATE INDEX extraschool_activityoccurrence_cild_rel_activityoccurrence_id_i ON extraschool_activityoccurrence_cild_rel USING btree (activityoccurrence_id);

CREATE INDEX extraschool_activityoccurrence_cild_rel_child_id_index ON extraschool_activityoccurrence_cild_rel USING btree (child_id);

CREATE INDEX extraschool_childposition_position_index ON extraschool_childposition USING btree ("position");

CREATE INDEX extraschool_childposition_pricelist_rel_extraschool_childpositi ON extraschool_childposition_pricelist_rel USING btree (extraschool_childposition_id);

CREATE INDEX extraschool_childposition_pricelist_rel_extraschool_price_list_ ON extraschool_childposition_pricelist_rel USING btree (extraschool_price_list_version_id);

CREATE INDEX extraschool_childsimportfilter_importlevelrule_rel_childsimport ON extraschool_childsimportfilter_importlevelrule_rel USING btree (childsimportfilter_id);

CREATE INDEX extraschool_childsimportfilter_importlevelrule_rel_importlevelr ON extraschool_childsimportfilter_importlevelrule_rel USING btree (importlevelrule_id);

CREATE INDEX extraschool_invoice_wizard_schoolimplantation_rel_invoice_wizar ON extraschool_invoice_wizard_schoolimplantation_rel USING btree (invoice_wizard_id);

CREATE INDEX extraschool_invoice_wizard_schoolimplantation_rel_schoolimplant ON extraschool_invoice_wizard_schoolimplantation_rel USING btree (schoolimplantation_id);

CREATE INDEX extraschool_invoicedprestations_activity_occurrence_id_index ON extraschool_invoicedprestations USING btree (activity_occurrence_id);

CREATE INDEX extraschool_invoicedprestations_child_position_id_index ON extraschool_invoicedprestations USING btree (child_position_id);

CREATE INDEX extraschool_invoicedprestations_child_position_index ON extraschool_invoicedprestations USING btree (child_position);

CREATE INDEX extraschool_one_report_day_child_rel_child_id_index ON extraschool_one_report_day_child_rel USING btree (child_id);

CREATE INDEX extraschool_one_report_day_child_rel_one_report_day_id_index ON extraschool_one_report_day_child_rel USING btree (one_report_day_id);

CREATE INDEX extraschool_place_schoolimplantation_rel_schoolimplantation_id_ ON extraschool_place_schoolimplantation_rel USING btree (schoolimplantation_id);

CREATE INDEX extraschool_prestationscheck_wizard_place_rel_place_id_index ON extraschool_prestationscheck_wizard_place_rel USING btree (place_id);

CREATE INDEX extraschool_prestationscheck_wizard_place_rel_prestationscheck_ ON extraschool_prestationscheck_wizard_place_rel USING btree (prestationscheck_wizard_id);

CREATE INDEX extraschool_prestationtimes_activity_category_id_index ON extraschool_prestationtimes USING btree (activity_category_id);

CREATE INDEX extraschool_prestationtimes_activity_occurrence_id_index ON extraschool_prestationtimes USING btree (activity_occurrence_id);

CREATE INDEX extraschool_prestationtimes_es_index ON extraschool_prestationtimes USING btree (es);

CREATE INDEX extraschool_prestationtimes_parent_id_index ON extraschool_prestationtimes USING btree (parent_id);

CREATE INDEX extraschool_prestationtimes_verified_index ON extraschool_prestationtimes USING btree (verified);

CREATE INDEX extraschool_remindersjournal_biller_rel_remindersjournal_id_ind ON extraschool_remindersjournal_biller_rel USING btree (remindersjournal_id);

CREATE INDEX extraschool_smartphone_activitycategory_rel_activitycategory_id ON extraschool_smartphone_activitycategory_rel USING btree (activitycategory_id);

CREATE INDEX extraschool_smartphone_activitycategory_rel_smartphone_id_index ON extraschool_smartphone_activitycategory_rel USING btree (smartphone_id);

CREATE INDEX extraschool_timecorrection_wizard_place_rel_place_id_index ON extraschool_timecorrection_wizard_place_rel USING btree (place_id);

CREATE INDEX extraschool_timecorrection_wizard_place_rel_prestationscheck_wi ON extraschool_timecorrection_wizard_place_rel USING btree (prestationscheck_wizard_id);

CREATE VIEW extraschool_guardian_prestation_times_report AS
	SELECT min(egt.id) AS id,
    egt.guardianid AS guardian_id,
    egt.prestation_date,
    date_part('week'::text, egt.prestation_date) AS week,
    eg.weekly_schedule,
    (sum(
        CASE
            WHEN ((egt.es)::text = 'S'::text) THEN egt.prestation_time
            ELSE (0)::double precision
        END) - sum(
        CASE
            WHEN ((egt.es)::text = 'E'::text) THEN egt.prestation_time
            ELSE (0)::double precision
        END)) AS duration,
    (eg.weekly_schedule - (sum(
        CASE
            WHEN ((egt.es)::text = 'S'::text) THEN egt.prestation_time
            ELSE (0)::double precision
        END) - sum(
        CASE
            WHEN ((egt.es)::text = 'E'::text) THEN egt.prestation_time
            ELSE (0)::double precision
        END))) AS solde
   FROM (extraschool_guardianprestationtimes egt
     LEFT JOIN extraschool_guardian eg ON ((eg.id = egt.guardianid)))
  GROUP BY egt.guardianid, egt.prestation_date, eg.weekly_schedule;
