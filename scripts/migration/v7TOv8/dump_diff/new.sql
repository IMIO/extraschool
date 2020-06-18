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
    create_date timestamp without time zone,
    write_uid integer,
    category integer,
    create_uid integer,
    validity_to date,
    parent_id integer,
    subsidizedbyone boolean,
    period_duration integer,
    prest_from double precision,
    fixedperiod boolean,
    price_list_id integer,
    short_name character varying(20),
    root_id integer,
    default_from_to character varying,
    price numeric,
    leveltype character varying,
    validity_from date,
    write_date timestamp without time zone,
    default_from double precision,
    default_to double precision,
    name character varying(100) NOT NULL,
    autoaddchilds boolean,
    onlyregisteredchilds boolean,
    days character varying,
    prest_to double precision
);


ALTER TABLE public.extraschool_activity OWNER TO openerp;

--
-- Name: TABLE extraschool_activity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity IS 'activity';


--
-- Name: COLUMN extraschool_activity.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_activity.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_activity.category; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.category IS 'Category';


--
-- Name: COLUMN extraschool_activity.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_activity.validity_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.validity_to IS 'Validity to';


--
-- Name: COLUMN extraschool_activity.parent_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.parent_id IS 'Parent';


--
-- Name: COLUMN extraschool_activity.subsidizedbyone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.subsidizedbyone IS 'Subsidized by one';


--
-- Name: COLUMN extraschool_activity.period_duration; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.period_duration IS 'Period Duration';


--
-- Name: COLUMN extraschool_activity.prest_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.prest_from IS 'From';


--
-- Name: COLUMN extraschool_activity.fixedperiod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.fixedperiod IS 'Fixed period';


--
-- Name: COLUMN extraschool_activity.price_list_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.price_list_id IS 'Price List';


--
-- Name: COLUMN extraschool_activity.short_name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.short_name IS 'Short name';


--
-- Name: COLUMN extraschool_activity.root_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.root_id IS 'Root';


--
-- Name: COLUMN extraschool_activity.default_from_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.default_from_to IS 'Default From To';


--
-- Name: COLUMN extraschool_activity.price; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.price IS 'Price';


--
-- Name: COLUMN extraschool_activity.leveltype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.leveltype IS 'Level type';


--
-- Name: COLUMN extraschool_activity.validity_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.validity_from IS 'Validity from';


--
-- Name: COLUMN extraschool_activity.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_activity.default_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.default_from IS 'Default from';


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
-- Name: COLUMN extraschool_activity.onlyregisteredchilds; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.onlyregisteredchilds IS 'Only registered childs';


--
-- Name: COLUMN extraschool_activity.days; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.days IS 'Days';


--
-- Name: COLUMN extraschool_activity.prest_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activity.prest_to IS 'To';


--
-- Name: extraschool_activity_activityexclusiondates_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activity_activityexclusiondates_rel (
    activity_id integer NOT NULL,
    activityexclusiondates_id integer NOT NULL
);


ALTER TABLE public.extraschool_activity_activityexclusiondates_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_activityexclusiondates_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_activityexclusiondates_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_activityexclusiondates';


--
-- Name: extraschool_activity_activityplanneddate_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activity_activityplanneddate_rel (
    activity_id integer NOT NULL,
    activityplanneddate_id integer NOT NULL
);


ALTER TABLE public.extraschool_activity_activityplanneddate_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_activityplanneddate_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_activityplanneddate_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_activityplanneddate';


--
-- Name: extraschool_activity_childposition_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activity_childposition_rel (
    activity_id integer NOT NULL,
    childposition_id integer NOT NULL
);


ALTER TABLE public.extraschool_activity_childposition_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_childposition_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_childposition_rel IS 'RELATION BETWEEN extraschool_discount AND extraschool_childposition';


--
-- Name: extraschool_activity_childtype_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activity_childtype_rel (
    activity_id integer NOT NULL,
    childtype_id integer NOT NULL
);


ALTER TABLE public.extraschool_activity_childtype_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_activity_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_activity_place_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_activity_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activity_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activity_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_activity AND extraschool_schoolimplantation';


--
-- Name: extraschool_activitycategory; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activitycategory (
    id integer NOT NULL,
    reminderemailtext text,
    create_date timestamp without time zone,
    write_uid integer,
    invoicetemplate character varying(50),
    invoiceemailtext text,
    invoicecomstructprefix character varying(4),
    bankaccount character varying(4),
    create_uid integer,
    invoiceemailaddress character varying(50),
    invoiceemailsubject character varying(50),
    reminderlastcomstruct integer,
    priorityorder integer,
    remindercomstructprefix character varying(4),
    childpositiondetermination character varying,
    write_date timestamp without time zone,
    invoicelastcomstruct integer,
    name character varying(50),
    reminderemailsubject character varying(50),
    taxcertificatetemplate character varying(50),
    reminderemailaddress character varying(50)
);


ALTER TABLE public.extraschool_activitycategory OWNER TO openerp;

--
-- Name: TABLE extraschool_activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitycategory IS 'Activities categories';


--
-- Name: COLUMN extraschool_activitycategory.reminderemailtext; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderemailtext IS 'Reminder email text';


--
-- Name: COLUMN extraschool_activitycategory.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_activitycategory.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_activitycategory.invoicetemplate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoicetemplate IS 'Invoice Template';


--
-- Name: COLUMN extraschool_activitycategory.invoiceemailtext; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoiceemailtext IS 'Invoice email text';


--
-- Name: COLUMN extraschool_activitycategory.invoicecomstructprefix; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoicecomstructprefix IS 'Invoice Comstruct prefix';


--
-- Name: COLUMN extraschool_activitycategory.bankaccount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.bankaccount IS 'Bank account';


--
-- Name: COLUMN extraschool_activitycategory.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_activitycategory.invoiceemailaddress; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoiceemailaddress IS 'Invoice email address';


--
-- Name: COLUMN extraschool_activitycategory.invoiceemailsubject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoiceemailsubject IS 'Invoice email subject';


--
-- Name: COLUMN extraschool_activitycategory.reminderlastcomstruct; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderlastcomstruct IS 'Last Reminder structured comunication number';


--
-- Name: COLUMN extraschool_activitycategory.priorityorder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.priorityorder IS 'Priority order';


--
-- Name: COLUMN extraschool_activitycategory.remindercomstructprefix; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.remindercomstructprefix IS 'Reminder Comstruct prefix';


--
-- Name: COLUMN extraschool_activitycategory.childpositiondetermination; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.childpositiondetermination IS 'Child position determination';


--
-- Name: COLUMN extraschool_activitycategory.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_activitycategory.invoicelastcomstruct; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.invoicelastcomstruct IS 'Last Invoice structured comunication number';


--
-- Name: COLUMN extraschool_activitycategory.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.name IS 'Name';


--
-- Name: COLUMN extraschool_activitycategory.reminderemailsubject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderemailsubject IS 'Reminder email subject';


--
-- Name: COLUMN extraschool_activitycategory.taxcertificatetemplate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.taxcertificatetemplate IS 'Tax Certificate Template';


--
-- Name: COLUMN extraschool_activitycategory.reminderemailaddress; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitycategory.reminderemailaddress IS 'Reminder email address';


--
-- Name: extraschool_activitycategory_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activitycategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_activitycategory_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_activitycategory_place_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activitycategory_place_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitycategory_place_rel IS 'RELATION BETWEEN extraschool_activitycategory AND extraschool_place';


--
-- Name: extraschool_activitychildregistration; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activitychildregistration (
    id integer NOT NULL,
    create_uid integer,
    activity_id integer,
    create_date timestamp without time zone,
    place_id integer NOT NULL,
    write_uid integer,
    write_date timestamp without time zone,
    child_id integer NOT NULL,
    registration_from date NOT NULL,
    registration_to date NOT NULL
);


ALTER TABLE public.extraschool_activitychildregistration OWNER TO openerp;

--
-- Name: TABLE extraschool_activitychildregistration; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activitychildregistration IS 'activity child registration';


--
-- Name: COLUMN extraschool_activitychildregistration.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_activitychildregistration.activity_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.activity_id IS 'Activity';


--
-- Name: COLUMN extraschool_activitychildregistration.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_activitychildregistration.place_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.place_id IS 'Place';


--
-- Name: COLUMN extraschool_activitychildregistration.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_activitychildregistration.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_activitychildregistration.child_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.child_id IS 'Child';


--
-- Name: COLUMN extraschool_activitychildregistration.registration_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.registration_from IS 'Registration from';


--
-- Name: COLUMN extraschool_activitychildregistration.registration_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activitychildregistration.registration_to IS 'Registration to';


--
-- Name: extraschool_activitychildregistration_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activitychildregistration_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_activitychildregistration_id_seq OWNER TO openerp;

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
    date_from date NOT NULL,
    write_uid integer,
    write_date timestamp without time zone,
    date_to date NOT NULL
);


ALTER TABLE public.extraschool_activityexclusiondates OWNER TO openerp;

--
-- Name: TABLE extraschool_activityexclusiondates; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activityexclusiondates IS 'Activity exclusion dates';


--
-- Name: COLUMN extraschool_activityexclusiondates.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_activityexclusiondates.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_activityexclusiondates.date_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.date_from IS 'Date from';


--
-- Name: COLUMN extraschool_activityexclusiondates.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_activityexclusiondates.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityexclusiondates.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_activityexclusiondates_id_seq OWNER TO openerp;

--
-- Name: extraschool_activityexclusiondates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activityexclusiondates_id_seq OWNED BY extraschool_activityexclusiondates.id;


--
-- Name: extraschool_activityoccurrence; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activityoccurrence (
    id integer NOT NULL,
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


ALTER TABLE public.extraschool_activityoccurrence OWNER TO openerp;

--
-- Name: TABLE extraschool_activityoccurrence; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activityoccurrence IS 'activity occurrence';


--
-- Name: COLUMN extraschool_activityoccurrence.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_activityoccurrence.date_stop; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.date_stop IS 'Date stop';


--
-- Name: COLUMN extraschool_activityoccurrence.date_start; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.date_start IS 'Date start';


--
-- Name: COLUMN extraschool_activityoccurrence.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_activityoccurrence.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.name IS 'Name';


--
-- Name: COLUMN extraschool_activityoccurrence.place_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.place_id IS 'Place';


--
-- Name: COLUMN extraschool_activityoccurrence.activityid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.activityid IS 'Activity';


--
-- Name: COLUMN extraschool_activityoccurrence.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_activityoccurrence.prest_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.prest_to IS 'prest_to';


--
-- Name: COLUMN extraschool_activityoccurrence.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_activityoccurrence.occurrence_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.occurrence_date IS 'Date';


--
-- Name: COLUMN extraschool_activityoccurrence.prest_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityoccurrence.prest_from IS 'prest_from';


--
-- Name: extraschool_activityoccurrence_cild_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activityoccurrence_cild_rel (
    activityoccurrence_id integer NOT NULL,
    child_id integer NOT NULL
);


ALTER TABLE public.extraschool_activityoccurrence_cild_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_activityoccurrence_cild_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activityoccurrence_cild_rel IS 'RELATION BETWEEN extraschool_activityoccurrence AND extraschool_child';


--
-- Name: extraschool_activityoccurrence_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_activityoccurrence_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_activityoccurrence_id_seq OWNER TO openerp;

--
-- Name: extraschool_activityoccurrence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_activityoccurrence_id_seq OWNED BY extraschool_activityoccurrence.id;


--
-- Name: extraschool_activityplanneddate; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_activityplanneddate (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    write_uid integer,
    write_date timestamp without time zone,
    activitydate date
);


ALTER TABLE public.extraschool_activityplanneddate OWNER TO openerp;

--
-- Name: TABLE extraschool_activityplanneddate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_activityplanneddate IS 'Activities planned dates';


--
-- Name: COLUMN extraschool_activityplanneddate.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityplanneddate.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_activityplanneddate.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityplanneddate.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_activityplanneddate.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityplanneddate.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_activityplanneddate.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_activityplanneddate.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_activityplanneddate_id_seq OWNER TO openerp;

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
    activitycategoryid integer,
    payment_term date,
    period_to date,
    period_from date,
    write_uid integer,
    biller_file bytea,
    oldid integer,
    write_date timestamp without time zone,
    invoices_date date,
    filename character varying(20),
    name character varying(100)
);


ALTER TABLE public.extraschool_biller OWNER TO openerp;

--
-- Name: TABLE extraschool_biller; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_biller IS 'Biller';


--
-- Name: COLUMN extraschool_biller.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_biller.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.create_date IS 'Created on';


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
-- Name: COLUMN extraschool_biller.period_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.period_from IS 'Period from';


--
-- Name: COLUMN extraschool_biller.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_biller.biller_file; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.biller_file IS 'File';


--
-- Name: COLUMN extraschool_biller.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_biller.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_biller.invoices_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.invoices_date IS 'Invoices date';


--
-- Name: COLUMN extraschool_biller.filename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.filename IS 'filename';


--
-- Name: COLUMN extraschool_biller.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_biller.name IS 'Name';


--
-- Name: extraschool_biller_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_biller_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_biller_id_seq OWNER TO openerp;

--
-- Name: extraschool_biller_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_biller_id_seq OWNED BY extraschool_biller.id;


--
-- Name: extraschool_child; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_child (
    id integer NOT NULL,
    classid integer,
    create_uid integer,
    childtypeid integer NOT NULL,
    create_date timestamp without time zone,
    firstname character varying(50) NOT NULL,
    tagid character varying(50),
    lastname character varying(50) NOT NULL,
    isdisabled boolean,
    schoolimplantation integer NOT NULL,
    birthdate date NOT NULL,
    write_uid integer,
    otherref character varying(50),
    levelid integer NOT NULL,
    write_date timestamp without time zone,
    parentid integer NOT NULL,
    oldid integer
);


ALTER TABLE public.extraschool_child OWNER TO openerp;

--
-- Name: TABLE extraschool_child; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_child IS 'Child';


--
-- Name: COLUMN extraschool_child.classid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.classid IS 'Class';


--
-- Name: COLUMN extraschool_child.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_child.childtypeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.childtypeid IS 'Type';


--
-- Name: COLUMN extraschool_child.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_child.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.firstname IS 'FirstName';


--
-- Name: COLUMN extraschool_child.tagid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.tagid IS 'Tag ID';


--
-- Name: COLUMN extraschool_child.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_child.isdisabled; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.isdisabled IS 'Disabled';


--
-- Name: COLUMN extraschool_child.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_child.birthdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.birthdate IS 'Birthdate';


--
-- Name: COLUMN extraschool_child.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_child.otherref; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.otherref IS 'Other ref';


--
-- Name: COLUMN extraschool_child.levelid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.levelid IS 'Level';


--
-- Name: COLUMN extraschool_child.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_child.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.parentid IS 'Parent';


--
-- Name: COLUMN extraschool_child.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_child.oldid IS 'oldid';


--
-- Name: extraschool_child_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_child_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_child_id_seq OWNER TO openerp;

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
    name character varying(50) NOT NULL,
    write_uid integer,
    write_date timestamp without time zone,
    "position" integer NOT NULL
);


ALTER TABLE public.extraschool_childposition OWNER TO openerp;

--
-- Name: TABLE extraschool_childposition; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childposition IS 'Child position';


--
-- Name: COLUMN extraschool_childposition.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_childposition.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_childposition.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition.name IS 'Name';


--
-- Name: COLUMN extraschool_childposition.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_childposition.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childposition.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_childposition_id_seq OWNER TO openerp;

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
    schoolimplantation integer NOT NULL,
    create_date timestamp without time zone,
    childsfile bytea NOT NULL,
    childsimportfilter integer NOT NULL,
    write_uid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_childsimport OWNER TO openerp;

--
-- Name: TABLE extraschool_childsimport; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsimport IS 'extraschool.childsimport';


--
-- Name: COLUMN extraschool_childsimport.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_childsimport.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_childsimport.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_childsimport.childsfile; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.childsfile IS 'Childs File';


--
-- Name: COLUMN extraschool_childsimport.childsimportfilter; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.childsimportfilter IS 'Childs import filter';


--
-- Name: COLUMN extraschool_childsimport.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_childsimport.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimport.write_date IS 'Last Updated on';


--
-- Name: extraschool_childsimport_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childsimport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_childsimport_id_seq OWNER TO openerp;

--
-- Name: extraschool_childsimport_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childsimport_id_seq OWNED BY extraschool_childsimport.id;


--
-- Name: extraschool_childsimportfilter; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_childsimportfilter (
    id integer NOT NULL,
    childclassnamecolumns character varying(10),
    childotherrefcolumn integer,
    majchildotherref boolean,
    create_date timestamp without time zone,
    majparentworkphone boolean,
    parentstreetcolumns character varying(10),
    write_uid integer,
    parentfirstnamecolumn integer,
    parentzipcodecolumnname character varying(30),
    childbirthdatecolumn integer,
    parentgsmcolumn integer,
    parentcitycolumn integer,
    parentcitycolumnname character varying(30),
    childotherrefcolumnname character varying(30),
    majparentcity boolean,
    create_uid integer,
    parentemailcolumnname character varying(30),
    parentgsmcolumnname character varying(30),
    majchildlevel boolean,
    childbirthdatecolumnname character varying(30),
    majparentgsm boolean,
    parentworkphonecolumn integer,
    parentfirstnamecolumnname character varying(30),
    parenthousephonecolumnname character varying(30),
    childfirstnamecolumn integer,
    childclassnamecolumnsname character varying(60),
    majparentlastname boolean,
    parentworkphonecolumnname character varying(30),
    parentlastnamecolumnname character varying(30),
    startrow integer,
    childlevelcolumns character varying(10),
    write_date timestamp without time zone,
    parentlastnamecolumn integer,
    parenthousephonecolumn integer,
    childlastnamecolumn integer,
    majchildclassname boolean,
    majparentfirstname boolean,
    majparentzipcode boolean,
    childlastnamecolumnname character varying(30),
    name character varying(50),
    majschoolimplantation boolean,
    majparenthousephone boolean,
    majparentstreet boolean,
    majparentemail boolean,
    parentzipcodecolumn integer,
    childlevelcolumnsname character varying(60),
    childfirstnamecolumnname character varying(30),
    parentemailcolumn integer,
    parentstreetcolumnsname character varying(60)
);


ALTER TABLE public.extraschool_childsimportfilter OWNER TO openerp;

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
-- Name: COLUMN extraschool_childsimportfilter.majchildotherref; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majchildotherref IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentworkphone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentworkphone IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.parentstreetcolumns; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentstreetcolumns IS 'Parent street columns';


--
-- Name: COLUMN extraschool_childsimportfilter.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.write_uid IS 'Last Updated by';


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
-- Name: COLUMN extraschool_childsimportfilter.parentcitycolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentcitycolumn IS 'Parent city column';


--
-- Name: COLUMN extraschool_childsimportfilter.parentcitycolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentcitycolumnname IS 'Parent city column name';


--
-- Name: COLUMN extraschool_childsimportfilter.childotherrefcolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childotherrefcolumnname IS 'Child other ref column name';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentcity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentcity IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_childsimportfilter.parentemailcolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentemailcolumnname IS 'Parent email column name';


--
-- Name: COLUMN extraschool_childsimportfilter.parentgsmcolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentgsmcolumnname IS 'Parent gsm column name';


--
-- Name: COLUMN extraschool_childsimportfilter.majchildlevel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majchildlevel IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.childbirthdatecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childbirthdatecolumnname IS 'Child birthdate column name';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentgsm; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentgsm IS 'MAJ';


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
-- Name: COLUMN extraschool_childsimportfilter.majparentlastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentlastname IS 'MAJ';


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
-- Name: COLUMN extraschool_childsimportfilter.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.write_date IS 'Last Updated on';


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
-- Name: COLUMN extraschool_childsimportfilter.childlastnamecolumnname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.childlastnamecolumnname IS 'Child lastname column name';


--
-- Name: COLUMN extraschool_childsimportfilter.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.name IS 'Name';


--
-- Name: COLUMN extraschool_childsimportfilter.majschoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majschoolimplantation IS 'MAJ implantation';


--
-- Name: COLUMN extraschool_childsimportfilter.majparenthousephone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparenthousephone IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentstreet; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentstreet IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.majparentemail; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.majparentemail IS 'MAJ';


--
-- Name: COLUMN extraschool_childsimportfilter.parentzipcodecolumn; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsimportfilter.parentzipcodecolumn IS 'Parent zipcode column';


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
-- Name: extraschool_childsimportfilter_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childsimportfilter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_childsimportfilter_id_seq OWNER TO openerp;

--
-- Name: extraschool_childsimportfilter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_childsimportfilter_id_seq OWNED BY extraschool_childsimportfilter.id;


--
-- Name: extraschool_childsimportfilter_importlevelrule_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_childsimportfilter_importlevelrule_rel (
    childsimportfilter_id integer NOT NULL,
    importlevelrule_id integer NOT NULL
);


ALTER TABLE public.extraschool_childsimportfilter_importlevelrule_rel OWNER TO openerp;

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
    name character varying(16),
    childsworkbook bytea,
    placeid integer,
    write_uid integer,
    state character varying NOT NULL,
    write_date timestamp without time zone,
    child_id integer
);


ALTER TABLE public.extraschool_childsworkbook_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_childsworkbook_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childsworkbook_wizard IS 'extraschool.childsworkbook_wizard';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.childsworkbook; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.childsworkbook IS 'File';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_childsworkbook_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childsworkbook_wizard.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_childsworkbook_wizard_id_seq OWNER TO openerp;

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
    name character varying(50) NOT NULL,
    write_uid integer,
    oldid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_childtype OWNER TO openerp;

--
-- Name: TABLE extraschool_childtype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_childtype IS 'ChildType';


--
-- Name: COLUMN extraschool_childtype.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_childtype.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_childtype.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.name IS 'Name';


--
-- Name: COLUMN extraschool_childtype.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_childtype.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_childtype.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_childtype.write_date IS 'Last Updated on';


--
-- Name: extraschool_childtype_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_childtype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_childtype_id_seq OWNER TO openerp;

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
    schoolimplantation integer,
    create_date timestamp without time zone,
    name character varying(50) NOT NULL,
    write_uid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_class OWNER TO openerp;

--
-- Name: TABLE extraschool_class; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_class IS 'Class';


--
-- Name: COLUMN extraschool_class.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_class.schoolimplantation; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.schoolimplantation IS 'School implantation';


--
-- Name: COLUMN extraschool_class.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_class.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.name IS 'Name';


--
-- Name: COLUMN extraschool_class.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_class.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_class.write_date IS 'Last Updated on';


--
-- Name: extraschool_class_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_class_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_class_level_rel OWNER TO openerp;

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
    name character varying(20),
    codafile bytea,
    write_uid integer,
    write_date timestamp without time zone,
    create_date timestamp without time zone,
    codadate date
);


ALTER TABLE public.extraschool_coda OWNER TO openerp;

--
-- Name: TABLE extraschool_coda; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_coda IS 'extraschool.coda';


--
-- Name: COLUMN extraschool_coda.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_coda.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.name IS 'Name';


--
-- Name: COLUMN extraschool_coda.codafile; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.codafile IS 'CODA File';


--
-- Name: COLUMN extraschool_coda.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_coda.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_coda.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_coda.codadate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_coda.codadate IS 'CODA Date';


--
-- Name: extraschool_coda_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_coda_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_coda_id_seq OWNER TO openerp;

--
-- Name: extraschool_coda_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_coda_id_seq OWNED BY extraschool_coda.id;


--
-- Name: extraschool_discount; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_discount (
    id integer NOT NULL,
    discounttype character varying,
    wichactivities character varying,
    create_uid integer,
    period character varying,
    write_uid integer,
    discount character varying(6),
    write_date timestamp without time zone,
    create_date timestamp without time zone,
    name character varying(50)
);


ALTER TABLE public.extraschool_discount OWNER TO openerp;

--
-- Name: TABLE extraschool_discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discount IS 'Discount';


--
-- Name: COLUMN extraschool_discount.discounttype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.discounttype IS 'Discount type';


--
-- Name: COLUMN extraschool_discount.wichactivities; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.wichactivities IS 'Wich activities';


--
-- Name: COLUMN extraschool_discount.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_discount.period; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.period IS 'Period';


--
-- Name: COLUMN extraschool_discount.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_discount.discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.discount IS 'Discount';


--
-- Name: COLUMN extraschool_discount.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_discount.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_discount.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discount.name IS 'Name';


--
-- Name: extraschool_discount_activity_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_discount_activity_rel (
    discount_id integer NOT NULL,
    activity_id integer NOT NULL
);


ALTER TABLE public.extraschool_discount_activity_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_discount_childtype_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_discount_discountrule_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_discount_id_seq OWNER TO openerp;

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
    name character varying(50),
    value character varying(50),
    write_uid integer,
    field character varying(60),
    write_date timestamp without time zone,
    operator character varying
);


ALTER TABLE public.extraschool_discountrule OWNER TO openerp;

--
-- Name: TABLE extraschool_discountrule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_discountrule IS 'Discount Rule';


--
-- Name: COLUMN extraschool_discountrule.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_discountrule.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_discountrule.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.name IS 'Name';


--
-- Name: COLUMN extraschool_discountrule.value; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.value IS 'Value';


--
-- Name: COLUMN extraschool_discountrule.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_discountrule.field; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.field IS 'Field';


--
-- Name: COLUMN extraschool_discountrule.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_discountrule.operator; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_discountrule.operator IS 'Operator';


--
-- Name: extraschool_discountrule_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_discountrule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_discountrule_id_seq OWNER TO openerp;

--
-- Name: extraschool_discountrule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_discountrule_id_seq OWNED BY extraschool_discountrule.id;


--
-- Name: extraschool_guardian; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_guardian (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    firstname character varying(50),
    lastname character varying(50) NOT NULL,
    tagid character varying(50),
    write_uid integer,
    oldid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_guardian OWNER TO openerp;

--
-- Name: TABLE extraschool_guardian; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_guardian IS 'Guardian';


--
-- Name: COLUMN extraschool_guardian.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_guardian.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_guardian.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.firstname IS 'FirstName';


--
-- Name: COLUMN extraschool_guardian.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_guardian.tagid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.tagid IS 'Tag ID';


--
-- Name: COLUMN extraschool_guardian.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_guardian.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_guardian.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardian.write_date IS 'Last Updated on';


--
-- Name: extraschool_guardian_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_guardian_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_guardian_id_seq OWNER TO openerp;

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
    write_uid integer,
    guardianid integer,
    prestation_date date,
    write_date timestamp without time zone,
    manualy_encoded boolean,
    prestation_time double precision,
    es character varying
);


ALTER TABLE public.extraschool_guardianprestationtimes OWNER TO openerp;

--
-- Name: TABLE extraschool_guardianprestationtimes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_guardianprestationtimes IS 'Guardian Prestation Times';


--
-- Name: COLUMN extraschool_guardianprestationtimes.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_guardianprestationtimes.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_guardianprestationtimes.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_guardianprestationtimes.guardianid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.guardianid IS 'Guardian';


--
-- Name: COLUMN extraschool_guardianprestationtimes.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_guardianprestationtimes.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_guardianprestationtimes.manualy_encoded; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.manualy_encoded IS 'Manualy encoded';


--
-- Name: COLUMN extraschool_guardianprestationtimes.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_guardianprestationtimes.es; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes.es IS 'ES';


--
-- Name: extraschool_guardianprestationtimes_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_guardianprestationtimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_guardianprestationtimes_id_seq OWNER TO openerp;

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
    prestations_from date NOT NULL,
    create_date timestamp without time zone,
    name character varying(16),
    prestations_to date NOT NULL,
    write_uid integer,
    guardianid integer,
    state character varying NOT NULL,
    prestationsreport bytea,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_guardianprestationtimes_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_guardianprestationtimes_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_guardianprestationtimes_wizard IS 'Guardian Prestation Times Wizard';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.prestations_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.prestations_from IS 'Prestations from';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.prestations_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.prestations_to IS 'Prestations to';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.guardianid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.guardianid IS 'Guardian';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.prestationsreport; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.prestationsreport IS 'File';


--
-- Name: COLUMN extraschool_guardianprestationtimes_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_guardianprestationtimes_wizard.write_date IS 'Last Updated on';


--
-- Name: extraschool_guardianprestationtimes_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_guardianprestationtimes_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_guardianprestationtimes_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_guardianprestationtimes_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_guardianprestationtimes_wizard_id_seq OWNED BY extraschool_guardianprestationtimes_wizard.id;


--
-- Name: extraschool_importlevelrule; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_importlevelrule (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    levelid integer NOT NULL,
    endpos1 integer,
    startpos1 integer,
    write_date timestamp without time zone,
    equalto1 character varying(10),
    write_uid integer
);


ALTER TABLE public.extraschool_importlevelrule OWNER TO openerp;

--
-- Name: TABLE extraschool_importlevelrule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_importlevelrule IS 'Child import level rule';


--
-- Name: COLUMN extraschool_importlevelrule.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_importlevelrule.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_importlevelrule.levelid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.levelid IS 'Level';


--
-- Name: COLUMN extraschool_importlevelrule.endpos1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.endpos1 IS 'End pos1';


--
-- Name: COLUMN extraschool_importlevelrule.startpos1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.startpos1 IS 'Start pos1';


--
-- Name: COLUMN extraschool_importlevelrule.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_importlevelrule.equalto1; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.equalto1 IS 'Equals to1';


--
-- Name: COLUMN extraschool_importlevelrule.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importlevelrule.write_uid IS 'Last Updated by';


--
-- Name: extraschool_importlevelrule_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_importlevelrule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_importlevelrule_id_seq OWNER TO openerp;

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
    childsimport integer,
    rejectcause character varying(60),
    write_uid integer,
    write_date timestamp without time zone,
    line integer
);


ALTER TABLE public.extraschool_importreject OWNER TO openerp;

--
-- Name: TABLE extraschool_importreject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_importreject IS 'Import Reject';


--
-- Name: COLUMN extraschool_importreject.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_importreject.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_importreject.childsimport; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.childsimport IS 'Childs import';


--
-- Name: COLUMN extraschool_importreject.rejectcause; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.rejectcause IS 'Reject cause';


--
-- Name: COLUMN extraschool_importreject.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_importreject.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_importreject.line; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_importreject.line IS 'Line';


--
-- Name: extraschool_importreject_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_importreject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_importreject_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_initupdate_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_initupdate_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_initupdate_wizard IS 'extraschool.initupdate_wizard';


--
-- Name: COLUMN extraschool_initupdate_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_initupdate_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_initupdate_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_initupdate_wizard.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_initupdate_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_initupdate_wizard.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_initupdate_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_initupdate_wizard.write_uid IS 'Last Updated by';


--
-- Name: extraschool_initupdate_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_initupdate_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_initupdate_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_initupdate_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_initupdate_wizard_id_seq OWNED BY extraschool_initupdate_wizard.id;


--
-- Name: extraschool_invoice; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_invoice (
    id integer NOT NULL,
    create_date timestamp without time zone,
    amount_received double precision,
    payment_term date,
    period_to date,
    number integer,
    write_uid integer,
    biller_id integer,
    create_uid integer,
    filename character varying(20),
    period_from date,
    activitycategoryid integer,
    structcom character varying(50),
    schoolimplantationid integer,
    discount double precision,
    oldid character varying(20),
    write_date timestamp without time zone,
    parentid integer,
    amount_total double precision,
    name character varying(20),
    invoice_file bytea,
    no_value double precision,
    balance double precision
);


ALTER TABLE public.extraschool_invoice OWNER TO openerp;

--
-- Name: TABLE extraschool_invoice; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoice IS 'invoice';


--
-- Name: COLUMN extraschool_invoice.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_invoice.amount_received; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.amount_received IS 'Received';


--
-- Name: COLUMN extraschool_invoice.payment_term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.payment_term IS 'biller_id.payment_term';


--
-- Name: COLUMN extraschool_invoice.period_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.period_to IS 'biller_id.period_to';


--
-- Name: COLUMN extraschool_invoice.number; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.number IS 'Number';


--
-- Name: COLUMN extraschool_invoice.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_invoice.biller_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.biller_id IS 'Biller';


--
-- Name: COLUMN extraschool_invoice.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_invoice.filename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.filename IS 'filename';


--
-- Name: COLUMN extraschool_invoice.period_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.period_from IS 'biller_id.period_from';


--
-- Name: COLUMN extraschool_invoice.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_invoice.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.structcom IS 'Structured Communication';


--
-- Name: COLUMN extraschool_invoice.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.schoolimplantationid IS 'School implantation';


--
-- Name: COLUMN extraschool_invoice.discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.discount IS 'Discount';


--
-- Name: COLUMN extraschool_invoice.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_invoice.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_invoice.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.parentid IS 'Parent';


--
-- Name: COLUMN extraschool_invoice.amount_total; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.amount_total IS 'Amount';


--
-- Name: COLUMN extraschool_invoice.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.name IS 'Name';


--
-- Name: COLUMN extraschool_invoice.invoice_file; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.invoice_file IS 'File';


--
-- Name: COLUMN extraschool_invoice.no_value; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice.no_value IS 'No value';


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


ALTER TABLE public.extraschool_invoice_id_seq OWNER TO openerp;

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
    name character varying(16),
    invoice_term date NOT NULL,
    invoices bytea,
    invoice_date date NOT NULL,
    period_to date NOT NULL,
    write_uid integer,
    period_from date NOT NULL,
    state character varying NOT NULL,
    activitycategory integer NOT NULL,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_invoice_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_invoice_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoice_wizard IS 'extraschool.invoice_wizard';


--
-- Name: COLUMN extraschool_invoice_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_invoice_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.create_date IS 'Created on';


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
-- Name: COLUMN extraschool_invoice_wizard.invoice_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.invoice_date IS 'invoice date';


--
-- Name: COLUMN extraschool_invoice_wizard.period_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.period_to IS 'Period to';


--
-- Name: COLUMN extraschool_invoice_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.write_uid IS 'Last Updated by';


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
-- Name: COLUMN extraschool_invoice_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoice_wizard.write_date IS 'Last Updated on';


--
-- Name: extraschool_invoice_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_invoice_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_invoice_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_invoice_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_invoice_wizard_id_seq OWNED BY extraschool_invoice_wizard.id;


--
-- Name: extraschool_invoice_wizard_schoolimplantation_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_invoice_wizard_schoolimplantation_rel (
    invoice_wizard_id integer NOT NULL,
    schoolimplantation_id integer NOT NULL
);


ALTER TABLE public.extraschool_invoice_wizard_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_invoice_wizard_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoice_wizard_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_invoice_wizard AND extraschool_schoolimplantation';


--
-- Name: extraschool_invoicedprestations; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_invoicedprestations (
    id integer NOT NULL,
    create_uid integer,
    invoiceid integer,
    create_date timestamp without time zone,
    placeid integer,
    write_uid integer,
    discount boolean,
    activityid integer,
    prestation_date date,
    write_date timestamp without time zone,
    childid integer,
    quantity integer
);


ALTER TABLE public.extraschool_invoicedprestations OWNER TO openerp;

--
-- Name: TABLE extraschool_invoicedprestations; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_invoicedprestations IS 'invoiced Prestations';


--
-- Name: COLUMN extraschool_invoicedprestations.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_invoicedprestations.invoiceid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.invoiceid IS 'invoice';


--
-- Name: COLUMN extraschool_invoicedprestations.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_invoicedprestations.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.placeid IS 'Place';


--
-- Name: COLUMN extraschool_invoicedprestations.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_invoicedprestations.discount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.discount IS 'Discount';


--
-- Name: COLUMN extraschool_invoicedprestations.activityid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.activityid IS 'Activity';


--
-- Name: COLUMN extraschool_invoicedprestations.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_invoicedprestations.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_invoicedprestations.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.childid IS 'Child';


--
-- Name: COLUMN extraschool_invoicedprestations.quantity; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_invoicedprestations.quantity IS 'Quantity';


--
-- Name: extraschool_invoicedprestations_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_invoicedprestations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_invoicedprestations_id_seq OWNER TO openerp;

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
    name character varying(50),
    ordernumber integer NOT NULL,
    write_uid integer,
    oldid integer,
    write_date timestamp without time zone,
    leveltype character varying NOT NULL
);


ALTER TABLE public.extraschool_level OWNER TO openerp;

--
-- Name: TABLE extraschool_level; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_level IS 'Level';


--
-- Name: COLUMN extraschool_level.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_level.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_level.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.name IS 'Name';


--
-- Name: COLUMN extraschool_level.ordernumber; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.ordernumber IS 'ordernumber';


--
-- Name: COLUMN extraschool_level.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_level.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_level.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_level.leveltype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_level.leveltype IS 'Level type';


--
-- Name: extraschool_level_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_level_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_level_id_seq OWNER TO openerp;

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
    qrencode character varying(80),
    create_date timestamp without time zone,
    lastqrcodenbr integer,
    tempfolder character varying(80),
    templatesfolder character varying(80),
    write_uid integer,
    codasfolder character varying(80),
    processedcodasfolder character varying(80),
    write_date timestamp without time zone,
    emailfornotifications character varying(80)
);


ALTER TABLE public.extraschool_mainsettings OWNER TO openerp;

--
-- Name: TABLE extraschool_mainsettings; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_mainsettings IS 'Main Settings';


--
-- Name: COLUMN extraschool_mainsettings.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_mainsettings.qrencode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.qrencode IS 'qrencode';


--
-- Name: COLUMN extraschool_mainsettings.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.create_date IS 'Created on';


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
-- Name: COLUMN extraschool_mainsettings.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_mainsettings.codasfolder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.codasfolder IS 'codasfolder';


--
-- Name: COLUMN extraschool_mainsettings.processedcodasfolder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.processedcodasfolder IS 'processedcodasfolder';


--
-- Name: COLUMN extraschool_mainsettings.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_mainsettings.emailfornotifications; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_mainsettings.emailfornotifications IS 'Email for notifications';


--
-- Name: extraschool_mainsettings_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_mainsettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_mainsettings_id_seq OWNER TO openerp;

--
-- Name: extraschool_mainsettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_mainsettings_id_seq OWNED BY extraschool_mainsettings.id;


--
-- Name: extraschool_one_report; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_one_report (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    transmissiondate date NOT NULL,
    placeid integer,
    write_uid integer,
    activitycategory integer,
    nb_m_childs integer,
    write_date timestamp without time zone,
    year integer NOT NULL,
    quarter character varying NOT NULL,
    nb_p_childs integer
);


ALTER TABLE public.extraschool_one_report OWNER TO openerp;

--
-- Name: TABLE extraschool_one_report; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_one_report IS 'extraschool.one_report';


--
-- Name: COLUMN extraschool_one_report.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_one_report.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_one_report.transmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.transmissiondate IS 'Transmissiondate';


--
-- Name: COLUMN extraschool_one_report.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.placeid IS 'Placeid';


--
-- Name: COLUMN extraschool_one_report.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_one_report.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.activitycategory IS 'Activitycategory';


--
-- Name: COLUMN extraschool_one_report.nb_m_childs; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.nb_m_childs IS 'Nb m childs';


--
-- Name: COLUMN extraschool_one_report.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_one_report.year; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.year IS 'Year';


--
-- Name: COLUMN extraschool_one_report.quarter; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.quarter IS 'Quarter';


--
-- Name: COLUMN extraschool_one_report.nb_p_childs; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report.nb_p_childs IS 'Nb p childs';


--
-- Name: extraschool_one_report_day; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_one_report_day (
    id integer NOT NULL,
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


ALTER TABLE public.extraschool_one_report_day OWNER TO openerp;

--
-- Name: TABLE extraschool_one_report_day; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_one_report_day IS 'extraschool.one_report_day';


--
-- Name: COLUMN extraschool_one_report_day.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_one_report_day.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_one_report_day.subvention_type; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.subvention_type IS 'Subvention type';


--
-- Name: COLUMN extraschool_one_report_day.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_one_report_day.day_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.day_date IS 'Day date';


--
-- Name: COLUMN extraschool_one_report_day.one_report_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.one_report_id IS 'One report id';


--
-- Name: COLUMN extraschool_one_report_day.nb_m_childs; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.nb_m_childs IS 'Nb m childs';


--
-- Name: COLUMN extraschool_one_report_day.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_one_report_day.nb_p_childs; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_one_report_day.nb_p_childs IS 'Nb p childs';


--
-- Name: extraschool_one_report_day_child_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_one_report_day_child_rel (
    one_report_day_id integer NOT NULL,
    child_id integer NOT NULL
);


ALTER TABLE public.extraschool_one_report_day_child_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_one_report_day_child_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_one_report_day_child_rel IS 'RELATION BETWEEN extraschool_one_report_day AND extraschool_child';


--
-- Name: extraschool_one_report_day_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_one_report_day_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_one_report_day_id_seq OWNER TO openerp;

--
-- Name: extraschool_one_report_day_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_one_report_day_id_seq OWNED BY extraschool_one_report_day.id;


--
-- Name: extraschool_one_report_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_one_report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_one_report_id_seq OWNER TO openerp;

--
-- Name: extraschool_one_report_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_one_report_id_seq OWNED BY extraschool_one_report.id;


--
-- Name: extraschool_parent; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_parent (
    id integer NOT NULL,
    invoicesendmethod character varying NOT NULL,
    workphone character varying(20),
    remindersendmethod character varying NOT NULL,
    write_uid integer,
    one_subvention_type character varying NOT NULL,
    street character varying(50) NOT NULL,
    create_date timestamp without time zone,
    create_uid integer,
    housephone character varying(20),
    zipcode character varying(6) NOT NULL,
    email character varying(100),
    firstname character varying(50) NOT NULL,
    city character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    oldid integer,
    write_date timestamp without time zone,
    streetcode character varying(50),
    name character varying(100),
    gsm character varying(20)
);


ALTER TABLE public.extraschool_parent OWNER TO openerp;

--
-- Name: TABLE extraschool_parent; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_parent IS 'Parent';


--
-- Name: COLUMN extraschool_parent.invoicesendmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.invoicesendmethod IS 'Invoice send method';


--
-- Name: COLUMN extraschool_parent.workphone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.workphone IS 'Work Phone';


--
-- Name: COLUMN extraschool_parent.remindersendmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.remindersendmethod IS 'Reminder send method';


--
-- Name: COLUMN extraschool_parent.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_parent.one_subvention_type; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.one_subvention_type IS 'One subvention type';


--
-- Name: COLUMN extraschool_parent.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.street IS 'Street';


--
-- Name: COLUMN extraschool_parent.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_parent.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_parent.housephone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.housephone IS 'House Phone';


--
-- Name: COLUMN extraschool_parent.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_parent.email; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.email IS 'Email';


--
-- Name: COLUMN extraschool_parent.firstname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.firstname IS 'FirstName';


--
-- Name: COLUMN extraschool_parent.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.city IS 'City';


--
-- Name: COLUMN extraschool_parent.lastname; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.lastname IS 'LastName';


--
-- Name: COLUMN extraschool_parent.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_parent.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_parent.streetcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.streetcode IS 'Street code';


--
-- Name: COLUMN extraschool_parent.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.name IS 'FullName';


--
-- Name: COLUMN extraschool_parent.gsm; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_parent.gsm IS 'GSM';


--
-- Name: extraschool_parent_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_parent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_parent_id_seq OWNER TO openerp;

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
    account character varying(20),
    create_date timestamp without time zone,
    name character varying(50),
    coda integer,
    write_uid integer,
    paymenttype character varying,
    amount double precision,
    concernedinvoice integer,
    paymentdate date,
    write_date timestamp without time zone,
    structcom character varying(50)
);


ALTER TABLE public.extraschool_payment OWNER TO openerp;

--
-- Name: TABLE extraschool_payment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_payment IS 'Payment';


--
-- Name: COLUMN extraschool_payment.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_payment.account; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.account IS 'Account';


--
-- Name: COLUMN extraschool_payment.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_payment.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.name IS 'Name';


--
-- Name: COLUMN extraschool_payment.coda; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.coda IS 'Coda';


--
-- Name: COLUMN extraschool_payment.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_payment.paymenttype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.paymenttype IS 'Payment type';


--
-- Name: COLUMN extraschool_payment.amount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.amount IS 'Amount';


--
-- Name: COLUMN extraschool_payment.concernedinvoice; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.concernedinvoice IS 'Concerned invoice';


--
-- Name: COLUMN extraschool_payment.paymentdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.paymentdate IS 'Date';


--
-- Name: COLUMN extraschool_payment.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_payment.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_payment.structcom IS 'Structured Communication';


--
-- Name: extraschool_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_payment_id_seq OWNER TO openerp;

--
-- Name: extraschool_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_payment_id_seq OWNED BY extraschool_payment.id;


--
-- Name: extraschool_pdaprestationtimes; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_pdaprestationtimes (
    id integer NOT NULL,
    prestation_times_of_the_day_id integer,
    create_date timestamp without time zone,
    activitycategoryid integer,
    create_uid integer,
    placeid integer NOT NULL,
    write_uid integer,
    prestation_date date,
    es character varying,
    write_date timestamp without time zone,
    prestation_time double precision,
    childid integer
);


ALTER TABLE public.extraschool_pdaprestationtimes OWNER TO openerp;

--
-- Name: TABLE extraschool_pdaprestationtimes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_pdaprestationtimes IS 'PDA Prestation Times';


--
-- Name: COLUMN extraschool_pdaprestationtimes.prestation_times_of_the_day_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.prestation_times_of_the_day_id IS 'Prestation of the day';


--
-- Name: COLUMN extraschool_pdaprestationtimes.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_pdaprestationtimes.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_pdaprestationtimes.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_pdaprestationtimes.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_pdaprestationtimes.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_pdaprestationtimes.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_pdaprestationtimes.es; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.es IS 'ES';


--
-- Name: COLUMN extraschool_pdaprestationtimes.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_pdaprestationtimes.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_pdaprestationtimes.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_pdaprestationtimes.childid IS 'Child';


--
-- Name: extraschool_pdaprestationtimes_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_pdaprestationtimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_pdaprestationtimes_id_seq OWNER TO openerp;

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
    name character varying(50),
    schedule text,
    zipcode character varying(6),
    write_uid integer,
    street character varying(50),
    city character varying(50),
    oldid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_place OWNER TO openerp;

--
-- Name: TABLE extraschool_place; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_place IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_place.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_place.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_place.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.name IS 'Name';


--
-- Name: COLUMN extraschool_place.schedule; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.schedule IS 'Schedule';


--
-- Name: COLUMN extraschool_place.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_place.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_place.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.street IS 'Street';


--
-- Name: COLUMN extraschool_place.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.city IS 'City';


--
-- Name: COLUMN extraschool_place.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_place.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_place.write_date IS 'Last Updated on';


--
-- Name: extraschool_place_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_place_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_place_schoolimplantation_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_place_schoolimplantation_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_place_schoolimplantation_rel IS 'RELATION BETWEEN extraschool_place AND extraschool_schoolimplantation';


--
-- Name: extraschool_prestation_times_encodage_manuel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_prestation_times_encodage_manuel (
    id integer NOT NULL,
    comment text,
    create_uid integer,
    create_date timestamp without time zone,
    place_id integer NOT NULL,
    write_uid integer,
    write_date timestamp without time zone,
    date_of_the_day date NOT NULL
);


ALTER TABLE public.extraschool_prestation_times_encodage_manuel OWNER TO openerp;

--
-- Name: TABLE extraschool_prestation_times_encodage_manuel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestation_times_encodage_manuel IS 'extraschool.prestation_times_encodage_manuel';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.comment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.comment IS 'Comment';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.place_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.place_id IS 'Place id';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_prestation_times_encodage_manuel.date_of_the_day; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_encodage_manuel.date_of_the_day IS 'Date of the day';


--
-- Name: extraschool_prestation_times_encodage_manuel_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestation_times_encodage_manuel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_prestation_times_encodage_manuel_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestation_times_encodage_manuel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestation_times_encodage_manuel_id_seq OWNED BY extraschool_prestation_times_encodage_manuel.id;


--
-- Name: extraschool_prestation_times_manuel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_prestation_times_manuel (
    id integer NOT NULL,
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


ALTER TABLE public.extraschool_prestation_times_manuel OWNER TO openerp;

--
-- Name: TABLE extraschool_prestation_times_manuel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestation_times_manuel IS 'extraschool.prestation_times_manuel';


--
-- Name: COLUMN extraschool_prestation_times_manuel.comment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.comment IS 'Comment';


--
-- Name: COLUMN extraschool_prestation_times_manuel.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_prestation_times_manuel.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_prestation_times_manuel.prestation_time_entry; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.prestation_time_entry IS 'Entry Time';


--
-- Name: COLUMN extraschool_prestation_times_manuel.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_prestation_times_manuel.prestation_times_encodage_manuel_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.prestation_times_encodage_manuel_id IS 'encodage manuel';


--
-- Name: COLUMN extraschool_prestation_times_manuel.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_prestation_times_manuel.child_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.child_id IS 'Child id';


--
-- Name: COLUMN extraschool_prestation_times_manuel.prestation_time_exit; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_manuel.prestation_time_exit IS 'Exit Time';


--
-- Name: extraschool_prestation_times_manuel_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestation_times_manuel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_prestation_times_manuel_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestation_times_manuel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestation_times_manuel_id_seq OWNED BY extraschool_prestation_times_manuel.id;


--
-- Name: extraschool_prestation_times_of_the_day; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_prestation_times_of_the_day (
    id integer NOT NULL,
    comment text,
    create_uid integer,
    create_date timestamp without time zone,
    write_uid integer,
    write_date timestamp without time zone,
    date_of_the_day date NOT NULL,
    verified boolean,
    child_id integer NOT NULL
);


ALTER TABLE public.extraschool_prestation_times_of_the_day OWNER TO openerp;

--
-- Name: TABLE extraschool_prestation_times_of_the_day; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestation_times_of_the_day IS 'extraschool.prestation_times_of_the_day';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.comment; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.comment IS 'Comment';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.date_of_the_day; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.date_of_the_day IS 'Date of the day';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.verified; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.verified IS 'Verified';


--
-- Name: COLUMN extraschool_prestation_times_of_the_day.child_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestation_times_of_the_day.child_id IS 'Child id';


--
-- Name: extraschool_prestation_times_of_the_day_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestation_times_of_the_day_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_prestation_times_of_the_day_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestation_times_of_the_day_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestation_times_of_the_day_id_seq OWNED BY extraschool_prestation_times_of_the_day.id;


--
-- Name: extraschool_prestationscheck_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_prestationscheck_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    period_to date,
    write_uid integer,
    period_from date,
    state character varying NOT NULL,
    activitycategory integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_prestationscheck_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_prestationscheck_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestationscheck_wizard IS 'extraschool.prestationscheck_wizard';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.period_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.period_to IS 'Period to';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.write_uid IS 'Last Updated by';


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

COMMENT ON COLUMN extraschool_prestationscheck_wizard.activitycategory IS 'Activitycategory';


--
-- Name: COLUMN extraschool_prestationscheck_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationscheck_wizard.write_date IS 'Last Updated on';


--
-- Name: extraschool_prestationscheck_wizard_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestationscheck_wizard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_prestationscheck_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestationscheck_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestationscheck_wizard_id_seq OWNED BY extraschool_prestationscheck_wizard.id;


--
-- Name: extraschool_prestationscheck_wizard_place_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_prestationscheck_wizard_place_rel (
    prestationscheck_wizard_id integer NOT NULL,
    place_id integer NOT NULL
);


ALTER TABLE public.extraschool_prestationscheck_wizard_place_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_prestationscheck_wizard_place_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestationscheck_wizard_place_rel IS 'RELATION BETWEEN extraschool_prestationscheck_wizard AND extraschool_place';


--
-- Name: extraschool_prestationtimes; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_prestationtimes (
    id integer NOT NULL,
    prestation_times_of_the_day_id integer,
    error_msg character varying(255),
    verified boolean,
    create_uid integer,
    exit_all boolean,
    placeid integer,
    write_uid integer,
    activity_occurrence_id integer,
    prestation_date date,
    childid integer,
    write_date timestamp without time zone,
    manualy_encoded boolean,
    create_date timestamp without time zone,
    prestation_time double precision NOT NULL,
    es character varying
);


ALTER TABLE public.extraschool_prestationtimes OWNER TO openerp;

--
-- Name: TABLE extraschool_prestationtimes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_prestationtimes IS 'Prestation Times';


--
-- Name: COLUMN extraschool_prestationtimes.prestation_times_of_the_day_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.prestation_times_of_the_day_id IS 'Prestation of the day';


--
-- Name: COLUMN extraschool_prestationtimes.error_msg; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.error_msg IS 'Error';


--
-- Name: COLUMN extraschool_prestationtimes.verified; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.verified IS 'Verified';


--
-- Name: COLUMN extraschool_prestationtimes.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_prestationtimes.exit_all; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.exit_all IS 'Exit all';


--
-- Name: COLUMN extraschool_prestationtimes.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_prestationtimes.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_prestationtimes.activity_occurrence_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.activity_occurrence_id IS 'Activity occurrence';


--
-- Name: COLUMN extraschool_prestationtimes.prestation_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.prestation_date IS 'Date';


--
-- Name: COLUMN extraschool_prestationtimes.childid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.childid IS 'Child';


--
-- Name: COLUMN extraschool_prestationtimes.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_prestationtimes.manualy_encoded; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.manualy_encoded IS 'Manualy encoded';


--
-- Name: COLUMN extraschool_prestationtimes.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_prestationtimes.prestation_time; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.prestation_time IS 'Time';


--
-- Name: COLUMN extraschool_prestationtimes.es; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_prestationtimes.es IS 'es';


--
-- Name: extraschool_prestationtimes_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_prestationtimes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_prestationtimes_id_seq OWNER TO openerp;

--
-- Name: extraschool_prestationtimes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_prestationtimes_id_seq OWNED BY extraschool_prestationtimes.id;


--
-- Name: extraschool_price_list; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_price_list (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying(50),
    write_uid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_price_list OWNER TO openerp;

--
-- Name: TABLE extraschool_price_list; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_price_list IS 'Activities price list';


--
-- Name: COLUMN extraschool_price_list.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_price_list.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_price_list.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list.name IS 'Name';


--
-- Name: COLUMN extraschool_price_list.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_price_list.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list.write_date IS 'Last Updated on';


--
-- Name: extraschool_price_list_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_price_list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_price_list_id_seq OWNER TO openerp;

--
-- Name: extraschool_price_list_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_price_list_id_seq OWNED BY extraschool_price_list.id;


--
-- Name: extraschool_price_list_version; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_price_list_version (
    id integer NOT NULL,
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


ALTER TABLE public.extraschool_price_list_version OWNER TO openerp;

--
-- Name: TABLE extraschool_price_list_version; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_price_list_version IS 'Activities price list version';


--
-- Name: COLUMN extraschool_price_list_version.validity_to; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.validity_to IS 'Validity to';


--
-- Name: COLUMN extraschool_price_list_version.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_price_list_version.price_list_id; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.price_list_id IS 'Price list';


--
-- Name: COLUMN extraschool_price_list_version.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_price_list_version.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.name IS 'Name';


--
-- Name: COLUMN extraschool_price_list_version.price; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.price IS 'Price';


--
-- Name: COLUMN extraschool_price_list_version.validity_from; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.validity_from IS 'Validity from';


--
-- Name: COLUMN extraschool_price_list_version.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_price_list_version.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_price_list_version.period_duration; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_price_list_version.period_duration IS 'Period Duration';


--
-- Name: extraschool_price_list_version_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_price_list_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_price_list_version_id_seq OWNER TO openerp;

--
-- Name: extraschool_price_list_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_price_list_version_id_seq OWNED BY extraschool_price_list_version.id;


--
-- Name: extraschool_qrcodes_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_qrcodes_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying(16),
    qrcodes bytea,
    write_uid integer,
    state character varying NOT NULL,
    write_date timestamp without time zone,
    quantity integer
);


ALTER TABLE public.extraschool_qrcodes_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_qrcodes_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_qrcodes_wizard IS 'extraschool.qrcodes_wizard';


--
-- Name: COLUMN extraschool_qrcodes_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_qrcodes_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_qrcodes_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_qrcodes_wizard.qrcodes; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.qrcodes IS 'File';


--
-- Name: COLUMN extraschool_qrcodes_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_qrcodes_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_qrcodes_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_qrcodes_wizard.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_qrcodes_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_qrcodes_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_qrcodes_wizard_id_seq OWNED BY extraschool_qrcodes_wizard.id;


--
-- Name: extraschool_reject; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_reject (
    id integer NOT NULL,
    create_uid integer,
    account character varying(20),
    create_date timestamp without time zone,
    name character varying(50),
    coda integer,
    rejectcause character varying(60),
    write_uid integer,
    amount double precision,
    paymentdate date,
    write_date timestamp without time zone,
    structcom character varying(50)
);


ALTER TABLE public.extraschool_reject OWNER TO openerp;

--
-- Name: TABLE extraschool_reject; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reject IS 'Reject';


--
-- Name: COLUMN extraschool_reject.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_reject.account; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.account IS 'Account';


--
-- Name: COLUMN extraschool_reject.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_reject.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.name IS 'Name';


--
-- Name: COLUMN extraschool_reject.coda; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.coda IS 'Coda';


--
-- Name: COLUMN extraschool_reject.rejectcause; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.rejectcause IS 'Reject cause';


--
-- Name: COLUMN extraschool_reject.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_reject.amount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.amount IS 'Amount';


--
-- Name: COLUMN extraschool_reject.paymentdate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.paymentdate IS 'Date';


--
-- Name: COLUMN extraschool_reject.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reject.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_reject_id_seq OWNER TO openerp;

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
    term date,
    remindersjournalid integer,
    create_date timestamp without time zone,
    activitycategoryid integer,
    transmissiondate date,
    reminder_file bytea,
    parentid integer,
    filename character varying(30),
    write_uid integer,
    amount double precision,
    write_date timestamp without time zone,
    structcom character varying(50),
    schoolimplantationid integer
);


ALTER TABLE public.extraschool_reminder OWNER TO openerp;

--
-- Name: TABLE extraschool_reminder; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reminder IS 'Reminder';


--
-- Name: COLUMN extraschool_reminder.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_reminder.term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.term IS 'remindersjournalid.term';


--
-- Name: COLUMN extraschool_reminder.remindersjournalid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.remindersjournalid IS 'Reminders journal';


--
-- Name: COLUMN extraschool_reminder.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_reminder.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_reminder.transmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.transmissiondate IS 'remindersjournalid.transmissiondate';


--
-- Name: COLUMN extraschool_reminder.reminder_file; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.reminder_file IS 'File';


--
-- Name: COLUMN extraschool_reminder.parentid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.parentid IS 'Parent';


--
-- Name: COLUMN extraschool_reminder.filename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.filename IS 'filename';


--
-- Name: COLUMN extraschool_reminder.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_reminder.amount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.amount IS 'Amount';


--
-- Name: COLUMN extraschool_reminder.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_reminder.structcom; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.structcom IS 'Structured Communication';


--
-- Name: COLUMN extraschool_reminder.schoolimplantationid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_reminder.schoolimplantationid IS 'School implantation';


--
-- Name: extraschool_reminder_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_reminder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_reminder_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_reminder_invoice_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_reminder_invoice_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_reminder_invoice_rel IS 'RELATION BETWEEN extraschool_reminder AND extraschool_invoice';


--
-- Name: extraschool_remindersjournal; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_remindersjournal (
    id integer NOT NULL,
    create_uid integer,
    term date NOT NULL,
    name character varying(80) NOT NULL,
    transmissiondate date NOT NULL,
    minamount double precision NOT NULL,
    reminders bytea,
    remindertype integer NOT NULL,
    filename character varying(16),
    oldid integer,
    activitycategoryid integer NOT NULL,
    write_date timestamp without time zone,
    create_date timestamp without time zone,
    write_uid integer
);


ALTER TABLE public.extraschool_remindersjournal OWNER TO openerp;

--
-- Name: TABLE extraschool_remindersjournal; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_remindersjournal IS 'Reminders journal';


--
-- Name: COLUMN extraschool_remindersjournal.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_remindersjournal.term; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.term IS 'Term';


--
-- Name: COLUMN extraschool_remindersjournal.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.name IS 'Name';


--
-- Name: COLUMN extraschool_remindersjournal.transmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.transmissiondate IS 'Transmission date';


--
-- Name: COLUMN extraschool_remindersjournal.minamount; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.minamount IS 'Minimum amount';


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
-- Name: COLUMN extraschool_remindersjournal.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_remindersjournal.activitycategoryid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.activitycategoryid IS 'Activity Category';


--
-- Name: COLUMN extraschool_remindersjournal.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_remindersjournal.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_remindersjournal.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindersjournal.write_uid IS 'Last Updated by';


--
-- Name: extraschool_remindersjournal_biller_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_remindersjournal_biller_rel (
    remindersjournal_id integer NOT NULL,
    biller_id integer NOT NULL
);


ALTER TABLE public.extraschool_remindersjournal_biller_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_remindersjournal_id_seq OWNER TO openerp;

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
    name character varying(50),
    write_uid integer,
    write_date timestamp without time zone,
    fees double precision,
    "order" integer,
    template character varying(50)
);


ALTER TABLE public.extraschool_remindertype OWNER TO openerp;

--
-- Name: TABLE extraschool_remindertype; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_remindertype IS 'Reminder type';


--
-- Name: COLUMN extraschool_remindertype.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_remindertype.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_remindertype.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.name IS 'name';


--
-- Name: COLUMN extraschool_remindertype.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_remindertype.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_remindertype.fees; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.fees IS 'Amount';


--
-- Name: COLUMN extraschool_remindertype."order"; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype."order" IS 'Order';


--
-- Name: COLUMN extraschool_remindertype.template; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_remindertype.template IS 'Template';


--
-- Name: extraschool_remindertype_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_remindertype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_remindertype_id_seq OWNER TO openerp;

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


ALTER TABLE public.extraschool_scheduledtasks OWNER TO openerp;

--
-- Name: TABLE extraschool_scheduledtasks; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_scheduledtasks IS 'Scheduled tasks';


--
-- Name: COLUMN extraschool_scheduledtasks.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_scheduledtasks.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_scheduledtasks.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_scheduledtasks.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_scheduledtasks.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_scheduledtasks.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_scheduledtasks.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_scheduledtasks.write_uid IS 'Last Updated by';


--
-- Name: extraschool_scheduledtasks_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_scheduledtasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_scheduledtasks_id_seq OWNER TO openerp;

--
-- Name: extraschool_scheduledtasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_scheduledtasks_id_seq OWNED BY extraschool_scheduledtasks.id;


--
-- Name: extraschool_school; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_school (
    id integer NOT NULL,
    city character varying(50),
    create_date timestamp without time zone,
    name character varying(50),
    create_uid integer,
    zipcode character varying(6),
    write_uid integer,
    street character varying(50),
    oldid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_school OWNER TO openerp;

--
-- Name: TABLE extraschool_school; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_school IS 'School';


--
-- Name: COLUMN extraschool_school.city; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.city IS 'City';


--
-- Name: COLUMN extraschool_school.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_school.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.name IS 'Name';


--
-- Name: COLUMN extraschool_school.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_school.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_school.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_school.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.street IS 'Street';


--
-- Name: COLUMN extraschool_school.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_school.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_school.write_date IS 'Last Updated on';


--
-- Name: extraschool_school_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_school_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_school_id_seq OWNER TO openerp;

--
-- Name: extraschool_school_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_school_id_seq OWNED BY extraschool_school.id;


--
-- Name: extraschool_schoolimplantation; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_schoolimplantation (
    id integer NOT NULL,
    city character varying(50),
    schoolid integer,
    create_date timestamp without time zone,
    name character varying(100),
    create_uid integer,
    zipcode character varying(6),
    write_uid integer,
    street character varying(100),
    oldid integer,
    write_date timestamp without time zone
);


ALTER TABLE public.extraschool_schoolimplantation OWNER TO openerp;

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
-- Name: COLUMN extraschool_schoolimplantation.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_schoolimplantation.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.name IS 'Name';


--
-- Name: COLUMN extraschool_schoolimplantation.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_schoolimplantation.zipcode; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.zipcode IS 'ZipCode';


--
-- Name: COLUMN extraschool_schoolimplantation.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_schoolimplantation.street; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.street IS 'Street';


--
-- Name: COLUMN extraschool_schoolimplantation.oldid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.oldid IS 'oldid';


--
-- Name: COLUMN extraschool_schoolimplantation.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_schoolimplantation.write_date IS 'Last Updated on';


--
-- Name: extraschool_schoolimplantation_id_seq; Type: SEQUENCE; Schema: public; Owner: openerp
--

CREATE SEQUENCE extraschool_schoolimplantation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.extraschool_schoolimplantation_id_seq OWNER TO openerp;

--
-- Name: extraschool_schoolimplantation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_schoolimplantation_id_seq OWNED BY extraschool_schoolimplantation.id;


--
-- Name: extraschool_smartphone; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_smartphone (
    id integer NOT NULL,
    username character varying(30),
    create_uid integer,
    qrconfig bytea,
    create_date timestamp without time zone,
    name character varying(50),
    softwareurl character varying(100),
    userpassword character varying(20),
    oldversion boolean,
    lasttransmissiondate timestamp without time zone,
    placeid integer NOT NULL,
    scanmethod character varying,
    write_uid integer,
    databasename character varying(30),
    write_date timestamp without time zone,
    qrdownload bytea,
    maxtimedelta integer,
    transfertmethod character varying,
    serveraddress character varying(50),
    transmissiontime character varying(5)
);


ALTER TABLE public.extraschool_smartphone OWNER TO openerp;

--
-- Name: TABLE extraschool_smartphone; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_smartphone IS 'Smartphone';


--
-- Name: COLUMN extraschool_smartphone.username; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.username IS 'User name';


--
-- Name: COLUMN extraschool_smartphone.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_smartphone.qrconfig; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.qrconfig IS 'QR Config';


--
-- Name: COLUMN extraschool_smartphone.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_smartphone.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.name IS 'Name';


--
-- Name: COLUMN extraschool_smartphone.softwareurl; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.softwareurl IS 'Software url';


--
-- Name: COLUMN extraschool_smartphone.userpassword; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.userpassword IS 'User password';


--
-- Name: COLUMN extraschool_smartphone.oldversion; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.oldversion IS 'Old version';


--
-- Name: COLUMN extraschool_smartphone.lasttransmissiondate; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.lasttransmissiondate IS 'Last Transmission Date';


--
-- Name: COLUMN extraschool_smartphone.placeid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.placeid IS 'Schoolcare Place';


--
-- Name: COLUMN extraschool_smartphone.scanmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.scanmethod IS 'Scan method';


--
-- Name: COLUMN extraschool_smartphone.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_smartphone.databasename; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.databasename IS 'Database name';


--
-- Name: COLUMN extraschool_smartphone.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.write_date IS 'Last Updated on';


--
-- Name: COLUMN extraschool_smartphone.qrdownload; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.qrdownload IS 'QR Download';


--
-- Name: COLUMN extraschool_smartphone.maxtimedelta; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.maxtimedelta IS 'Max time delta';


--
-- Name: COLUMN extraschool_smartphone.transfertmethod; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.transfertmethod IS 'Transfert method';


--
-- Name: COLUMN extraschool_smartphone.serveraddress; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.serveraddress IS 'Server address';


--
-- Name: COLUMN extraschool_smartphone.transmissiontime; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_smartphone.transmissiontime IS 'Transmission time';


--
-- Name: extraschool_smartphone_activitycategory_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_smartphone_activitycategory_rel (
    smartphone_id integer NOT NULL,
    activitycategory_id integer NOT NULL
);


ALTER TABLE public.extraschool_smartphone_activitycategory_rel OWNER TO openerp;

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


ALTER TABLE public.extraschool_smartphone_id_seq OWNER TO openerp;

--
-- Name: extraschool_smartphone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_smartphone_id_seq OWNED BY extraschool_smartphone.id;


--
-- Name: extraschool_taxcertificates_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_taxcertificates_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    name character varying(50),
    year character varying(4),
    write_uid integer,
    state character varying NOT NULL,
    activitycategory integer NOT NULL,
    taxcertificates bytea,
    write_date timestamp without time zone,
    parentid integer
);


ALTER TABLE public.extraschool_taxcertificates_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_taxcertificates_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_taxcertificates_wizard IS 'extraschool.taxcertificates_wizard';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.create_date IS 'Created on';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.name; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.name IS 'File Name';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.year; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.year IS 'Year';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.activitycategory; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.activitycategory IS 'Activity category';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.taxcertificates; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.taxcertificates IS 'File';


--
-- Name: COLUMN extraschool_taxcertificates_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_taxcertificates_wizard.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_taxcertificates_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_taxcertificates_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_taxcertificates_wizard_id_seq OWNED BY extraschool_taxcertificates_wizard.id;


--
-- Name: extraschool_timecorrection_wizard; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_timecorrection_wizard (
    id integer NOT NULL,
    create_uid integer,
    create_date timestamp without time zone,
    correctiontype character varying NOT NULL,
    dateto date NOT NULL,
    datefrom date NOT NULL,
    write_uid integer,
    state character varying NOT NULL,
    write_date timestamp without time zone,
    correctiontime double precision NOT NULL
);


ALTER TABLE public.extraschool_timecorrection_wizard OWNER TO openerp;

--
-- Name: TABLE extraschool_timecorrection_wizard; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_timecorrection_wizard IS 'extraschool.timecorrection_wizard';


--
-- Name: COLUMN extraschool_timecorrection_wizard.create_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.create_uid IS 'Created by';


--
-- Name: COLUMN extraschool_timecorrection_wizard.create_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.create_date IS 'Created on';


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
-- Name: COLUMN extraschool_timecorrection_wizard.write_uid; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.write_uid IS 'Last Updated by';


--
-- Name: COLUMN extraschool_timecorrection_wizard.state; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.state IS 'State';


--
-- Name: COLUMN extraschool_timecorrection_wizard.write_date; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON COLUMN extraschool_timecorrection_wizard.write_date IS 'Last Updated on';


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


ALTER TABLE public.extraschool_timecorrection_wizard_id_seq OWNER TO openerp;

--
-- Name: extraschool_timecorrection_wizard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: openerp
--

ALTER SEQUENCE extraschool_timecorrection_wizard_id_seq OWNED BY extraschool_timecorrection_wizard.id;


--
-- Name: extraschool_timecorrection_wizard_place_rel; Type: TABLE; Schema: public; Owner: openerp; Tablespace:
--

CREATE TABLE extraschool_timecorrection_wizard_place_rel (
    prestationscheck_wizard_id integer NOT NULL,
    place_id integer NOT NULL
);


ALTER TABLE public.extraschool_timecorrection_wizard_place_rel OWNER TO openerp;

--
-- Name: TABLE extraschool_timecorrection_wizard_place_rel; Type: COMMENT; Schema: public; Owner: openerp
--

COMMENT ON TABLE extraschool_timecorrection_wizard_place_rel IS 'RELATION BETWEEN extraschool_timecorrection_wizard AND extraschool_place';


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

ALTER TABLE ONLY extraschool_activityoccurrence ALTER COLUMN id SET DEFAULT nextval('extraschool_activityoccurrence_id_seq'::regclass);


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

ALTER TABLE ONLY extraschool_discount ALTER COLUMN id SET DEFAULT nextval('extraschool_discount_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_discountrule ALTER COLUMN id SET DEFAULT nextval('extraschool_discountrule_id_seq'::regclass);


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

ALTER TABLE ONLY extraschool_one_report ALTER COLUMN id SET DEFAULT nextval('extraschool_one_report_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report_day ALTER COLUMN id SET DEFAULT nextval('extraschool_one_report_day_id_seq'::regclass);


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

ALTER TABLE ONLY extraschool_prestation_times_encodage_manuel ALTER COLUMN id SET DEFAULT nextval('extraschool_prestation_times_encodage_manuel_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_manuel ALTER COLUMN id SET DEFAULT nextval('extraschool_prestation_times_manuel_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_of_the_day ALTER COLUMN id SET DEFAULT nextval('extraschool_prestation_times_of_the_day_id_seq'::regclass);


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

ALTER TABLE ONLY extraschool_price_list ALTER COLUMN id SET DEFAULT nextval('extraschool_price_list_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_price_list_version ALTER COLUMN id SET DEFAULT nextval('extraschool_price_list_version_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_qrcodes_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_qrcodes_wizard_id_seq'::regclass);


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

ALTER TABLE ONLY extraschool_taxcertificates_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_taxcertificates_wizard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard ALTER COLUMN id SET DEFAULT nextval('extraschool_timecorrection_wizard_id_seq'::regclass);


--
-- Name: extraschool_activity_activity_activity_id_activityexclusion_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activity_activityexclusiondates_rel
    ADD CONSTRAINT extraschool_activity_activity_activity_id_activityexclusion_key UNIQUE (activity_id, activityexclusiondates_id);


--
-- Name: extraschool_activity_activity_activity_id_activityplannedda_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activity_activityplanneddate_rel
    ADD CONSTRAINT extraschool_activity_activity_activity_id_activityplannedda_key UNIQUE (activity_id, activityplanneddate_id);


--
-- Name: extraschool_activity_childposi_activity_id_childposition_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activity_childposition_rel
    ADD CONSTRAINT extraschool_activity_childposi_activity_id_childposition_id_key UNIQUE (activity_id, childposition_id);


--
-- Name: extraschool_activity_childtype_rel_activity_id_childtype_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activity_childtype_rel
    ADD CONSTRAINT extraschool_activity_childtype_rel_activity_id_childtype_id_key UNIQUE (activity_id, childtype_id);


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
-- Name: extraschool_activity_schoolim_activity_id_schoolimplantatio_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activity_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activity_schoolim_activity_id_schoolimplantatio_key UNIQUE (activity_id, schoolimplantation_id);


--
-- Name: extraschool_activitycategory_p_activitycategory_id_place_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activitycategory_place_rel
    ADD CONSTRAINT extraschool_activitycategory_p_activitycategory_id_place_id_key UNIQUE (activitycategory_id, place_id);


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
-- Name: extraschool_activityoccurrenc_activityoccurrence_id_child_i_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activityoccurrence_cild_rel
    ADD CONSTRAINT extraschool_activityoccurrenc_activityoccurrence_id_child_i_key UNIQUE (activityoccurrence_id, child_id);


--
-- Name: extraschool_activityoccurrence_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_activityoccurrence
    ADD CONSTRAINT extraschool_activityoccurrence_pkey PRIMARY KEY (id);


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
-- Name: extraschool_childsimportfilte_childsimportfilter_id_importl_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_childsimportfilter_importlevelrule_rel
    ADD CONSTRAINT extraschool_childsimportfilte_childsimportfilter_id_importl_key UNIQUE (childsimportfilter_id, importlevelrule_id);


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
-- Name: extraschool_discount_activity_rel_discount_id_activity_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_discount_activity_rel
    ADD CONSTRAINT extraschool_discount_activity_rel_discount_id_activity_id_key UNIQUE (discount_id, activity_id);


--
-- Name: extraschool_discount_childtype_rel_discount_id_childtype_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_discount_childtype_rel
    ADD CONSTRAINT extraschool_discount_childtype_rel_discount_id_childtype_id_key UNIQUE (discount_id, childtype_id);


--
-- Name: extraschool_discount_discountru_discount_id_discountrule_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_discount_discountrule_rel
    ADD CONSTRAINT extraschool_discount_discountru_discount_id_discountrule_id_key UNIQUE (discount_id, discountrule_id);


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
-- Name: extraschool_invoice_wizard_sc_invoice_wizard_id_schoolimpla_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_invoice_wizard_schoolimplantation_rel
    ADD CONSTRAINT extraschool_invoice_wizard_sc_invoice_wizard_id_schoolimpla_key UNIQUE (invoice_wizard_id, schoolimplantation_id);


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
-- Name: extraschool_one_report_day_child_one_report_day_id_child_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_one_report_day_child_rel
    ADD CONSTRAINT extraschool_one_report_day_child_one_report_day_id_child_id_key UNIQUE (one_report_day_id, child_id);


--
-- Name: extraschool_one_report_day_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_one_report_day
    ADD CONSTRAINT extraschool_one_report_day_pkey PRIMARY KEY (id);


--
-- Name: extraschool_one_report_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_one_report
    ADD CONSTRAINT extraschool_one_report_pkey PRIMARY KEY (id);


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
-- Name: extraschool_place_schoolimpla_place_id_schoolimplantation_i_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_place_schoolimplantation_rel
    ADD CONSTRAINT extraschool_place_schoolimpla_place_id_schoolimplantation_i_key UNIQUE (place_id, schoolimplantation_id);


--
-- Name: extraschool_prestation_times_encodage_manuel_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_prestation_times_encodage_manuel
    ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_pkey PRIMARY KEY (id);


--
-- Name: extraschool_prestation_times_manuel_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_prestation_times_manuel
    ADD CONSTRAINT extraschool_prestation_times_manuel_pkey PRIMARY KEY (id);


--
-- Name: extraschool_prestation_times_of_the_day_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_prestation_times_of_the_day
    ADD CONSTRAINT extraschool_prestation_times_of_the_day_pkey PRIMARY KEY (id);


--
-- Name: extraschool_prestationscheck__prestationscheck_wizard_id_pl_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard_place_rel
    ADD CONSTRAINT extraschool_prestationscheck__prestationscheck_wizard_id_pl_key UNIQUE (prestationscheck_wizard_id, place_id);


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
-- Name: extraschool_price_list_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_price_list
    ADD CONSTRAINT extraschool_price_list_pkey PRIMARY KEY (id);


--
-- Name: extraschool_price_list_version_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_price_list_version
    ADD CONSTRAINT extraschool_price_list_version_pkey PRIMARY KEY (id);


--
-- Name: extraschool_qrcodes_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_qrcodes_wizard
    ADD CONSTRAINT extraschool_qrcodes_wizard_pkey PRIMARY KEY (id);


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
-- Name: extraschool_remindersjournal__remindersjournal_id_biller_id_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_remindersjournal_biller_rel
    ADD CONSTRAINT extraschool_remindersjournal__remindersjournal_id_biller_id_key UNIQUE (remindersjournal_id, biller_id);


--
-- Name: extraschool_remindersjournal_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_pkey PRIMARY KEY (id);


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
-- Name: extraschool_smartphone_activi_smartphone_id_activitycategor_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_smartphone_activitycategory_rel
    ADD CONSTRAINT extraschool_smartphone_activi_smartphone_id_activitycategor_key UNIQUE (smartphone_id, activitycategory_id);


--
-- Name: extraschool_smartphone_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_smartphone
    ADD CONSTRAINT extraschool_smartphone_pkey PRIMARY KEY (id);


--
-- Name: extraschool_taxcertificates_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_timecorrection_wi_prestationscheck_wizard_id_pl_key; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_timecorrection_wizard_place_rel
    ADD CONSTRAINT extraschool_timecorrection_wi_prestationscheck_wizard_id_pl_key UNIQUE (prestationscheck_wizard_id, place_id);


--
-- Name: extraschool_timecorrection_wizard_pkey; Type: CONSTRAINT; Schema: public; Owner: openerp; Tablespace:
--

ALTER TABLE ONLY extraschool_timecorrection_wizard
    ADD CONSTRAINT extraschool_timecorrection_wizard_pkey PRIMARY KEY (id);


--
-- Name: extraschool_activity_activityexclusiondates_rel_activity_id_ind; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activity_activityexclusiondates_rel_activity_id_ind ON extraschool_activity_activityexclusiondates_rel USING btree (activity_id);


--
-- Name: extraschool_activity_activityexclusiondates_rel_activityexclusi; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activity_activityexclusiondates_rel_activityexclusi ON extraschool_activity_activityexclusiondates_rel USING btree (activityexclusiondates_id);


--
-- Name: extraschool_activity_activityplanneddate_rel_activity_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activity_activityplanneddate_rel_activity_id_index ON extraschool_activity_activityplanneddate_rel USING btree (activity_id);


--
-- Name: extraschool_activity_activityplanneddate_rel_activityplanneddat; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activity_activityplanneddate_rel_activityplanneddat ON extraschool_activity_activityplanneddate_rel USING btree (activityplanneddate_id);


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
-- Name: extraschool_activity_schoolimplantation_rel_schoolimplantation_; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activity_schoolimplantation_rel_schoolimplantation_ ON extraschool_activity_schoolimplantation_rel USING btree (schoolimplantation_id);


--
-- Name: extraschool_activitycategory_place_rel_activitycategory_id_inde; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activitycategory_place_rel_activitycategory_id_inde ON extraschool_activitycategory_place_rel USING btree (activitycategory_id);


--
-- Name: extraschool_activitycategory_place_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activitycategory_place_rel_place_id_index ON extraschool_activitycategory_place_rel USING btree (place_id);


--
-- Name: extraschool_activityoccurrence_cild_rel_activityoccurrence_id_i; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activityoccurrence_cild_rel_activityoccurrence_id_i ON extraschool_activityoccurrence_cild_rel USING btree (activityoccurrence_id);


--
-- Name: extraschool_activityoccurrence_cild_rel_child_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_activityoccurrence_cild_rel_child_id_index ON extraschool_activityoccurrence_cild_rel USING btree (child_id);


--
-- Name: extraschool_childsimportfilter_importlevelrule_rel_childsimport; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_childsimportfilter_importlevelrule_rel_childsimport ON extraschool_childsimportfilter_importlevelrule_rel USING btree (childsimportfilter_id);


--
-- Name: extraschool_childsimportfilter_importlevelrule_rel_importlevelr; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_childsimportfilter_importlevelrule_rel_importlevelr ON extraschool_childsimportfilter_importlevelrule_rel USING btree (importlevelrule_id);


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
-- Name: extraschool_invoice_wizard_schoolimplantation_rel_invoice_wizar; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_invoice_wizard_schoolimplantation_rel_invoice_wizar ON extraschool_invoice_wizard_schoolimplantation_rel USING btree (invoice_wizard_id);


--
-- Name: extraschool_invoice_wizard_schoolimplantation_rel_schoolimplant; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_invoice_wizard_schoolimplantation_rel_schoolimplant ON extraschool_invoice_wizard_schoolimplantation_rel USING btree (schoolimplantation_id);


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
-- Name: extraschool_one_report_day_child_rel_child_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_one_report_day_child_rel_child_id_index ON extraschool_one_report_day_child_rel USING btree (child_id);


--
-- Name: extraschool_one_report_day_child_rel_one_report_day_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_one_report_day_child_rel_one_report_day_id_index ON extraschool_one_report_day_child_rel USING btree (one_report_day_id);


--
-- Name: extraschool_place_schoolimplantation_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_place_schoolimplantation_rel_place_id_index ON extraschool_place_schoolimplantation_rel USING btree (place_id);


--
-- Name: extraschool_place_schoolimplantation_rel_schoolimplantation_id_; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_place_schoolimplantation_rel_schoolimplantation_id_ ON extraschool_place_schoolimplantation_rel USING btree (schoolimplantation_id);


--
-- Name: extraschool_prestationscheck_wizard_place_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_prestationscheck_wizard_place_rel_place_id_index ON extraschool_prestationscheck_wizard_place_rel USING btree (place_id);


--
-- Name: extraschool_prestationscheck_wizard_place_rel_prestationscheck_; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_prestationscheck_wizard_place_rel_prestationscheck_ ON extraschool_prestationscheck_wizard_place_rel USING btree (prestationscheck_wizard_id);


--
-- Name: extraschool_prestationtimes_childid_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_prestationtimes_childid_index ON extraschool_prestationtimes USING btree (childid);


--
-- Name: extraschool_prestationtimes_es_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_prestationtimes_es_index ON extraschool_prestationtimes USING btree (es);


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
-- Name: extraschool_remindersjournal_biller_rel_remindersjournal_id_ind; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_remindersjournal_biller_rel_remindersjournal_id_ind ON extraschool_remindersjournal_biller_rel USING btree (remindersjournal_id);


--
-- Name: extraschool_smartphone_activitycategory_rel_activitycategory_id; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_smartphone_activitycategory_rel_activitycategory_id ON extraschool_smartphone_activitycategory_rel USING btree (activitycategory_id);


--
-- Name: extraschool_smartphone_activitycategory_rel_smartphone_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_smartphone_activitycategory_rel_smartphone_id_index ON extraschool_smartphone_activitycategory_rel USING btree (smartphone_id);


--
-- Name: extraschool_timecorrection_wizard_place_rel_place_id_index; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_timecorrection_wizard_place_rel_place_id_index ON extraschool_timecorrection_wizard_place_rel USING btree (place_id);


--
-- Name: extraschool_timecorrection_wizard_place_rel_prestationscheck_wi; Type: INDEX; Schema: public; Owner: openerp; Tablespace:
--

CREATE INDEX extraschool_timecorrection_wizard_place_rel_prestationscheck_wi ON extraschool_timecorrection_wizard_place_rel USING btree (prestationscheck_wizard_id);


--
-- Name: extraschool_activity_activityexc_activityexclusiondates_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityexclusiondates_rel
    ADD CONSTRAINT extraschool_activity_activityexc_activityexclusiondates_id_fkey FOREIGN KEY (activityexclusiondates_id) REFERENCES extraschool_activityexclusiondates(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_activityexclusiondates_re_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityexclusiondates_rel
    ADD CONSTRAINT extraschool_activity_activityexclusiondates_re_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_activity(id) ON DELETE CASCADE;


--
-- Name: extraschool_activity_activityplanne_activityplanneddate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_activityplanneddate_rel
    ADD CONSTRAINT extraschool_activity_activityplanne_activityplanneddate_id_fkey FOREIGN KEY (activityplanneddate_id) REFERENCES extraschool_activityplanneddate(id) ON DELETE CASCADE;


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
-- Name: extraschool_activity_childposition_rel_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_childposition_rel
    ADD CONSTRAINT extraschool_activity_childposition_rel_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES extraschool_discount(id) ON DELETE CASCADE;


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
-- Name: extraschool_activity_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;


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
-- Name: extraschool_activity_price_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_price_list_id_fkey FOREIGN KEY (price_list_id) REFERENCES extraschool_price_list(id) ON DELETE SET NULL;


--
-- Name: extraschool_activity_root_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity
    ADD CONSTRAINT extraschool_activity_root_id_fkey FOREIGN KEY (root_id) REFERENCES extraschool_activity(id) ON DELETE SET NULL;


--
-- Name: extraschool_activity_schoolimplantat_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activity_schoolimplantation_rel
    ADD CONSTRAINT extraschool_activity_schoolimplantat_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


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
-- Name: extraschool_activitycategory_place_rel_activitycategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory_place_rel
    ADD CONSTRAINT extraschool_activitycategory_place_rel_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


--
-- Name: extraschool_activitycategory_place_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitycategory_place_rel
    ADD CONSTRAINT extraschool_activitycategory_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


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
-- Name: extraschool_activitychildregistration_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activitychildregistration
    ADD CONSTRAINT extraschool_activitychildregistration_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;


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
-- Name: extraschool_activityoccurrence_activityid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityoccurrence
    ADD CONSTRAINT extraschool_activityoccurrence_activityid_fkey FOREIGN KEY (activityid) REFERENCES extraschool_activity(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityoccurrence_cild__activityoccurrence_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityoccurrence_cild_rel
    ADD CONSTRAINT extraschool_activityoccurrence_cild__activityoccurrence_id_fkey FOREIGN KEY (activityoccurrence_id) REFERENCES extraschool_activityoccurrence(id) ON DELETE CASCADE;


--
-- Name: extraschool_activityoccurrence_cild_rel_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityoccurrence_cild_rel
    ADD CONSTRAINT extraschool_activityoccurrence_cild_rel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE CASCADE;


--
-- Name: extraschool_activityoccurrence_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityoccurrence
    ADD CONSTRAINT extraschool_activityoccurrence_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityoccurrence_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityoccurrence
    ADD CONSTRAINT extraschool_activityoccurrence_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_activityoccurrence_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_activityoccurrence
    ADD CONSTRAINT extraschool_activityoccurrence_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


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
    ADD CONSTRAINT extraschool_child_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE RESTRICT;


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
-- Name: extraschool_childsimportfilter_impor_childsimportfilter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter_importlevelrule_rel
    ADD CONSTRAINT extraschool_childsimportfilter_impor_childsimportfilter_id_fkey FOREIGN KEY (childsimportfilter_id) REFERENCES extraschool_childsimportfilter(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsimportfilter_importle_importlevelrule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter_importlevelrule_rel
    ADD CONSTRAINT extraschool_childsimportfilter_importle_importlevelrule_id_fkey FOREIGN KEY (importlevelrule_id) REFERENCES extraschool_importlevelrule(id) ON DELETE CASCADE;


--
-- Name: extraschool_childsimportfilter_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsimportfilter
    ADD CONSTRAINT extraschool_childsimportfilter_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsworkbook_wizard_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsworkbook_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_childsworkbook_wizard_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_childsworkbook_wizard
    ADD CONSTRAINT extraschool_childsworkbook_wizard_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;


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
    ADD CONSTRAINT extraschool_guardianprestationtimes_wizard_guardianid_fkey FOREIGN KEY (guardianid) REFERENCES extraschool_guardian(id) ON DELETE SET NULL;


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
    ADD CONSTRAINT extraschool_invoice_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard
    ADD CONSTRAINT extraschool_invoice_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_invoice_wizard_schoolimp_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard_schoolimplantation_rel
    ADD CONSTRAINT extraschool_invoice_wizard_schoolimp_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_invoice_wizard_schoolimplant_invoice_wizard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_invoice_wizard_schoolimplantation_rel
    ADD CONSTRAINT extraschool_invoice_wizard_schoolimplant_invoice_wizard_id_fkey FOREIGN KEY (invoice_wizard_id) REFERENCES extraschool_invoice_wizard(id) ON DELETE CASCADE;


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
-- Name: extraschool_mainsettings_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_mainsettings
    ADD CONSTRAINT extraschool_mainsettings_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_one_report_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report
    ADD CONSTRAINT extraschool_one_report_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_one_report_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report
    ADD CONSTRAINT extraschool_one_report_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_one_report_day_child_rel_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report_day_child_rel
    ADD CONSTRAINT extraschool_one_report_day_child_rel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE CASCADE;


--
-- Name: extraschool_one_report_day_child_rel_one_report_day_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report_day_child_rel
    ADD CONSTRAINT extraschool_one_report_day_child_rel_one_report_day_id_fkey FOREIGN KEY (one_report_day_id) REFERENCES extraschool_one_report_day(id) ON DELETE CASCADE;


--
-- Name: extraschool_one_report_day_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report_day
    ADD CONSTRAINT extraschool_one_report_day_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_one_report_day_one_report_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report_day
    ADD CONSTRAINT extraschool_one_report_day_one_report_id_fkey FOREIGN KEY (one_report_id) REFERENCES extraschool_one_report(id) ON DELETE CASCADE;


--
-- Name: extraschool_one_report_day_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report_day
    ADD CONSTRAINT extraschool_one_report_day_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_one_report_placeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report
    ADD CONSTRAINT extraschool_one_report_placeid_fkey FOREIGN KEY (placeid) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_one_report_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_one_report
    ADD CONSTRAINT extraschool_one_report_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


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
-- Name: extraschool_pdaprestationtime_prestation_times_of_the_day__fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_pdaprestationtimes
    ADD CONSTRAINT extraschool_pdaprestationtime_prestation_times_of_the_day__fkey FOREIGN KEY (prestation_times_of_the_day_id) REFERENCES extraschool_prestation_times_of_the_day(id) ON DELETE SET NULL;


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
-- Name: extraschool_place_schoolimplantation_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place_schoolimplantation_rel
    ADD CONSTRAINT extraschool_place_schoolimplantation_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_place_schoolimplantation_schoolimplantation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place_schoolimplantation_rel
    ADD CONSTRAINT extraschool_place_schoolimplantation_schoolimplantation_id_fkey FOREIGN KEY (schoolimplantation_id) REFERENCES extraschool_schoolimplantation(id) ON DELETE CASCADE;


--
-- Name: extraschool_place_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_place
    ADD CONSTRAINT extraschool_place_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times__prestation_times_encodage_ma_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_manuel
    ADD CONSTRAINT extraschool_prestation_times__prestation_times_encodage_ma_fkey FOREIGN KEY (prestation_times_encodage_manuel_id) REFERENCES extraschool_prestation_times_encodage_manuel(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_encodage_manuel_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_encodage_manuel
    ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_encodage_manuel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_encodage_manuel
    ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_encodage_manuel_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_encodage_manuel
    ADD CONSTRAINT extraschool_prestation_times_encodage_manuel_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_manuel_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_manuel
    ADD CONSTRAINT extraschool_prestation_times_manuel_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_manuel_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_manuel
    ADD CONSTRAINT extraschool_prestation_times_manuel_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_manuel_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_manuel
    ADD CONSTRAINT extraschool_prestation_times_manuel_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_of_the_day_child_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_of_the_day
    ADD CONSTRAINT extraschool_prestation_times_of_the_day_child_id_fkey FOREIGN KEY (child_id) REFERENCES extraschool_child(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_of_the_day_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_of_the_day
    ADD CONSTRAINT extraschool_prestation_times_of_the_day_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestation_times_of_the_day_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestation_times_of_the_day
    ADD CONSTRAINT extraschool_prestation_times_of_the_day_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationscheck_wi_prestationscheck_wizard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard_place_rel
    ADD CONSTRAINT extraschool_prestationscheck_wi_prestationscheck_wizard_id_fkey FOREIGN KEY (prestationscheck_wizard_id) REFERENCES extraschool_prestationscheck_wizard(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestationscheck_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationscheck_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationscheck_wizard_place_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard_place_rel
    ADD CONSTRAINT extraschool_prestationscheck_wizard_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_prestationscheck_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationscheck_wizard
    ADD CONSTRAINT extraschool_prestationscheck_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_activity_occurrence_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_activity_occurrence_id_fkey FOREIGN KEY (activity_occurrence_id) REFERENCES extraschool_activityoccurrence(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_childid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_childid_fkey FOREIGN KEY (childid) REFERENCES extraschool_child(id) ON DELETE RESTRICT;


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
-- Name: extraschool_prestationtimes_prestation_times_of_the_day_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_prestation_times_of_the_day_id_fkey FOREIGN KEY (prestation_times_of_the_day_id) REFERENCES extraschool_prestation_times_of_the_day(id) ON DELETE SET NULL;


--
-- Name: extraschool_prestationtimes_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_prestationtimes
    ADD CONSTRAINT extraschool_prestationtimes_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_price_list_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_price_list
    ADD CONSTRAINT extraschool_price_list_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_price_list_version_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_price_list_version
    ADD CONSTRAINT extraschool_price_list_version_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_price_list_version_price_list_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_price_list_version
    ADD CONSTRAINT extraschool_price_list_version_price_list_id_fkey FOREIGN KEY (price_list_id) REFERENCES extraschool_price_list(id) ON DELETE SET NULL;


--
-- Name: extraschool_price_list_version_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_price_list_version
    ADD CONSTRAINT extraschool_price_list_version_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_price_list_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_price_list
    ADD CONSTRAINT extraschool_price_list_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


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
-- Name: extraschool_remindersjournal_activitycategoryid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal
    ADD CONSTRAINT extraschool_remindersjournal_activitycategoryid_fkey FOREIGN KEY (activitycategoryid) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_remindersjournal_biller_re_remindersjournal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_remindersjournal_biller_rel
    ADD CONSTRAINT extraschool_remindersjournal_biller_re_remindersjournal_id_fkey FOREIGN KEY (remindersjournal_id) REFERENCES extraschool_remindersjournal(id) ON DELETE CASCADE;


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
-- Name: extraschool_smartphone_activitycategor_activitycategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone_activitycategory_rel
    ADD CONSTRAINT extraschool_smartphone_activitycategor_activitycategory_id_fkey FOREIGN KEY (activitycategory_id) REFERENCES extraschool_activitycategory(id) ON DELETE CASCADE;


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
-- Name: extraschool_smartphone_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_smartphone
    ADD CONSTRAINT extraschool_smartphone_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_taxcertificates_wizard_activitycategory_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_activitycategory_fkey FOREIGN KEY (activitycategory) REFERENCES extraschool_activitycategory(id) ON DELETE SET NULL;


--
-- Name: extraschool_taxcertificates_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_taxcertificates_wizard_parentid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_parentid_fkey FOREIGN KEY (parentid) REFERENCES extraschool_parent(id) ON DELETE SET NULL;


--
-- Name: extraschool_taxcertificates_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_taxcertificates_wizard
    ADD CONSTRAINT extraschool_taxcertificates_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_timecorrection_wiza_prestationscheck_wizard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard_place_rel
    ADD CONSTRAINT extraschool_timecorrection_wiza_prestationscheck_wizard_id_fkey FOREIGN KEY (prestationscheck_wizard_id) REFERENCES extraschool_timecorrection_wizard(id) ON DELETE CASCADE;


--
-- Name: extraschool_timecorrection_wizard_create_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard
    ADD CONSTRAINT extraschool_timecorrection_wizard_create_uid_fkey FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- Name: extraschool_timecorrection_wizard_place_rel_place_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard_place_rel
    ADD CONSTRAINT extraschool_timecorrection_wizard_place_rel_place_id_fkey FOREIGN KEY (place_id) REFERENCES extraschool_place(id) ON DELETE CASCADE;


--
-- Name: extraschool_timecorrection_wizard_write_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: openerp
--

ALTER TABLE ONLY extraschool_timecorrection_wizard
    ADD CONSTRAINT extraschool_timecorrection_wizard_write_uid_fkey FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

