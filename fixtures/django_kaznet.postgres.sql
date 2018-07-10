--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Ubuntu 10.4-2.pgdg16.04+1)
-- Dumped by pg_dump version 10.4 (Ubuntu 10.4-2.pgdg16.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.account_emailaddress OWNER TO postgres;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_emailaddress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailaddress_id_seq OWNER TO postgres;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_emailaddress_id_seq OWNED BY public.account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE public.account_emailconfirmation OWNER TO postgres;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_emailconfirmation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailconfirmation_id_seq OWNER TO postgres;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_emailconfirmation_id_seq OWNED BY public.account_emailconfirmation.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: main_bounty; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_bounty (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    amount numeric(64,2) NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.main_bounty OWNER TO postgres;

--
-- Name: main_bounty_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_bounty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_bounty_id_seq OWNER TO postgres;

--
-- Name: main_bounty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_bounty_id_seq OWNED BY public.main_bounty.id;


--
-- Name: main_client; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_client (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.main_client OWNER TO postgres;

--
-- Name: main_client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_client_id_seq OWNER TO postgres;

--
-- Name: main_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_client_id_seq OWNED BY public.main_client.id;


--
-- Name: main_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_location (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    country character varying(2) NOT NULL,
    geopoint public.geometry(Point,4326),
    radius numeric(64,4),
    shapefile public.geometry(MultiPolygon,4326),
    description text NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    location_type_id integer,
    parent_id integer,
    CONSTRAINT main_location_level_check CHECK ((level >= 0)),
    CONSTRAINT main_location_lft_check CHECK ((lft >= 0)),
    CONSTRAINT main_location_rght_check CHECK ((rght >= 0)),
    CONSTRAINT main_location_tree_id_check CHECK ((tree_id >= 0))
);


ALTER TABLE public.main_location OWNER TO postgres;

--
-- Name: main_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_location_id_seq OWNER TO postgres;

--
-- Name: main_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_location_id_seq OWNED BY public.main_location.id;


--
-- Name: main_locationtype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_locationtype (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.main_locationtype OWNER TO postgres;

--
-- Name: main_locationtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_locationtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_locationtype_id_seq OWNER TO postgres;

--
-- Name: main_locationtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_locationtype_id_seq OWNED BY public.main_locationtype.id;


--
-- Name: main_project; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_project (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    target_object_id integer,
    name character varying(255) NOT NULL,
    target_content_type_id integer,
    CONSTRAINT main_project_target_object_id_check CHECK ((target_object_id >= 0))
);


ALTER TABLE public.main_project OWNER TO postgres;

--
-- Name: main_project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_project_id_seq OWNER TO postgres;

--
-- Name: main_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_project_id_seq OWNED BY public.main_project.id;


--
-- Name: main_project_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_project_tasks (
    id integer NOT NULL,
    project_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.main_project_tasks OWNER TO postgres;

--
-- Name: main_project_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_project_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_project_tasks_id_seq OWNER TO postgres;

--
-- Name: main_project_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_project_tasks_id_seq OWNED BY public.main_project_tasks.id;


--
-- Name: main_segmentrule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_segmentrule (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    target_field character varying(255) NOT NULL,
    target_field_value character varying(255) NOT NULL,
    active boolean NOT NULL,
    target_content_type_id integer
);


ALTER TABLE public.main_segmentrule OWNER TO postgres;

--
-- Name: main_segmentrule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_segmentrule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_segmentrule_id_seq OWNER TO postgres;

--
-- Name: main_segmentrule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_segmentrule_id_seq OWNED BY public.main_segmentrule.id;


--
-- Name: main_submission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_submission (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    target_object_id integer,
    submission_time timestamp with time zone NOT NULL,
    valid boolean NOT NULL,
    status character varying(1) NOT NULL,
    comments text NOT NULL,
    bounty_id integer,
    location_id integer,
    target_content_type_id integer,
    task_id integer NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT main_submission_target_object_id_check CHECK ((target_object_id >= 0))
);


ALTER TABLE public.main_submission OWNER TO postgres;

--
-- Name: main_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_submission_id_seq OWNER TO postgres;

--
-- Name: main_submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_submission_id_seq OWNED BY public.main_submission.id;


--
-- Name: main_task; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_task (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    target_object_id integer,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    start timestamp with time zone NOT NULL,
    "end" timestamp with time zone,
    timing_rule text,
    total_submission_target integer,
    user_submission_target integer,
    status character varying(1) NOT NULL,
    estimated_time interval,
    required_expertise character varying(1) NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    client_id integer,
    created_by_id integer,
    parent_id integer,
    target_content_type_id integer,
    CONSTRAINT main_task_level_check CHECK ((level >= 0)),
    CONSTRAINT main_task_lft_check CHECK ((lft >= 0)),
    CONSTRAINT main_task_rght_check CHECK ((rght >= 0)),
    CONSTRAINT main_task_target_object_id_check CHECK ((target_object_id >= 0)),
    CONSTRAINT main_task_tree_id_check CHECK ((tree_id >= 0))
);


ALTER TABLE public.main_task OWNER TO postgres;

--
-- Name: main_task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_task_id_seq OWNER TO postgres;

--
-- Name: main_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_task_id_seq OWNED BY public.main_task.id;


--
-- Name: main_task_segment_rules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_task_segment_rules (
    id integer NOT NULL,
    task_id integer NOT NULL,
    segmentrule_id integer NOT NULL
);


ALTER TABLE public.main_task_segment_rules OWNER TO postgres;

--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_task_segment_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_task_segment_rules_id_seq OWNER TO postgres;

--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_task_segment_rules_id_seq OWNED BY public.main_task_segment_rules.id;


--
-- Name: main_tasklocation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_tasklocation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    timing_rule text NOT NULL,
    start time without time zone NOT NULL,
    "end" time without time zone NOT NULL,
    location_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.main_tasklocation OWNER TO postgres;

--
-- Name: main_tasklocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_tasklocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_tasklocation_id_seq OWNER TO postgres;

--
-- Name: main_tasklocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_tasklocation_id_seq OWNED BY public.main_tasklocation.id;


--
-- Name: main_taskoccurrence; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_taskoccurrence (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.main_taskoccurrence OWNER TO postgres;

--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_taskoccurrence_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_taskoccurrence_id_seq OWNER TO postgres;

--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_taskoccurrence_id_seq OWNED BY public.main_taskoccurrence.id;


--
-- Name: ona_instance; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ona_instance (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    ona_pk integer NOT NULL,
    json jsonb NOT NULL,
    deleted_at timestamp with time zone,
    last_updated timestamp with time zone,
    user_id integer NOT NULL,
    xform_id integer NOT NULL,
    CONSTRAINT ona_instance_ona_pk_check CHECK ((ona_pk >= 0))
);


ALTER TABLE public.ona_instance OWNER TO postgres;

--
-- Name: ona_instance_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ona_instance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ona_instance_id_seq OWNER TO postgres;

--
-- Name: ona_instance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ona_instance_id_seq OWNED BY public.ona_instance.id;


--
-- Name: ona_project; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ona_project (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    ona_pk integer NOT NULL,
    organization integer,
    name character varying(255) NOT NULL,
    deleted_at timestamp with time zone,
    last_updated timestamp with time zone,
    CONSTRAINT ona_project_ona_pk_check CHECK ((ona_pk >= 0)),
    CONSTRAINT ona_project_organization_check CHECK ((organization >= 0))
);


ALTER TABLE public.ona_project OWNER TO postgres;

--
-- Name: ona_project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ona_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ona_project_id_seq OWNER TO postgres;

--
-- Name: ona_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ona_project_id_seq OWNED BY public.ona_project.id;


--
-- Name: ona_xform; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ona_xform (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    ona_pk integer NOT NULL,
    project_id integer NOT NULL,
    title character varying(255) NOT NULL,
    id_string character varying(100) NOT NULL,
    deleted_at timestamp with time zone,
    last_updated timestamp with time zone,
    CONSTRAINT ona_xform_ona_pk_check CHECK ((ona_pk >= 0)),
    CONSTRAINT ona_xform_project_id_check CHECK ((project_id >= 0))
);


ALTER TABLE public.ona_xform OWNER TO postgres;

--
-- Name: ona_xform_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ona_xform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ona_xform_id_seq OWNER TO postgres;

--
-- Name: ona_xform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ona_xform_id_seq OWNED BY public.ona_xform.id;


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialaccount (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    uid character varying(191) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    extra_data text NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialaccount OWNER TO postgres;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.socialaccount_socialaccount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialaccount_id_seq OWNER TO postgres;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.socialaccount_socialaccount_id_seq OWNED BY public.socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL
);


ALTER TABLE public.socialaccount_socialapp OWNER TO postgres;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.socialaccount_socialapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialapp_id_seq OWNER TO postgres;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.socialaccount_socialapp_id_seq OWNED BY public.socialaccount_socialapp.id;


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialapp_sites (
    id integer NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialapp_sites OWNER TO postgres;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.socialaccount_socialapp_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialapp_sites_id_seq OWNER TO postgres;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.socialaccount_socialapp_sites_id_seq OWNED BY public.socialaccount_socialapp_sites.id;


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialtoken OWNER TO postgres;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.socialaccount_socialtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialtoken_id_seq OWNER TO postgres;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.socialaccount_socialtoken_id_seq OWNED BY public.socialaccount_socialtoken.id;


--
-- Name: users_userprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_userprofile (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    ona_pk integer,
    ona_username character varying(255),
    national_id character varying(255),
    payment_number character varying(128) NOT NULL,
    phone_number character varying(128) NOT NULL,
    role character varying(1) NOT NULL,
    expertise character varying(1) NOT NULL,
    gender character varying(1) NOT NULL,
    user_id integer NOT NULL,
    CONSTRAINT users_userprofile_ona_pk_check CHECK ((ona_pk >= 0))
);


ALTER TABLE public.users_userprofile OWNER TO postgres;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_userprofile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_userprofile_id_seq OWNER TO postgres;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_userprofile_id_seq OWNED BY public.users_userprofile.id;


--
-- Name: account_emailaddress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress ALTER COLUMN id SET DEFAULT nextval('public.account_emailaddress_id_seq'::regclass);


--
-- Name: account_emailconfirmation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('public.account_emailconfirmation_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: main_bounty id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_bounty ALTER COLUMN id SET DEFAULT nextval('public.main_bounty_id_seq'::regclass);


--
-- Name: main_client id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_client ALTER COLUMN id SET DEFAULT nextval('public.main_client_id_seq'::regclass);


--
-- Name: main_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_location ALTER COLUMN id SET DEFAULT nextval('public.main_location_id_seq'::regclass);


--
-- Name: main_locationtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_locationtype ALTER COLUMN id SET DEFAULT nextval('public.main_locationtype_id_seq'::regclass);


--
-- Name: main_project id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project ALTER COLUMN id SET DEFAULT nextval('public.main_project_id_seq'::regclass);


--
-- Name: main_project_tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project_tasks ALTER COLUMN id SET DEFAULT nextval('public.main_project_tasks_id_seq'::regclass);


--
-- Name: main_segmentrule id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_segmentrule ALTER COLUMN id SET DEFAULT nextval('public.main_segmentrule_id_seq'::regclass);


--
-- Name: main_submission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission ALTER COLUMN id SET DEFAULT nextval('public.main_submission_id_seq'::regclass);


--
-- Name: main_task id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task ALTER COLUMN id SET DEFAULT nextval('public.main_task_id_seq'::regclass);


--
-- Name: main_task_segment_rules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_segment_rules ALTER COLUMN id SET DEFAULT nextval('public.main_task_segment_rules_id_seq'::regclass);


--
-- Name: main_tasklocation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tasklocation ALTER COLUMN id SET DEFAULT nextval('public.main_tasklocation_id_seq'::regclass);


--
-- Name: main_taskoccurrence id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_taskoccurrence ALTER COLUMN id SET DEFAULT nextval('public.main_taskoccurrence_id_seq'::regclass);


--
-- Name: ona_instance id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_instance ALTER COLUMN id SET DEFAULT nextval('public.ona_instance_id_seq'::regclass);


--
-- Name: ona_project id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_project ALTER COLUMN id SET DEFAULT nextval('public.ona_project_id_seq'::regclass);


--
-- Name: ona_xform id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_xform ALTER COLUMN id SET DEFAULT nextval('public.ona_xform_id_seq'::regclass);


--
-- Name: socialaccount_socialaccount id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: socialaccount_socialapp id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_id_seq'::regclass);


--
-- Name: socialaccount_socialapp_sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_sites_id_seq'::regclass);


--
-- Name: socialaccount_socialtoken id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialtoken_id_seq'::regclass);


--
-- Name: users_userprofile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile ALTER COLUMN id SET DEFAULT nextval('public.users_userprofile_id_seq'::regclass);


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
\.


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add Token	8	add_token
23	Can change Token	8	change_token
24	Can delete Token	8	delete_token
25	Can add email address	9	add_emailaddress
26	Can change email address	9	change_emailaddress
27	Can delete email address	9	delete_emailaddress
28	Can add email confirmation	10	add_emailconfirmation
29	Can change email confirmation	10	change_emailconfirmation
30	Can delete email confirmation	10	delete_emailconfirmation
31	Can add social account	11	add_socialaccount
32	Can change social account	11	change_socialaccount
33	Can delete social account	11	delete_socialaccount
34	Can add social application	12	add_socialapp
35	Can change social application	12	change_socialapp
36	Can delete social application	12	delete_socialapp
37	Can add social application token	13	add_socialtoken
38	Can change social application token	13	change_socialtoken
39	Can delete social application token	13	delete_socialtoken
40	Can add instance	14	add_instance
41	Can change instance	14	change_instance
42	Can delete instance	14	delete_instance
43	Can add project	15	add_project
44	Can change project	15	change_project
45	Can delete project	15	delete_project
46	Can add x form	16	add_xform
47	Can change x form	16	change_xform
48	Can delete x form	16	delete_xform
49	Can add Bounty	17	add_bounty
50	Can change Bounty	17	change_bounty
51	Can delete Bounty	17	delete_bounty
52	Can add Client	18	add_client
53	Can change Client	18	change_client
54	Can delete Client	18	delete_client
55	Can add location	19	add_location
56	Can change location	19	change_location
57	Can delete location	19	delete_location
58	Can add location type	20	add_locationtype
59	Can change location type	20	change_locationtype
60	Can delete location type	20	delete_locationtype
61	Can add project	21	add_project
62	Can change project	21	change_project
63	Can delete project	21	delete_project
64	Can add segment rule	22	add_segmentrule
65	Can change segment rule	22	change_segmentrule
66	Can delete segment rule	22	delete_segmentrule
67	Can add submission	23	add_submission
68	Can change submission	23	change_submission
69	Can delete submission	23	delete_submission
70	Can add task	24	add_task
71	Can change task	24	change_task
72	Can delete task	24	delete_task
73	Can add task occurrence	25	add_taskoccurrence
74	Can change task occurrence	25	change_taskoccurrence
75	Can delete task occurrence	25	delete_taskoccurrence
76	Can add Profile	26	add_userprofile
77	Can change Profile	26	change_userprofile
78	Can delete Profile	26	delete_userprofile
79	Can add task location	27	add_tasklocation
80	Can change task location	27	change_tasklocation
81	Can delete task location	27	delete_tasklocation
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$100000$crp64mZ83aj6$UVR//QS5Kr6IfzfvuuzGT3cO2CwSqgKzYLgZDlwqlXw=	2018-06-27 15:06:45+03	t	sol	Davis	Raymond	sol@admin.me	t	t	2018-06-27 15:06:29+03
3	pbkdf2_sha256$100000$2HvAPzjGkoLV$I9B4K2gWlrgO5XXdy3J4yrq7JYohbztJ8+XRsmPXRsk=	2018-07-02 13:13:52.082403+03	t	onauser	Ona	User		t	t	2018-06-27 15:08:09+03
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
afba84d36d7279ac1f104ddbfbea348a36779610	2018-06-27 15:06:29.129617+03	1
3164da5d8e34b52370e426065b8d42ed3c992424	2018-06-27 15:08:09.535924+03	3
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2018-06-27 15:07:19.197116+03	1	sol	2	[{"changed": {"fields": ["first_name", "last_name"]}}, {"changed": {"name": "Profile", "object": "Davis Raymond's profile", "fields": ["role", "expertise", "gender"]}}]	4	1
2	2018-06-27 15:10:20.057318+03	3	onauser	2	[{"changed": {"fields": ["first_name", "last_name"]}}, {"changed": {"name": "Profile", "object": "Ona User's profile", "fields": ["ona_username", "expertise"]}}]	4	1
3	2018-06-27 15:11:39.655205+03	3	onauser	2	[{"changed": {"fields": ["is_superuser"]}}]	4	1
4	2018-06-27 15:15:45.748612+03	1	Client1	1	[{"added": {}}]	18	1
5	2018-06-27 15:15:48.470108+03	2	Client2	1	[{"added": {}}]	18	1
6	2018-06-27 15:15:50.790354+03	3	Client3	1	[{"added": {}}]	18	1
7	2018-06-27 15:15:53.416615+03	4	Client4	1	[{"added": {}}]	18	1
8	2018-06-27 15:15:55.692602+03	5	Client5	1	[{"added": {}}]	18	1
9	2018-06-27 15:15:57.986943+03	6	Client6	1	[{"added": {}}]	18	1
10	2018-06-27 15:16:01.765612+03	7	Client7	1	[{"added": {}}]	18	1
11	2018-06-27 15:16:21.872052+03	8	Client8	1	[{"added": {}}]	18	1
12	2018-06-27 15:16:26.644547+03	9	Client9	1	[{"added": {}}]	18	1
13	2018-06-27 15:16:29.471802+03	10	Client10	1	[{"added": {}}]	18	1
14	2018-06-27 15:20:47.059059+03	1	City	1	[{"added": {}}]	20	1
15	2018-06-27 15:20:48.292224+03	1	Kenya - Nairobi	1	[{"added": {}}]	19	1
16	2018-06-27 15:21:52.161206+03	2	Area	1	[{"added": {}}]	20	1
17	2018-06-27 15:21:53.639094+03	2	Kenya - Hurlingham	1	[{"added": {}}]	19	1
18	2018-07-05 13:40:30.148576+03	1	X - 1	2	[{"changed": {"fields": ["created_by"]}}]	24	3
19	2018-07-05 15:22:14.740782+03	1	X - 1	2	[{"changed": {"fields": ["target_object_id"]}}]	24	3
20	2018-07-05 15:23:01.310989+03	1	Task 1 bounty is Money('245', 'KES')	1	[{"added": {}}]	17	3
21	2018-07-09 15:08:56.331232+03	1	Awful Task - 1	2	[{"changed": {"fields": ["created_by"]}}]	24	3
22	2018-07-09 15:09:03.045265+03	2	Coconut Quest - 2	2	[{"changed": {"fields": ["created_by"]}}]	24	3
23	2018-07-09 15:09:10.702972+03	3	Livestock Prices - 3	2	[{"changed": {"fields": ["created_by"]}}]	24	3
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	sites	site
8	authtoken	token
9	account	emailaddress
10	account	emailconfirmation
11	socialaccount	socialaccount
12	socialaccount	socialapp
13	socialaccount	socialtoken
14	ona	instance
15	ona	project
16	ona	xform
17	main	bounty
18	main	client
19	main	location
20	main	locationtype
21	main	project
22	main	segmentrule
23	main	submission
24	main	task
25	main	taskoccurrence
26	users	userprofile
27	main	tasklocation
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2018-06-27 15:05:55.526718+03
2	auth	0001_initial	2018-06-27 15:05:55.731891+03
3	account	0001_initial	2018-06-27 15:05:55.806967+03
4	account	0002_email_max_length	2018-06-27 15:05:55.82171+03
5	admin	0001_initial	2018-06-27 15:05:55.869201+03
6	admin	0002_logentry_remove_auto_add	2018-06-27 15:05:55.880149+03
7	contenttypes	0002_remove_content_type_name	2018-06-27 15:05:55.907388+03
8	auth	0002_alter_permission_name_max_length	2018-06-27 15:05:55.917147+03
9	auth	0003_alter_user_email_max_length	2018-06-27 15:05:55.930395+03
10	auth	0004_alter_user_username_opts	2018-06-27 15:05:55.942825+03
11	auth	0005_alter_user_last_login_null	2018-06-27 15:05:55.956964+03
12	auth	0006_require_contenttypes_0002	2018-06-27 15:05:55.960248+03
13	auth	0007_alter_validators_add_error_messages	2018-06-27 15:05:55.974415+03
14	auth	0008_alter_user_username_max_length	2018-06-27 15:05:56.01311+03
15	auth	0009_alter_user_last_name_max_length	2018-06-27 15:05:56.027231+03
16	authtoken	0001_initial	2018-06-27 15:05:56.070314+03
17	authtoken	0002_auto_20160226_1747	2018-06-27 15:05:56.121084+03
19	ona	0001_initial	2018-06-27 15:05:56.96471+03
20	sessions	0001_initial	2018-06-27 15:05:56.994692+03
21	sites	0001_initial	2018-06-27 15:05:57.008801+03
22	sites	0002_alter_domain_unique	2018-06-27 15:05:57.027277+03
23	socialaccount	0001_initial	2018-06-27 15:05:57.195465+03
24	socialaccount	0002_token_max_lengths	2018-06-27 15:05:57.285625+03
25	socialaccount	0003_extra_data_default_dict	2018-06-27 15:05:57.296713+03
26	users	0001_initial	2018-06-27 15:05:57.40772+03
30	main	0001_initial	2018-07-09 11:34:49.964286+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
feaqmcs1cob55jw2dsb425dj1g8k2typ	YWY4Y2Y3MzgzZWZhMzk5N2Q3OTc1MjlmYmVjMGE2ZWFmODgwY2NlNjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NTEwY2ZkNTg2NmYzYzc0Njc1ODY5OWY5ZGM2MTE0YjNlOGMxMDVhIn0=	2018-07-11 15:06:45.651222+03
f92eagj70yksg1yv0px13czt4uaqik0y	ZGU2YzBlZDZiNzEwMmI1YmY2MGZhOTQxNGEyNTY0MmVmMzcxMzA2NDp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxNDJkMDdmMjIzZGYzMTMwYjIzODExNGJlYjRiNjE5ZTcyNDgyYWI1In0=	2018-07-16 13:13:52.098934+03
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: main_bounty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_bounty (id, created, amount, task_id) FROM stdin;
\.


--
-- Data for Name: main_client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_client (id, created, modified, name) FROM stdin;
1	2018-07-09 14:54:06.584747+03	2018-07-09 14:54:06.584794+03	Knights Order
2	2018-07-10 18:05:24.418356+03	2018-07-10 18:05:24.418388+03	Client 1
3	2018-07-10 18:05:24.421049+03	2018-07-10 18:05:24.421073+03	Client 2
4	2018-07-10 18:05:24.423091+03	2018-07-10 18:05:24.423113+03	Client 3
5	2018-07-10 18:05:24.425088+03	2018-07-10 18:05:24.425111+03	Client 4
6	2018-07-10 18:05:24.42715+03	2018-07-10 18:05:24.427171+03	Client 5
7	2018-07-10 18:05:24.428933+03	2018-07-10 18:05:24.428953+03	Client 6
8	2018-07-10 18:05:24.430716+03	2018-07-10 18:05:24.430736+03	Client 7
9	2018-07-10 18:05:24.432437+03	2018-07-10 18:05:24.432456+03	Client 8
10	2018-07-10 18:05:24.433945+03	2018-07-10 18:05:24.433964+03	Client 9
11	2018-07-10 18:05:24.435446+03	2018-07-10 18:05:24.435466+03	Client 10
12	2018-07-10 18:05:24.43704+03	2018-07-10 18:05:24.437069+03	Client 11
13	2018-07-10 18:05:24.439012+03	2018-07-10 18:05:24.439049+03	Client 12
14	2018-07-10 18:05:24.442915+03	2018-07-10 18:05:24.442991+03	Client 13
15	2018-07-10 18:05:24.444956+03	2018-07-10 18:05:24.444981+03	Client 14
16	2018-07-10 18:05:24.446758+03	2018-07-10 18:05:24.446778+03	Client 15
17	2018-07-10 18:05:24.44856+03	2018-07-10 18:05:24.448581+03	Client 16
18	2018-07-10 18:05:24.450342+03	2018-07-10 18:05:24.450362+03	Client 17
19	2018-07-10 18:05:24.451888+03	2018-07-10 18:05:24.451907+03	Client 18
20	2018-07-10 18:05:24.453682+03	2018-07-10 18:05:24.453702+03	Client 19
21	2018-07-10 18:05:24.455477+03	2018-07-10 18:05:24.455497+03	Client 20
22	2018-07-10 18:05:24.457282+03	2018-07-10 18:05:24.457303+03	Client 21
23	2018-07-10 18:05:24.45907+03	2018-07-10 18:05:24.45909+03	Client 22
24	2018-07-10 18:05:24.460794+03	2018-07-10 18:05:24.460813+03	Client 23
25	2018-07-10 18:05:24.462557+03	2018-07-10 18:05:24.462594+03	Client 24
26	2018-07-10 18:05:24.465097+03	2018-07-10 18:05:24.465125+03	Client 25
27	2018-07-10 18:05:24.466739+03	2018-07-10 18:05:24.46676+03	Client 26
28	2018-07-10 18:05:24.468208+03	2018-07-10 18:05:24.468227+03	Client 27
29	2018-07-10 18:05:24.469704+03	2018-07-10 18:05:24.469723+03	Client 28
30	2018-07-10 18:05:24.471078+03	2018-07-10 18:05:24.471097+03	Client 29
31	2018-07-10 18:05:24.472465+03	2018-07-10 18:05:24.472485+03	Client 30
32	2018-07-10 18:05:24.47398+03	2018-07-10 18:05:24.473999+03	Client 31
33	2018-07-10 18:05:24.47546+03	2018-07-10 18:05:24.475478+03	Client 32
34	2018-07-10 18:05:24.476992+03	2018-07-10 18:05:24.477011+03	Client 33
35	2018-07-10 18:05:24.478669+03	2018-07-10 18:05:24.478688+03	Client 34
36	2018-07-10 18:05:24.480174+03	2018-07-10 18:05:24.480193+03	Client 35
37	2018-07-10 18:05:24.48156+03	2018-07-10 18:05:24.481579+03	Client 36
38	2018-07-10 18:05:24.48346+03	2018-07-10 18:05:24.483507+03	Client 37
39	2018-07-10 18:05:24.485907+03	2018-07-10 18:05:24.485965+03	Client 38
40	2018-07-10 18:05:24.488383+03	2018-07-10 18:05:24.488424+03	Client 39
41	2018-07-10 18:05:24.490735+03	2018-07-10 18:05:24.490777+03	Client 40
42	2018-07-10 18:05:24.493062+03	2018-07-10 18:05:24.493104+03	Client 41
43	2018-07-10 18:05:24.495289+03	2018-07-10 18:05:24.495331+03	Client 42
44	2018-07-10 18:05:24.497776+03	2018-07-10 18:05:24.497824+03	Client 43
45	2018-07-10 18:05:24.500402+03	2018-07-10 18:05:24.500445+03	Client 44
46	2018-07-10 18:05:24.503289+03	2018-07-10 18:05:24.503338+03	Client 45
47	2018-07-10 18:05:24.506192+03	2018-07-10 18:05:24.506238+03	Client 46
48	2018-07-10 18:05:24.508945+03	2018-07-10 18:05:24.508988+03	Client 47
49	2018-07-10 18:05:24.511616+03	2018-07-10 18:05:24.511658+03	Client 48
50	2018-07-10 18:05:24.514334+03	2018-07-10 18:05:24.514381+03	Client 49
51	2018-07-10 18:05:24.517127+03	2018-07-10 18:05:24.517171+03	Client 50
52	2018-07-10 18:05:24.519889+03	2018-07-10 18:05:24.519931+03	Client 51
53	2018-07-10 18:05:24.52262+03	2018-07-10 18:05:24.522665+03	Client 52
54	2018-07-10 18:05:24.525338+03	2018-07-10 18:05:24.525382+03	Client 53
55	2018-07-10 18:05:24.528247+03	2018-07-10 18:05:24.528293+03	Client 54
56	2018-07-10 18:05:24.531008+03	2018-07-10 18:05:24.531054+03	Client 55
57	2018-07-10 18:05:24.534025+03	2018-07-10 18:05:24.534072+03	Client 56
58	2018-07-10 18:05:24.536794+03	2018-07-10 18:05:24.536837+03	Client 57
59	2018-07-10 18:05:24.539636+03	2018-07-10 18:05:24.539679+03	Client 58
60	2018-07-10 18:05:24.542441+03	2018-07-10 18:05:24.542484+03	Client 59
61	2018-07-10 18:05:24.545134+03	2018-07-10 18:05:24.545178+03	Client 60
62	2018-07-10 18:05:24.547823+03	2018-07-10 18:05:24.547867+03	Client 61
63	2018-07-10 18:05:24.550549+03	2018-07-10 18:05:24.550593+03	Client 62
64	2018-07-10 18:05:24.553269+03	2018-07-10 18:05:24.553314+03	Client 63
65	2018-07-10 18:05:24.556031+03	2018-07-10 18:05:24.556098+03	Client 64
66	2018-07-10 18:05:24.558863+03	2018-07-10 18:05:24.558909+03	Client 65
67	2018-07-10 18:05:24.561644+03	2018-07-10 18:05:24.561689+03	Client 66
68	2018-07-10 18:05:24.564406+03	2018-07-10 18:05:24.564449+03	Client 67
69	2018-07-10 18:05:24.567069+03	2018-07-10 18:05:24.567112+03	Client 68
70	2018-07-10 18:05:24.569812+03	2018-07-10 18:05:24.569854+03	Client 69
\.


--
-- Data for Name: main_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_location (id, created, modified, name, country, geopoint, radius, shapefile, description, lft, rght, tree_id, level, location_type_id, parent_id) FROM stdin;
1	2018-07-09 14:53:09.73223+03	2018-07-09 14:53:09.732261+03	Sol Point	CK	\N	\N	\N	Something	1	2	1	0	\N	\N
\.


--
-- Data for Name: main_locationtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_locationtype (id, created, modified, name) FROM stdin;
\.


--
-- Data for Name: main_project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_project (id, created, modified, target_object_id, name, target_content_type_id) FROM stdin;
\.


--
-- Data for Name: main_project_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_project_tasks (id, project_id, task_id) FROM stdin;
\.


--
-- Data for Name: main_segmentrule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_segmentrule (id, created, modified, name, description, target_field, target_field_value, active, target_content_type_id) FROM stdin;
\.


--
-- Data for Name: main_submission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_submission (id, created, modified, target_object_id, submission_time, valid, status, comments, bounty_id, location_id, target_content_type_id, task_id, user_id) FROM stdin;
\.


--
-- Data for Name: main_task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_task (id, created, modified, target_object_id, name, description, start, "end", timing_rule, total_submission_target, user_submission_target, status, estimated_time, required_expertise, lft, rght, tree_id, level, client_id, created_by_id, parent_id, target_content_type_id) FROM stdin;
4	2018-07-10 16:50:20.16532+03	2018-07-10 16:50:20.165343+03	6	Kaznet	This is an awesome task	2018-07-10 12:00:00+03	2020-07-10 12:00:00+03	FREQ=WEEKLY;INTERVAL=1;BYDAY=FR,SA	\N	10	a	00:15:00	1	1	2	1	0	1	3	\N	16
\.


--
-- Data for Name: main_task_segment_rules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_task_segment_rules (id, task_id, segmentrule_id) FROM stdin;
\.


--
-- Data for Name: main_tasklocation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_tasklocation (id, created, modified, timing_rule, start, "end", location_id, task_id) FROM stdin;
\.


--
-- Data for Name: main_taskoccurrence; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_taskoccurrence (id, created, modified, date, start_time, end_time, task_id) FROM stdin;
\.


--
-- Data for Name: ona_instance; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ona_instance (id, created, modified, ona_pk, json, deleted_at, last_updated, user_id, xform_id) FROM stdin;
\.


--
-- Data for Name: ona_project; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ona_project (id, created, modified, ona_pk, organization, name, deleted_at, last_updated) FROM stdin;
1	2018-07-10 10:55:53.413763+03	2018-07-10 10:55:53.4138+03	5561	\N	BRCiS Registration Data Share	\N	2015-07-21 14:59:50.031746+03
2	2018-07-10 10:56:21.485843+03	2018-07-10 10:56:21.485908+03	3412	\N	FAO Forcier Consulting	\N	2015-04-23 11:39:14.282507+03
3	2018-07-10 10:56:21.492007+03	2018-07-10 10:56:21.492109+03	10743	\N	Zambia 2015 Merged	\N	2017-02-20 15:59:42.628928+03
4	2018-07-10 10:56:21.497371+03	2018-07-10 10:56:21.497432+03	15664	\N	mc testing	\N	2016-05-19 17:23:33.632225+03
5	2018-07-10 10:56:21.503498+03	2018-07-10 10:56:21.50356+03	4213	\N	BRCiS - TARGETED COMMUNITIES (March 2015)	\N	2017-02-15 16:11:32.571115+03
6	2018-07-10 10:56:21.508639+03	2018-07-10 10:56:21.508702+03	27458	\N	Thank You / Happy Holidays 2016	\N	2017-03-25 10:20:09.299031+03
7	2018-07-10 10:56:21.513078+03	2018-07-10 10:56:21.51311+03	15693	\N	Public Schools	\N	2016-05-18 02:34:50.779779+03
8	2018-07-10 10:56:21.516169+03	2018-07-10 10:56:21.516196+03	925	\N	betatester's Project	\N	2017-04-06 13:52:13.028213+03
9	2018-07-10 10:56:21.518771+03	2018-07-10 10:56:21.518797+03	25215	\N	Nyanza	\N	2016-11-08 11:01:56.088026+03
10	2018-07-10 10:56:21.521536+03	2018-07-10 10:56:21.52156+03	26048	\N	HKIBD	\N	2016-11-23 17:10:58.875718+03
11	2018-07-10 10:56:21.523793+03	2018-07-10 10:56:21.523813+03	7922	\N	Feedback	\N	2016-10-27 23:21:18.626961+03
12	2018-07-10 10:56:21.526063+03	2018-07-10 10:56:21.526085+03	20277	\N	Kenya MDP	\N	2017-01-27 12:08:55.744651+03
13	2018-07-10 10:56:21.52831+03	2018-07-10 10:56:21.528331+03	5940	\N	SDI India Dataset	\N	2017-04-05 09:08:53.926399+03
14	2018-07-10 10:56:21.5306+03	2018-07-10 10:56:21.530621+03	2988	\N	Dolow Midline Test Project	\N	2018-02-22 18:09:32.810016+03
15	2018-07-10 10:56:21.53278+03	2018-07-10 10:56:21.5328+03	41754	\N	qa_wd	\N	2017-10-13 04:29:06.132326+03
16	2018-07-10 10:56:21.534926+03	2018-07-10 10:56:21.534946+03	47086	\N	test project 3	\N	2017-11-16 16:03:34.104109+03
17	2018-07-10 10:56:21.537031+03	2018-07-10 10:56:21.537051+03	15661	\N	MC Demo	\N	2017-03-24 11:04:45.831167+03
18	2018-07-10 10:56:21.539306+03	2018-07-10 10:56:21.539324+03	7609	\N	Ona Webinar	\N	2017-03-24 11:04:46.747054+03
19	2018-07-10 10:56:21.544378+03	2018-07-10 10:56:21.544461+03	2812	\N	Help	\N	2018-01-10 14:39:39.148677+03
20	2018-07-10 10:56:21.550136+03	2018-07-10 10:56:21.550225+03	59118	\N	SDI Liberia	\N	2018-04-26 12:38:23.447877+03
21	2018-07-10 10:56:21.553899+03	2018-07-10 10:56:21.553931+03	3571	\N	Test Project A	\N	2017-08-18 16:33:41.474618+03
22	2018-07-10 10:56:21.558955+03	2018-07-10 10:56:21.559016+03	820	\N	onasupport's Project	\N	2018-04-19 14:40:51.500971+03
23	2018-07-10 10:56:21.565685+03	2018-07-10 10:56:21.565749+03	25264	\N	Marketing Surveys	\N	2018-06-22 16:25:31.503533+03
24	2018-07-10 10:56:21.571939+03	2018-07-10 10:56:21.571999+03	43048	\N	Kelvin Private	\N	2018-04-19 14:35:01.717798+03
25	2018-07-10 10:56:21.578127+03	2018-07-10 10:56:21.578186+03	51891	\N	Ranking Test	\N	2018-01-19 16:55:11.577606+03
26	2018-07-10 10:56:21.583661+03	2018-07-10 10:56:21.583704+03	49035	\N	Demo Project	\N	2017-11-24 16:25:38.074041+03
27	2018-07-10 10:56:21.590007+03	2018-07-10 10:56:21.590089+03	49868	\N	CCP4	\N	2017-12-07 14:36:57.061871+03
28	2018-07-10 10:56:21.596995+03	2018-07-10 10:56:21.597039+03	5407	\N	Filter Data view QA	\N	2018-02-07 11:32:18.739268+03
29	2018-07-10 10:56:21.601021+03	2018-07-10 10:56:21.601054+03	61227	\N	dfid dash 2	\N	2018-05-23 17:12:04.641279+03
30	2018-07-10 10:56:21.604029+03	2018-07-10 10:56:21.604088+03	56363	\N	Somali Head Count	\N	2018-03-20 12:00:40.261437+03
31	2018-07-10 10:56:21.607855+03	2018-07-10 10:56:21.607882+03	60757	\N	Test Project	\N	2018-05-17 16:42:20.870055+03
32	2018-07-10 10:56:21.610776+03	2018-07-10 10:56:21.610797+03	41759	\N	Environmental Cleanliness	\N	2017-09-07 15:41:32.574637+03
\.


--
-- Data for Name: ona_xform; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ona_xform (id, created, modified, ona_pk, project_id, title, id_string, deleted_at, last_updated) FROM stdin;
42	2018-07-10 16:41:01.860017+03	2018-07-10 16:55:07.261227+03	196871	21	Q10_edit	Q10_edit	\N	\N
24	2018-07-10 16:41:01.834115+03	2018-07-10 16:55:07.193242+03	31416	19	WFP VAM - Traders' Questionnaire	SOMTRADER	\N	\N
57	2018-07-10 16:41:01.879344+03	2018-07-10 16:55:07.279442+03	197604	21	HAGN Coordinator Monitoring Form v2. ENGLISH ONLY Multi Select	hagnCoordinatorMonitoringENG_Multi	\N	\N
22	2018-07-10 16:41:01.830738+03	2018-07-10 16:55:07.188222+03	31114	19	FAO Practise Survey	fao_practise_survey_1	\N	\N
30	2018-07-10 16:41:01.847106+03	2018-07-10 16:55:07.210208+03	49891	19	BRCiS - TARGETED COMMUNITIES (March 2015)	brcis_targeted_comm_march2015	\N	\N
19	2018-07-10 16:41:01.827268+03	2018-07-10 16:55:07.160665+03	85259	18	Getting Started with Ona - Webinar Registration	Getting_Started_with_Ona_Webinar	\N	\N
33	2018-07-10 16:41:01.849825+03	2018-07-10 16:55:07.222476+03	60943	19	choice_filter	choice_filter	\N	\N
75	2018-07-10 16:41:01.912058+03	2018-07-10 16:55:07.394762+03	7527	22	hki_foodgroup_example	hki_foodgroup_example	\N	\N
44	2018-07-10 16:41:01.861392+03	2018-07-10 16:55:07.374633+03	2954	22	Household	household	\N	\N
50	2018-07-10 16:41:01.867921+03	2018-07-10 16:55:07.269823+03	197132	21	Pull_Photo	Pull_Photo	\N	\N
49	2018-07-10 16:41:01.867821+03	2018-07-10 16:55:07.25075+03	66592	19	Call Centre Survey - Unicef Cash 3	CCS_UnicefCash3	\N	\N
48	2018-07-10 16:41:01.866681+03	2018-07-10 16:55:07.377564+03	3018	22	ANC Registration	ANC_Registration_EngKan	\N	\N
56	2018-07-10 16:41:01.877422+03	2018-07-10 16:55:07.261596+03	68678	19	Pupil School Survey - Boys & Girls	NORAD_baseline_pupil	\N	\N
41	2018-07-10 16:41:01.859214+03	2018-07-10 16:55:07.23537+03	65215	19	demo_repeat_count	demo_repeat_count	\N	\N
45	2018-07-10 16:41:01.862173+03	2018-07-10 16:55:07.241849+03	66531	19	BRCiS Registration and Baseline without repeats	BRCiS_Registration-NoRepeats_20150716	\N	\N
74	2018-07-10 16:41:01.908603+03	2018-07-10 16:55:07.306012+03	68985	19	SDI South Africa Solar Project Ruimsig	sdi_sa_solar_ruimsig	\N	\N
27	2018-07-10 16:41:01.839147+03	2018-07-10 16:55:07.204465+03	49888	19	BRCiS - TARGETED COMMUNITIES (March 2015)	brcis_targ_comm_march2015	\N	\N
39	2018-07-10 16:41:01.857453+03	2018-07-10 16:55:07.371423+03	2785	22	Sample Survey	sample_survey	\N	\N
69	2018-07-10 16:41:01.898421+03	2018-07-10 16:55:07.29669+03	198875	21	Test_Form	Test_Form	\N	\N
46	2018-07-10 16:41:01.86329+03	2018-07-10 16:55:07.265653+03	197120	21	Photo_Form	Photo_Form	\N	\N
25	2018-07-10 16:41:01.83806+03	2018-07-10 16:55:07.1184+03	29290	14	Weekly Items	weekly_items	\N	\N
52	2018-07-10 16:41:01.87061+03	2018-07-10 16:55:07.255767+03	66593	19	Ebola Center - External Quality Improvement Survey v8 20150330	quality_improvement_survey_v8_20150330	\N	\N
63	2018-07-10 16:41:01.8909+03	2018-07-10 16:55:07.386147+03	4530	22	Repeat example	repeat_example	\N	\N
55	2018-07-10 16:41:01.876822+03	2018-07-10 16:55:07.195702+03	73231	14	section_T	section_T	\N	\N
66	2018-07-10 16:41:01.894887+03	2018-07-10 16:55:07.293307+03	68695	19	select_one_external_testing	select_one_external_testing	\N	\N
68	2018-07-10 16:41:01.896694+03	2018-07-10 16:55:07.388909+03	6287	22	Tutorial XLSForms 2	tutorial_xlsform2	\N	\N
62	2018-07-10 16:41:01.890244+03	2018-07-10 16:55:07.287538+03	197688	21	form	form	\N	\N
67	2018-07-10 16:41:01.89647+03	2018-07-10 16:55:07.445038+03	179817	23	Customer Feedback form	aUXCDwPD8Z6hfAAbxLxcyY	\N	\N
31	2018-07-10 16:41:01.847406+03	2018-07-10 16:55:07.364479+03	2348	22	Tutorial	tutorial	\N	\N
59	2018-07-10 16:41:01.882468+03	2018-07-10 16:55:07.272333+03	68685	19	cascading select test	cascading_select_test_1	\N	\N
76	2018-07-10 16:41:01.912329+03	2018-07-10 16:55:07.310083+03	69244	19	section_above5_years	section_above5_years	\N	\N
35	2018-07-10 16:41:01.852855+03	2018-07-10 16:55:07.368145+03	2517	22	consent_signature	consent_signature	\N	\N
61	2018-07-10 16:41:01.888422+03	2018-07-10 16:55:07.278396+03	68687	19	cascading select test1	cascading_select_test1	\N	\N
65	2018-07-10 16:41:01.894878+03	2018-07-10 16:55:07.291581+03	198713	21	TZ_TL3_ICRISAT-Survey_updated	TZ_TL3_ICRISAT-Survey_updated	\N	\N
11	2018-07-10 16:41:01.800832+03	2018-07-10 16:55:07.066384+03	86442	11	Ona 2 Feedback Survey	feedback_survey	\N	\N
72	2018-07-10 16:41:01.902545+03	2018-07-10 16:55:07.447541+03	234466	23	Ona User Survey	aHgayMqNY6tf3wXosEjeWj	\N	\N
6	2018-07-10 11:04:23.474657+03	2018-07-10 16:55:07.04219+03	98939	3	2015 IRS Data Collection Form	Zambia_2015IRS	\N	\N
73	2018-07-10 16:41:01.906903+03	2018-07-10 16:55:07.300895+03	199153	21	Participant Registration Form	registration_form	\N	\N
8	2018-07-10 16:41:01.780123+03	2018-07-10 16:55:07.056382+03	169955	6	Thank you / happy holidays 2016	ona-thank-you-form-new	\N	\N
13	2018-07-10 16:41:01.808267+03	2018-07-10 16:55:07.089491+03	28481	14	Hh roster section	hh_roster_section	\N	\N
10	2018-07-10 16:41:01.800819+03	2018-07-10 16:55:07.07585+03	72402	13	Informal Settlement Profile (May 2014)	sdi_settlement_profile_May2014	\N	\N
12	2018-07-10 16:41:01.804506+03	2018-07-10 16:55:07.07281+03	142053	12	Education Tool	education_form_1	\N	\N
64	2018-07-10 16:41:01.891917+03	2018-07-10 16:55:07.442229+03	162499	23	Ona Marketing Survey	Marketing_Survey_Form_1_1	\N	\N
14	2018-07-10 16:41:01.810487+03	2018-07-10 16:55:07.07603+03	142055	12	Education Tool	education_form	\N	\N
18	2018-07-10 16:41:01.825507+03	2018-07-10 16:55:07.103254+03	28837	14	Section l	section_l	\N	\N
70	2018-07-10 16:41:01.900259+03	2018-07-10 16:55:07.391756+03	6570	22	Tutorial XLSForm Multi-language	tutorial_xlsform_multilanguage	\N	\N
15	2018-07-10 16:41:01.81216+03	2018-07-10 16:55:07.09297+03	229798	15	Test form	adaXK3kqfZg2aqTvcXff2k	\N	\N
17	2018-07-10 16:41:01.817047+03	2018-07-10 16:55:07.094701+03	28835	14	Section hk	section_hk	\N	\N
21	2018-07-10 16:41:01.830695+03	2018-07-10 16:55:07.164798+03	117771	18	MC webinar signup	mc_webinar_signup	\N	\N
32	2018-07-10 16:41:01.848819+03	2018-07-10 16:55:07.147847+03	29745	14	Section P	section_p	\N	\N
16	2018-07-10 16:41:01.814276+03	2018-07-10 16:55:07.116412+03	254674	16	RTM Demo NUTRITION: Bi-Weekly Reporting	Sandbox_SitRep_Reporting_Form_Nutrition_v01	\N	\N
20	2018-07-10 16:41:01.82855+03	2018-07-10 16:55:07.140987+03	122938	17	Baseline_Questionnaire	Baseline_Questionnaire	\N	\N
47	2018-07-10 16:41:01.864876+03	2018-07-10 16:55:07.176582+03	34400	14	Dolow Midline 20150313	dolow_midline_20150313	\N	\N
37	2018-07-10 16:41:01.856067+03	2018-07-10 16:55:07.229548+03	61488	19	expected_pay_choice_filter	expected_pay_choice_filter	\N	\N
23	2018-07-10 16:41:01.830716+03	2018-07-10 16:55:07.109425+03	28918	14	Section M	section_m	\N	\N
43	2018-07-10 16:41:01.860942+03	2018-07-10 16:55:07.172449+03	31025	14	Section 4 5	Section_4_5	\N	\N
36	2018-07-10 16:41:01.854474+03	2018-07-10 16:55:07.162063+03	29753	14	Section R	section_R	\N	\N
53	2018-07-10 16:41:01.869828+03	2018-07-10 16:55:07.380333+03	3440	22	Delivery Outcome	Delivery_Outcome	\N	\N
58	2018-07-10 16:41:01.878611+03	2018-07-10 16:55:07.383297+03	3462	22	VersionTwo	VersionTwo	\N	\N
54	2018-07-10 16:41:01.873705+03	2018-07-10 16:55:07.274358+03	197445	21	barcode_example	barcode_example	\N	\N
60	2018-07-10 16:41:01.8831+03	2018-07-10 16:55:07.283694+03	197687	21	Favorite Fruits	favorite_fruits	\N	\N
38	2018-07-10 16:41:01.856798+03	2018-07-10 16:55:07.255789+03	196396	21	to_ona	to_ona	\N	\N
71	2018-07-10 16:41:01.902003+03	2018-07-10 16:55:07.300817+03	68731	19	Pupil School Survey - Boys and Girls	NORAD_baseline_pupil_test	\N	\N
40	2018-07-10 16:41:01.85757+03	2018-07-10 16:55:07.166583+03	29754	14	Section s	section_S	\N	\N
51	2018-07-10 16:41:01.868943+03	2018-07-10 16:55:07.188419+03	70160	14	Livestock Restocking Vaccination Impact Assesment Study	fao_livestock_070615_danvers	\N	\N
132	2018-07-10 16:41:01.997686+03	2018-07-10 16:55:07.384094+03	210754	21	example	example	\N	\N
135	2018-07-10 16:41:02.006684+03	2018-07-10 16:55:07.387002+03	210805	21	Password_for_questions	Password_for_questions	\N	\N
138	2018-07-10 16:41:02.012565+03	2018-07-10 16:55:07.389814+03	211158	21	instance_problem	instance_problem	\N	\N
140	2018-07-10 16:41:02.015928+03	2018-07-10 16:55:07.3928+03	211175	21	instance_problem1	instance_problem1	\N	\N
142	2018-07-10 16:41:02.019165+03	2018-07-10 16:55:07.395656+03	211389	21	REACH Household Survey (Matlab)	reach_matlab_survey	\N	\N
144	2018-07-10 16:41:02.022598+03	2018-07-10 16:55:07.398119+03	211403	21	REACH/IFPRI Household Survey	reach_ifpri_survey2_test	\N	\N
146	2018-07-10 16:41:02.028526+03	2018-07-10 16:55:07.400636+03	211929	21	DFID Somalia ER TPM Health Facilities Survey	DFID_252_tpm_health_facilities_1	\N	\N
148	2018-07-10 16:41:02.035554+03	2018-07-10 16:55:07.403123+03	211984	21	Test_Notes_and_table-list	Test_Notes_and_table-list	\N	\N
151	2018-07-10 16:41:02.038914+03	2018-07-10 16:55:07.40561+03	211987	21	Test_Notes_and_table-list1	Test_Notes_and_table-list1	\N	\N
152	2018-07-10 16:41:02.042247+03	2018-07-10 16:55:07.408395+03	212598	21	Geopoints2	Geopoints2	\N	\N
154	2018-07-10 16:41:02.044855+03	2018-07-10 16:55:07.411186+03	212600	21	Geopoints3	Geopoints3	\N	\N
156	2018-07-10 16:41:02.047939+03	2018-07-10 16:55:07.414219+03	213085	21	Basic_Example_11234	Basic_Example_1	\N	\N
158	2018-07-10 16:41:02.050773+03	2018-07-10 16:55:07.417223+03	213991	21	Photo_trial12	Photo_trial12	\N	\N
160	2018-07-10 16:41:02.054439+03	2018-07-10 16:55:07.420101+03	214440	21	XLS_Report_Form	XLS_Report_Form	\N	\N
162	2018-07-10 16:41:02.05723+03	2018-07-10 16:55:07.422849+03	214447	21	Attendance_form1	Attendance_form1	\N	\N
164	2018-07-10 16:41:02.060129+03	2018-07-10 16:55:07.425831+03	214466	21	pulldata_test	pulldata_test	\N	\N
166	2018-07-10 16:41:02.062857+03	2018-07-10 16:55:07.428408+03	214467	21	pulldata_from	pulldata_from	\N	\N
168	2018-07-10 16:41:02.065645+03	2018-07-10 16:55:07.431033+03	214636	21	bike_trip_repeat	bike_trip_repeat	\N	\N
170	2018-07-10 16:41:02.068759+03	2018-07-10 16:55:07.433736+03	215092	21	CBIRI_Checklist	CBIRI	\N	\N
77	2018-07-10 16:41:01.912451+03	2018-07-10 16:55:07.305426+03	199430	21	Mali Health Facilities	mali_health_facilities_EDIT_3	\N	\N
80	2018-07-10 16:41:01.921696+03	2018-07-10 16:55:07.313775+03	200236	21	UNICEF Partner Reporting: WASH	UNICEF_Partner_Reporting_XLForm_WASH_v1	\N	\N
83	2018-07-10 16:41:01.926722+03	2018-07-10 16:55:07.319594+03	200360	21	pull_data	pull_data	\N	\N
87	2018-07-10 16:41:01.931605+03	2018-07-10 16:55:07.325498+03	200362	21	pull_data12345	pull_data12345	\N	\N
91	2018-07-10 16:41:01.937139+03	2018-07-10 16:55:07.330009+03	202974	21	Phone number example	phone_number_example	\N	\N
94	2018-07-10 16:41:01.944601+03	2018-07-10 16:55:07.334808+03	202975	21	EPI_test	EPI_test	\N	\N
98	2018-07-10 16:41:01.948801+03	2018-07-10 16:55:07.339018+03	202979	21	XLSX_String_Name_Export1	XLSX_String_Name_Export1	\N	\N
102	2018-07-10 16:41:01.953267+03	2018-07-10 16:55:07.343575+03	203355	21	Rank_Priority	Rank_Priority	\N	\N
106	2018-07-10 16:41:01.957213+03	2018-07-10 16:55:07.347683+03	203359	21	Percent_totals1	Percent_totals1	\N	\N
108	2018-07-10 16:41:01.960234+03	2018-07-10 16:55:07.352025+03	203768	21	Photo_trial_2345	Photo_trial_2345	\N	\N
111	2018-07-10 16:41:01.963568+03	2018-07-10 16:55:07.356295+03	204019	21	Tanzania Groundnut Impact FINAL	TZ_TL3_GN	\N	\N
114	2018-07-10 16:41:01.967312+03	2018-07-10 16:55:07.361727+03	207543	21	select multiple csv	selectmultiplecsv	\N	\N
117	2018-07-10 16:41:01.971956+03	2018-07-10 16:55:07.36754+03	209040	21	select_one_grid_view	select_one_grid_view	\N	\N
120	2018-07-10 16:41:01.975114+03	2018-07-10 16:55:07.371283+03	209402	21	repeat_group_example	repeat_group_example	\N	\N
123	2018-07-10 16:41:01.978+03	2018-07-10 16:55:07.37536+03	209406	21	repeat_group_example1	repeat_group_example1	\N	\N
126	2018-07-10 16:41:01.981324+03	2018-07-10 16:55:07.378175+03	209419	21	Participant Attendance Sheet	second_registration_form	\N	\N
129	2018-07-10 16:41:01.984663+03	2018-07-10 16:55:07.380953+03	210510	21	Latrine_Assessment_2017	Latrine_Assessment_2017_test	\N	\N
97	2018-07-10 16:41:01.946419+03	2018-07-10 16:55:07.410577+03	14716	22	expense_report	expense_report	\N	\N
99	2018-07-10 16:41:01.951301+03	2018-07-10 16:55:07.413401+03	14720	22	household_survey_water	household_survey_water	\N	\N
103	2018-07-10 16:41:01.954823+03	2018-07-10 16:55:07.416421+03	14753	22	Test	test	\N	\N
107	2018-07-10 16:41:01.958788+03	2018-07-10 16:55:07.419296+03	14813	22	Ona Kenya XLSForm Authoring Training!	ona_kenya_internal_training	\N	\N
109	2018-07-10 16:41:01.96221+03	2018-07-10 16:55:07.422509+03	14821	22	Appearance Widgets	appearance_widgets	\N	\N
112	2018-07-10 16:41:01.965198+03	2018-07-10 16:55:07.425173+03	14823	22	New Cascading Example	new_cascading_example	\N	\N
115	2018-07-10 16:41:01.968231+03	2018-07-10 16:55:07.427826+03	14824	22	Transtech XLSForm Authoring Training	transtech_training	\N	\N
118	2018-07-10 16:41:01.972754+03	2018-07-10 16:55:07.430426+03	15119	22	questionnaireRFM	questionnaireRFM	\N	\N
121	2018-07-10 16:41:01.976162+03	2018-07-10 16:55:07.433128+03	15952	22	pizza_questionnaire	pizza_questionnaire	\N	\N
139	2018-07-10 16:41:02.013724+03	2018-07-10 16:55:07.449618+03	22379	22	Healthworkers_updated	Healthworkers_updated	\N	\N
141	2018-07-10 16:41:02.017295+03	2018-07-10 16:55:07.453261+03	22441	22	UFC_Survey	UFCS	\N	\N
143	2018-07-10 16:41:02.020639+03	2018-07-10 16:55:07.456031+03	22667	22	Menage_R2_2014_TR	Menage_R2_2014_TR	\N	\N
145	2018-07-10 16:41:02.025685+03	2018-07-10 16:55:07.45871+03	24162	22	External Choices	select_one_external_sample	\N	\N
147	2018-07-10 16:41:02.03004+03	2018-07-10 16:55:07.461184+03	24171	22	Ethiopia_Roster	Ethiopia_Roster	\N	\N
149	2018-07-10 16:41:02.036296+03	2018-07-10 16:55:07.46374+03	24915	22	Group Form	group_form_updated_version	\N	\N
150	2018-07-10 16:41:02.038989+03	2018-07-10 16:55:07.466317+03	25765	22	FUEL	FUEL	\N	\N
153	2018-07-10 16:41:02.04214+03	2018-07-10 16:55:07.468898+03	25816	22	Steps instrument v3 1	steps_instrument_v3_1	\N	\N
171	2018-07-10 16:41:02.070367+03	2018-07-10 16:55:07.492031+03	47029	22	Gender Impact of Labour Saving Devices Use In Maize Groups - UPDATED	gender_impact_1	\N	\N
172	2018-07-10 16:41:02.073597+03	2018-07-10 16:55:07.494626+03	47705	22	NGO Field Staff Questionnaire	NGO_Field_Staff_Questionnaire_1	\N	\N
173	2018-07-10 16:41:02.076445+03	2018-07-10 16:55:07.497219+03	50398	22	Tutorial XLSForm	tutorial_xlsform_1	\N	\N
174	2018-07-10 16:41:02.079484+03	2018-07-10 16:55:07.500472+03	68736	22	Pupil School Survey - Boys & Girls	NORAD_baseline_pupil_test_1	\N	\N
175	2018-07-10 16:41:02.082322+03	2018-07-10 16:55:07.506252+03	74740	22	Mango_Pa_Manm	Mango_Pa_Manm	\N	\N
176	2018-07-10 16:41:02.084876+03	2018-07-10 16:55:07.513582+03	81024	22	Pharmaceutical warehouse monitoring visit	pharmaceutical_warehouse_monitoring	\N	\N
177	2018-07-10 16:41:02.087358+03	2018-07-10 16:55:07.520563+03	118289	22	Nationwide TB-related catastrophic costs survey in Myanmar	pcs3	\N	\N
178	2018-07-10 16:41:02.089928+03	2018-07-10 16:55:07.527479+03	234467	22	Inactive user survey	aZKNzDQoJbrETs6EPKC7BU	\N	\N
179	2018-07-10 16:41:02.0925+03	2018-07-10 16:55:07.534016+03	237980	22	School Feeding Programme	school_food123	\N	\N
180	2018-07-10 16:41:02.094564+03	2018-07-10 16:55:07.540549+03	238010	22	funded_schools123	funded_schools123	\N	\N
78	2018-07-10 16:41:01.91844+03	2018-07-10 16:55:07.397481+03	9822	22	Tutorial XLSForm	tutorial_xlsform_encryptedform	\N	\N
81	2018-07-10 16:41:01.924366+03	2018-07-10 16:55:07.399992+03	10639	22	INFORMAL MARKETS PROFILE CAG	informal_market_profile_cag	\N	\N
181	2018-07-10 16:41:02.0971+03	2018-07-10 16:55:07.546986+03	251836	22	Adolescentes na Unidade de Saúde	adolescent_client_V3	\N	\N
182	2018-07-10 16:41:02.101646+03	2018-07-10 16:55:07.551957+03	266439	22	Adolescentes na Comunidade	adolescent_in_community_V2	\N	\N
183	2018-07-10 16:41:02.104608+03	2018-07-10 16:55:07.556682+03	303435	22	NORC-IGA-Menage_TEST10	NORC-IGA-Menage_10	\N	\N
85	2018-07-10 16:41:01.928679+03	2018-07-10 16:55:07.402532+03	11646	22	Spec test	spec_test	\N	\N
89	2018-07-10 16:41:01.933581+03	2018-07-10 16:55:07.405099+03	12282	22	Mig_Malaka_Ceria_1_SurveyPAUD_revised_new	Mig_Malaka_Ceria_1_SurveyPAUD_revised_new	\N	\N
93	2018-07-10 16:41:01.940324+03	2018-07-10 16:55:07.407752+03	13106	22	2014 WHO Verbal Autopsy RC1 - With Groupings2	va_who_2014_groupings2	\N	\N
124	2018-07-10 16:41:01.979457+03	2018-07-10 16:55:07.435844+03	16118	22	Informal Settlement Boundaries	sdi_boundaries	\N	\N
127	2018-07-10 16:41:01.982973+03	2018-07-10 16:55:07.439115+03	19624	22	Ultimate Geo Widgets	geo	\N	\N
130	2018-07-10 16:41:01.995719+03	2018-07-10 16:55:07.441715+03	21634	22	Facility Infection Prevention and Control Daily Checklist	daily_improvement_survey_for_grid	\N	\N
133	2018-07-10 16:41:02.004953+03	2018-07-10 16:55:07.444363+03	22337	22	multiple_languages_new_cascades	multiple_languages_new_cascades	\N	\N
136	2018-07-10 16:41:02.010028+03	2018-07-10 16:55:07.446986+03	22377	22	Healthworkers	Healthworkers	\N	\N
155	2018-07-10 16:41:02.04602+03	2018-07-10 16:55:07.471474+03	29969	22	Child	child_under_five_1	\N	\N
157	2018-07-10 16:41:02.048818+03	2018-07-10 16:55:07.47416+03	33892	22	rename	rename	\N	\N
159	2018-07-10 16:41:02.052825+03	2018-07-10 16:55:07.47668+03	33911	22	one	one	\N	\N
161	2018-07-10 16:41:02.055714+03	2018-07-10 16:55:07.479274+03	34114	22	Two	two	\N	\N
163	2018-07-10 16:41:02.058876+03	2018-07-10 16:55:07.481832+03	34256	22	New	new	\N	\N
165	2018-07-10 16:41:02.061956+03	2018-07-10 16:55:07.484303+03	35131	22	Money vendor staff questionnaire 2015	Money_Vendor_Staff_Questionnaire_2015	\N	\N
167	2018-07-10 16:41:02.064904+03	2018-07-10 16:55:07.486886+03	45257	22	India Form	India_form	\N	\N
169	2018-07-10 16:41:02.067634+03	2018-07-10 16:55:07.489495+03	46126	22	DERC Daily Report V4.2.2	derc_daily_report_v4_2-2	\N	\N
110	2018-07-10 16:41:01.963258+03	2018-07-10 16:55:07.472203+03	273103	24	Entrevista com Profissional de Saúde	health_care_provider_V3	\N	\N
113	2018-07-10 16:41:01.966862+03	2018-07-10 16:55:07.474811+03	273136	24	Entrevista com o membro da comunidade	community_member_V3	\N	\N
116	2018-07-10 16:41:01.970315+03	2018-07-10 16:55:07.47734+03	273139	24	derfe	derfe	\N	\N
119	2018-07-10 16:41:01.973476+03	2018-07-10 16:55:07.479905+03	279132	24	Baseline_Questionnaire	Baseline_Questionnaire22	\N	\N
122	2018-07-10 16:41:01.976756+03	2018-07-10 16:55:07.482367+03	283719	24	GUINEA_Integrated Supportive Supervisory Checklist	GUINEA_iss	\N	\N
125	2018-07-10 16:41:01.980482+03	2018-07-10 16:55:07.48483+03	283721	24	NIGER_SUPERVISION FORMATIVE INTÉGRÉE AU CENTRE DE SANTÉ	NIGER_iss	\N	\N
128	2018-07-10 16:41:01.983874+03	2018-07-10 16:55:07.487634+03	283751	24	CHAD_Integrated Supportive Supervisory Checklist	chad_iss	\N	\N
7	2018-07-10 16:41:01.779445+03	2018-07-10 16:55:07.053322+03	49857	5	BRCiS - TARGETED COMMUNITIES (March 2015)	brcis_targ_comm_march2015	\N	\N
9	2018-07-10 16:41:01.788084+03	2018-07-10 16:55:07.062834+03	28152	8	Kenya prim school survey 18feb2015	kenya_prim_school_survey	\N	\N
28	2018-07-10 16:41:01.845876+03	2018-07-10 16:55:07.134454+03	29694	14	Section O	section_o	\N	\N
26	2018-07-10 16:41:01.838659+03	2018-07-10 16:55:07.228092+03	73578	21	IRF Registration and Baseline	IRF_Registration_Form_test	\N	\N
29	2018-07-10 16:41:01.84573+03	2018-07-10 16:55:07.232927+03	195407	21	Maps And Geo Example	maps_example	\N	\N
34	2018-07-10 16:41:01.849511+03	2018-07-10 16:55:07.2409+03	195442	21	TESTING 04062017	afkTWx6RsxeVqmZPTBi7VK	\N	\N
79	2018-07-10 16:41:01.920354+03	2018-07-10 16:55:07.31825+03	69658	19	concern_kenya_IDSUE_Final	concern_kenya_IDSUE_Final	\N	\N
84	2018-07-10 16:41:01.926878+03	2018-07-10 16:55:07.321823+03	146394	19	SA SDI Alliance WC RAP Settlement Service Mapping	SA_SDI_Alliance_Services_Mapping_1	\N	\N
88	2018-07-10 16:41:01.932746+03	2018-07-10 16:55:07.325787+03	146663	19	Adult Mosquito Collections Grid Theme	Adult_mosquito_collections_Grid	\N	\N
92	2018-07-10 16:41:01.937259+03	2018-07-10 16:55:07.330621+03	151505	19	brcis_irf_hh_jan14_dec15_20160517_form	brcis_irf_hh_jan14_dec15_20160517_form	\N	\N
96	2018-07-10 16:41:01.945206+03	2018-07-10 16:55:07.338455+03	152857	19	Refugee Well-Being and Adjustment Index (2016-Numeric)	numeric_lebanon_2016	\N	\N
131	2018-07-10 16:41:01.997517+03	2018-07-10 16:55:07.490106+03	283752	24	CAMEROON_Integrated Supportive Supervisory Checklist	cameroon_iss	\N	\N
134	2018-07-10 16:41:02.006075+03	2018-07-10 16:55:07.492612+03	283753	24	asdfghjk	MjQ5ZTlh	\N	\N
137	2018-07-10 16:41:02.010993+03	2018-07-10 16:55:07.495306+03	303430	24	NORC-IGA-Menage_TEST10	NORC-IGA-Menage_10	\N	\N
100	2018-07-10 16:41:01.951389+03	2018-07-10 16:55:07.345648+03	172930	19	bike_trip	bike_trip	\N	\N
105	2018-07-10 16:41:01.956109+03	2018-07-10 16:55:07.349437+03	189632	19	Project_Solar-V1	Project_Solar-V1	\N	\N
82	2018-07-10 16:41:01.923282+03	2018-07-10 16:55:07.456438+03	235675	24	X	aUaNhHAaQfLErJoTp4YL6M	\N	\N
86	2018-07-10 16:41:01.930255+03	2018-07-10 16:55:07.459315+03	246180	24	Baseline_Questionnaire	Baseline_Questionnaire_1	\N	\N
90	2018-07-10 16:41:01.935751+03	2018-07-10 16:55:07.461793+03	252851	24	cascading select test	cascading_select_test	\N	\N
95	2018-07-10 16:41:01.944602+03	2018-07-10 16:55:07.464445+03	253470	24	attachment_test	attachment_test	\N	\N
101	2018-07-10 16:41:01.951611+03	2018-07-10 16:55:07.466916+03	263050	24	kelvins 2017 IRS HH Submission Form	Zambia_2017IRS_HH	\N	\N
104	2018-07-10 16:41:01.956138+03	2018-07-10 16:55:07.469477+03	273027	24	Online ReDSS Solutions Framework to Inform Analysis and Rating	ReDDsShorter1	\N	\N
\.


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialapp; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialapp (id, provider, name, client_id, secret, key) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialapp_sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialapp_sites (id, socialapp_id, site_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialtoken; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: users_userprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_userprofile (id, created, modified, ona_pk, ona_username, national_id, payment_number, phone_number, role, expertise, gender, user_id) FROM stdin;
1	2018-06-27 15:06:29.120453+03	2018-06-27 15:07:19.190802+03	\N	\N	\N			1	3	1	1
4	2018-06-27 15:08:09.531149+03	2018-06-27 15:10:20.050217+03	\N	onauser	\N			1	4	0	3
\.


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 1, false);


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 81, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 3, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 23, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 27, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 30, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: main_bounty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_bounty_id_seq', 1, true);


--
-- Name: main_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_client_id_seq', 70, true);


--
-- Name: main_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_location_id_seq', 1, true);


--
-- Name: main_locationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_locationtype_id_seq', 1, false);


--
-- Name: main_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_project_id_seq', 1, false);


--
-- Name: main_project_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_project_tasks_id_seq', 1, false);


--
-- Name: main_segmentrule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_segmentrule_id_seq', 1, false);


--
-- Name: main_submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_submission_id_seq', 1, false);


--
-- Name: main_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_task_id_seq', 4, true);


--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_task_segment_rules_id_seq', 1, false);


--
-- Name: main_tasklocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_tasklocation_id_seq', 2, true);


--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_taskoccurrence_id_seq', 1090, true);


--
-- Name: ona_instance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ona_instance_id_seq', 1, false);


--
-- Name: ona_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ona_project_id_seq', 32, true);


--
-- Name: ona_xform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ona_xform_id_seq', 183, true);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialaccount_id_seq', 1, false);


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_id_seq', 1, false);


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_sites_id_seq', 1, false);


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.socialaccount_socialtoken_id_seq', 1, false);


--
-- Name: users_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_userprofile_id_seq', 4, true);


--
-- Name: account_emailaddress account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: main_bounty main_bounty_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_bounty
    ADD CONSTRAINT main_bounty_pkey PRIMARY KEY (id);


--
-- Name: main_client main_client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_client
    ADD CONSTRAINT main_client_pkey PRIMARY KEY (id);


--
-- Name: main_location main_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_location
    ADD CONSTRAINT main_location_pkey PRIMARY KEY (id);


--
-- Name: main_locationtype main_locationtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_locationtype
    ADD CONSTRAINT main_locationtype_pkey PRIMARY KEY (id);


--
-- Name: main_project main_project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project
    ADD CONSTRAINT main_project_pkey PRIMARY KEY (id);


--
-- Name: main_project_tasks main_project_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_pkey PRIMARY KEY (id);


--
-- Name: main_project_tasks main_project_tasks_project_id_task_id_4aa4886c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_project_id_task_id_4aa4886c_uniq UNIQUE (project_id, task_id);


--
-- Name: main_segmentrule main_segmentrule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_segmentrule
    ADD CONSTRAINT main_segmentrule_pkey PRIMARY KEY (id);


--
-- Name: main_submission main_submission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_pkey PRIMARY KEY (id);


--
-- Name: main_task main_task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_pkey PRIMARY KEY (id);


--
-- Name: main_task_segment_rules main_task_segment_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_rules_pkey PRIMARY KEY (id);


--
-- Name: main_task_segment_rules main_task_segment_rules_task_id_segmentrule_id_e2dcafd6_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_rules_task_id_segmentrule_id_e2dcafd6_uniq UNIQUE (task_id, segmentrule_id);


--
-- Name: main_tasklocation main_tasklocation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tasklocation
    ADD CONSTRAINT main_tasklocation_pkey PRIMARY KEY (id);


--
-- Name: main_taskoccurrence main_taskoccurrence_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_taskoccurrence
    ADD CONSTRAINT main_taskoccurrence_pkey PRIMARY KEY (id);


--
-- Name: ona_instance ona_instance_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_ona_pk_key UNIQUE (ona_pk);


--
-- Name: ona_instance ona_instance_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_pkey PRIMARY KEY (id);


--
-- Name: ona_project ona_project_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_project
    ADD CONSTRAINT ona_project_ona_pk_key UNIQUE (ona_pk);


--
-- Name: ona_project ona_project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_project
    ADD CONSTRAINT ona_project_pkey PRIMARY KEY (id);


--
-- Name: ona_xform ona_xform_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_xform
    ADD CONSTRAINT ona_xform_ona_pk_key UNIQUE (ona_pk);


--
-- Name: ona_xform ona_xform_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_xform
    ADD CONSTRAINT ona_xform_pkey PRIMARY KEY (id);


--
-- Name: ona_xform ona_xform_project_id_id_string_609aa2ea_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_xform
    ADD CONSTRAINT ona_xform_project_id_id_string_609aa2ea_uniq UNIQUE (project_id, id_string);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_national_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_national_id_key UNIQUE (national_id);


--
-- Name: users_userprofile users_userprofile_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_ona_pk_key UNIQUE (ona_pk);


--
-- Name: users_userprofile users_userprofile_ona_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_ona_username_key UNIQUE (ona_username);


--
-- Name: users_userprofile users_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: main_bounty_task_id_077b3eb2; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_bounty_task_id_077b3eb2 ON public.main_bounty USING btree (task_id);


--
-- Name: main_location_geopoint_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_geopoint_id ON public.main_location USING gist (geopoint);


--
-- Name: main_location_level_b4e5d7ac; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_level_b4e5d7ac ON public.main_location USING btree (level);


--
-- Name: main_location_lft_236ba59c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_lft_236ba59c ON public.main_location USING btree (lft);


--
-- Name: main_location_location_type_id_49726352; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_location_type_id_49726352 ON public.main_location USING btree (location_type_id);


--
-- Name: main_location_parent_id_0da80772; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_parent_id_0da80772 ON public.main_location USING btree (parent_id);


--
-- Name: main_location_rght_5b068c79; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_rght_5b068c79 ON public.main_location USING btree (rght);


--
-- Name: main_location_shapefile_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_shapefile_id ON public.main_location USING gist (shapefile);


--
-- Name: main_location_tree_id_38352621; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_location_tree_id_38352621 ON public.main_location USING btree (tree_id);


--
-- Name: main_project_target_content_type_id_0a864095; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_project_target_content_type_id_0a864095 ON public.main_project USING btree (target_content_type_id);


--
-- Name: main_project_target_object_id_2b8de976; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_project_target_object_id_2b8de976 ON public.main_project USING btree (target_object_id);


--
-- Name: main_project_tasks_project_id_92c703dd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_project_tasks_project_id_92c703dd ON public.main_project_tasks USING btree (project_id);


--
-- Name: main_project_tasks_task_id_c5893bbe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_project_tasks_task_id_c5893bbe ON public.main_project_tasks USING btree (task_id);


--
-- Name: main_segmentrule_target_content_type_id_0cfefa99; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_segmentrule_target_content_type_id_0cfefa99 ON public.main_segmentrule USING btree (target_content_type_id);


--
-- Name: main_segmentrule_target_field_ac9dd2fc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_segmentrule_target_field_ac9dd2fc ON public.main_segmentrule USING btree (target_field);


--
-- Name: main_segmentrule_target_field_ac9dd2fc_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_segmentrule_target_field_ac9dd2fc_like ON public.main_segmentrule USING btree (target_field varchar_pattern_ops);


--
-- Name: main_submission_bounty_id_92bff86b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_submission_bounty_id_92bff86b ON public.main_submission USING btree (bounty_id);


--
-- Name: main_submission_location_id_071c36e4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_submission_location_id_071c36e4 ON public.main_submission USING btree (location_id);


--
-- Name: main_submission_target_content_type_id_66f602f8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_submission_target_content_type_id_66f602f8 ON public.main_submission USING btree (target_content_type_id);


--
-- Name: main_submission_target_object_id_11b5ca32; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_submission_target_object_id_11b5ca32 ON public.main_submission USING btree (target_object_id);


--
-- Name: main_submission_task_id_e97c36a1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_submission_task_id_e97c36a1 ON public.main_submission USING btree (task_id);


--
-- Name: main_submission_user_id_3808c258; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_submission_user_id_3808c258 ON public.main_submission USING btree (user_id);


--
-- Name: main_task_client_id_08588672; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_client_id_08588672 ON public.main_task USING btree (client_id);


--
-- Name: main_task_created_by_id_23ce62ed; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_created_by_id_23ce62ed ON public.main_task USING btree (created_by_id);


--
-- Name: main_task_level_1378e816; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_level_1378e816 ON public.main_task USING btree (level);


--
-- Name: main_task_lft_d860dd9c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_lft_d860dd9c ON public.main_task USING btree (lft);


--
-- Name: main_task_parent_id_129a5c2d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_parent_id_129a5c2d ON public.main_task USING btree (parent_id);


--
-- Name: main_task_rght_77203e01; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_rght_77203e01 ON public.main_task USING btree (rght);


--
-- Name: main_task_segment_rules_segmentrule_id_dc49fa6d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_segment_rules_segmentrule_id_dc49fa6d ON public.main_task_segment_rules USING btree (segmentrule_id);


--
-- Name: main_task_segment_rules_task_id_e14afcd9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_segment_rules_task_id_e14afcd9 ON public.main_task_segment_rules USING btree (task_id);


--
-- Name: main_task_target_content_type_id_716af254; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_target_content_type_id_716af254 ON public.main_task USING btree (target_content_type_id);


--
-- Name: main_task_target_object_id_a0e37746; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_target_object_id_a0e37746 ON public.main_task USING btree (target_object_id);


--
-- Name: main_task_tree_id_f8c4f751; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_tree_id_f8c4f751 ON public.main_task USING btree (tree_id);


--
-- Name: main_tasklocation_location_id_20c36cf6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_tasklocation_location_id_20c36cf6 ON public.main_tasklocation USING btree (location_id);


--
-- Name: main_tasklocation_task_id_6da926a5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_tasklocation_task_id_6da926a5 ON public.main_tasklocation USING btree (task_id);


--
-- Name: main_taskoccurrence_task_id_f53c5914; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_taskoccurrence_task_id_f53c5914 ON public.main_taskoccurrence USING btree (task_id);


--
-- Name: ona_instance_user_id_09ba67dc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ona_instance_user_id_09ba67dc ON public.ona_instance USING btree (user_id);


--
-- Name: ona_instance_xform_id_3965627d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ona_instance_xform_id_3965627d ON public.ona_instance USING btree (xform_id);


--
-- Name: ona_xform_id_string_7da3f9d4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ona_xform_id_string_7da3f9d4 ON public.ona_xform USING btree (id_string);


--
-- Name: ona_xform_id_string_7da3f9d4_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ona_xform_id_string_7da3f9d4_like ON public.ona_xform USING btree (id_string varchar_pattern_ops);


--
-- Name: ona_xform_project_id_24e668cc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ona_xform_project_id_24e668cc ON public.ona_xform USING btree (project_id);


--
-- Name: socialaccount_socialaccount_user_id_8146e70c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON public.socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_site_id_2579dee5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialapp_sites_site_id_2579dee5 ON public.socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_socialapp_id_97fb6e7d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialapp_sites_socialapp_id_97fb6e7d ON public.socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_account_id_951f210e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON public.socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_app_id_636a42d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON public.socialaccount_socialtoken USING btree (app_id);


--
-- Name: users_userprofile_national_id_fcf8cecc_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_userprofile_national_id_fcf8cecc_like ON public.users_userprofile USING btree (national_id varchar_pattern_ops);


--
-- Name: users_userprofile_ona_username_5607f10f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_userprofile_ona_username_5607f10f_like ON public.users_userprofile USING btree (ona_username varchar_pattern_ops);


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_bounty main_bounty_task_id_077b3eb2_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_bounty
    ADD CONSTRAINT main_bounty_task_id_077b3eb2_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_location main_location_location_type_id_49726352_fk_main_locationtype_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_location
    ADD CONSTRAINT main_location_location_type_id_49726352_fk_main_locationtype_id FOREIGN KEY (location_type_id) REFERENCES public.main_locationtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_location main_location_parent_id_0da80772_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_location
    ADD CONSTRAINT main_location_parent_id_0da80772_fk_main_location_id FOREIGN KEY (parent_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_project main_project_target_content_type__0a864095_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project
    ADD CONSTRAINT main_project_target_content_type__0a864095_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_project_tasks main_project_tasks_project_id_92c703dd_fk_main_project_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_project_id_92c703dd_fk_main_project_id FOREIGN KEY (project_id) REFERENCES public.main_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_project_tasks main_project_tasks_task_id_c5893bbe_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_task_id_c5893bbe_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_segmentrule main_segmentrule_target_content_type__0cfefa99_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_segmentrule
    ADD CONSTRAINT main_segmentrule_target_content_type__0cfefa99_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_bounty_id_92bff86b_fk_main_bounty_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_bounty_id_92bff86b_fk_main_bounty_id FOREIGN KEY (bounty_id) REFERENCES public.main_bounty(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_location_id_071c36e4_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_location_id_071c36e4_fk_main_location_id FOREIGN KEY (location_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_target_content_type__66f602f8_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_target_content_type__66f602f8_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_task_id_e97c36a1_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_task_id_e97c36a1_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_user_id_3808c258_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_user_id_3808c258_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_client_id_08588672_fk_main_client_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_client_id_08588672_fk_main_client_id FOREIGN KEY (client_id) REFERENCES public.main_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_created_by_id_23ce62ed_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_created_by_id_23ce62ed_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_parent_id_129a5c2d_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_parent_id_129a5c2d_fk_main_task_id FOREIGN KEY (parent_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_segment_rules main_task_segment_ru_segmentrule_id_dc49fa6d_fk_main_segm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_ru_segmentrule_id_dc49fa6d_fk_main_segm FOREIGN KEY (segmentrule_id) REFERENCES public.main_segmentrule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_segment_rules main_task_segment_rules_task_id_e14afcd9_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_rules_task_id_e14afcd9_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_target_content_type__716af254_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_target_content_type__716af254_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_tasklocation main_tasklocation_location_id_20c36cf6_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tasklocation
    ADD CONSTRAINT main_tasklocation_location_id_20c36cf6_fk_main_location_id FOREIGN KEY (location_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_tasklocation main_tasklocation_task_id_6da926a5_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_tasklocation
    ADD CONSTRAINT main_tasklocation_task_id_6da926a5_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_taskoccurrence main_taskoccurrence_task_id_f53c5914_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_taskoccurrence
    ADD CONSTRAINT main_taskoccurrence_task_id_f53c5914_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ona_instance ona_instance_user_id_09ba67dc_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_user_id_09ba67dc_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ona_instance ona_instance_xform_id_3965627d_fk_ona_xform_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_xform_id_3965627d_fk_ona_xform_id FOREIGN KEY (xform_id) REFERENCES public.ona_xform(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_site_id_2579dee5_fk_django_si; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc FOREIGN KEY (socialapp_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofile_user_id_87251ef1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_87251ef1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

