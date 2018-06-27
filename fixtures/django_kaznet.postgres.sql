--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)
-- Dumped by pg_dump version 10.4 (Ubuntu 10.4-0ubuntu0.18.04)

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
-- Name: account_emailaddress; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.account_emailaddress (
    id integer NOT NULL,
    email character varying(254) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.account_emailaddress OWNER TO sol;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.account_emailaddress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailaddress_id_seq OWNER TO sol;

--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.account_emailaddress_id_seq OWNED BY public.account_emailaddress.id;


--
-- Name: account_emailconfirmation; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.account_emailconfirmation (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sent timestamp with time zone,
    key character varying(64) NOT NULL,
    email_address_id integer NOT NULL
);


ALTER TABLE public.account_emailconfirmation OWNER TO sol;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.account_emailconfirmation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_emailconfirmation_id_seq OWNER TO sol;

--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.account_emailconfirmation_id_seq OWNED BY public.account_emailconfirmation.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO sol;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO sol;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO sol;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO sol;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO sol;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO sol;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.auth_user OWNER TO sol;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO sol;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO sol;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO sol;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO sol;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO sol;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO sol;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.django_admin_log OWNER TO sol;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO sol;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO sol;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO sol;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO sol;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO sol;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO sol;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO sol;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO sol;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: main_bounty; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.main_bounty (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    amount numeric(64,2) NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.main_bounty OWNER TO sol;

--
-- Name: main_bounty_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_bounty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_bounty_id_seq OWNER TO sol;

--
-- Name: main_bounty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_bounty_id_seq OWNED BY public.main_bounty.id;


--
-- Name: main_client; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.main_client (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.main_client OWNER TO sol;

--
-- Name: main_client_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_client_id_seq OWNER TO sol;

--
-- Name: main_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_client_id_seq OWNED BY public.main_client.id;


--
-- Name: main_location; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.main_location OWNER TO sol;

--
-- Name: main_location_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_location_id_seq OWNER TO sol;

--
-- Name: main_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_location_id_seq OWNED BY public.main_location.id;


--
-- Name: main_locationtype; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.main_locationtype (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.main_locationtype OWNER TO sol;

--
-- Name: main_locationtype_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_locationtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_locationtype_id_seq OWNER TO sol;

--
-- Name: main_locationtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_locationtype_id_seq OWNED BY public.main_locationtype.id;


--
-- Name: main_project; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.main_project OWNER TO sol;

--
-- Name: main_project_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_project_id_seq OWNER TO sol;

--
-- Name: main_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_project_id_seq OWNED BY public.main_project.id;


--
-- Name: main_project_tasks; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.main_project_tasks (
    id integer NOT NULL,
    project_id integer NOT NULL,
    task_id integer NOT NULL
);


ALTER TABLE public.main_project_tasks OWNER TO sol;

--
-- Name: main_project_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_project_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_project_tasks_id_seq OWNER TO sol;

--
-- Name: main_project_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_project_tasks_id_seq OWNED BY public.main_project_tasks.id;


--
-- Name: main_segmentrule; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.main_segmentrule OWNER TO sol;

--
-- Name: main_segmentrule_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_segmentrule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_segmentrule_id_seq OWNER TO sol;

--
-- Name: main_segmentrule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_segmentrule_id_seq OWNED BY public.main_segmentrule.id;


--
-- Name: main_submission; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.main_submission OWNER TO sol;

--
-- Name: main_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_submission_id_seq OWNER TO sol;

--
-- Name: main_submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_submission_id_seq OWNED BY public.main_submission.id;


--
-- Name: main_task; Type: TABLE; Schema: public; Owner: sol
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
    parent_id integer,
    target_content_type_id integer,
    CONSTRAINT main_task_level_check CHECK ((level >= 0)),
    CONSTRAINT main_task_lft_check CHECK ((lft >= 0)),
    CONSTRAINT main_task_rght_check CHECK ((rght >= 0)),
    CONSTRAINT main_task_target_object_id_check CHECK ((target_object_id >= 0)),
    CONSTRAINT main_task_tree_id_check CHECK ((tree_id >= 0))
);


ALTER TABLE public.main_task OWNER TO sol;

--
-- Name: main_task_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_task_id_seq OWNER TO sol;

--
-- Name: main_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_task_id_seq OWNED BY public.main_task.id;


--
-- Name: main_task_locations; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.main_task_locations (
    id integer NOT NULL,
    task_id integer NOT NULL,
    location_id integer NOT NULL
);


ALTER TABLE public.main_task_locations OWNER TO sol;

--
-- Name: main_task_locations_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_task_locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_task_locations_id_seq OWNER TO sol;

--
-- Name: main_task_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_task_locations_id_seq OWNED BY public.main_task_locations.id;


--
-- Name: main_task_segment_rules; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.main_task_segment_rules (
    id integer NOT NULL,
    task_id integer NOT NULL,
    segmentrule_id integer NOT NULL
);


ALTER TABLE public.main_task_segment_rules OWNER TO sol;

--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_task_segment_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_task_segment_rules_id_seq OWNER TO sol;

--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_task_segment_rules_id_seq OWNED BY public.main_task_segment_rules.id;


--
-- Name: main_taskoccurrence; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.main_taskoccurrence OWNER TO sol;

--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.main_taskoccurrence_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_taskoccurrence_id_seq OWNER TO sol;

--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.main_taskoccurrence_id_seq OWNED BY public.main_taskoccurrence.id;


--
-- Name: ona_instance; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.ona_instance OWNER TO sol;

--
-- Name: ona_instance_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.ona_instance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ona_instance_id_seq OWNER TO sol;

--
-- Name: ona_instance_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.ona_instance_id_seq OWNED BY public.ona_instance.id;


--
-- Name: ona_project; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.ona_project OWNER TO sol;

--
-- Name: ona_project_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.ona_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ona_project_id_seq OWNER TO sol;

--
-- Name: ona_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.ona_project_id_seq OWNED BY public.ona_project.id;


--
-- Name: ona_xform; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.ona_xform OWNER TO sol;

--
-- Name: ona_xform_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.ona_xform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ona_xform_id_seq OWNER TO sol;

--
-- Name: ona_xform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.ona_xform_id_seq OWNED BY public.ona_xform.id;


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.socialaccount_socialaccount OWNER TO sol;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.socialaccount_socialaccount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialaccount_id_seq OWNER TO sol;

--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.socialaccount_socialaccount_id_seq OWNED BY public.socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialapp; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.socialaccount_socialapp (
    id integer NOT NULL,
    provider character varying(30) NOT NULL,
    name character varying(40) NOT NULL,
    client_id character varying(191) NOT NULL,
    secret character varying(191) NOT NULL,
    key character varying(191) NOT NULL
);


ALTER TABLE public.socialaccount_socialapp OWNER TO sol;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.socialaccount_socialapp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialapp_id_seq OWNER TO sol;

--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.socialaccount_socialapp_id_seq OWNED BY public.socialaccount_socialapp.id;


--
-- Name: socialaccount_socialapp_sites; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.socialaccount_socialapp_sites (
    id integer NOT NULL,
    socialapp_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialapp_sites OWNER TO sol;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.socialaccount_socialapp_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialapp_sites_id_seq OWNER TO sol;

--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.socialaccount_socialapp_sites_id_seq OWNED BY public.socialaccount_socialapp_sites.id;


--
-- Name: socialaccount_socialtoken; Type: TABLE; Schema: public; Owner: sol
--

CREATE TABLE public.socialaccount_socialtoken (
    id integer NOT NULL,
    token text NOT NULL,
    token_secret text NOT NULL,
    expires_at timestamp with time zone,
    account_id integer NOT NULL,
    app_id integer NOT NULL
);


ALTER TABLE public.socialaccount_socialtoken OWNER TO sol;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.socialaccount_socialtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.socialaccount_socialtoken_id_seq OWNER TO sol;

--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.socialaccount_socialtoken_id_seq OWNED BY public.socialaccount_socialtoken.id;


--
-- Name: users_userprofile; Type: TABLE; Schema: public; Owner: sol
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


ALTER TABLE public.users_userprofile OWNER TO sol;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: sol
--

CREATE SEQUENCE public.users_userprofile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_userprofile_id_seq OWNER TO sol;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sol
--

ALTER SEQUENCE public.users_userprofile_id_seq OWNED BY public.users_userprofile.id;


--
-- Name: account_emailaddress id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailaddress ALTER COLUMN id SET DEFAULT nextval('public.account_emailaddress_id_seq'::regclass);


--
-- Name: account_emailconfirmation id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('public.account_emailconfirmation_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: main_bounty id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_bounty ALTER COLUMN id SET DEFAULT nextval('public.main_bounty_id_seq'::regclass);


--
-- Name: main_client id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_client ALTER COLUMN id SET DEFAULT nextval('public.main_client_id_seq'::regclass);


--
-- Name: main_location id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_location ALTER COLUMN id SET DEFAULT nextval('public.main_location_id_seq'::regclass);


--
-- Name: main_locationtype id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_locationtype ALTER COLUMN id SET DEFAULT nextval('public.main_locationtype_id_seq'::regclass);


--
-- Name: main_project id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project ALTER COLUMN id SET DEFAULT nextval('public.main_project_id_seq'::regclass);


--
-- Name: main_project_tasks id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project_tasks ALTER COLUMN id SET DEFAULT nextval('public.main_project_tasks_id_seq'::regclass);


--
-- Name: main_segmentrule id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_segmentrule ALTER COLUMN id SET DEFAULT nextval('public.main_segmentrule_id_seq'::regclass);


--
-- Name: main_submission id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission ALTER COLUMN id SET DEFAULT nextval('public.main_submission_id_seq'::regclass);


--
-- Name: main_task id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task ALTER COLUMN id SET DEFAULT nextval('public.main_task_id_seq'::regclass);


--
-- Name: main_task_locations id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_locations ALTER COLUMN id SET DEFAULT nextval('public.main_task_locations_id_seq'::regclass);


--
-- Name: main_task_segment_rules id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_segment_rules ALTER COLUMN id SET DEFAULT nextval('public.main_task_segment_rules_id_seq'::regclass);


--
-- Name: main_taskoccurrence id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_taskoccurrence ALTER COLUMN id SET DEFAULT nextval('public.main_taskoccurrence_id_seq'::regclass);


--
-- Name: ona_instance id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_instance ALTER COLUMN id SET DEFAULT nextval('public.ona_instance_id_seq'::regclass);


--
-- Name: ona_project id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_project ALTER COLUMN id SET DEFAULT nextval('public.ona_project_id_seq'::regclass);


--
-- Name: ona_xform id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_xform ALTER COLUMN id SET DEFAULT nextval('public.ona_xform_id_seq'::regclass);


--
-- Name: socialaccount_socialaccount id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: socialaccount_socialapp id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_id_seq'::regclass);


--
-- Name: socialaccount_socialapp_sites id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialapp_sites_id_seq'::regclass);


--
-- Name: socialaccount_socialtoken id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialtoken ALTER COLUMN id SET DEFAULT nextval('public.socialaccount_socialtoken_id_seq'::regclass);


--
-- Name: users_userprofile id; Type: DEFAULT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile ALTER COLUMN id SET DEFAULT nextval('public.users_userprofile_id_seq'::regclass);


--
-- Data for Name: account_emailaddress; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.account_emailaddress (id, email, verified, "primary", user_id) FROM stdin;
\.


--
-- Data for Name: account_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.account_emailconfirmation (id, created, sent, key, email_address_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: sol
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
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$100000$crp64mZ83aj6$UVR//QS5Kr6IfzfvuuzGT3cO2CwSqgKzYLgZDlwqlXw=	2018-06-27 15:06:45+03	t	sol	Davis	Raymond	sol@admin.me	t	t	2018-06-27 15:06:29+03
3	pbkdf2_sha256$100000$uCQ6w3jJr81E$mz0/T7M7hP2c09Ox/rjQCkSJqzOjuxKI7UTCI96vtjE=	\N	t	onauser	Ona	User		f	t	2018-06-27 15:08:09+03
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
afba84d36d7279ac1f104ddbfbea348a36779610	2018-06-27 15:06:29.129617+03	1
3164da5d8e34b52370e426065b8d42ed3c992424	2018-06-27 15:08:09.535924+03	3
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: sol
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
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: sol
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
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: sol
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
18	main	0001_initial	2018-06-27 15:05:56.793162+03
19	ona	0001_initial	2018-06-27 15:05:56.96471+03
20	sessions	0001_initial	2018-06-27 15:05:56.994692+03
21	sites	0001_initial	2018-06-27 15:05:57.008801+03
22	sites	0002_alter_domain_unique	2018-06-27 15:05:57.027277+03
23	socialaccount	0001_initial	2018-06-27 15:05:57.195465+03
24	socialaccount	0002_token_max_lengths	2018-06-27 15:05:57.285625+03
25	socialaccount	0003_extra_data_default_dict	2018-06-27 15:05:57.296713+03
26	users	0001_initial	2018-06-27 15:05:57.40772+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
feaqmcs1cob55jw2dsb425dj1g8k2typ	YWY4Y2Y3MzgzZWZhMzk5N2Q3OTc1MjlmYmVjMGE2ZWFmODgwY2NlNjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2NTEwY2ZkNTg2NmYzYzc0Njc1ODY5OWY5ZGM2MTE0YjNlOGMxMDVhIn0=	2018-07-11 15:06:45.651222+03
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: main_bounty; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_bounty (id, created, amount, task_id) FROM stdin;
\.


--
-- Data for Name: main_client; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_client (id, created, modified, name) FROM stdin;
1	2018-06-27 15:15:45.743001+03	2018-06-27 15:15:45.743021+03	Client1
2	2018-06-27 15:15:48.464778+03	2018-06-27 15:15:48.464798+03	Client2
3	2018-06-27 15:15:50.783372+03	2018-06-27 15:15:50.783398+03	Client3
4	2018-06-27 15:15:53.411336+03	2018-06-27 15:15:53.411356+03	Client4
5	2018-06-27 15:15:55.687348+03	2018-06-27 15:15:55.687367+03	Client5
6	2018-06-27 15:15:57.980725+03	2018-06-27 15:15:57.980748+03	Client6
7	2018-06-27 15:16:01.760373+03	2018-06-27 15:16:01.760393+03	Client7
8	2018-06-27 15:16:21.866839+03	2018-06-27 15:16:21.866859+03	Client8
9	2018-06-27 15:16:26.639508+03	2018-06-27 15:16:26.639528+03	Client9
10	2018-06-27 15:16:29.466603+03	2018-06-27 15:16:29.466622+03	Client10
\.


--
-- Data for Name: main_location; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_location (id, created, modified, name, country, geopoint, radius, shapefile, description, lft, rght, tree_id, level, location_type_id, parent_id) FROM stdin;
1	2018-06-27 15:20:48.271943+03	2018-06-27 15:20:48.271967+03	Nairobi	KE	\N	\N	\N	Nairobi is so HUGE!!!!! I can't even remember where i live.	1	4	1	0	1	\N
2	2018-06-27 15:21:53.61901+03	2018-06-27 15:21:53.619053+03	Hurlingham	KE	\N	\N	\N	Part of nairobi	2	3	1	1	2	1
\.


--
-- Data for Name: main_locationtype; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_locationtype (id, created, modified, name) FROM stdin;
1	2018-06-27 15:20:47.053706+03	2018-06-27 15:20:47.053727+03	City
2	2018-06-27 15:21:52.146571+03	2018-06-27 15:21:52.146594+03	Area
\.


--
-- Data for Name: main_project; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_project (id, created, modified, target_object_id, name, target_content_type_id) FROM stdin;
\.


--
-- Data for Name: main_project_tasks; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_project_tasks (id, project_id, task_id) FROM stdin;
\.


--
-- Data for Name: main_segmentrule; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_segmentrule (id, created, modified, name, description, target_field, target_field_value, active, target_content_type_id) FROM stdin;
\.


--
-- Data for Name: main_submission; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_submission (id, created, modified, target_object_id, submission_time, valid, status, comments, bounty_id, location_id, target_content_type_id, task_id, user_id) FROM stdin;
\.


--
-- Data for Name: main_task; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_task (id, created, modified, target_object_id, name, description, start, "end", timing_rule, total_submission_target, user_submission_target, status, estimated_time, required_expertise, lft, rght, tree_id, level, client_id, parent_id, target_content_type_id) FROM stdin;
1	2018-06-27 15:14:42.953615+03	2018-06-27 15:14:42.953642+03	2	Awesome Task	Super Awesome Task!!!!!!!!!!!!!	2018-06-27 12:00:00+03	2018-06-27 12:00:00+03	\N	\N	100	a	00:10:00	3	1	2	1	0	\N	\N	16
2	2018-06-27 15:15:19.790924+03	2018-06-27 15:15:19.790962+03	\N	Awesomeness in Progress	Super Task	2018-06-27 12:00:00+03	2018-06-27 12:00:00+03	\N	\N	10	d	00:15:00	1	1	2	2	0	\N	\N	16
\.


--
-- Data for Name: main_task_locations; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_task_locations (id, task_id, location_id) FROM stdin;
\.


--
-- Data for Name: main_task_segment_rules; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_task_segment_rules (id, task_id, segmentrule_id) FROM stdin;
\.


--
-- Data for Name: main_taskoccurrence; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_taskoccurrence (id, created, modified, date, start_time, end_time, task_id) FROM stdin;
\.


--
-- Data for Name: ona_instance; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.ona_instance (id, created, modified, ona_pk, json, deleted_at, last_updated, user_id, xform_id) FROM stdin;
\.


--
-- Data for Name: ona_project; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.ona_project (id, created, modified, ona_pk, organization, name, deleted_at, last_updated) FROM stdin;
\.


--
-- Data for Name: ona_xform; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.ona_xform (id, created, modified, ona_pk, project_id, title, id_string, deleted_at, last_updated) FROM stdin;
1	2018-06-27 15:09:28.235285+03	2018-06-27 15:09:28.235321+03	8949	6083	Form1	Hf0NStRnXYre2VKiDqgf-VlJ9hVSfZdoFT8lbneTSKurscWybsxH8T4hmfQ-in6ZVhRHSxengHqPJ-ssoc1Hg6VCa-8S8q0P8WzK	\N	\N
2	2018-06-27 15:09:30.232453+03	2018-06-27 15:09:30.232515+03	2849	3129	Form2	lRIstdPX9RYXqjxM5sTCvBJ-PVpMJwNUXP3ZQlEeJ-dT1nE3s7cuUfI7ZTiUMxK1bVK-mgRjLBQEbZoXFrYO1Hx9Re8bbHVQf_xy	\N	\N
3	2018-06-27 15:09:32.754463+03	2018-06-27 15:09:32.75452+03	3273	2779	Form3	i2yKINGC8EXUPlbMZ2PWyDxmocEisJfbmnSjSuZe_1av2R_n4B7rlEa9LSHjgE8FjUBYDnVw2Hi4CjSk_nGKZVZy5LeXetm3YGAP	\N	\N
4	2018-06-27 15:09:34.454346+03	2018-06-27 15:09:34.454379+03	733	1357	Form4	X3MvgAL-ehjt0cU0E1d6mv29dIUlsjeUNjsSpb08xl7t8k4mYLVAmBLXroodidDFwqWhghV7U9Es_BAJXK1Z27_9jrmF8X-Ppq6v	\N	\N
5	2018-06-27 15:09:36.282385+03	2018-06-27 15:09:36.282413+03	7699	9899	Form5	F7ttwaUrFXK-KUluLoCrA_2F_iCnHxjcqYiskwsHKU_axhTU2rRoRNWYmGK5bv_Vv-Hk40MO1P2Vqfew1I0pgMK35PUENxlXjaiB	\N	\N
\.


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.socialaccount_socialaccount (id, provider, uid, last_login, date_joined, extra_data, user_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialapp; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.socialaccount_socialapp (id, provider, name, client_id, secret, key) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialapp_sites; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.socialaccount_socialapp_sites (id, socialapp_id, site_id) FROM stdin;
\.


--
-- Data for Name: socialaccount_socialtoken; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.socialaccount_socialtoken (id, token, token_secret, expires_at, account_id, app_id) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: users_userprofile; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.users_userprofile (id, created, modified, ona_pk, ona_username, national_id, payment_number, phone_number, role, expertise, gender, user_id) FROM stdin;
1	2018-06-27 15:06:29.120453+03	2018-06-27 15:07:19.190802+03	\N	\N	\N			1	3	1	1
4	2018-06-27 15:08:09.531149+03	2018-06-27 15:10:20.050217+03	\N	onauser	\N			1	4	0	3
\.


--
-- Name: account_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.account_emailaddress_id_seq', 1, false);


--
-- Name: account_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.account_emailconfirmation_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 78, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 3, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 17, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 26, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 26, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: main_bounty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_bounty_id_seq', 1, false);


--
-- Name: main_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_client_id_seq', 10, true);


--
-- Name: main_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_location_id_seq', 2, true);


--
-- Name: main_locationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_locationtype_id_seq', 2, true);


--
-- Name: main_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_project_id_seq', 1, false);


--
-- Name: main_project_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_project_tasks_id_seq', 1, false);


--
-- Name: main_segmentrule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_segmentrule_id_seq', 1, false);


--
-- Name: main_submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_submission_id_seq', 1, false);


--
-- Name: main_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_task_id_seq', 2, true);


--
-- Name: main_task_locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_task_locations_id_seq', 1, false);


--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_task_segment_rules_id_seq', 1, false);


--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_taskoccurrence_id_seq', 1, false);


--
-- Name: ona_instance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.ona_instance_id_seq', 1, false);


--
-- Name: ona_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.ona_project_id_seq', 1, false);


--
-- Name: ona_xform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.ona_xform_id_seq', 5, true);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.socialaccount_socialaccount_id_seq', 1, false);


--
-- Name: socialaccount_socialapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_id_seq', 1, false);


--
-- Name: socialaccount_socialapp_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.socialaccount_socialapp_sites_id_seq', 1, false);


--
-- Name: socialaccount_socialtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.socialaccount_socialtoken_id_seq', 1, false);


--
-- Name: users_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.users_userprofile_id_seq', 4, true);


--
-- Name: account_emailaddress account_emailaddress_email_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_email_key UNIQUE (email);


--
-- Name: account_emailaddress account_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: account_emailconfirmation account_emailconfirmation_key_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_key_key UNIQUE (key);


--
-- Name: account_emailconfirmation account_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: main_bounty main_bounty_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_bounty
    ADD CONSTRAINT main_bounty_pkey PRIMARY KEY (id);


--
-- Name: main_client main_client_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_client
    ADD CONSTRAINT main_client_pkey PRIMARY KEY (id);


--
-- Name: main_location main_location_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_location
    ADD CONSTRAINT main_location_pkey PRIMARY KEY (id);


--
-- Name: main_locationtype main_locationtype_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_locationtype
    ADD CONSTRAINT main_locationtype_pkey PRIMARY KEY (id);


--
-- Name: main_project main_project_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project
    ADD CONSTRAINT main_project_pkey PRIMARY KEY (id);


--
-- Name: main_project_tasks main_project_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_pkey PRIMARY KEY (id);


--
-- Name: main_project_tasks main_project_tasks_project_id_task_id_4aa4886c_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_project_id_task_id_4aa4886c_uniq UNIQUE (project_id, task_id);


--
-- Name: main_segmentrule main_segmentrule_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_segmentrule
    ADD CONSTRAINT main_segmentrule_pkey PRIMARY KEY (id);


--
-- Name: main_submission main_submission_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_pkey PRIMARY KEY (id);


--
-- Name: main_task_locations main_task_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_pkey PRIMARY KEY (id);


--
-- Name: main_task_locations main_task_locations_task_id_location_id_51dc375b_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_task_id_location_id_51dc375b_uniq UNIQUE (task_id, location_id);


--
-- Name: main_task main_task_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_pkey PRIMARY KEY (id);


--
-- Name: main_task_segment_rules main_task_segment_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_rules_pkey PRIMARY KEY (id);


--
-- Name: main_task_segment_rules main_task_segment_rules_task_id_segmentrule_id_e2dcafd6_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_rules_task_id_segmentrule_id_e2dcafd6_uniq UNIQUE (task_id, segmentrule_id);


--
-- Name: main_taskoccurrence main_taskoccurrence_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_taskoccurrence
    ADD CONSTRAINT main_taskoccurrence_pkey PRIMARY KEY (id);


--
-- Name: ona_instance ona_instance_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_ona_pk_key UNIQUE (ona_pk);


--
-- Name: ona_instance ona_instance_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_pkey PRIMARY KEY (id);


--
-- Name: ona_project ona_project_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_project
    ADD CONSTRAINT ona_project_ona_pk_key UNIQUE (ona_pk);


--
-- Name: ona_project ona_project_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_project
    ADD CONSTRAINT ona_project_pkey PRIMARY KEY (id);


--
-- Name: ona_xform ona_xform_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_xform
    ADD CONSTRAINT ona_xform_ona_pk_key UNIQUE (ona_pk);


--
-- Name: ona_xform ona_xform_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_xform
    ADD CONSTRAINT ona_xform_pkey PRIMARY KEY (id);


--
-- Name: ona_xform ona_xform_project_id_id_string_609aa2ea_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_xform
    ADD CONSTRAINT ona_xform_project_id_id_string_609aa2ea_uniq UNIQUE (project_id, id_string);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_provider_uid_fc810c6e_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_provider_uid_fc810c6e_uniq UNIQUE (provider, uid);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp__socialapp_id_site_id_71a9a768_uniq UNIQUE (socialapp_id, site_id);


--
-- Name: socialaccount_socialapp socialaccount_socialapp_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp
    ADD CONSTRAINT socialaccount_socialapp_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialapp_sites socialaccount_socialapp_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_socialapp_sites_pkey PRIMARY KEY (id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq UNIQUE (app_id, account_id);


--
-- Name: socialaccount_socialtoken socialaccount_socialtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_socialtoken_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_national_id_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_national_id_key UNIQUE (national_id);


--
-- Name: users_userprofile users_userprofile_ona_pk_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_ona_pk_key UNIQUE (ona_pk);


--
-- Name: users_userprofile users_userprofile_ona_username_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_ona_username_key UNIQUE (ona_username);


--
-- Name: users_userprofile users_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile users_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: account_emailaddress_email_03be32b2_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX account_emailaddress_email_03be32b2_like ON public.account_emailaddress USING btree (email varchar_pattern_ops);


--
-- Name: account_emailaddress_user_id_2c513194; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX account_emailaddress_user_id_2c513194 ON public.account_emailaddress USING btree (user_id);


--
-- Name: account_emailconfirmation_email_address_id_5b7f8c58; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON public.account_emailconfirmation USING btree (email_address_id);


--
-- Name: account_emailconfirmation_key_f43612bd_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX account_emailconfirmation_key_f43612bd_like ON public.account_emailconfirmation USING btree (key varchar_pattern_ops);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: main_bounty_task_id_077b3eb2; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_bounty_task_id_077b3eb2 ON public.main_bounty USING btree (task_id);


--
-- Name: main_location_geopoint_id; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_geopoint_id ON public.main_location USING gist (geopoint);


--
-- Name: main_location_level_b4e5d7ac; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_level_b4e5d7ac ON public.main_location USING btree (level);


--
-- Name: main_location_lft_236ba59c; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_lft_236ba59c ON public.main_location USING btree (lft);


--
-- Name: main_location_location_type_id_49726352; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_location_type_id_49726352 ON public.main_location USING btree (location_type_id);


--
-- Name: main_location_parent_id_0da80772; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_parent_id_0da80772 ON public.main_location USING btree (parent_id);


--
-- Name: main_location_rght_5b068c79; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_rght_5b068c79 ON public.main_location USING btree (rght);


--
-- Name: main_location_shapefile_id; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_shapefile_id ON public.main_location USING gist (shapefile);


--
-- Name: main_location_tree_id_38352621; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_location_tree_id_38352621 ON public.main_location USING btree (tree_id);


--
-- Name: main_project_target_content_type_id_0a864095; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_project_target_content_type_id_0a864095 ON public.main_project USING btree (target_content_type_id);


--
-- Name: main_project_target_object_id_2b8de976; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_project_target_object_id_2b8de976 ON public.main_project USING btree (target_object_id);


--
-- Name: main_project_tasks_project_id_92c703dd; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_project_tasks_project_id_92c703dd ON public.main_project_tasks USING btree (project_id);


--
-- Name: main_project_tasks_task_id_c5893bbe; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_project_tasks_task_id_c5893bbe ON public.main_project_tasks USING btree (task_id);


--
-- Name: main_segmentrule_target_content_type_id_0cfefa99; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_segmentrule_target_content_type_id_0cfefa99 ON public.main_segmentrule USING btree (target_content_type_id);


--
-- Name: main_segmentrule_target_field_ac9dd2fc; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_segmentrule_target_field_ac9dd2fc ON public.main_segmentrule USING btree (target_field);


--
-- Name: main_segmentrule_target_field_ac9dd2fc_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_segmentrule_target_field_ac9dd2fc_like ON public.main_segmentrule USING btree (target_field varchar_pattern_ops);


--
-- Name: main_submission_bounty_id_92bff86b; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_submission_bounty_id_92bff86b ON public.main_submission USING btree (bounty_id);


--
-- Name: main_submission_location_id_071c36e4; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_submission_location_id_071c36e4 ON public.main_submission USING btree (location_id);


--
-- Name: main_submission_target_content_type_id_66f602f8; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_submission_target_content_type_id_66f602f8 ON public.main_submission USING btree (target_content_type_id);


--
-- Name: main_submission_target_object_id_11b5ca32; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_submission_target_object_id_11b5ca32 ON public.main_submission USING btree (target_object_id);


--
-- Name: main_submission_task_id_e97c36a1; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_submission_task_id_e97c36a1 ON public.main_submission USING btree (task_id);


--
-- Name: main_submission_user_id_3808c258; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_submission_user_id_3808c258 ON public.main_submission USING btree (user_id);


--
-- Name: main_task_client_id_08588672; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_client_id_08588672 ON public.main_task USING btree (client_id);


--
-- Name: main_task_level_1378e816; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_level_1378e816 ON public.main_task USING btree (level);


--
-- Name: main_task_lft_d860dd9c; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_lft_d860dd9c ON public.main_task USING btree (lft);


--
-- Name: main_task_locations_location_id_fb7e3064; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_locations_location_id_fb7e3064 ON public.main_task_locations USING btree (location_id);


--
-- Name: main_task_locations_task_id_39f2e68a; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_locations_task_id_39f2e68a ON public.main_task_locations USING btree (task_id);


--
-- Name: main_task_parent_id_129a5c2d; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_parent_id_129a5c2d ON public.main_task USING btree (parent_id);


--
-- Name: main_task_rght_77203e01; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_rght_77203e01 ON public.main_task USING btree (rght);


--
-- Name: main_task_segment_rules_segmentrule_id_dc49fa6d; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_segment_rules_segmentrule_id_dc49fa6d ON public.main_task_segment_rules USING btree (segmentrule_id);


--
-- Name: main_task_segment_rules_task_id_e14afcd9; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_segment_rules_task_id_e14afcd9 ON public.main_task_segment_rules USING btree (task_id);


--
-- Name: main_task_target_content_type_id_716af254; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_target_content_type_id_716af254 ON public.main_task USING btree (target_content_type_id);


--
-- Name: main_task_target_object_id_a0e37746; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_target_object_id_a0e37746 ON public.main_task USING btree (target_object_id);


--
-- Name: main_task_tree_id_f8c4f751; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_tree_id_f8c4f751 ON public.main_task USING btree (tree_id);


--
-- Name: main_taskoccurrence_task_id_f53c5914; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_taskoccurrence_task_id_f53c5914 ON public.main_taskoccurrence USING btree (task_id);


--
-- Name: ona_instance_user_id_09ba67dc; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX ona_instance_user_id_09ba67dc ON public.ona_instance USING btree (user_id);


--
-- Name: ona_instance_xform_id_3965627d; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX ona_instance_xform_id_3965627d ON public.ona_instance USING btree (xform_id);


--
-- Name: ona_xform_id_string_7da3f9d4; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX ona_xform_id_string_7da3f9d4 ON public.ona_xform USING btree (id_string);


--
-- Name: ona_xform_id_string_7da3f9d4_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX ona_xform_id_string_7da3f9d4_like ON public.ona_xform USING btree (id_string varchar_pattern_ops);


--
-- Name: ona_xform_project_id_24e668cc; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX ona_xform_project_id_24e668cc ON public.ona_xform USING btree (project_id);


--
-- Name: socialaccount_socialaccount_user_id_8146e70c; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX socialaccount_socialaccount_user_id_8146e70c ON public.socialaccount_socialaccount USING btree (user_id);


--
-- Name: socialaccount_socialapp_sites_site_id_2579dee5; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX socialaccount_socialapp_sites_site_id_2579dee5 ON public.socialaccount_socialapp_sites USING btree (site_id);


--
-- Name: socialaccount_socialapp_sites_socialapp_id_97fb6e7d; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX socialaccount_socialapp_sites_socialapp_id_97fb6e7d ON public.socialaccount_socialapp_sites USING btree (socialapp_id);


--
-- Name: socialaccount_socialtoken_account_id_951f210e; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX socialaccount_socialtoken_account_id_951f210e ON public.socialaccount_socialtoken USING btree (account_id);


--
-- Name: socialaccount_socialtoken_app_id_636a42d7; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX socialaccount_socialtoken_app_id_636a42d7 ON public.socialaccount_socialtoken USING btree (app_id);


--
-- Name: users_userprofile_national_id_fcf8cecc_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX users_userprofile_national_id_fcf8cecc_like ON public.users_userprofile USING btree (national_id varchar_pattern_ops);


--
-- Name: users_userprofile_ona_username_5607f10f_like; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX users_userprofile_ona_username_5607f10f_like ON public.users_userprofile USING btree (ona_username varchar_pattern_ops);


--
-- Name: account_emailaddress account_emailaddress_user_id_2c513194_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailaddress
    ADD CONSTRAINT account_emailaddress_user_id_2c513194_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_emailconfirmation account_emailconfirm_email_address_id_5b7f8c58_fk_account_e; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.account_emailconfirmation
    ADD CONSTRAINT account_emailconfirm_email_address_id_5b7f8c58_fk_account_e FOREIGN KEY (email_address_id) REFERENCES public.account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_bounty main_bounty_task_id_077b3eb2_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_bounty
    ADD CONSTRAINT main_bounty_task_id_077b3eb2_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_location main_location_location_type_id_49726352_fk_main_locationtype_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_location
    ADD CONSTRAINT main_location_location_type_id_49726352_fk_main_locationtype_id FOREIGN KEY (location_type_id) REFERENCES public.main_locationtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_location main_location_parent_id_0da80772_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_location
    ADD CONSTRAINT main_location_parent_id_0da80772_fk_main_location_id FOREIGN KEY (parent_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_project main_project_target_content_type__0a864095_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project
    ADD CONSTRAINT main_project_target_content_type__0a864095_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_project_tasks main_project_tasks_project_id_92c703dd_fk_main_project_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_project_id_92c703dd_fk_main_project_id FOREIGN KEY (project_id) REFERENCES public.main_project(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_project_tasks main_project_tasks_task_id_c5893bbe_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_project_tasks
    ADD CONSTRAINT main_project_tasks_task_id_c5893bbe_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_segmentrule main_segmentrule_target_content_type__0cfefa99_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_segmentrule
    ADD CONSTRAINT main_segmentrule_target_content_type__0cfefa99_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_bounty_id_92bff86b_fk_main_bounty_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_bounty_id_92bff86b_fk_main_bounty_id FOREIGN KEY (bounty_id) REFERENCES public.main_bounty(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_location_id_071c36e4_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_location_id_071c36e4_fk_main_location_id FOREIGN KEY (location_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_target_content_type__66f602f8_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_target_content_type__66f602f8_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_task_id_e97c36a1_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_task_id_e97c36a1_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_submission main_submission_user_id_3808c258_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_submission
    ADD CONSTRAINT main_submission_user_id_3808c258_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_client_id_08588672_fk_main_client_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_client_id_08588672_fk_main_client_id FOREIGN KEY (client_id) REFERENCES public.main_client(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_locations main_task_locations_location_id_fb7e3064_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_location_id_fb7e3064_fk_main_location_id FOREIGN KEY (location_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_locations main_task_locations_task_id_39f2e68a_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_task_id_39f2e68a_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_parent_id_129a5c2d_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_parent_id_129a5c2d_fk_main_task_id FOREIGN KEY (parent_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_segment_rules main_task_segment_ru_segmentrule_id_dc49fa6d_fk_main_segm; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_ru_segmentrule_id_dc49fa6d_fk_main_segm FOREIGN KEY (segmentrule_id) REFERENCES public.main_segmentrule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_segment_rules main_task_segment_rules_task_id_e14afcd9_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task_segment_rules
    ADD CONSTRAINT main_task_segment_rules_task_id_e14afcd9_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task main_task_target_content_type__716af254_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_target_content_type__716af254_fk_django_co FOREIGN KEY (target_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_taskoccurrence main_taskoccurrence_task_id_f53c5914_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_taskoccurrence
    ADD CONSTRAINT main_taskoccurrence_task_id_f53c5914_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ona_instance ona_instance_user_id_09ba67dc_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_user_id_09ba67dc_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ona_instance ona_instance_xform_id_3965627d_fk_ona_xform_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.ona_instance
    ADD CONSTRAINT ona_instance_xform_id_3965627d_fk_ona_xform_id FOREIGN KEY (xform_id) REFERENCES public.ona_xform(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_account_id_951f210e_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_account_id_951f210e_fk_socialacc FOREIGN KEY (account_id) REFERENCES public.socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialtoken socialaccount_social_app_id_636a42d7_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialtoken
    ADD CONSTRAINT socialaccount_social_app_id_636a42d7_fk_socialacc FOREIGN KEY (app_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_site_id_2579dee5_fk_django_si; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_site_id_2579dee5_fk_django_si FOREIGN KEY (site_id) REFERENCES public.django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialapp_sites socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialapp_sites
    ADD CONSTRAINT socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc FOREIGN KEY (socialapp_id) REFERENCES public.socialaccount_socialapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_socialaccount socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_userprofile users_userprofile_user_id_87251ef1_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_87251ef1_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

