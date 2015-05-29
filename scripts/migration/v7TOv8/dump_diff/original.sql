--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: extraschool_activity; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    fixedperiod boolean,
    validity_from date,
    default_from double precision,
    validity_to date,
    category integer,
    default_to double precision,
    name character varying(50),
    autoaddchilds boolean,
    days character varying,
    prest_to double precision,
    subsidizedbyone boolean,
    leveltype character varying,
    period_duration integer,
    prest_from double precision,
    short_name character varying(20),
    price numeric,
    minamount numeric,
    maxamount numeric,
    onlyregisteredchilds boolean
);


ALTER TABLE extraschool_activity OWNER TO openerp;

--
-- Name: TABLE extraschool_activity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity IS 'activity';


--
-- Name: COLUMN extraschool_activity.fixedperiod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.fixedperiod IS 'Fixed period';


--
-- Name: COLUMN extraschool_activity.validity_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.validity_from IS 'Validity from';


--
-- Name: COLUMN extraschool_activity.default_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.default_from IS 'Default from';


--
-- Name: COLUMN extraschool_activity.validity_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.validity_to IS 'Validity to';


--
-- Name: COLUMN extraschool_activity.category; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.category IS 'Category';


--
-- Name: COLUMN extraschool_activity.default_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.default_to IS 'Default to';


--
-- Name: COLUMN extraschool_activity.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.name IS 'Name';


--
-- Name: COLUMN extraschool_activity.autoaddchilds; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.autoaddchilds IS 'Auto add registered';


--
-- Name: COLUMN extraschool_activity.days; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.days IS 'Days';


--
-- Name: COLUMN extraschool_activity.prest_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.prest_to IS 'To';


--
-- Name: COLUMN extraschool_activity.subsidizedbyone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.subsidizedbyone IS 'Subsidized by one';


--
-- Name: COLUMN extraschool_activity.leveltype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.leveltype IS 'Level type';


--
-- Name: COLUMN extraschool_activity.period_duration; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.period_duration IS 'Period Duration';


--
-- Name: COLUMN extraschool_activity.prest_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.prest_from IS 'From';


--
-- Name: COLUMN extraschool_activity.minamount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.minamount IS 'Min Amount';


--
-- Name: COLUMN extraschool_activity.maxamount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.maxamount IS 'Max Amount';


--
-- Name: COLUMN extraschool_activity.onlyregisteredchilds; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.onlyregisteredchilds IS 'Only registered childs';


--
-- Name: extraschool_activity_activityexclusiondates_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_activityexclusiondates_rel (
    activity_id integer NOT NULL,
    activityexclusiondates_id integer NOT NULL
);


ALTER TABLE extraschool_activity_activityexclusiondates_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_activityexclusiondates_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_activityexclusiondates_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_activityexclusiondates';


--
-- Name: extraschool_activity_activityplanneddate_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_activityplanneddate_rel (
    activityplanneddate_id integer NOT NULL,
    activity_id integer NOT NULL
);


ALTER TABLE extraschool_activity_activityplanneddate_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_activityplanneddate_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_activityplanneddate_rel IS 'RELATION BETWEEN extraschool_activityplanneddate AND extraschool_activity';


--
-- Name: extraschool_activity_child_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_child_rel (
    activity_id integer NOT NULL,
    child_id integer NOT NULL
);


ALTER TABLE extraschool_activity_child_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_child_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_child_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_child';


--
-- Name: extraschool_activity_childposition_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_childposition_rel (
    activity_id integer NOT NULL,
    childposition_id integer NOT NULL
);


ALTER TABLE extraschool_activity_childposition_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_childposition_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_childposition_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_childposition';


--
-- Name: extraschool_activity_childtype_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_childtype_rel (
    activity_id integer NOT NULL,
    childtype_id integer NOT NULL
);


ALTER TABLE extraschool_activity_childtype_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_childtype_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_childtype_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_childtype';


--
-- Name: extraschool_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_activity_id_seq OWNER TO openerp;

--
-- Name: extraschool_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activity_id_seq OWNED BY extraschool_activity.id;


--
-- Name: extraschool_activity_place_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_place_rel (
    activity_id integer NOT NULL,
    place_id integer NOT NULL
);


ALTER TABLE extraschool_activity_place_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_place_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_place_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_place';


--
-- Name: extraschool_activity_schoolimplantation_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activity_schoolimplantation_rel (
    activity_id integer NOT NULL,
    schoolimplantation_id integer NOT NULL
);


ALTER TABLE extraschool_activity_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_schoolimplantation';


--
-- Name: extraschool_activitycategory; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activitycategory (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    bankaccount character varying(4),
    name character varying(50),
    remindercomstructprefix character varying(4),
    invoicetemplate character varying(50),
    invoicelastcomstruct integer,
    invoicecomstructprefix character varying(4),
    reminderlastcomstruct integer,
    priorityorder integer,
    daydiscountforbadgeusage double precision,
    childpositiondetermination character varying,
    reminderemailtext text,
    reminderemailsubject character varying(50),
    invoiceemailtext text,
    invoiceemailaddress character varying(50),
    reminderemailaddress character varying(50),
    invoiceemailsubject character varying(50),
    taxcertificatetemplate character varying(50)
);


ALTER TABLE extraschool_activitycategory OWNER TO openerp;

--
-- Name: TABLE extraschool_activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitycategory IS 'Activities categories';


--
-- Name: COLUMN extraschool_activitycategory.bankaccount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.bankaccount IS 'Bank account';


--
-- Name: COLUMN extraschool_activitycategory.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.name IS 'Name';


--
-- Name: COLUMN extraschool_activitycategory.remindercomstructprefix; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.remindercomstructprefix IS 'Reminder Comstruct prefix';


--
-- Name: COLUMN extraschool_activitycategory.invoicetemplate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoicetemplate IS 'Invoice Template';


--
-- Name: COLUMN extraschool_activitycategory.invoicelastcomstruct; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoicelastcomstruct IS 'Last Invoice structured comunication number';


--
-- Name: COLUMN extraschool_activitycategory.invoicecomstructprefix; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoicecomstructprefix IS 'Invoice Comstruct prefix';


--
-- Name: COLUMN extraschool_activitycategory.reminderlastcomstruct; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderlastcomstruct IS 'Last Reminder structured comunication number';


--
-- Name: COLUMN extraschool_activitycategory.priorityorder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.priorityorder IS 'Priority order';


--
-- Name: COLUMN extraschool_activitycategory.daydiscountforbadgeusage; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.daydiscountforbadgeusage IS 'Discount by day for badge usage';


--
-- Name: COLUMN extraschool_activitycategory.childpositiondetermination; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.childpositiondetermination IS 'Child position determination';


--
-- Name: COLUMN extraschool_activitycategory.reminderemailtext; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderemailtext IS 'Reminder email text';


--
-- Name: COLUMN extraschool_activitycategory.reminderemailsubject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderemailsubject IS 'Reminder email subject';


--
-- Name: COLUMN extraschool_activitycategory.invoiceemailtext; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoiceemailtext IS 'Invoice email text';


--
-- Name: COLUMN extraschool_activitycategory.invoiceemailaddress; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoiceemailaddress IS 'Invoice email address';


--
-- Name: COLUMN extraschool_activitycategory.reminderemailaddress; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderemailaddress IS 'Reminder email address';


--
-- Name: COLUMN extraschool_activitycategory.invoiceemailsubject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoiceemailsubject IS 'Invoice email subject';


--
-- Name: COLUMN extraschool_activitycategory.taxcertificatetemplate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.taxcertificatetemplate IS 'Tax Certificate Template';


--
-- Name: extraschool_activitycategory_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activitycategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_activitycategory_id_seq OWNER TO openerp;

--
-- Name: extraschool_activitycategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activitycategory_id_seq OWNED BY extraschool_activitycategory.id;


--
-- Name: extraschool_activitycategory_place_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activitycategory_place_rel (
    activitycategory_id integer NOT NULL,
    place_id integer NOT NULL
);


ALTER TABLE extraschool_activitycategory_place_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activitycategory_place_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitycategory_place_rel IS 'RELATION BETWEEN extraschool_activitycategory AND extraschool_place';


--
-- Name: extraschool_activitycategory_schoolimplantation_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activitycategory_schoolimplantation_rel (
    activitycategory_id integer NOT NULL,
    schoolimplantation_id integer NOT NULL
);


ALTER TABLE extraschool_activitycategory_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activitycategory_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitycategory_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_activitycategory AND extraschool_schoolimplantation';


--
-- Name: extraschool_activitychildregistration; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activitychildregistration (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    registration_to date,
    child_id integer,
    registration_from date,
    activity_id integer
);


ALTER TABLE extraschool_activitychildregistration OWNER TO openerp;

--
-- Name: TABLE extraschool_activitychildregistration; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitychildregistration IS 'activity child registration';


--
-- Name: COLUMN extraschool_activitychildregistration.registration_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.registration_to IS 'Registration to';


--
-- Name: COLUMN extraschool_activitychildregistration.child_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.child_id IS 'Child';


--
-- Name: COLUMN extraschool_activitychildregistration.registration_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.registration_from IS 'Registration from';


--
-- Name: COLUMN extraschool_activitychildregistration.activity_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.activity_id IS 'Activity';


--
-- Name: extraschool_activitychildregistration_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activitychildregistration_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_activitychildregistration_id_seq OWNER TO openerp;

--
-- Name: extraschool_activitychildregistration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activitychildregistration_id_seq OWNED BY extraschool_activitychildregistration.id;


--
-- Name: extraschool_activityexclusiondates; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activityexclusiondates (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    date_from date NOT NULL,
    name character varying(50),
    date_to date NOT NULL
);


ALTER TABLE extraschool_activityexclusiondates OWNER TO openerp;

--
-- Name: TABLE extraschool_activityexclusiondates; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activityexclusiondates IS 'Activity exclusion dates';


--
-- Name: COLUMN extraschool_activityexclusiondates.date_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.date_from IS 'Date from';


--
-- Name: COLUMN extraschool_activityexclusiondates.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.name IS 'Name';


--
-- Name: COLUMN extraschool_activityexclusiondates.date_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.date_to IS 'Date to';


--
-- Name: extraschool_activityexclusiondates_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activityexclusiondates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_activityexclusiondates_id_seq OWNER TO openerp;

--
-- Name: extraschool_activityexclusiondates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activityexclusiondates_id_seq OWNED BY extraschool_activityexclusiondates.id;


--
-- Name: extraschool_activityplanneddate; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_activityplanneddate (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    activitydate date
);


ALTER TABLE extraschool_activityplanneddate OWNER TO openerp;

--
-- Name: TABLE extraschool_activityplanneddate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activityplanneddate IS 'Activities planned dates';


--
-- Name: COLUMN extraschool_activityplanneddate.activitydate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityplanneddate.activitydate IS 'Date';


--
-- Name: extraschool_activityplanneddate_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activityplanneddate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_activityplanneddate_id_seq OWNER TO openerp;

--
-- Name: extraschool_activityplanneddate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activityplanneddate_id_seq OWNED BY extraschool_activityplanneddate.id;


--
-- Name: extraschool_biller; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_biller (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    period_from date,
    name character varying(20),
    activitycategoryid integer,
    payment_term date,
    period_to date,
    oldid integer,
    filename character varying(20),
    biller_file bytea,
    invoices_date date
);


ALTER TABLE extraschool_biller OWNER TO openerp;

--
-- Name: TABLE extraschool_biller; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_biller IS 'Biller';


--
-- Name: COLUMN extraschool_biller.period_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.period_from IS 'Period from';


--
-- Name: COLUMN extraschool_biller.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.name IS 'Name';


--
-- Name: COLUMN extraschool_biller.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_biller.payment_term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.payment_term IS 'Payment term';


--
-- Name: COLUMN extraschool_biller.period_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.period_to IS 'Period to';


--
-- Name: COLUMN extraschool_biller.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_biller.filename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.filename IS 'filename';


--
-- Name: COLUMN extraschool_biller.biller_file; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.biller_file IS 'File';


--
-- Name: COLUMN extraschool_biller.invoices_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.invoices_date IS 'Invoices date';


--
-- Name: extraschool_biller_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_biller_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_biller_id_seq OWNER TO openerp;

--
-- Name: extraschool_biller_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_biller_id_seq OWNED BY extraschool_biller.id;


--
-- Name: extraschool_child; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_child (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    classid integer,
    schoolimplantation integer NOT NULL,
    name character varying(100),
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    isdisabled boolean,
    childtypeid integer NOT NULL,
    levelid integer NOT NULL,
    otherref character varying(50),
    oldid integer,
    parentid integer NOT NULL,
    birthdate date NOT NULL,
    tagid character varying(50)
);


ALTER TABLE extraschool_child OWNER TO openerp;

--
-- Name: TABLE extraschool_child; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_child IS 'Child';


--
-- Name: COLUMN extraschool_child.classid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.classid IS 'Class';


--
-- Name: COLUMN extraschool_child.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_child.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.name IS 'FullName';


--
-- Name: COLUMN extraschool_child.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.firstname IS 'FirstName';


--
-- Name: COLUMN extraschool_child.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_child.isdisabled; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.isdisabled IS 'Disabled';


--
-- Name: COLUMN extraschool_child.childtypeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.childtypeid IS 'Type';


--
-- Name: COLUMN extraschool_child.levelid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.levelid IS 'Level';


--
-- Name: COLUMN extraschool_child.otherref; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.otherref IS 'Other ref';


--
-- Name: COLUMN extraschool_child.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_child.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.parentid IS 'Parent';


--
-- Name: COLUMN extraschool_child.birthdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.birthdate IS 'Birthdate';


--
-- Name: COLUMN extraschool_child.tagid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.tagid IS 'Tag ID';


--
-- Name: extraschool_child_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_child_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_child_id_seq OWNER TO openerp;

--
-- Name: extraschool_child_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_child_id_seq OWNED BY extraschool_child.id;


--
-- Name: extraschool_childposition; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childposition (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    "Position" integer,
    name character varying(50),
    "position" integer
);


ALTER TABLE extraschool_childposition OWNER TO openerp;

--
-- Name: TABLE extraschool_childposition; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childposition IS 'Child position';


--
-- Name: COLUMN extraschool_childposition."Position"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition."Position" IS 'Position';


--
-- Name: COLUMN extraschool_childposition.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition.name IS 'Name';


--
-- Name: COLUMN extraschool_childposition."position"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition."position" IS 'Position';


--
-- Name: extraschool_childposition_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childposition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_childposition_id_seq OWNER TO openerp;

--
-- Name: extraschool_childposition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childposition_id_seq OWNED BY extraschool_childposition.id;


--
-- Name: extraschool_childsimport; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childsimport (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    childsfile bytea NOT NULL,
    schoolimplantation integer NOT NULL,
    childsimportfilter integer NOT NULL
);


ALTER TABLE extraschool_childsimport OWNER TO openerp;

--
-- Name: TABLE extraschool_childsimport; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsimport IS 'extraschool.childsimport';


--
-- Name: COLUMN extraschool_childsimport.childsfile; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.childsfile IS 'Childs File';


--
-- Name: COLUMN extraschool_childsimport.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_childsimport.childsimportfilter; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.childsimportfilter IS 'Childs import filter';


--
-- Name: extraschool_childsimport_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childsimport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_childsimport_id_seq OWNER TO openerp;

--
-- Name: extraschool_childsimport_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childsimport_id_seq OWNED BY extraschool_childsimport.id;


--
-- Name: extraschool_childsimportfilter; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childsimportfilter (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    childclassnamecolumns character varying(10),
    childotherrefcolumn integer,
    parentstreetcolumns character varying(10),
    parentfirstnamecolumn integer,
    parentzipcodecolumnname character varying(30),
    childbirthdatecolumn integer,
    parentgsmcolumn integer,
    parentzipcodecolumn integer,
    parentcitycolumnname character varying(30),
    childotherrefcolumnname character varying(30),
    parentemailcolumnname character varying(30),
    parentgsmcolumnname character varying(30),
    childbirthdatecolumnname character varying(30),
    parentworkphonecolumn integer,
    parentfirstnamecolumnname character varying(30),
    parenthousephonecolumnname character varying(30),
    childfirstnamecolumn integer,
    childclassnamecolumnsname character varying(60),
    parentworkphonecolumnname character varying(30),
    parentlastnamecolumnname character varying(30),
    startrow integer,
    childlevelcolumns character varying(10),
    parentlastnamecolumn integer,
    parenthousephonecolumn integer,
    childlastnamecolumn integer,
    childlastnamecolumnname character varying(30),
    name character varying(50),
    parentcitycolumn integer,
    childlevelcolumnsname character varying(60),
    childfirstnamecolumnname character varying(30),
    parentemailcolumn integer,
    parentstreetcolumnsname character varying(60),
    majparenthousephone boolean,
    majparentworkphone boolean,
    majparentstreet boolean,
    majparentcity boolean,
    majchildlevel boolean,
    majparentgsm boolean,
    majparentlastname boolean,
    majchildclassname boolean,
    majparentfirstname boolean,
    majparentzipcode boolean,
    majchildotherref boolean,
    majparentemail boolean,
    majschoolimplantation boolean,
    childtypecolumn integer,
    childtypecolumnname character varying(60),
    majchildtype boolean
);


ALTER TABLE extraschool_childsimportfilter OWNER TO openerp;

--
-- Name: TABLE extraschool_childsimportfilter; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsimportfilter IS 'Childs import filter';


--
-- Name: COLUMN extraschool_childsimportfilter.childclassnamecolumns; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childclassnamecolumns IS 'Child class name columns';


--
-- Name: COLUMN extraschool_childsimportfilter.childotherrefcolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childotherrefcolumn IS 'Child other ref column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentstreetcolumns; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentstreetcolumns IS 'Parent street columns';


--
-- Name: COLUMN extraschool_childsimportfilter.parentfirstnamecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentfirstnamecolumn IS 'Parent firstname column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentzipcodecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentzipcodecolumnname IS 'Parent zipcode column name';


--
-- Name: COLUMN extraschool_childsimportfilter.childbirthdatecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childbirthdatecolumn IS 'Child birthdate column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentgsmcolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentgsmcolumn IS 'Parent gsm column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentzipcodecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentzipcodecolumn IS 'Parent zipcode column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentcitycolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentcitycolumnname IS 'Parent city column name';


--
-- Name: COLUMN extraschool_childsimportfilter.childotherrefcolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childotherrefcolumnname IS 'Child other ref column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentemailcolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentemailcolumnname IS 'Parent email column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentgsmcolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentgsmcolumnname IS 'Parent gsm column name';


--
-- Name: COLUMN extraschool_childsimportfilter.childbirthdatecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childbirthdatecolumnname IS 'Child birthdate column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentworkphonecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentworkphonecolumn IS 'Parent work phone column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentfirstnamecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentfirstnamecolumnname IS 'Parent firstname column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parenthousephonecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parenthousephonecolumnname IS 'Parent house phone column name';


--
-- Name: COLUMN extraschool_childsimportfilter.childfirstnamecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childfirstnamecolumn IS 'Child firstname column';


--
-- Name: COLUMN extraschool_childsimportfilter.childclassnamecolumnsname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childclassnamecolumnsname IS 'Child class name columns name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentworkphonecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentworkphonecolumnname IS 'Parent work phone column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentlastnamecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentlastnamecolumnname IS 'Parent lastname column name';


--
-- Name: COLUMN extraschool_childsimportfilter.startrow; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.startrow IS 'Start row';


--
-- Name: COLUMN extraschool_childsimportfilter.childlevelcolumns; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childlevelcolumns IS 'Child level column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentlastnamecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentlastnamecolumn IS 'Parent lastname column';


--
-- Name: COLUMN extraschool_childsimportfilter.parenthousephonecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parenthousephonecolumn IS 'Parent house phone column';


--
-- Name: COLUMN extraschool_childsimportfilter.childlastnamecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childlastnamecolumn IS 'Child lastname column';


--
-- Name: COLUMN extraschool_childsimportfilter.childlastnamecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childlastnamecolumnname IS 'Child lastname column name';


--
-- Name: COLUMN extraschool_childsimportfilter.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.name IS 'Name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentcitycolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentcitycolumn IS 'Parent city column';


--
-- Name: COLUMN extraschool_childsimportfilter.childlevelcolumnsname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childlevelcolumnsname IS 'Child level columns name';


--
-- Name: COLUMN extraschool_childsimportfilter.childfirstnamecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childfirstnamecolumnname IS 'Child firstname column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentemailcolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentemailcolumn IS 'Parent email column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentstreetcolumnsname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentstreetcolumnsname IS 'Parent street columns name';


--
-- Name: COLUMN extraschool_childsimportfilter.majparenthousephone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparenthousephone IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentworkphone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentworkphone IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentstreet; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentstreet IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentcity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentcity IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majchildlevel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majchildlevel IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentgsm; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentgsm IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentlastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentlastname IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majchildclassname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majchildclassname IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentfirstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentfirstname IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentzipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentzipcode IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majchildotherref; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majchildotherref IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentemail; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentemail IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majschoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majschoolimplantation IS 'MAJ implantation';


--
-- Name: COLUMN extraschool_childsimportfilter.childtypecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childtypecolumn IS 'Child type column';


--
-- Name: COLUMN extraschool_childsimportfilter.childtypecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childtypecolumnname IS 'Child type column name';


--
-- Name: COLUMN extraschool_childsimportfilter.majchildtype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majchildtype IS 'MAJ';


--
-- Name: extraschool_childsimportfilter_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childsimportfilter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_childsimportfilter_id_seq OWNER TO openerp;

--
-- Name: extraschool_childsimportfilter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childsimportfilter_id_seq OWNED BY extraschool_childsimportfilter.id;


--
-- Name: extraschool_childsimportfilter_importchildtyperule_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childsimportfilter_importchildtyperule_rel (
    childsimportfilter_id integer NOT NULL,
    importchildtyperule_id integer NOT NULL
);


ALTER TABLE extraschool_childsimportfilter_importchildtyperule_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_childsimportfilter_importchildtyperule_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsimportfilter_importchildtyperule_rel IS 'RELATION BETWEEN extraschool_childsimportfilter AND extraschool_importchildtyperule';


--
-- Name: extraschool_childsimportfilter_importlevelrule_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childsimportfilter_importlevelrule_rel (
    childsimportfilter_id integer NOT NULL,
    importlevelrule_id integer NOT NULL
);


ALTER TABLE extraschool_childsimportfilter_importlevelrule_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_childsimportfilter_importlevelrule_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsimportfilter_importlevelrule_rel IS 'RELATION BETWEEN extraschool_childsimportfilter AND extraschool_importlevelrule';


--
-- Name: extraschool_childsworkbook_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childsworkbook_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    schoolimplantation integer,
    childsworkbook bytea,
    name character varying(16),
    state character varying NOT NULL,
    placeid integer,
    child_id integer
);


ALTER TABLE extraschool_childsworkbook_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_childsworkbook_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsworkbook_wizard IS 'extraschool.childsworkbook_wizard';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.childsworkbook; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.childsworkbook IS 'File';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.child_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.child_id IS 'Child';


--
-- Name: extraschool_childsworkbook_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childsworkbook_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_childsworkbook_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_childsworkbook_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childsworkbook_wizard_id_seq OWNED BY extraschool_childsworkbook_wizard.id;


--
-- Name: extraschool_childtype; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_childtype (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    name character varying(50),
    oldid integer
);


ALTER TABLE extraschool_childtype OWNER TO openerp;

--
-- Name: TABLE extraschool_childtype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childtype IS 'ChildType';


--
-- Name: COLUMN extraschool_childtype.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.name IS 'Name';


--
-- Name: COLUMN extraschool_childtype.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.oldid IS 'oldid';


--
-- Name: extraschool_childtype_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_childtype_id_seq OWNER TO openerp;

--
-- Name: extraschool_childtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childtype_id_seq OWNED BY extraschool_childtype.id;


--
-- Name: extraschool_class; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_class (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    schoolimplantation integer,
    name character varying(50),
    titular integer,
    oldid integer
);


ALTER TABLE extraschool_class OWNER TO openerp;

--
-- Name: TABLE extraschool_class; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_class IS 'Class';


--
-- Name: COLUMN extraschool_class.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_class.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.name IS 'Name';


--
-- Name: COLUMN extraschool_class.titular; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.titular IS 'Teacher';


--
-- Name: COLUMN extraschool_class.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.oldid IS 'oldid';


--
-- Name: extraschool_class_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_class_id_seq OWNER TO openerp;

--
-- Name: extraschool_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_class_id_seq OWNED BY extraschool_class.id;


--
-- Name: extraschool_class_level_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_class_level_rel (
    class_id integer NOT NULL,
    level_id integer NOT NULL
);


ALTER TABLE extraschool_class_level_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_class_level_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_class_level_rel IS 'RELATION BETWEEN extraschool_class AND extraschool_level';


--
-- Name: extraschool_coda; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_coda (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    name character varying(20),
    codadate date,
    codafile bytea
);


ALTER TABLE extraschool_coda OWNER TO openerp;

--
-- Name: TABLE extraschool_coda; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_coda IS 'extraschool.coda';


--
-- Name: COLUMN extraschool_coda.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.name IS 'Name';


--
-- Name: COLUMN extraschool_coda.codadate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.codadate IS 'CODA Date';


--
-- Name: COLUMN extraschool_coda.codafile; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.codafile IS 'CODA File';


--
-- Name: extraschool_coda_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_coda_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_coda_id_seq OWNER TO openerp;

--
-- Name: extraschool_coda_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_coda_id_seq OWNED BY extraschool_coda.id;


--
-- Name: extraschool_copiercode; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_copiercode (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    teacherid integer,
    name character varying(7),
    pin character varying(7),
    oldid integer
);


ALTER TABLE extraschool_copiercode OWNER TO openerp;

--
-- Name: TABLE extraschool_copiercode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_copiercode IS 'Copier Code';


--
-- Name: COLUMN extraschool_copiercode.teacherid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copiercode.teacherid IS 'Teacher';


--
-- Name: COLUMN extraschool_copiercode.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copiercode.name IS 'Code';


--
-- Name: COLUMN extraschool_copiercode.pin; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copiercode.pin IS 'Pin';


--
-- Name: COLUMN extraschool_copiercode.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copiercode.oldid IS 'oldid';


--
-- Name: extraschool_copiercode_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_copiercode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_copiercode_id_seq OWNER TO openerp;

--
-- Name: extraschool_copiercode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_copiercode_id_seq OWNED BY extraschool_copiercode.id;


--
-- Name: extraschool_copierquota; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_copierquota (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    schoolimplantationid integer NOT NULL,
    nbperiods integer,
    nbchilds integer,
    copiercodeid integer NOT NULL,
    nbcopiesdone integer,
    oldid integer
);


ALTER TABLE extraschool_copierquota OWNER TO openerp;

--
-- Name: TABLE extraschool_copierquota; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_copierquota IS 'Copier Quota';


--
-- Name: COLUMN extraschool_copierquota.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copierquota.schoolimplantationid IS 'School implantation';


--
-- Name: COLUMN extraschool_copierquota.nbperiods; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copierquota.nbperiods IS 'Number of periods';


--
-- Name: COLUMN extraschool_copierquota.nbchilds; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copierquota.nbchilds IS 'Number of childs';


--
-- Name: COLUMN extraschool_copierquota.copiercodeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copierquota.copiercodeid IS 'Copier Code';


--
-- Name: COLUMN extraschool_copierquota.nbcopiesdone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copierquota.nbcopiesdone IS 'Number of Copies done';


--
-- Name: COLUMN extraschool_copierquota.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_copierquota.oldid IS 'oldid';


--
-- Name: extraschool_copierquota_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_copierquota_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_copierquota_id_seq OWNER TO openerp;

--
-- Name: extraschool_copierquota_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_copierquota_id_seq OWNED BY extraschool_copierquota.id;


--
-- Name: extraschool_discount; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_discount (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    name character varying(50),
    oneofactivities boolean,
    discount character varying(6),
    period character varying,
    wichactivities character varying,
    discounttype character varying
);


ALTER TABLE extraschool_discount OWNER TO openerp;

--
-- Name: TABLE extraschool_discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discount IS 'Discount';


--
-- Name: COLUMN extraschool_discount.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.name IS 'Name';


--
-- Name: COLUMN extraschool_discount.oneofactivities; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.oneofactivities IS 'One of these activities';


--
-- Name: COLUMN extraschool_discount.discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.discount IS 'Discount';


--
-- Name: COLUMN extraschool_discount.period; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.period IS 'Period';


--
-- Name: COLUMN extraschool_discount.wichactivities; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.wichactivities IS 'Wich activities';


--
-- Name: COLUMN extraschool_discount.discounttype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.discounttype IS 'Discount type';


--
-- Name: extraschool_discount_activity_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_discount_activity_rel (
    discount_id integer NOT NULL,
    activity_id integer NOT NULL
);


ALTER TABLE extraschool_discount_activity_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_discount_activity_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discount_activity_rel IS 'RELATION BETWEEN extraschool_discount AND extraschool_activity';


--
-- Name: extraschool_discount_childtype_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_discount_childtype_rel (
    discount_id integer NOT NULL,
    childtype_id integer NOT NULL
);


ALTER TABLE extraschool_discount_childtype_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_discount_childtype_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discount_childtype_rel IS 'RELATION BETWEEN extraschool_discount AND extraschool_childtype';


--
-- Name: extraschool_discount_discountrule_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_discount_discountrule_rel (
    discount_id integer NOT NULL,
    discountrule_id integer NOT NULL
);


ALTER TABLE extraschool_discount_discountrule_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_discount_discountrule_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discount_discountrule_rel IS 'RELATION BETWEEN extraschool_discount AND extraschool_discountrule';


--
-- Name: extraschool_discount_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_discount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_discount_id_seq OWNER TO openerp;

--
-- Name: extraschool_discount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_discount_id_seq OWNED BY extraschool_discount.id;


--
-- Name: extraschool_discountrule; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_discountrule (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    operator character varying,
    field character varying(60),
    name character varying(50),
    value character varying(50)
);


ALTER TABLE extraschool_discountrule OWNER TO openerp;

--
-- Name: TABLE extraschool_discountrule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discountrule IS 'Discount Rule';


--
-- Name: COLUMN extraschool_discountrule.operator; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.operator IS 'Operator';


--
-- Name: COLUMN extraschool_discountrule.field; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.field IS 'Field';


--
-- Name: COLUMN extraschool_discountrule.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.name IS 'Name';


--
-- Name: COLUMN extraschool_discountrule.value; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.value IS 'Value';


--
-- Name: extraschool_discountrule_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_discountrule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_discountrule_id_seq OWNER TO openerp;

--
-- Name: extraschool_discountrule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_discountrule_id_seq OWNED BY extraschool_discountrule.id;


--
-- Name: extraschool_file_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_file_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    thefile bytea,
    fname character varying(16)
);


ALTER TABLE extraschool_file_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_file_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_file_wizard IS 'extraschool.file_wizard';


--
-- Name: COLUMN extraschool_file_wizard.thefile; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_file_wizard.thefile IS 'File';


--
-- Name: COLUMN extraschool_file_wizard.fname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_file_wizard.fname IS 'File Name';


--
-- Name: extraschool_file_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_file_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_file_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_file_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_file_wizard_id_seq OWNED BY extraschool_file_wizard.id;


--
-- Name: extraschool_guardian; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_guardian (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    lastname character varying(50) NOT NULL,
    tagid character varying(50),
    name character varying(100),
    firstname character varying(50),
    oldid integer
);


ALTER TABLE extraschool_guardian OWNER TO openerp;

--
-- Name: TABLE extraschool_guardian; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_guardian IS 'Guardian';


--
-- Name: COLUMN extraschool_guardian.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_guardian.tagid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.tagid IS 'Tag ID';


--
-- Name: COLUMN extraschool_guardian.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.name IS 'FullName';


--
-- Name: COLUMN extraschool_guardian.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.firstname IS 'FirstName';


--
-- Name: COLUMN extraschool_guardian.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.oldid IS 'oldid';


--
-- Name: extraschool_guardian_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_guardian_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_guardian_id_seq OWNER TO openerp;

--
-- Name: extraschool_guardian_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_guardian_id_seq OWNED BY extraschool_guardian.id;


--
-- Name: extraschool_guardianprestationtimes; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_guardianprestationtimes (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    guardianid integer,
    prestation_date date,
    prestation_time double precision,
    "ES" character varying,
    manualy_encoded boolean
);


ALTER TABLE extraschool_guardianprestationtimes OWNER TO openerp;

--
-- Name: TABLE extraschool_guardianprestationtimes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_guardianprestationtimes IS 'Guardian Prestation Times';


--
-- Name: COLUMN extraschool_guardianprestationtimes.guardianid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.guardianid IS 'Child';


--
-- Name: COLUMN extraschool_guardianprestationtimes.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_guardianprestationtimes.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_guardianprestationtimes."ES"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes."ES" IS 'ES';


--
-- Name: COLUMN extraschool_guardianprestationtimes.manualy_encoded; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.manualy_encoded IS 'Manualy encoded';


--
-- Name: extraschool_guardianprestationtimes_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_guardianprestationtimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_guardianprestationtimes_id_seq OWNER TO openerp;

--
-- Name: extraschool_guardianprestationtimes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_guardianprestationtimes_id_seq OWNED BY extraschool_guardianprestationtimes.id;


--
-- Name: extraschool_guardianprestationtimes_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_guardianprestationtimes_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    guardianid integer NOT NULL,
    state character varying NOT NULL,
    prestations_from date NOT NULL,
    prestationsreport bytea,
    name character varying(16),
    prestations_to date NOT NULL
);


ALTER TABLE extraschool_guardianprestationtimes_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_guardianprestationtimes_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_guardianprestationtimes_wizard IS 'Guardian Prestation Times Wizard';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.guardianid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.guardianid IS 'Guardian';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.prestations_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.prestations_from IS 'Prestations from';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.prestationsreport; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.prestationsreport IS 'File';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.prestations_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.prestations_to IS 'Prestations to';


--
-- Name: extraschool_guardianprestationtimes_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_guardianprestationtimes_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_guardianprestationtimes_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_guardianprestationtimes_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_guardianprestationtimes_wizard_id_seq OWNED BY extraschool_guardianprestationtimes_wizard.id;


--
-- Name: extraschool_importchildtyperule; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_importchildtyperule (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    equalto1 character varying(10),
    childtypeid integer NOT NULL,
    startpos1 integer,
    endpos1 integer
);


ALTER TABLE extraschool_importchildtyperule OWNER TO openerp;

--
-- Name: TABLE extraschool_importchildtyperule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_importchildtyperule IS 'Child import type rule';


--
-- Name: COLUMN extraschool_importchildtyperule.equalto1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importchildtyperule.equalto1 IS 'Equals to1';


--
-- Name: COLUMN extraschool_importchildtyperule.childtypeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importchildtyperule.childtypeid IS 'Child Type';


--
-- Name: COLUMN extraschool_importchildtyperule.startpos1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importchildtyperule.startpos1 IS 'Start pos1';


--
-- Name: COLUMN extraschool_importchildtyperule.endpos1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importchildtyperule.endpos1 IS 'End pos1';


--
-- Name: extraschool_importchildtyperule_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_importchildtyperule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_importchildtyperule_id_seq OWNER TO openerp;

--
-- Name: extraschool_importchildtyperule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_importchildtyperule_id_seq OWNED BY extraschool_importchildtyperule.id;


--
-- Name: extraschool_importlevelrule; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_importlevelrule (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    equalto1 character varying(10),
    levelid integer NOT NULL,
    startpos1 integer,
    endpos1 integer
);


ALTER TABLE extraschool_importlevelrule OWNER TO openerp;

--
-- Name: TABLE extraschool_importlevelrule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_importlevelrule IS 'Child import level rule';


--
-- Name: COLUMN extraschool_importlevelrule.equalto1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.equalto1 IS 'Equals to1';


--
-- Name: COLUMN extraschool_importlevelrule.levelid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.levelid IS 'Level';


--
-- Name: COLUMN extraschool_importlevelrule.startpos1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.startpos1 IS 'Start pos1';


--
-- Name: COLUMN extraschool_importlevelrule.endpos1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.endpos1 IS 'End pos1';


--
-- Name: extraschool_importlevelrule_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_importlevelrule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_importlevelrule_id_seq OWNER TO openerp;

--
-- Name: extraschool_importlevelrule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_importlevelrule_id_seq OWNED BY extraschool_importlevelrule.id;


--
-- Name: extraschool_importreject; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_importreject (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    line integer,
    rejectcause character varying(60),
    childsimport integer
);


ALTER TABLE extraschool_importreject OWNER TO openerp;

--
-- Name: TABLE extraschool_importreject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_importreject IS 'Import Reject';


--
-- Name: COLUMN extraschool_importreject.line; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.line IS 'Line';


--
-- Name: COLUMN extraschool_importreject.rejectcause; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.rejectcause IS 'Reject cause';


--
-- Name: COLUMN extraschool_importreject.childsimport; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.childsimport IS 'Childs import';


--
-- Name: extraschool_importreject_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_importreject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_importreject_id_seq OWNER TO openerp;

--
-- Name: extraschool_importreject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_importreject_id_seq OWNED BY extraschool_importreject.id;


--
-- Name: extraschool_initupdate_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_initupdate_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer
);


ALTER TABLE extraschool_initupdate_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_initupdate_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_initupdate_wizard IS 'extraschool.initupdate_wizard';


--
-- Name: extraschool_initupdate_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_initupdate_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_initupdate_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_initupdate_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_initupdate_wizard_id_seq OWNED BY extraschool_initupdate_wizard.id;


--
-- Name: extraschool_invoice; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_invoice (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    amount_received double precision,
    number integer,
    discount double precision,
    biller_id integer,
    oldid character varying(20),
    parentid integer,
    amount_total double precision,
    schoolimplantationid integer,
    name character varying(20),
    invoice_file bytea,
    filename character varying(20),
    no_value double precision,
    structcom character varying(50),
    balance double precision
);


ALTER TABLE extraschool_invoice OWNER TO openerp;

--
-- Name: TABLE extraschool_invoice; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoice IS 'invoice';


--
-- Name: COLUMN extraschool_invoice.amount_received; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.amount_received IS 'Received';


--
-- Name: COLUMN extraschool_invoice.number; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.number IS 'Number';


--
-- Name: COLUMN extraschool_invoice.discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.discount IS 'Discount';


--
-- Name: COLUMN extraschool_invoice.biller_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.biller_id IS 'Biller';


--
-- Name: COLUMN extraschool_invoice.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_invoice.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.parentid IS 'Parent';


--
-- Name: COLUMN extraschool_invoice.amount_total; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.amount_total IS 'Amount';


--
-- Name: COLUMN extraschool_invoice.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.schoolimplantationid IS 'School implantation';


--
-- Name: COLUMN extraschool_invoice.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.name IS 'Name';


--
-- Name: COLUMN extraschool_invoice.invoice_file; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.invoice_file IS 'File';


--
-- Name: COLUMN extraschool_invoice.filename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.filename IS 'filename';


--
-- Name: COLUMN extraschool_invoice.no_value; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.no_value IS 'No value';


--
-- Name: COLUMN extraschool_invoice.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.structcom IS 'Structured Communication';


--
-- Name: COLUMN extraschool_invoice.balance; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.balance IS 'Balance';


--
-- Name: extraschool_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_invoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_invoice_id_seq OWNER TO openerp;

--
-- Name: extraschool_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_invoice_id_seq OWNED BY extraschool_invoice.id;


--
-- Name: extraschool_invoice_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_invoice_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    name character varying(16),
    invoice_term date NOT NULL,
    invoices bytea,
    period_to date NOT NULL,
    invoice_date date NOT NULL,
    period_from date NOT NULL,
    state character varying NOT NULL,
    activitycategory integer NOT NULL
);


ALTER TABLE extraschool_invoice_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_invoice_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoice_wizard IS 'extraschool.invoice_wizard';


--
-- Name: COLUMN extraschool_invoice_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_invoice_wizard.invoice_term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.invoice_term IS 'invoice term';


--
-- Name: COLUMN extraschool_invoice_wizard.invoices; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.invoices IS 'File';


--
-- Name: COLUMN extraschool_invoice_wizard.period_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.period_to IS 'Period to';


--
-- Name: COLUMN extraschool_invoice_wizard.invoice_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.invoice_date IS 'invoice date';


--
-- Name: COLUMN extraschool_invoice_wizard.period_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.period_from IS 'Period from';


--
-- Name: COLUMN extraschool_invoice_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_invoice_wizard.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.activitycategory IS 'Activity category';


--
-- Name: extraschool_invoice_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_invoice_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_invoice_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_invoice_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_invoice_wizard_id_seq OWNED BY extraschool_invoice_wizard.id;


--
-- Name: extraschool_invoicedprestations; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_invoicedprestations (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    discount boolean,
    activityid integer,
    invoiceid integer,
    prestation_date date,
    childid integer,
    quantity integer,
    placeid integer
);


ALTER TABLE extraschool_invoicedprestations OWNER TO openerp;

--
-- Name: TABLE extraschool_invoicedprestations; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoicedprestations IS 'invoiced Prestations';


--
-- Name: COLUMN extraschool_invoicedprestations.discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.discount IS 'Discount';


--
-- Name: COLUMN extraschool_invoicedprestations.activityid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.activityid IS 'Activity';


--
-- Name: COLUMN extraschool_invoicedprestations.invoiceid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.invoiceid IS 'invoice';


--
-- Name: COLUMN extraschool_invoicedprestations.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_invoicedprestations.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.childid IS 'Child';


--
-- Name: COLUMN extraschool_invoicedprestations.quantity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.quantity IS 'Quantity';


--
-- Name: COLUMN extraschool_invoicedprestations.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.placeid IS 'Place';


--
-- Name: extraschool_invoicedprestations_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_invoicedprestations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_invoicedprestations_id_seq OWNER TO openerp;

--
-- Name: extraschool_invoicedprestations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_invoicedprestations_id_seq OWNED BY extraschool_invoicedprestations.id;


--
-- Name: extraschool_level; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_level (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    ordernumber integer NOT NULL,
    leveltype character varying NOT NULL,
    name character varying(50),
    oldid integer
);


ALTER TABLE extraschool_level OWNER TO openerp;

--
-- Name: TABLE extraschool_level; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_level IS 'Level';


--
-- Name: COLUMN extraschool_level.ordernumber; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.ordernumber IS 'ordernumber';


--
-- Name: COLUMN extraschool_level.leveltype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.leveltype IS 'Level Type';


--
-- Name: COLUMN extraschool_level.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.name IS 'Name';


--
-- Name: COLUMN extraschool_level.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.oldid IS 'oldid';


--
-- Name: extraschool_level_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_level_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_level_id_seq OWNER TO openerp;

--
-- Name: extraschool_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_level_id_seq OWNED BY extraschool_level.id;


--
-- Name: extraschool_mainsettings; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_mainsettings (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    codasfolder character varying(80),
    processedcodasfolder character varying(80),
    qrencode character varying(80),
    lastqrcodenbr integer,
    tempfolder character varying(80),
    templatesfolder character varying(80),
    emailfornotifications character varying(80),
    leveldeterminationbirthdate date,
    levelbeforedisable integer
);


ALTER TABLE extraschool_mainsettings OWNER TO openerp;

--
-- Name: TABLE extraschool_mainsettings; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_mainsettings IS 'Main Settings';


--
-- Name: COLUMN extraschool_mainsettings.codasfolder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.codasfolder IS 'codasfolder';


--
-- Name: COLUMN extraschool_mainsettings.processedcodasfolder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.processedcodasfolder IS 'processedcodasfolder';


--
-- Name: COLUMN extraschool_mainsettings.qrencode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.qrencode IS 'qrencode';


--
-- Name: COLUMN extraschool_mainsettings.lastqrcodenbr; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.lastqrcodenbr IS 'lastqrcodenbr';


--
-- Name: COLUMN extraschool_mainsettings.tempfolder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.tempfolder IS 'tempfolder';


--
-- Name: COLUMN extraschool_mainsettings.templatesfolder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.templatesfolder IS 'templatesfolder';


--
-- Name: COLUMN extraschool_mainsettings.emailfornotifications; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.emailfornotifications IS 'Email for notifications';


--
-- Name: COLUMN extraschool_mainsettings.leveldeterminationbirthdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.leveldeterminationbirthdate IS 'Level determination birthdate';


--
-- Name: COLUMN extraschool_mainsettings.levelbeforedisable; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.levelbeforedisable IS 'Level before disable';


--
-- Name: extraschool_mainsettings_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_mainsettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_mainsettings_id_seq OWNER TO openerp;

--
-- Name: extraschool_mainsettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_mainsettings_id_seq OWNED BY extraschool_mainsettings.id;


--
-- Name: extraschool_parent; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_parent (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    city character varying(50) NOT NULL,
    workphone character varying(20),
    name character varying(100),
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    housephone character varying(20),
    zipcode character varying(6) NOT NULL,
    street character varying(50) NOT NULL,
    oldid integer,
    gsm character varying(20),
    streetcode character varying(50),
    email character varying(100),
    invoicesendmethod character varying NOT NULL,
    remindersendmethod character varying NOT NULL
);


ALTER TABLE extraschool_parent OWNER TO openerp;

--
-- Name: TABLE extraschool_parent; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_parent IS 'Parent';


--
-- Name: COLUMN extraschool_parent.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.city IS 'City';


--
-- Name: COLUMN extraschool_parent.workphone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.workphone IS 'Work Phone';


--
-- Name: COLUMN extraschool_parent.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.name IS 'FullName';


--
-- Name: COLUMN extraschool_parent.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.firstname IS 'FirstName';


--
-- Name: COLUMN extraschool_parent.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_parent.housephone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.housephone IS 'House Phone';


--
-- Name: COLUMN extraschool_parent.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_parent.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.street IS 'Street';


--
-- Name: COLUMN extraschool_parent.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_parent.gsm; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.gsm IS 'GSM';


--
-- Name: COLUMN extraschool_parent.streetcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.streetcode IS 'Street code';


--
-- Name: COLUMN extraschool_parent.invoicesendmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.invoicesendmethod IS 'Invoice send method';


--
-- Name: COLUMN extraschool_parent.remindersendmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.remindersendmethod IS 'Invoice send method';


--
-- Name: extraschool_parent_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_parent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_parent_id_seq OWNER TO openerp;

--
-- Name: extraschool_parent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_parent_id_seq OWNED BY extraschool_parent.id;


--
-- Name: extraschool_payment; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_payment (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    account character varying(20),
    name character varying(50),
    coda integer,
    addr1 character varying(50),
    paymenttype character varying,
    amount double precision,
    addr2 character varying(50),
    paymentdate date,
    structcom character varying(50),
    concernedinvoice integer
);


ALTER TABLE extraschool_payment OWNER TO openerp;

--
-- Name: TABLE extraschool_payment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_payment IS 'Payment';


--
-- Name: COLUMN extraschool_payment.account; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.account IS 'Account';


--
-- Name: COLUMN extraschool_payment.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.name IS 'Name';


--
-- Name: COLUMN extraschool_payment.coda; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.coda IS 'Coda';


--
-- Name: COLUMN extraschool_payment.addr1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.addr1 IS 'Addr1';


--
-- Name: COLUMN extraschool_payment.paymenttype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.paymenttype IS 'Payment type';


--
-- Name: COLUMN extraschool_payment.amount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.amount IS 'Amount';


--
-- Name: COLUMN extraschool_payment.addr2; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.addr2 IS 'Addr2';


--
-- Name: COLUMN extraschool_payment.paymentdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.paymentdate IS 'Date';


--
-- Name: COLUMN extraschool_payment.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.structcom IS 'Structured Communication';


--
-- Name: COLUMN extraschool_payment.concernedinvoice; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.concernedinvoice IS 'Concerned invoice';


--
-- Name: extraschool_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_payment_id_seq OWNER TO openerp;

--
-- Name: extraschool_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_payment_id_seq OWNED BY extraschool_payment.id;


--
-- Name: extraschool_pdaprestationtimes; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_pdaprestationtimes (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    activitycategoryid integer,
    prestation_date date,
    prestation_time double precision,
    childid integer,
    "ES" character varying,
    placeid integer NOT NULL
);


ALTER TABLE extraschool_pdaprestationtimes OWNER TO openerp;

--
-- Name: TABLE extraschool_pdaprestationtimes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_pdaprestationtimes IS 'PDA Prestation Times';


--
-- Name: COLUMN extraschool_pdaprestationtimes.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_pdaprestationtimes.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_pdaprestationtimes.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_pdaprestationtimes.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.childid IS 'Child';


--
-- Name: COLUMN extraschool_pdaprestationtimes."ES"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes."ES" IS 'ES';


--
-- Name: COLUMN extraschool_pdaprestationtimes.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.placeid IS 'Schoolcare Place';


--
-- Name: extraschool_pdaprestationtimes_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_pdaprestationtimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_pdaprestationtimes_id_seq OWNER TO openerp;

--
-- Name: extraschool_pdaprestationtimes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_pdaprestationtimes_id_seq OWNED BY extraschool_pdaprestationtimes.id;


--
-- Name: extraschool_place; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_place (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    city character varying(50),
    street character varying(50),
    name character varying(50),
    zipcode character varying(6),
    oldid integer,
    schedule text
);


ALTER TABLE extraschool_place OWNER TO openerp;

--
-- Name: TABLE extraschool_place; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_place IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_place.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.city IS 'City';


--
-- Name: COLUMN extraschool_place.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.street IS 'Street';


--
-- Name: COLUMN extraschool_place.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.name IS 'Name';


--
-- Name: COLUMN extraschool_place.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_place.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_place.schedule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.schedule IS 'Schedule';


--
-- Name: extraschool_place_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_place_id_seq OWNER TO openerp;

--
-- Name: extraschool_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_place_id_seq OWNED BY extraschool_place.id;


--
-- Name: extraschool_place_schoolimplantation_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_place_schoolimplantation_rel (
    place_id integer NOT NULL,
    schoolimplantation_id integer NOT NULL
);


ALTER TABLE extraschool_place_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_place_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_place_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_place AND extraschool_schoolimplantation';


--
-- Name: extraschool_prestations_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_prestations_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    es character varying,
    activitycategory integer,
    prestation_date date,
    schoolimplantationid integer,
    prestation_time character varying(5),
    childid integer NOT NULL,
    placeid integer NOT NULL
);


ALTER TABLE extraschool_prestations_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_prestations_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestations_wizard IS 'extraschool.prestations_wizard';


--
-- Name: COLUMN extraschool_prestations_wizard.es; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.es IS 'ES';


--
-- Name: COLUMN extraschool_prestations_wizard.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.activitycategory IS 'Activity category';


--
-- Name: COLUMN extraschool_prestations_wizard.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.prestation_date IS 'Prestation Date';


--
-- Name: COLUMN extraschool_prestations_wizard.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.schoolimplantationid IS 'School Implantation';


--
-- Name: COLUMN extraschool_prestations_wizard.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_prestations_wizard.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.childid IS 'Child';


--
-- Name: COLUMN extraschool_prestations_wizard.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestations_wizard.placeid IS 'Schoolcare Place';


--
-- Name: extraschool_prestations_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestations_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_prestations_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestations_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestations_wizard_id_seq OWNED BY extraschool_prestations_wizard.id;


--
-- Name: extraschool_prestationscheck_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_prestationscheck_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    period_to date NOT NULL,
    period_from date NOT NULL,
    state character varying NOT NULL,
    activitycategory integer,
    childid integer,
    currentdate date,
    schoolimplantationid integer,
    prestation_time character varying(5),
    es character varying
);


ALTER TABLE extraschool_prestationscheck_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_prestationscheck_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestationscheck_wizard IS 'extraschool.prestationscheck_wizard';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.period_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.period_to IS 'Period to';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.period_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.period_from IS 'Period from';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.activitycategory IS 'Activity category';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.childid IS 'Child';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.currentdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.currentdate IS 'Current date';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.schoolimplantationid IS 'School implantation';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.es; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.es IS 'ES';


--
-- Name: extraschool_prestationscheck_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestationscheck_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_prestationscheck_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestationscheck_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestationscheck_wizard_id_seq OWNED BY extraschool_prestationscheck_wizard.id;


--
-- Name: extraschool_prestationtimes; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_prestationtimes (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    verified boolean,
    prestation_date date,
    childid integer,
    activitycategoryid integer,
    manualy_encoded boolean,
    prestation_time double precision NOT NULL,
    "ES" character varying NOT NULL,
    placeid integer,
    activityid integer
);


ALTER TABLE extraschool_prestationtimes OWNER TO openerp;

--
-- Name: TABLE extraschool_prestationtimes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestationtimes IS 'Prestation Times';


--
-- Name: COLUMN extraschool_prestationtimes.verified; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.verified IS 'Verified';


--
-- Name: COLUMN extraschool_prestationtimes.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_prestationtimes.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.childid IS 'Child';


--
-- Name: COLUMN extraschool_prestationtimes.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_prestationtimes.manualy_encoded; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.manualy_encoded IS 'Manualy encoded';


--
-- Name: COLUMN extraschool_prestationtimes.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_prestationtimes."ES"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes."ES" IS 'ES';


--
-- Name: COLUMN extraschool_prestationtimes.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_prestationtimes.activityid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.activityid IS 'Activity';


--
-- Name: extraschool_prestationtimes_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestationtimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_prestationtimes_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestationtimes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestationtimes_id_seq OWNED BY extraschool_prestationtimes.id;


--
-- Name: extraschool_qrcodes_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_qrcodes_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    state character varying NOT NULL,
    name character varying(16),
    qrcodes bytea,
    quantity integer
);


ALTER TABLE extraschool_qrcodes_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_qrcodes_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_qrcodes_wizard IS 'extraschool.qrcodes_wizard';


--
-- Name: COLUMN extraschool_qrcodes_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_qrcodes_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_qrcodes_wizard.qrcodes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.qrcodes IS 'File';


--
-- Name: COLUMN extraschool_qrcodes_wizard.quantity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.quantity IS 'Quantity to print';


--
-- Name: extraschool_qrcodes_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_qrcodes_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_qrcodes_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_qrcodes_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_qrcodes_wizard_id_seq OWNED BY extraschool_qrcodes_wizard.id;


--
-- Name: extraschool_quotaadjustment; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_quotaadjustment (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    reason character varying,
    copierquotaid integer,
    oldid integer,
    quotaadjustment integer
);


ALTER TABLE extraschool_quotaadjustment OWNER TO openerp;

--
-- Name: TABLE extraschool_quotaadjustment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_quotaadjustment IS 'Quota adjustment';


--
-- Name: COLUMN extraschool_quotaadjustment.reason; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_quotaadjustment.reason IS 'Reason';


--
-- Name: COLUMN extraschool_quotaadjustment.copierquotaid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_quotaadjustment.copierquotaid IS 'Copier Quota';


--
-- Name: COLUMN extraschool_quotaadjustment.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_quotaadjustment.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_quotaadjustment.quotaadjustment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_quotaadjustment.quotaadjustment IS 'Adjustment of quota';


--
-- Name: extraschool_quotaadjustment_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_quotaadjustment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_quotaadjustment_id_seq OWNER TO openerp;

--
-- Name: extraschool_quotaadjustment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_quotaadjustment_id_seq OWNED BY extraschool_quotaadjustment.id;


--
-- Name: extraschool_reject; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_reject (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    account character varying(20),
    name character varying(50),
    coda integer,
    addr1 character varying(50),
    rejectcause character varying(60),
    amount double precision,
    addr2 character varying(50),
    paymentdate date,
    structcom character varying(50)
);


ALTER TABLE extraschool_reject OWNER TO openerp;

--
-- Name: TABLE extraschool_reject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reject IS 'Reject';


--
-- Name: COLUMN extraschool_reject.account; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.account IS 'Account';


--
-- Name: COLUMN extraschool_reject.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.name IS 'Name';


--
-- Name: COLUMN extraschool_reject.coda; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.coda IS 'Coda';


--
-- Name: COLUMN extraschool_reject.addr1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.addr1 IS 'Addr1';


--
-- Name: COLUMN extraschool_reject.rejectcause; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.rejectcause IS 'Reject cause';


--
-- Name: COLUMN extraschool_reject.amount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.amount IS 'Amount';


--
-- Name: COLUMN extraschool_reject.addr2; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.addr2 IS 'Addr2';


--
-- Name: COLUMN extraschool_reject.paymentdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.paymentdate IS 'Date';


--
-- Name: COLUMN extraschool_reject.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.structcom IS 'Structured Communication';


--
-- Name: extraschool_reject_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_reject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_reject_id_seq OWNER TO openerp;

--
-- Name: extraschool_reject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_reject_id_seq OWNED BY extraschool_reject.id;


--
-- Name: extraschool_reminder; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_reminder (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    amount double precision,
    schoolimplantationid integer,
    parentid integer,
    remindersjournalid integer,
    structcom character varying(50),
    reminder_file bytea,
    filename character varying(30)
);


ALTER TABLE extraschool_reminder OWNER TO openerp;

--
-- Name: TABLE extraschool_reminder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reminder IS 'Reminder';


--
-- Name: COLUMN extraschool_reminder.amount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.amount IS 'Amount';


--
-- Name: COLUMN extraschool_reminder.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.schoolimplantationid IS 'School implantation';


--
-- Name: COLUMN extraschool_reminder.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.parentid IS 'Parent';


--
-- Name: COLUMN extraschool_reminder.remindersjournalid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.remindersjournalid IS 'Reminders journal';


--
-- Name: COLUMN extraschool_reminder.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.structcom IS 'Structured Communication';


--
-- Name: COLUMN extraschool_reminder.reminder_file; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.reminder_file IS 'File';


--
-- Name: extraschool_reminder_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_reminder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_reminder_id_seq OWNER TO openerp;

--
-- Name: extraschool_reminder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_reminder_id_seq OWNED BY extraschool_reminder.id;


--
-- Name: extraschool_reminder_invoice_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_reminder_invoice_rel (
    reminder_id integer NOT NULL,
    invoice_id integer NOT NULL
);


ALTER TABLE extraschool_reminder_invoice_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_reminder_invoice_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reminder_invoice_rel IS 'RELATION BETWEEN extraschool_reminder AND extraschool_invoice';


--
-- Name: extraschool_reminders_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_reminders_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    unpaidinvoicefrom date NOT NULL,
    term date,
    name character varying(16),
    transmissiondate date,
    minamount double precision,
    unpaidinvoiceto date NOT NULL,
    state character varying NOT NULL,
    activitycategoryid integer,
    reminders bytea
);


ALTER TABLE extraschool_reminders_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_reminders_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reminders_wizard IS 'extraschool.reminders_wizard';


--
-- Name: COLUMN extraschool_reminders_wizard.unpaidinvoicefrom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.unpaidinvoicefrom IS 'Unpaid invoices from';


--
-- Name: COLUMN extraschool_reminders_wizard.term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.term IS 'Term';


--
-- Name: COLUMN extraschool_reminders_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_reminders_wizard.transmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.transmissiondate IS 'Transmission date';


--
-- Name: COLUMN extraschool_reminders_wizard.minamount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.minamount IS 'Minimum amount';


--
-- Name: COLUMN extraschool_reminders_wizard.unpaidinvoiceto; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.unpaidinvoiceto IS 'to';


--
-- Name: COLUMN extraschool_reminders_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_reminders_wizard.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_reminders_wizard.reminders; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminders_wizard.reminders IS 'File';


--
-- Name: extraschool_reminders_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_reminders_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_reminders_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_reminders_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_reminders_wizard_id_seq OWNED BY extraschool_reminders_wizard.id;


--
-- Name: extraschool_remindersjournal; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_remindersjournal (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    unpaidinvoicefrom date,
    term date NOT NULL,
    oldid integer,
    activitycategoryid integer NOT NULL,
    transmissiondate date NOT NULL,
    minamount double precision NOT NULL,
    unpaidinvoiceto date,
    reminders bytea,
    remindertype integer NOT NULL,
    filename character varying(16),
    name character varying(80) NOT NULL
);


ALTER TABLE extraschool_remindersjournal OWNER TO openerp;

--
-- Name: TABLE extraschool_remindersjournal; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_remindersjournal IS 'Reminders journal';


--
-- Name: COLUMN extraschool_remindersjournal.unpaidinvoicefrom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.unpaidinvoicefrom IS 'Unpaid invoices from';


--
-- Name: COLUMN extraschool_remindersjournal.term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.term IS 'Term';


--
-- Name: COLUMN extraschool_remindersjournal.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_remindersjournal.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_remindersjournal.transmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.transmissiondate IS 'Transmission date';


--
-- Name: COLUMN extraschool_remindersjournal.minamount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.minamount IS 'Minimum amount';


--
-- Name: COLUMN extraschool_remindersjournal.unpaidinvoiceto; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.unpaidinvoiceto IS 'to';


--
-- Name: COLUMN extraschool_remindersjournal.reminders; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.reminders IS 'File';


--
-- Name: COLUMN extraschool_remindersjournal.remindertype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.remindertype IS 'Reminder type';


--
-- Name: COLUMN extraschool_remindersjournal.filename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.filename IS 'File Name';


--
-- Name: COLUMN extraschool_remindersjournal.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.name IS 'Name';


--
-- Name: extraschool_remindersjournal_biller_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_remindersjournal_biller_rel (
    remindersjournal_id integer NOT NULL,
    biller_id integer NOT NULL
);


ALTER TABLE extraschool_remindersjournal_biller_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_remindersjournal_biller_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_remindersjournal_biller_rel IS 'RELATION BETWEEN extraschool_remindersjournal AND extraschool_biller';


--
-- Name: extraschool_remindersjournal_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_remindersjournal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_remindersjournal_id_seq OWNER TO openerp;

--
-- Name: extraschool_remindersjournal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_remindersjournal_id_seq OWNED BY extraschool_remindersjournal.id;


--
-- Name: extraschool_remindertype; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_remindertype (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    "order" integer,
    name character varying(50),
    template character varying(50),
    fees double precision
);


ALTER TABLE extraschool_remindertype OWNER TO openerp;

--
-- Name: TABLE extraschool_remindertype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_remindertype IS 'Reminder type';


--
-- Name: COLUMN extraschool_remindertype."order"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype."order" IS 'Order';


--
-- Name: COLUMN extraschool_remindertype.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.name IS 'name';


--
-- Name: COLUMN extraschool_remindertype.template; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.template IS 'Template';


--
-- Name: COLUMN extraschool_remindertype.fees; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.fees IS 'Amount';


--
-- Name: extraschool_remindertype_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_remindertype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_remindertype_id_seq OWNER TO openerp;

--
-- Name: extraschool_remindertype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_remindertype_id_seq OWNED BY extraschool_remindertype.id;


--
-- Name: extraschool_scheduledtasks; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_scheduledtasks (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer
);


ALTER TABLE extraschool_scheduledtasks OWNER TO openerp;

--
-- Name: TABLE extraschool_scheduledtasks; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_scheduledtasks IS 'Scheduled tasks';


--
-- Name: extraschool_scheduledtasks_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_scheduledtasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_scheduledtasks_id_seq OWNER TO openerp;

--
-- Name: extraschool_scheduledtasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_scheduledtasks_id_seq OWNED BY extraschool_scheduledtasks.id;


--
-- Name: extraschool_school; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_school (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    city character varying(50),
    street character varying(50),
    name character varying(50),
    zipcode character varying(6),
    oldid integer
);


ALTER TABLE extraschool_school OWNER TO openerp;

--
-- Name: TABLE extraschool_school; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_school IS 'School';


--
-- Name: COLUMN extraschool_school.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.city IS 'City';


--
-- Name: COLUMN extraschool_school.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.street IS 'Street';


--
-- Name: COLUMN extraschool_school.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.name IS 'Name';


--
-- Name: COLUMN extraschool_school.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_school.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.oldid IS 'oldid';


--
-- Name: extraschool_school_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_school_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_school_id_seq OWNER TO openerp;

--
-- Name: extraschool_school_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_school_id_seq OWNED BY extraschool_school.id;


--
-- Name: extraschool_schoolimplantation; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_schoolimplantation (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    city character varying(50),
    schoolid integer,
    street character varying(50),
    name character varying(50),
    zipcode character varying(6),
    oldid integer
);


ALTER TABLE extraschool_schoolimplantation OWNER TO openerp;

--
-- Name: TABLE extraschool_schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_schoolimplantation.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.city IS 'City';


--
-- Name: COLUMN extraschool_schoolimplantation.schoolid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.schoolid IS 'School';


--
-- Name: COLUMN extraschool_schoolimplantation.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.street IS 'Street';


--
-- Name: COLUMN extraschool_schoolimplantation.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.name IS 'Name';


--
-- Name: COLUMN extraschool_schoolimplantation.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_schoolimplantation.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.oldid IS 'oldid';


--
-- Name: extraschool_schoolimplantation_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_schoolimplantation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_schoolimplantation_id_seq OWNER TO openerp;

--
-- Name: extraschool_schoolimplantation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_schoolimplantation_id_seq OWNED BY extraschool_schoolimplantation.id;


--
-- Name: extraschool_smartphone; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_smartphone (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    softwareurl character varying(100),
    lasttransmissiondate timestamp without time zone,
    name character varying(50),
    username character varying(30),
    qrconfig bytea,
    userpassword character varying(20),
    placeid integer NOT NULL,
    scanmethod character varying,
    transfertmethod character varying,
    databasename character varying(30),
    qrdownload bytea,
    serveraddress character varying(50),
    transmissiontime character varying(5),
    maxtimedelta integer,
    oldversion boolean
);


ALTER TABLE extraschool_smartphone OWNER TO openerp;

--
-- Name: TABLE extraschool_smartphone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_smartphone IS 'Smartphone';


--
-- Name: COLUMN extraschool_smartphone.softwareurl; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.softwareurl IS 'Software url';


--
-- Name: COLUMN extraschool_smartphone.lasttransmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.lasttransmissiondate IS 'Last Transmission Date';


--
-- Name: COLUMN extraschool_smartphone.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.name IS 'Name';


--
-- Name: COLUMN extraschool_smartphone.username; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.username IS 'User name';


--
-- Name: COLUMN extraschool_smartphone.qrconfig; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.qrconfig IS 'QR Config';


--
-- Name: COLUMN extraschool_smartphone.userpassword; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.userpassword IS 'User password';


--
-- Name: COLUMN extraschool_smartphone.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_smartphone.scanmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.scanmethod IS 'Scan method';


--
-- Name: COLUMN extraschool_smartphone.transfertmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.transfertmethod IS 'Transfert method';


--
-- Name: COLUMN extraschool_smartphone.databasename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.databasename IS 'Database name';


--
-- Name: COLUMN extraschool_smartphone.qrdownload; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.qrdownload IS 'QR Download';


--
-- Name: COLUMN extraschool_smartphone.serveraddress; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.serveraddress IS 'Server address';


--
-- Name: COLUMN extraschool_smartphone.transmissiontime; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.transmissiontime IS 'Transmission time';


--
-- Name: COLUMN extraschool_smartphone.maxtimedelta; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.maxtimedelta IS 'Max time delta';


--
-- Name: COLUMN extraschool_smartphone.oldversion; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.oldversion IS 'Old version';


--
-- Name: extraschool_smartphone_activitycategory_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_smartphone_activitycategory_rel (
    smartphone_id integer NOT NULL,
    activitycategory_id integer NOT NULL
);


ALTER TABLE extraschool_smartphone_activitycategory_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_smartphone_activitycategory_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_smartphone_activitycategory_rel IS 'RELATION BETWEEN extraschool_smartphone AND extraschool_activitycategory';


--
-- Name: extraschool_smartphone_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_smartphone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_smartphone_id_seq OWNER TO openerp;

--
-- Name: extraschool_smartphone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_smartphone_id_seq OWNED BY extraschool_smartphone.id;


--
-- Name: extraschool_smartphone_schoolimplantation_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_smartphone_schoolimplantation_rel (
    smartphone_id integer NOT NULL,
    schoolimplantation_id integer NOT NULL
);


ALTER TABLE extraschool_smartphone_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_smartphone_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_smartphone_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_smartphone AND extraschool_schoolimplantation';


--
-- Name: extraschool_statsone_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_statsone_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    schoolimplantationid integer,
    name character varying(16),
    transmissiondate date NOT NULL,
    statsone bytea,
    state character varying NOT NULL,
    activitycategory integer NOT NULL,
    year integer NOT NULL,
    quarter character varying NOT NULL,
    placeid integer NOT NULL
);


ALTER TABLE extraschool_statsone_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_statsone_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_statsone_wizard IS 'extraschool.statsone_wizard';


--
-- Name: COLUMN extraschool_statsone_wizard.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.schoolimplantationid IS 'School implantation';


--
-- Name: COLUMN extraschool_statsone_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_statsone_wizard.transmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.transmissiondate IS 'Transmission date';


--
-- Name: COLUMN extraschool_statsone_wizard.statsone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.statsone IS 'File';


--
-- Name: COLUMN extraschool_statsone_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_statsone_wizard.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.activitycategory IS 'Activity category';


--
-- Name: COLUMN extraschool_statsone_wizard.year; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.year IS 'Year';


--
-- Name: COLUMN extraschool_statsone_wizard.quarter; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.quarter IS 'Quarter';


--
-- Name: COLUMN extraschool_statsone_wizard.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_statsone_wizard.placeid IS 'Schoolcare Place';


--
-- Name: extraschool_statsone_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_statsone_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_statsone_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_statsone_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_statsone_wizard_id_seq OWNED BY extraschool_statsone_wizard.id;


--
-- Name: extraschool_taxcertificates_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_taxcertificates_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    state character varying NOT NULL,
    taxcertificates bytea,
    year character varying(4),
    activitycategory integer NOT NULL,
    name character varying(50),
    parentid integer
);


ALTER TABLE extraschool_taxcertificates_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_taxcertificates_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_taxcertificates_wizard IS 'extraschool.taxcertificates_wizard';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.taxcertificates; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.taxcertificates IS 'File';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.year; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.year IS 'Year';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.activitycategory IS 'Activity category';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.parentid IS 'Parent';


--
-- Name: extraschool_taxcertificates_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_taxcertificates_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_taxcertificates_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_taxcertificates_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_taxcertificates_wizard_id_seq OWNED BY extraschool_taxcertificates_wizard.id;


--
-- Name: extraschool_teacher; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_teacher (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    oldid integer,
    lastname character varying(50) NOT NULL,
    name character varying(100),
    firstname character varying(50) NOT NULL
);


ALTER TABLE extraschool_teacher OWNER TO openerp;

--
-- Name: TABLE extraschool_teacher; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_teacher IS 'Teacher';


--
-- Name: COLUMN extraschool_teacher.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_teacher.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_teacher.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_teacher.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_teacher.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_teacher.firstname IS 'FirstName';


--
-- Name: extraschool_teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_teacher_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_teacher_id_seq OWNER TO openerp;

--
-- Name: extraschool_teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_teacher_id_seq OWNED BY extraschool_teacher.id;


--
-- Name: extraschool_timecorrection_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace: 
--

CREATE TABLE extraschool_timecorrection_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_date timestamp without time zone,
    write_uid integer,
    state character varying NOT NULL,
    correctiontype character varying NOT NULL,
    dateto date NOT NULL,
    datefrom date NOT NULL,
    correctiontime double precision NOT NULL
);


ALTER TABLE extraschool_timecorrection_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_timecorrection_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_timecorrection_wizard IS 'extraschool.timecorrection_wizard';


--
-- Name: COLUMN extraschool_timecorrection_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_timecorrection_wizard.correctiontype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.correctiontype IS 'Correction type';


--
-- Name: COLUMN extraschool_timecorrection_wizard.dateto; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.dateto IS 'Date to';


--
-- Name: COLUMN extraschool_timecorrection_wizard.datefrom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.datefrom IS 'Date from';


--
-- Name: COLUMN extraschool_timecorrection_wizard.correctiontime; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.correctiontime IS 'Time';


--
-- Name: extraschool_timecorrection_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_timecorrection_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE extraschool_timecorrection_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_timecorrection_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_timecorrection_wizard_id_seq OWNED BY extraschool_timecorrection_wizard.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity ALTER COLUMN id SET DEFAULT nextval('extraschool_activity_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory ALTER COLUMN id SET DEFAULT nextval('extraschool_activitycategory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitychildregistration ALTER COLUMN id SET DEFAULT nextval('extraschool_activitychildregistration_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityexclusiondates ALTER COLUMN id SET DEFAULT nextval('extraschool_activityexclusiondates_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityplanneddate ALTER COLUMN id SET DEFAULT nextval('extraschool_activityplanneddate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_biller ALTER COLUMN id SET DEFAULT nextval('extraschool_biller_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child ALTER COLUMN id SET DEFAULT nextval('extraschool_child_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childposition ALTER COLUMN id SET DEFAULT nextval('extraschool_childposition_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimport ALTER COLUMN id SET DEFAULT nextval('extraschool_childsimport_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter ALTER COLUMN id SET DEFAULT nextval('extraschool_childsimportfilter_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_childsworkbook_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childtype ALTER COLUMN id SET DEFAULT nextval('extraschool_childtype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class ALTER COLUMN id SET DEFAULT nextval('extraschool_class_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_coda ALTER COLUMN id SET DEFAULT nextval('extraschool_coda_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copiercode ALTER COLUMN id SET DEFAULT nextval('extraschool_copiercode_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copierquota ALTER COLUMN id SET DEFAULT nextval('extraschool_copierquota_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount ALTER COLUMN id SET DEFAULT nextval('extraschool_discount_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discountrule ALTER COLUMN id SET DEFAULT nextval('extraschool_discountrule_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_file_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_file_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardian ALTER COLUMN id SET DEFAULT nextval('extraschool_guardian_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes ALTER COLUMN id SET DEFAULT nextval('extraschool_guardianprestationtimes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_guardianprestationtimes_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importchildtyperule ALTER COLUMN id SET DEFAULT nextval('extraschool_importchildtyperule_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importlevelrule ALTER COLUMN id SET DEFAULT nextval('extraschool_importlevelrule_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importreject ALTER COLUMN id SET DEFAULT nextval('extraschool_importreject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_initupdate_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_initupdate_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice ALTER COLUMN id SET DEFAULT nextval('extraschool_invoice_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_invoice_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations ALTER COLUMN id SET DEFAULT nextval('extraschool_invoicedprestations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_level ALTER COLUMN id SET DEFAULT nextval('extraschool_level_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_mainsettings ALTER COLUMN id SET DEFAULT nextval('extraschool_mainsettings_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_parent ALTER COLUMN id SET DEFAULT nextval('extraschool_parent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_payment ALTER COLUMN id SET DEFAULT nextval('extraschool_payment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes ALTER COLUMN id SET DEFAULT nextval('extraschool_pdaprestationtimes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place ALTER COLUMN id SET DEFAULT nextval('extraschool_place_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_prestations_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_prestationscheck_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes ALTER COLUMN id SET DEFAULT nextval('extraschool_prestationtimes_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_qrcodes_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_qrcodes_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_quotaadjustment ALTER COLUMN id SET DEFAULT nextval('extraschool_quotaadjustment_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reject ALTER COLUMN id SET DEFAULT nextval('extraschool_reject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder ALTER COLUMN id SET DEFAULT nextval('extraschool_reminder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminders_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_reminders_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal ALTER COLUMN id SET DEFAULT nextval('extraschool_remindersjournal_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindertype ALTER COLUMN id SET DEFAULT nextval('extraschool_remindertype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_scheduledtasks ALTER COLUMN id SET DEFAULT nextval('extraschool_scheduledtasks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_school ALTER COLUMN id SET DEFAULT nextval('extraschool_school_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_schoolimplantation ALTER COLUMN id SET DEFAULT nextval('extraschool_schoolimplantation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone ALTER COLUMN id SET DEFAULT nextval('extraschool_smartphone_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_statsone_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_statsone_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_taxcertificates_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_teacher ALTER COLUMN id SET DEFAULT nextval('extraschool_teacher_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_timecorrection_wizard_id_seq'::regclass);


--
-- Name: extraschool_activity_activit_activity_id_activityexclusion_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_activityexclusiondates_rel
    ADD CONSTRAINT extraschool_activity_activit_activity_id_activityexclusion_key UNIQUE (activity_id, activityexclusiondates_id);


--
-- Name: extraschool_activity_activit_activityplanneddate_id_activi_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_activityplanneddate_rel
    ADD CONSTRAINT extraschool_activity_activit_activityplanneddate_id_activi_key UNIQUE (activityplanneddate_id, activity_id);


--
-- Name: extraschool_activity_child_rel_activity_id_child_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_child_rel
    ADD CONSTRAINT extraschool_activity_child_rel_activity_id_child_id_key UNIQUE (activity_id, child_id);


--
-- Name: extraschool_activity_childpos_activity_id_childposition_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_childposition_rel
    ADD CONSTRAINT extraschool_activity_childpos_activity_id_childposition_id_key UNIQUE (activity_id, childposition_id);


--
-- Name: extraschool_activity_childtype_re_activity_id_childtype_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_childtype_rel
    ADD CONSTRAINT extraschool_activity_childtype_re_activity_id_childtype_id_key UNIQUE (activity_id, childtype_id);


--
-- Name: extraschool_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_pkey PRIMARY KEY (id);


--
-- Name: extraschool_activity_place_rel_activity_id_place_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_place_rel
    ADD CONSTRAINT extraschool_activity_place_rel_activity_id_place_id_key UNIQUE (activity_id, place_id);


--
-- Name: extraschool_activity_schooli_activity_id_schoolimplantatio_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activity_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activity_schooli_activity_id_schoolimplantatio_key UNIQUE (activity_id, schoolimplantation_id);


--
-- Name: extraschool_activitycategory__activitycategory_id_place_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activitycategory_place_rel
    ADD CONSTRAINT extraschool_activitycategory__activitycategory_id_place_id_key UNIQUE (activitycategory_id, place_id);


--
-- Name: extraschool_activitycategory_activitycategory_id_schoolimp_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activitycategory_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activitycategory_activitycategory_id_schoolimp_key UNIQUE (activitycategory_id, schoolimplantation_id);


--
-- Name: extraschool_activitycategory_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activitycategory
    ADD CONSTRAINT extraschool_activitycategory_pkey PRIMARY KEY (id);


--
-- Name: extraschool_activitychildregistration_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activitychildregistration
    ADD CONSTRAINT extraschool_activitychildregistration_pkey PRIMARY KEY (id);


--
-- Name: extraschool_activityexclusiondates_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activityexclusiondates
    ADD CONSTRAINT extraschool_activityexclusiondates_pkey PRIMARY KEY (id);


--
-- Name: extraschool_activityplanneddate_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_activityplanneddate
    ADD CONSTRAINT extraschool_activityplanneddate_pkey PRIMARY KEY (id);


--
-- Name: extraschool_biller_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_biller
    ADD CONSTRAINT extraschool_biller_pkey PRIMARY KEY (id);


--
-- Name: extraschool_child_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_pkey PRIMARY KEY (id);


--
-- Name: extraschool_childposition_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childposition
    ADD CONSTRAINT extraschool_childposition_pkey PRIMARY KEY (id);


--
-- Name: extraschool_childsimport_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childsimport
    ADD CONSTRAINT extraschool_childsimport_pkey PRIMARY KEY (id);


--
-- Name: extraschool_childsimportfilt_childsimportfilter_id_importc_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childsimportfilter_importchildtyperule_rel
    ADD CONSTRAINT extraschool_childsimportfilt_childsimportfilter_id_importc_key UNIQUE (childsimportfilter_id, importchildtyperule_id);


--
-- Name: extraschool_childsimportfilt_childsimportfilter_id_importl_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childsimportfilter_importlevelrule_rel
    ADD CONSTRAINT extraschool_childsimportfilt_childsimportfilter_id_importl_key UNIQUE (childsimportfilter_id, importlevelrule_id);


--
-- Name: extraschool_childsimportfilter_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childsimportfilter
    ADD CONSTRAINT extraschool_childsimportfilter_pkey PRIMARY KEY (id);


--
-- Name: extraschool_childsworkbook_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_childtype_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_childtype
    ADD CONSTRAINT extraschool_childtype_pkey PRIMARY KEY (id);


--
-- Name: extraschool_class_level_rel_class_id_level_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_class_level_rel
    ADD CONSTRAINT extraschool_class_level_rel_class_id_level_id_key UNIQUE (class_id, level_id);


--
-- Name: extraschool_class_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_class
    ADD CONSTRAINT extraschool_class_pkey PRIMARY KEY (id);


--
-- Name: extraschool_coda_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_coda
    ADD CONSTRAINT extraschool_coda_pkey PRIMARY KEY (id);


--
-- Name: extraschool_copiercode_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_copiercode
    ADD CONSTRAINT extraschool_copiercode_pkey PRIMARY KEY (id);


--
-- Name: extraschool_copierquota_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_copierquota
    ADD CONSTRAINT extraschool_copierquota_pkey PRIMARY KEY (id);


--
-- Name: extraschool_discount_activity_rel_discount_id_activity_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_discount_activity_rel
    ADD CONSTRAINT extraschool_discount_activity_rel_discount_id_activity_id_key UNIQUE (discount_id, activity_id);


--
-- Name: extraschool_discount_childtype_re_discount_id_childtype_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_discount_childtype_rel
    ADD CONSTRAINT extraschool_discount_childtype_re_discount_id_childtype_id_key UNIQUE (discount_id, childtype_id);


--
-- Name: extraschool_discount_discountr_discount_id_discountrule_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_discount_discountrule_rel
    ADD CONSTRAINT extraschool_discount_discountr_discount_id_discountrule_id_key UNIQUE (discount_id, discountrule_id);


--
-- Name: extraschool_discount_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_discount
    ADD CONSTRAINT extraschool_discount_pkey PRIMARY KEY (id);


--
-- Name: extraschool_discountrule_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_discountrule
    ADD CONSTRAINT extraschool_discountrule_pkey PRIMARY KEY (id);


--
-- Name: extraschool_file_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_file_wizard
    ADD CONSTRAINT extraschool_file_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_guardian_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_guardian
    ADD CONSTRAINT extraschool_guardian_pkey PRIMARY KEY (id);


--
-- Name: extraschool_guardianprestationtimes_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_guardianprestationtimes
    ADD CONSTRAINT extraschool_guardianprestationtimes_pkey PRIMARY KEY (id);


--
-- Name: extraschool_guardianprestationtimes_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_guardianprestationtimes_wizard
    ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_importchildtyperule_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_importchildtyperule
    ADD CONSTRAINT extraschool_importchildtyperule_pkey PRIMARY KEY (id);


--
-- Name: extraschool_importlevelrule_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_importlevelrule
    ADD CONSTRAINT extraschool_importlevelrule_pkey PRIMARY KEY (id);


--
-- Name: extraschool_importreject_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_importreject
    ADD CONSTRAINT extraschool_importreject_pkey PRIMARY KEY (id);


--
-- Name: extraschool_initupdate_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_initupdate_wizard
    ADD CONSTRAINT extraschool_initupdate_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_invoice
    ADD CONSTRAINT extraschool_invoice_pkey PRIMARY KEY (id);


--
-- Name: extraschool_invoice_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_invoice_wizard
    ADD CONSTRAINT extraschool_invoice_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_invoicedprestations_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_pkey PRIMARY KEY (id);


--
-- Name: extraschool_level_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_level
    ADD CONSTRAINT extraschool_level_pkey PRIMARY KEY (id);


--
-- Name: extraschool_mainsettings_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_mainsettings
    ADD CONSTRAINT extraschool_mainsettings_pkey PRIMARY KEY (id);


--
-- Name: extraschool_parent_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_parent
    ADD CONSTRAINT extraschool_parent_pkey PRIMARY KEY (id);


--
-- Name: extraschool_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_payment
    ADD CONSTRAINT extraschool_payment_pkey PRIMARY KEY (id);


--
-- Name: extraschool_pdaprestationtimes_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtimes_pkey PRIMARY KEY (id);


--
-- Name: extraschool_place_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_place
    ADD CONSTRAINT extraschool_place_pkey PRIMARY KEY (id);


--
-- Name: extraschool_place_schoolimpl_place_id_schoolimplantation_i_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_place_schoolimplantation_rel
    ADD CONSTRAINT extraschool_place_schoolimpl_place_id_schoolimplantation_i_key UNIQUE (place_id, schoolimplantation_id);


--
-- Name: extraschool_prestations_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_prestationscheck_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_prestationtimes_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_pkey PRIMARY KEY (id);


--
-- Name: extraschool_qrcodes_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_qrcodes_wizard
    ADD CONSTRAINT extraschool_qrcodes_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_quotaadjustment_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_quotaadjustment
    ADD CONSTRAINT extraschool_quotaadjustment_pkey PRIMARY KEY (id);


--
-- Name: extraschool_reject_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_reject
    ADD CONSTRAINT extraschool_reject_pkey PRIMARY KEY (id);


--
-- Name: extraschool_reminder_invoice_rel_reminder_id_invoice_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_reminder_invoice_rel
    ADD CONSTRAINT extraschool_reminder_invoice_rel_reminder_id_invoice_id_key UNIQUE (reminder_id, invoice_id);


--
-- Name: extraschool_reminder_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_reminder
    ADD CONSTRAINT extraschool_reminder_pkey PRIMARY KEY (id);


--
-- Name: extraschool_reminders_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_reminders_wizard
    ADD CONSTRAINT extraschool_reminders_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_remindersjournal_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_pkey PRIMARY KEY (id);


--
-- Name: extraschool_remindersjournal_remindersjournal_id_biller_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_remindersjournal_biller_rel
    ADD CONSTRAINT extraschool_remindersjournal_remindersjournal_id_biller_id_key UNIQUE (remindersjournal_id, biller_id);


--
-- Name: extraschool_remindertype_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_remindertype
    ADD CONSTRAINT extraschool_remindertype_pkey PRIMARY KEY (id);


--
-- Name: extraschool_scheduledtasks_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_scheduledtasks
    ADD CONSTRAINT extraschool_scheduledtasks_pkey PRIMARY KEY (id);


--
-- Name: extraschool_school_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_school
    ADD CONSTRAINT extraschool_school_pkey PRIMARY KEY (id);


--
-- Name: extraschool_schoolimplantation_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_schoolimplantation
    ADD CONSTRAINT extraschool_schoolimplantation_pkey PRIMARY KEY (id);


--
-- Name: extraschool_smartphone_activ_smartphone_id_activitycategor_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_smartphone_activitycategory_rel
    ADD CONSTRAINT extraschool_smartphone_activ_smartphone_id_activitycategor_key UNIQUE (smartphone_id, activitycategory_id);


--
-- Name: extraschool_smartphone_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_smartphone
    ADD CONSTRAINT extraschool_smartphone_pkey PRIMARY KEY (id);


--
-- Name: extraschool_smartphone_schoo_smartphone_id_schoolimplantat_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_smartphone_schoolimplantation_rel
    ADD CONSTRAINT extraschool_smartphone_schoo_smartphone_id_schoolimplantat_key UNIQUE (smartphone_id, schoolimplantation_id);


--
-- Name: extraschool_statsone_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_statsone_wizard
    ADD CONSTRAINT extraschool_statsone_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_taxcertificates_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_teacher
    ADD CONSTRAINT extraschool_teacher_pkey PRIMARY KEY (id);


--
-- Name: extraschool_timecorrection_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace: 
--

ALTER TABLE ONLY extraschool_timecorrection_wizard
    ADD CONSTRAINT extraschool_timecorrection_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_activity_activityexclusiondates_rel_activity_id_in; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_activityexclusiondates_rel_activity_id_in ON extraschool_activity_activityexclusiondates_rel USING btree (activity_id);


--
-- Name: extraschool_activity_activityexclusiondates_rel_activityexclus; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_activityexclusiondates_rel_activityexclus ON extraschool_activity_activityexclusiondates_rel USING btree (activityexclusiondates_id);


--
-- Name: extraschool_activity_activityplanneddate_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_activityplanneddate_rel_activity_id_index ON extraschool_activity_activityplanneddate_rel USING btree (activity_id);


--
-- Name: extraschool_activity_activityplanneddate_rel_activityplannedda; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_activityplanneddate_rel_activityplannedda ON extraschool_activity_activityplanneddate_rel USING btree (activityplanneddate_id);


--
-- Name: extraschool_activity_child_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_child_rel_activity_id_index ON extraschool_activity_child_rel USING btree (activity_id);


--
-- Name: extraschool_activity_child_rel_child_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_child_rel_child_id_index ON extraschool_activity_child_rel USING btree (child_id);


--
-- Name: extraschool_activity_childposition_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_childposition_rel_activity_id_index ON extraschool_activity_childposition_rel USING btree (activity_id);


--
-- Name: extraschool_activity_childposition_rel_childposition_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_childposition_rel_childposition_id_index ON extraschool_activity_childposition_rel USING btree (childposition_id);


--
-- Name: extraschool_activity_childtype_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_childtype_rel_activity_id_index ON extraschool_activity_childtype_rel USING btree (activity_id);


--
-- Name: extraschool_activity_childtype_rel_childtype_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_childtype_rel_childtype_id_index ON extraschool_activity_childtype_rel USING btree (childtype_id);


--
-- Name: extraschool_activity_place_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_place_rel_activity_id_index ON extraschool_activity_place_rel USING btree (activity_id);


--
-- Name: extraschool_activity_place_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_place_rel_place_id_index ON extraschool_activity_place_rel USING btree (place_id);


--
-- Name: extraschool_activity_schoolimplantation_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_schoolimplantation_rel_activity_id_index ON extraschool_activity_schoolimplantation_rel USING btree (activity_id);


--
-- Name: extraschool_activity_schoolimplantation_rel_schoolimplantation; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activity_schoolimplantation_rel_schoolimplantation ON extraschool_activity_schoolimplantation_rel USING btree (schoolimplantation_id);


--
-- Name: extraschool_activitycategory_place_rel_activitycategory_id_ind; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activitycategory_place_rel_activitycategory_id_ind ON extraschool_activitycategory_place_rel USING btree (activitycategory_id);


--
-- Name: extraschool_activitycategory_place_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activitycategory_place_rel_place_id_index ON extraschool_activitycategory_place_rel USING btree (place_id);


--
-- Name: extraschool_activitycategory_schoolimplantation_rel_activityca; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activitycategory_schoolimplantation_rel_activityca ON extraschool_activitycategory_schoolimplantation_rel USING btree (activitycategory_id);


--
-- Name: extraschool_activitycategory_schoolimplantation_rel_schoolimpl; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_activitycategory_schoolimplantation_rel_schoolimpl ON extraschool_activitycategory_schoolimplantation_rel USING btree (schoolimplantation_id);


--
-- Name: extraschool_childsimportfilter_importchildtyperule_rel_childsi; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_childsimportfilter_importchildtyperule_rel_childsi ON extraschool_childsimportfilter_importchildtyperule_rel USING btree (childsimportfilter_id);


--
-- Name: extraschool_childsimportfilter_importchildtyperule_rel_importc; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_childsimportfilter_importchildtyperule_rel_importc ON extraschool_childsimportfilter_importchildtyperule_rel USING btree (importchildtyperule_id);


--
-- Name: extraschool_childsimportfilter_importlevelrule_rel_childsimpor; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_childsimportfilter_importlevelrule_rel_childsimpor ON extraschool_childsimportfilter_importlevelrule_rel USING btree (childsimportfilter_id);


--
-- Name: extraschool_childsimportfilter_importlevelrule_rel_importlevel; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_childsimportfilter_importlevelrule_rel_importlevel ON extraschool_childsimportfilter_importlevelrule_rel USING btree (importlevelrule_id);


--
-- Name: extraschool_class_level_rel_class_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_class_level_rel_class_id_index ON extraschool_class_level_rel USING btree (class_id);


--
-- Name: extraschool_class_level_rel_level_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_class_level_rel_level_id_index ON extraschool_class_level_rel USING btree (level_id);


--
-- Name: extraschool_discount_activity_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_discount_activity_rel_activity_id_index ON extraschool_discount_activity_rel USING btree (activity_id);


--
-- Name: extraschool_discount_activity_rel_discount_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_discount_activity_rel_discount_id_index ON extraschool_discount_activity_rel USING btree (discount_id);


--
-- Name: extraschool_discount_childtype_rel_childtype_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_discount_childtype_rel_childtype_id_index ON extraschool_discount_childtype_rel USING btree (childtype_id);


--
-- Name: extraschool_discount_childtype_rel_discount_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_discount_childtype_rel_discount_id_index ON extraschool_discount_childtype_rel USING btree (discount_id);


--
-- Name: extraschool_discount_discountrule_rel_discount_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_discount_discountrule_rel_discount_id_index ON extraschool_discount_discountrule_rel USING btree (discount_id);


--
-- Name: extraschool_discount_discountrule_rel_discountrule_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_discount_discountrule_rel_discountrule_id_index ON extraschool_discount_discountrule_rel USING btree (discountrule_id);


--
-- Name: extraschool_invoicedprestations_activityid_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_invoicedprestations_activityid_index ON extraschool_invoicedprestations USING btree (activityid);


--
-- Name: extraschool_invoicedprestations_childid_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_invoicedprestations_childid_index ON extraschool_invoicedprestations USING btree (childid);


--
-- Name: extraschool_invoicedprestations_placeid_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_invoicedprestations_placeid_index ON extraschool_invoicedprestations USING btree (placeid);


--
-- Name: extraschool_invoicedprestations_prestation_date_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_invoicedprestations_prestation_date_index ON extraschool_invoicedprestations USING btree (prestation_date);


--
-- Name: extraschool_invoicedprestations_quantity_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_invoicedprestations_quantity_index ON extraschool_invoicedprestations USING btree (quantity);


--
-- Name: extraschool_place_schoolimplantation_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_place_schoolimplantation_rel_place_id_index ON extraschool_place_schoolimplantation_rel USING btree (place_id);


--
-- Name: extraschool_place_schoolimplantation_rel_schoolimplantation_id; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_place_schoolimplantation_rel_schoolimplantation_id ON extraschool_place_schoolimplantation_rel USING btree (schoolimplantation_id);


--
-- Name: extraschool_prestationtimes_ES_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX "extraschool_prestationtimes_ES_index" ON extraschool_prestationtimes USING btree ("ES");


--
-- Name: extraschool_prestationtimes_childid_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_prestationtimes_childid_index ON extraschool_prestationtimes USING btree (childid);


--
-- Name: extraschool_prestationtimes_prestation_date_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_prestationtimes_prestation_date_index ON extraschool_prestationtimes USING btree (prestation_date);


--
-- Name: extraschool_prestationtimes_prestation_time_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_prestationtimes_prestation_time_index ON extraschool_prestationtimes USING btree (prestation_time);


--
-- Name: extraschool_reminder_invoice_rel_invoice_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_reminder_invoice_rel_invoice_id_index ON extraschool_reminder_invoice_rel USING btree (invoice_id);


--
-- Name: extraschool_reminder_invoice_rel_reminder_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_reminder_invoice_rel_reminder_id_index ON extraschool_reminder_invoice_rel USING btree (reminder_id);


--
-- Name: extraschool_remindersjournal_biller_rel_biller_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_remindersjournal_biller_rel_biller_id_index ON extraschool_remindersjournal_biller_rel USING btree (biller_id);


--
-- Name: extraschool_remindersjournal_biller_rel_remindersjournal_id_in; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_remindersjournal_biller_rel_remindersjournal_id_in ON extraschool_remindersjournal_biller_rel USING btree (remindersjournal_id);


--
-- Name: extraschool_smartphone_activitycategory_rel_activitycategory_i; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_smartphone_activitycategory_rel_activitycategory_i ON extraschool_smartphone_activitycategory_rel USING btree (activitycategory_id);


--
-- Name: extraschool_smartphone_activitycategory_rel_smartphone_id_inde; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_smartphone_activitycategory_rel_smartphone_id_inde ON extraschool_smartphone_activitycategory_rel USING btree (smartphone_id);


--
-- Name: extraschool_smartphone_schoolimplantation_rel_schoolimplantati; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_smartphone_schoolimplantation_rel_schoolimplantati ON extraschool_smartphone_schoolimplantation_rel USING btree (schoolimplantation_id);


--
-- Name: extraschool_smartphone_schoolimplantation_rel_smartphone_id_in; Type: INDEX; Schema: public; Owner: openerp; Tablespace: 
--

CREATE INDEX extraschool_smartphone_schoolimplantation_rel_smartphone_id_in ON extraschool_smartphone_schoolimplantation_rel USING btree (smartphone_id);


--
-- Name: extraschool_activity_activityex_activityexclusiondates_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityexclusiondates_rel
    ADD CONSTRAINT extraschool_activity_activityex_activityexclusiondates_id_fkey FOREIGN KEY (activityexclusiondates_id) REFERENCES extraschool_activityexclusiondates(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_activityexclusiondates_r_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityexclusiondates_rel
    ADD CONSTRAINT extraschool_activity_activityexclusiondates_r_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_activityplann_activityplanneddate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityplanneddate_rel
    ADD CONSTRAINT extraschool_activity_activityplann_activityplanneddate_id_fkey FOREIGN KEY (activityplanneddate_id) REFERENCES extraschool_activityplanneddate(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_activityplanneddate_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityplanneddate_rel
    ADD CONSTRAINT extraschool_activity_activityplanneddate_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_category_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_category_fkey FOREIGN KEY (category) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_activity_child_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_child_rel
    ADD CONSTRAINT extraschool_activity_child_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_child_rel_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_child_rel
    ADD CONSTRAINT extraschool_activity_child_rel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_childposition_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_childposition_rel
    ADD CONSTRAINT extraschool_activity_childposition_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_childposition_rel_childposition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_childposition_rel
    ADD CONSTRAINT extraschool_activity_childposition_rel_childposition_id_fkey FOREIGN KEY (childposition_id) REFERENCES extraschool_childposition(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_childtype_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_childtype_rel
    ADD CONSTRAINT extraschool_activity_childtype_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_childtype_rel_childtype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_childtype_rel
    ADD CONSTRAINT extraschool_activity_childtype_rel_childtype_id_fkey FOREIGN KEY (childtype_id) REFERENCES extraschool_childtype(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activity_place_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_place_rel
    ADD CONSTRAINT extraschool_activity_place_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_place_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_place_rel
    ADD CONSTRAINT extraschool_activity_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_schoolimplanta_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activity_schoolimplanta_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_schoolimplantation_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activity_schoolimplantation_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activitycategory_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory
    ADD CONSTRAINT extraschool_activitycategory_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activitycategory_place_re_activitycategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory_place_rel
    ADD CONSTRAINT extraschool_activitycategory_place_re_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_activitycategory_place_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory_place_rel
    ADD CONSTRAINT extraschool_activitycategory_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_activitycategory_school_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activitycategory_school_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_activitycategory_schoolim_activitycategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activitycategory_schoolim_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_activitycategory_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory
    ADD CONSTRAINT extraschool_activitycategory_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activitychildregistration_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitychildregistration
    ADD CONSTRAINT extraschool_activitychildregistration_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;


--
-- Name: extraschool_activitychildregistration_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitychildregistration
    ADD CONSTRAINT extraschool_activitychildregistration_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_activitychildregistration_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitychildregistration
    ADD CONSTRAINT extraschool_activitychildregistration_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activitychildregistration_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitychildregistration
    ADD CONSTRAINT extraschool_activitychildregistration_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityexclusiondates_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityexclusiondates
    ADD CONSTRAINT extraschool_activityexclusiondates_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityexclusiondates_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityexclusiondates
    ADD CONSTRAINT extraschool_activityexclusiondates_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityplanneddate_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityplanneddate
    ADD CONSTRAINT extraschool_activityplanneddate_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityplanneddate_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityplanneddate
    ADD CONSTRAINT extraschool_activityplanneddate_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_biller_activitycategoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_biller
    ADD CONSTRAINT extraschool_biller_activitycategoryid_fkey FOREIGN KEY (activitycategoryid) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_biller_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_biller
    ADD CONSTRAINT extraschool_biller_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_biller_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_biller
    ADD CONSTRAINT extraschool_biller_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_childtypeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_childtypeid_fkey FOREIGN KEY (childtypeid) REFERENCES extraschool_childtype(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_classid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_classid_fkey FOREIGN KEY (classid) REFERENCES extraschool_class(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_levelid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_levelid_fkey FOREIGN KEY (levelid) REFERENCES extraschool_level(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_parentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_schoolimplantation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_schoolimplantation_fkey FOREIGN KEY (schoolimplantation) REFERENCES extraschool_schoolimplantation(id) ON DELETE SET NULL;


--
-- Name: extraschool_child_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_child
    ADD CONSTRAINT extraschool_child_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childposition_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childposition
    ADD CONSTRAINT extraschool_childposition_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childposition_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childposition
    ADD CONSTRAINT extraschool_childposition_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsimport_childsimportfilter_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimport
    ADD CONSTRAINT extraschool_childsimport_childsimportfilter_fkey FOREIGN KEY (childsimportfilter) REFERENCES extraschool_childsimportfilter(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsimport_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimport
    ADD CONSTRAINT extraschool_childsimport_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsimport_schoolimplantation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimport
    ADD CONSTRAINT extraschool_childsimport_schoolimplantation_fkey FOREIGN KEY (schoolimplantation) REFERENCES extraschool_schoolimplantation(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsimport_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimport
    ADD CONSTRAINT extraschool_childsimport_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsimportfilter_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter
    ADD CONSTRAINT extraschool_childsimportfilter_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsimportfilter_imp_childsimportfilter_id_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter_importchildtyperule_rel
    ADD CONSTRAINT extraschool_childsimportfilter_imp_childsimportfilter_id_fkey1 FOREIGN KEY (childsimportfilter_id) REFERENCES extraschool_childsimportfilter(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsimportfilter_imp_importchildtyperule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter_importchildtyperule_rel
    ADD CONSTRAINT extraschool_childsimportfilter_imp_importchildtyperule_id_fkey FOREIGN KEY (importchildtyperule_id) REFERENCES extraschool_importchildtyperule(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsimportfilter_impo_childsimportfilter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter_importlevelrule_rel
    ADD CONSTRAINT extraschool_childsimportfilter_impo_childsimportfilter_id_fkey FOREIGN KEY (childsimportfilter_id) REFERENCES extraschool_childsimportfilter(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsimportfilter_importl_importlevelrule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter_importlevelrule_rel
    ADD CONSTRAINT extraschool_childsimportfilter_importl_importlevelrule_id_fkey FOREIGN KEY (importlevelrule_id) REFERENCES extraschool_importlevelrule(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsimportfilter_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter
    ADD CONSTRAINT extraschool_childsimportfilter_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsworkbook_wizard_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsworkbook_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsworkbook_wizard_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsworkbook_wizard_schoolimplantation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_schoolimplantation_fkey FOREIGN KEY (schoolimplantation) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsworkbook_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childtype_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childtype
    ADD CONSTRAINT extraschool_childtype_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childtype_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childtype
    ADD CONSTRAINT extraschool_childtype_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_class_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class
    ADD CONSTRAINT extraschool_class_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_class_level_rel_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class_level_rel
    ADD CONSTRAINT extraschool_class_level_rel_class_id_fkey FOREIGN KEY (class_id) REFERENCES extraschool_class(id) ON DELETE CASCADE;


--
-- Name: extraschool_class_level_rel_level_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class_level_rel
    ADD CONSTRAINT extraschool_class_level_rel_level_id_fkey FOREIGN KEY (level_id) REFERENCES extraschool_level(id) ON DELETE CASCADE;


--
-- Name: extraschool_class_schoolimplantation_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class
    ADD CONSTRAINT extraschool_class_schoolimplantation_fkey FOREIGN KEY (schoolimplantation) REFERENCES extraschool_schoolimplantation(id) ON DELETE SET NULL;


--
-- Name: extraschool_class_titular_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class
    ADD CONSTRAINT extraschool_class_titular_fkey FOREIGN KEY (titular) REFERENCES extraschool_teacher(id) ON DELETE SET NULL;


--
-- Name: extraschool_class_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_class
    ADD CONSTRAINT extraschool_class_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_coda_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_coda
    ADD CONSTRAINT extraschool_coda_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_coda_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_coda
    ADD CONSTRAINT extraschool_coda_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_copiercode_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copiercode
    ADD CONSTRAINT extraschool_copiercode_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_copiercode_teacherid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copiercode
    ADD CONSTRAINT extraschool_copiercode_teacherid_fkey FOREIGN KEY (teacherid) REFERENCES extraschool_teacher(id) ON DELETE CASCADE;


--
-- Name: extraschool_copiercode_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copiercode
    ADD CONSTRAINT extraschool_copiercode_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_copierquota_copiercodeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copierquota
    ADD CONSTRAINT extraschool_copierquota_copiercodeid_fkey FOREIGN KEY (copiercodeid) REFERENCES extraschool_copiercode(id) ON DELETE CASCADE;


--
-- Name: extraschool_copierquota_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copierquota
    ADD CONSTRAINT extraschool_copierquota_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_copierquota_schoolimplantationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copierquota
    ADD CONSTRAINT extraschool_copierquota_schoolimplantationid_fkey FOREIGN KEY (schoolimplantationid) REFERENCES extraschool_schoolimplantation(id) ON DELETE SET NULL;


--
-- Name: extraschool_copierquota_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_copierquota
    ADD CONSTRAINT extraschool_copierquota_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_discount_activity_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount_activity_rel
    ADD CONSTRAINT extraschool_discount_activity_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_discount_activity_rel_discount_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount_activity_rel
    ADD CONSTRAINT extraschool_discount_activity_rel_discount_id_fkey FOREIGN KEY (discount_id) REFERENCES extraschool_discount(id) ON DELETE CASCADE;


--
-- Name: extraschool_discount_childtype_rel_childtype_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount_childtype_rel
    ADD CONSTRAINT extraschool_discount_childtype_rel_childtype_id_fkey FOREIGN KEY (childtype_id) REFERENCES extraschool_childtype(id) ON DELETE CASCADE;


--
-- Name: extraschool_discount_childtype_rel_discount_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount_childtype_rel
    ADD CONSTRAINT extraschool_discount_childtype_rel_discount_id_fkey FOREIGN KEY (discount_id) REFERENCES extraschool_discount(id) ON DELETE CASCADE;


--
-- Name: extraschool_discount_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount
    ADD CONSTRAINT extraschool_discount_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_discount_discountrule_rel_discount_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount_discountrule_rel
    ADD CONSTRAINT extraschool_discount_discountrule_rel_discount_id_fkey FOREIGN KEY (discount_id) REFERENCES extraschool_discount(id) ON DELETE CASCADE;


--
-- Name: extraschool_discount_discountrule_rel_discountrule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount_discountrule_rel
    ADD CONSTRAINT extraschool_discount_discountrule_rel_discountrule_id_fkey FOREIGN KEY (discountrule_id) REFERENCES extraschool_discountrule(id) ON DELETE CASCADE;


--
-- Name: extraschool_discount_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discount
    ADD CONSTRAINT extraschool_discount_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_discountrule_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discountrule
    ADD CONSTRAINT extraschool_discountrule_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_discountrule_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discountrule
    ADD CONSTRAINT extraschool_discountrule_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_file_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_file_wizard
    ADD CONSTRAINT extraschool_file_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_file_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_file_wizard
    ADD CONSTRAINT extraschool_file_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardian_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardian
    ADD CONSTRAINT extraschool_guardian_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardian_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardian
    ADD CONSTRAINT extraschool_guardian_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardianprestationtimes_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes
    ADD CONSTRAINT extraschool_guardianprestationtimes_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardianprestationtimes_guardianid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes
    ADD CONSTRAINT extraschool_guardianprestationtimes_guardianid_fkey FOREIGN KEY (guardianid) REFERENCES extraschool_guardian(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardianprestationtimes_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes_wizard
    ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardianprestationtimes_wizard_guardianid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes_wizard
    ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_guardianid_fkey FOREIGN KEY (guardianid) REFERENCES extraschool_guardian(id) ON DELETE CASCADE;


--
-- Name: extraschool_guardianprestationtimes_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes_wizard
    ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_guardianprestationtimes_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_guardianprestationtimes
    ADD CONSTRAINT extraschool_guardianprestationtimes_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_importchildtyperule_childtypeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importchildtyperule
    ADD CONSTRAINT extraschool_importchildtyperule_childtypeid_fkey FOREIGN KEY (childtypeid) REFERENCES extraschool_childtype(id) ON DELETE SET NULL;


--
-- Name: extraschool_importchildtyperule_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importchildtyperule
    ADD CONSTRAINT extraschool_importchildtyperule_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_importchildtyperule_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importchildtyperule
    ADD CONSTRAINT extraschool_importchildtyperule_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_importlevelrule_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importlevelrule
    ADD CONSTRAINT extraschool_importlevelrule_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_importlevelrule_levelid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importlevelrule
    ADD CONSTRAINT extraschool_importlevelrule_levelid_fkey FOREIGN KEY (levelid) REFERENCES extraschool_level(id) ON DELETE SET NULL;


--
-- Name: extraschool_importlevelrule_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importlevelrule
    ADD CONSTRAINT extraschool_importlevelrule_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_importreject_childsimport_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importreject
    ADD CONSTRAINT extraschool_importreject_childsimport_fkey FOREIGN KEY (childsimport) REFERENCES extraschool_childsimport(id) ON DELETE SET NULL;


--
-- Name: extraschool_importreject_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importreject
    ADD CONSTRAINT extraschool_importreject_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_importreject_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_importreject
    ADD CONSTRAINT extraschool_importreject_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_initupdate_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_initupdate_wizard
    ADD CONSTRAINT extraschool_initupdate_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_initupdate_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_initupdate_wizard
    ADD CONSTRAINT extraschool_initupdate_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_biller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice
    ADD CONSTRAINT extraschool_invoice_biller_id_fkey FOREIGN KEY (biller_id) REFERENCES extraschool_biller(id) ON DELETE CASCADE;


--
-- Name: extraschool_invoice_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice
    ADD CONSTRAINT extraschool_invoice_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_parentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice
    ADD CONSTRAINT extraschool_invoice_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_schoolimplantationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice
    ADD CONSTRAINT extraschool_invoice_schoolimplantationid_fkey FOREIGN KEY (schoolimplantationid) REFERENCES extraschool_schoolimplantation(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard
    ADD CONSTRAINT extraschool_invoice_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_invoice_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard
    ADD CONSTRAINT extraschool_invoice_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard
    ADD CONSTRAINT extraschool_invoice_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice
    ADD CONSTRAINT extraschool_invoice_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoicedprestations_activityid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_activityid_fkey FOREIGN KEY (activityid) REFERENCES extraschool_activity(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoicedprestations_childid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoicedprestations_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoicedprestations_invoiceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_invoiceid_fkey FOREIGN KEY (invoiceid) REFERENCES extraschool_invoice(id) ON DELETE CASCADE;


--
-- Name: extraschool_invoicedprestations_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoicedprestations_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoicedprestations
    ADD CONSTRAINT extraschool_invoicedprestations_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_level_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_level
    ADD CONSTRAINT extraschool_level_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_level_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_level
    ADD CONSTRAINT extraschool_level_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_mainsettings_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_mainsettings
    ADD CONSTRAINT extraschool_mainsettings_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_mainsettings_levelbeforedisable_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_mainsettings
    ADD CONSTRAINT extraschool_mainsettings_levelbeforedisable_fkey FOREIGN KEY (levelbeforedisable) REFERENCES extraschool_level(id) ON DELETE SET NULL;


--
-- Name: extraschool_mainsettings_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_mainsettings
    ADD CONSTRAINT extraschool_mainsettings_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_parent_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_parent
    ADD CONSTRAINT extraschool_parent_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_parent_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_parent
    ADD CONSTRAINT extraschool_parent_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_payment_coda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_payment
    ADD CONSTRAINT extraschool_payment_coda_fkey FOREIGN KEY (coda) REFERENCES extraschool_coda(id) ON DELETE SET NULL;


--
-- Name: extraschool_payment_concernedinvoice_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_payment
    ADD CONSTRAINT extraschool_payment_concernedinvoice_fkey FOREIGN KEY (concernedinvoice) REFERENCES extraschool_invoice(id) ON DELETE SET NULL;


--
-- Name: extraschool_payment_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_payment
    ADD CONSTRAINT extraschool_payment_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_payment_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_payment
    ADD CONSTRAINT extraschool_payment_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_pdaprestationtimes_activitycategoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtimes_activitycategoryid_fkey FOREIGN KEY (activitycategoryid) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_pdaprestationtimes_childid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtimes_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_pdaprestationtimes_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtimes_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_pdaprestationtimes_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtimes_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_pdaprestationtimes_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtimes_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_place_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place
    ADD CONSTRAINT extraschool_place_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_place_schoolimplantatio_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place_schoolimplantation_rel
    ADD CONSTRAINT extraschool_place_schoolimplantatio_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_place_schoolimplantation_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place_schoolimplantation_rel
    ADD CONSTRAINT extraschool_place_schoolimplantation_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_place_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place
    ADD CONSTRAINT extraschool_place_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestations_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestations_wizard_childid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestations_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestations_wizard_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestations_wizard_schoolimplantationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_schoolimplantationid_fkey FOREIGN KEY (schoolimplantationid) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestations_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestations_wizard
    ADD CONSTRAINT extraschool_prestations_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationscheck_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestationscheck_wizard_childid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestationscheck_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationscheck_wizard_schoolimplantationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_schoolimplantationid_fkey FOREIGN KEY (schoolimplantationid) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestationscheck_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_activitycategoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_activitycategoryid_fkey FOREIGN KEY (activitycategoryid) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_activityid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_activityid_fkey FOREIGN KEY (activityid) REFERENCES extraschool_activity(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_childid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_qrcodes_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_qrcodes_wizard
    ADD CONSTRAINT extraschool_qrcodes_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_qrcodes_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_qrcodes_wizard
    ADD CONSTRAINT extraschool_qrcodes_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_quotaadjustment_copierquotaid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_quotaadjustment
    ADD CONSTRAINT extraschool_quotaadjustment_copierquotaid_fkey FOREIGN KEY (copierquotaid) REFERENCES extraschool_copierquota(id) ON DELETE CASCADE;


--
-- Name: extraschool_quotaadjustment_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_quotaadjustment
    ADD CONSTRAINT extraschool_quotaadjustment_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_quotaadjustment_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_quotaadjustment
    ADD CONSTRAINT extraschool_quotaadjustment_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_reject_coda_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reject
    ADD CONSTRAINT extraschool_reject_coda_fkey FOREIGN KEY (coda) REFERENCES extraschool_coda(id) ON DELETE SET NULL;


--
-- Name: extraschool_reject_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reject
    ADD CONSTRAINT extraschool_reject_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_reject_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reject
    ADD CONSTRAINT extraschool_reject_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_reminder_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder
    ADD CONSTRAINT extraschool_reminder_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_reminder_invoice_rel_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder_invoice_rel
    ADD CONSTRAINT extraschool_reminder_invoice_rel_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES extraschool_invoice(id) ON DELETE CASCADE;


--
-- Name: extraschool_reminder_invoice_rel_reminder_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder_invoice_rel
    ADD CONSTRAINT extraschool_reminder_invoice_rel_reminder_id_fkey FOREIGN KEY (reminder_id) REFERENCES extraschool_reminder(id) ON DELETE CASCADE;


--
-- Name: extraschool_reminder_parentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder
    ADD CONSTRAINT extraschool_reminder_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE SET NULL;


--
-- Name: extraschool_reminder_remindersjournalid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder
    ADD CONSTRAINT extraschool_reminder_remindersjournalid_fkey FOREIGN KEY (remindersjournalid) REFERENCES extraschool_remindersjournal(id) ON DELETE CASCADE;


--
-- Name: extraschool_reminder_schoolimplantationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder
    ADD CONSTRAINT extraschool_reminder_schoolimplantationid_fkey FOREIGN KEY (schoolimplantationid) REFERENCES extraschool_schoolimplantation(id) ON DELETE SET NULL;


--
-- Name: extraschool_reminder_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminder
    ADD CONSTRAINT extraschool_reminder_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_reminders_wizard_activitycategoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminders_wizard
    ADD CONSTRAINT extraschool_reminders_wizard_activitycategoryid_fkey FOREIGN KEY (activitycategoryid) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_reminders_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminders_wizard
    ADD CONSTRAINT extraschool_reminders_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_reminders_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_reminders_wizard
    ADD CONSTRAINT extraschool_reminders_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindersjournal_activitycategoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_activitycategoryid_fkey FOREIGN KEY (activitycategoryid) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindersjournal_biller_r_remindersjournal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal_biller_rel
    ADD CONSTRAINT extraschool_remindersjournal_biller_r_remindersjournal_id_fkey FOREIGN KEY (remindersjournal_id) REFERENCES extraschool_remindersjournal(id) ON DELETE CASCADE;


--
-- Name: extraschool_remindersjournal_biller_rel_biller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal_biller_rel
    ADD CONSTRAINT extraschool_remindersjournal_biller_rel_biller_id_fkey FOREIGN KEY (biller_id) REFERENCES extraschool_biller(id) ON DELETE CASCADE;


--
-- Name: extraschool_remindersjournal_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindersjournal_remindertype_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_remindertype_fkey FOREIGN KEY (remindertype) REFERENCES extraschool_remindertype(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindersjournal_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindertype_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindertype
    ADD CONSTRAINT extraschool_remindertype_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindertype_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindertype
    ADD CONSTRAINT extraschool_remindertype_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_scheduledtasks_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_scheduledtasks
    ADD CONSTRAINT extraschool_scheduledtasks_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_scheduledtasks_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_scheduledtasks
    ADD CONSTRAINT extraschool_scheduledtasks_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_school_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_school
    ADD CONSTRAINT extraschool_school_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_school_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_school
    ADD CONSTRAINT extraschool_school_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_schoolimplantation_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_schoolimplantation
    ADD CONSTRAINT extraschool_schoolimplantation_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_schoolimplantation_schoolid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_schoolimplantation
    ADD CONSTRAINT extraschool_schoolimplantation_schoolid_fkey FOREIGN KEY (schoolid) REFERENCES extraschool_school(id) ON DELETE SET NULL;


--
-- Name: extraschool_schoolimplantation_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_schoolimplantation
    ADD CONSTRAINT extraschool_schoolimplantation_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_smartphone_activitycatego_activitycategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone_activitycategory_rel
    ADD CONSTRAINT extraschool_smartphone_activitycatego_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_smartphone_activitycategory_rel_smartphone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone_activitycategory_rel
    ADD CONSTRAINT extraschool_smartphone_activitycategory_rel_smartphone_id_fkey FOREIGN KEY (smartphone_id) REFERENCES extraschool_smartphone(id) ON DELETE CASCADE;


--
-- Name: extraschool_smartphone_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone
    ADD CONSTRAINT extraschool_smartphone_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_smartphone_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone
    ADD CONSTRAINT extraschool_smartphone_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_smartphone_schoolimplan_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone_schoolimplantation_rel
    ADD CONSTRAINT extraschool_smartphone_schoolimplan_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_smartphone_schoolimplantation_r_smartphone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone_schoolimplantation_rel
    ADD CONSTRAINT extraschool_smartphone_schoolimplantation_r_smartphone_id_fkey FOREIGN KEY (smartphone_id) REFERENCES extraschool_smartphone(id) ON DELETE CASCADE;


--
-- Name: extraschool_smartphone_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone
    ADD CONSTRAINT extraschool_smartphone_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_statsone_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_statsone_wizard
    ADD CONSTRAINT extraschool_statsone_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_statsone_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_statsone_wizard
    ADD CONSTRAINT extraschool_statsone_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_statsone_wizard_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_statsone_wizard
    ADD CONSTRAINT extraschool_statsone_wizard_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_statsone_wizard_schoolimplantationid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_statsone_wizard
    ADD CONSTRAINT extraschool_statsone_wizard_schoolimplantationid_fkey FOREIGN KEY (schoolimplantationid) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_statsone_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_statsone_wizard
    ADD CONSTRAINT extraschool_statsone_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_taxcertificates_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_taxcertificates_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_taxcertificates_wizard_parentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE CASCADE;


--
-- Name: extraschool_taxcertificates_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_teacher_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_teacher
    ADD CONSTRAINT extraschool_teacher_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_teacher_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_teacher
    ADD CONSTRAINT extraschool_teacher_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_timecorrection_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard
    ADD CONSTRAINT extraschool_timecorrection_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_timecorrection_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard
    ADD CONSTRAINT extraschool_timecorrection_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

