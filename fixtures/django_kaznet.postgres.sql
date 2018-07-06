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
    created_by_id integer,
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
1	pbkdf2_sha256$100000$t2ldQTfP2v52$lpizsStCy78Onaf/L+s4t9wlGpIjYLDg3D5MoM58CXo=	2018-07-06 10:29:16+03	t	sol	Davis	Raymond	sol@admin.me	t	t	2018-07-06 10:24:37+03
3	pbkdf2_sha256$100000$3ILIY69wqN1i$4tyBxiRGp62IWTicjXItsraf1iuUNN3r8k01rhIoyeI=	2018-07-06 10:31:50+03	t	onauser	Ona	User	ona@test.me	t	t	2018-07-06 10:31:28+03
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
d4451494908a73745770a880097b451984e78719	2018-07-06 10:24:37.657578+03	1
a068bf9af441dcb308d2ee51295d548218757bc5	2018-07-06 10:31:29.057849+03	3
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2018-07-06 10:30:46.576366+03	1	sol	2	[{"changed": {"fields": ["first_name", "last_name"]}}, {"changed": {"name": "Profile", "object": "Davis Raymond's profile", "fields": ["ona_username", "national_id", "payment_number", "phone_number", "role", "expertise", "gender"]}}]	4	1
2	2018-07-06 10:32:12.638188+03	3	onauser	2	[{"changed": {"fields": ["first_name", "last_name", "last_login"]}}, {"changed": {"name": "Profile", "object": "Ona User's profile", "fields": ["ona_username", "national_id", "payment_number", "phone_number", "role", "expertise"]}}]	4	1
3	2018-07-06 10:36:44.398877+03	1	City	1	[{"added": {}}]	20	1
4	2018-07-06 10:36:45.648653+03	1	Kenya - Nairobi	1	[{"added": {}}]	19	1
5	2018-07-06 10:37:37.434437+03	2	Area	1	[{"added": {}}]	20	1
6	2018-07-06 10:37:38.702024+03	2	Kenya - Hurlingham	1	[{"added": {}}]	19	1
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
1	contenttypes	0001_initial	2018-07-06 10:24:00.892531+03
2	auth	0001_initial	2018-07-06 10:24:01.117983+03
3	account	0001_initial	2018-07-06 10:24:01.207121+03
4	account	0002_email_max_length	2018-07-06 10:24:01.229349+03
5	admin	0001_initial	2018-07-06 10:24:01.27298+03
6	admin	0002_logentry_remove_auto_add	2018-07-06 10:24:01.286924+03
7	contenttypes	0002_remove_content_type_name	2018-07-06 10:24:01.336317+03
8	auth	0002_alter_permission_name_max_length	2018-07-06 10:24:01.346129+03
9	auth	0003_alter_user_email_max_length	2018-07-06 10:24:01.361633+03
10	auth	0004_alter_user_username_opts	2018-07-06 10:24:01.376558+03
11	auth	0005_alter_user_last_login_null	2018-07-06 10:24:01.393259+03
12	auth	0006_require_contenttypes_0002	2018-07-06 10:24:01.397132+03
13	auth	0007_alter_validators_add_error_messages	2018-07-06 10:24:01.418936+03
14	auth	0008_alter_user_username_max_length	2018-07-06 10:24:01.453421+03
15	auth	0009_alter_user_last_name_max_length	2018-07-06 10:24:01.474693+03
16	authtoken	0001_initial	2018-07-06 10:24:01.532957+03
17	authtoken	0002_auto_20160226_1747	2018-07-06 10:24:01.597731+03
18	main	0001_initial	2018-07-06 10:24:02.337991+03
19	ona	0001_initial	2018-07-06 10:24:02.498965+03
20	sessions	0001_initial	2018-07-06 10:24:02.545475+03
21	sites	0001_initial	2018-07-06 10:24:02.561457+03
22	sites	0002_alter_domain_unique	2018-07-06 10:24:02.580703+03
23	socialaccount	0001_initial	2018-07-06 10:24:02.794874+03
24	socialaccount	0002_token_max_lengths	2018-07-06 10:24:02.920391+03
25	socialaccount	0003_extra_data_default_dict	2018-07-06 10:24:02.936201+03
26	users	0001_initial	2018-07-06 10:24:03.036162+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
fw4d7xx8ry88jvzxi8oluctta3qz3zhc	MDEwODNkNzc4NmFkNzJlNDI0ODY3ZWExOTkxOTY2ZmUxMDhhYjIzZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNDU4ODk1ZThiNjllMDAyMDE2YTFjOWUyOTQwNDhiNzY4OTg3ODY2In0=	2018-07-20 10:29:16.09924+03
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
1	2018-07-06 10:34:26.317914+03	15000.00	1
2	2018-07-06 10:35:51.529766+03	9000.00	2
\.


--
-- Data for Name: main_client; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_client (id, created, modified, name) FROM stdin;
1	2018-07-06 10:25:29.812966+03	2018-07-06 10:25:29.81299+03	Client1
2	2018-07-06 10:25:31.593745+03	2018-07-06 10:25:31.593787+03	Client2
3	2018-07-06 10:25:33.240288+03	2018-07-06 10:25:33.240328+03	Client3
4	2018-07-06 10:25:36.615127+03	2018-07-06 10:25:36.615168+03	Client4
5	2018-07-06 10:25:38.078727+03	2018-07-06 10:25:38.078767+03	Client5
6	2018-07-06 10:25:39.815023+03	2018-07-06 10:25:39.815054+03	Client6
7	2018-07-06 10:25:41.510615+03	2018-07-06 10:25:41.510653+03	Client7
8	2018-07-06 10:25:43.277455+03	2018-07-06 10:25:43.277486+03	Client8
9	2018-07-06 10:25:48.402942+03	2018-07-06 10:25:48.403009+03	Client9
10	2018-07-06 10:25:50.645137+03	2018-07-06 10:25:50.645174+03	Client10
11	2018-07-06 10:25:52.388617+03	2018-07-06 10:25:52.388698+03	Client11
12	2018-07-06 10:25:55.170079+03	2018-07-06 10:25:55.170128+03	Client12
13	2018-07-06 10:25:56.93869+03	2018-07-06 10:25:56.93872+03	Client13
14	2018-07-06 10:25:58.609853+03	2018-07-06 10:25:58.609885+03	Client14
15	2018-07-06 10:26:00.504142+03	2018-07-06 10:26:00.504169+03	Client15
16	2018-07-06 10:26:02.390323+03	2018-07-06 10:26:02.390366+03	Client16
17	2018-07-06 10:26:04.040944+03	2018-07-06 10:26:04.04098+03	Client17
18	2018-07-06 10:26:06.058302+03	2018-07-06 10:26:06.058352+03	Client18
19	2018-07-06 10:26:07.837388+03	2018-07-06 10:26:07.83743+03	Client19
20	2018-07-06 10:26:10.706065+03	2018-07-06 10:26:10.706106+03	Client20
21	2018-07-06 10:26:12.188356+03	2018-07-06 10:26:12.188395+03	Client21
22	2018-07-06 10:26:13.793592+03	2018-07-06 10:26:13.793647+03	Client22
23	2018-07-06 10:26:15.416294+03	2018-07-06 10:26:15.416333+03	Client23
24	2018-07-06 10:26:17.337471+03	2018-07-06 10:26:17.337506+03	Client24
25	2018-07-06 10:26:19.050179+03	2018-07-06 10:26:19.050202+03	Client25
26	2018-07-06 10:26:20.822367+03	2018-07-06 10:26:20.822392+03	Client26
27	2018-07-06 10:26:22.536567+03	2018-07-06 10:26:22.536606+03	Client27
28	2018-07-06 10:26:26.366592+03	2018-07-06 10:26:26.366615+03	Client28
29	2018-07-06 10:26:28.28534+03	2018-07-06 10:26:28.285375+03	Client29
30	2018-07-06 10:26:31.019663+03	2018-07-06 10:26:31.019697+03	Client30
31	2018-07-06 10:26:32.518733+03	2018-07-06 10:26:32.518767+03	Client31
32	2018-07-06 10:26:34.045567+03	2018-07-06 10:26:34.0456+03	Client32
33	2018-07-06 10:26:36.082821+03	2018-07-06 10:26:36.08285+03	Client33
34	2018-07-06 10:26:38.084615+03	2018-07-06 10:26:38.08466+03	Client34
35	2018-07-06 10:26:39.924812+03	2018-07-06 10:26:39.924841+03	Client35
36	2018-07-06 10:26:41.541004+03	2018-07-06 10:26:41.541036+03	Client36
37	2018-07-06 10:26:43.060056+03	2018-07-06 10:26:43.06008+03	Client37
38	2018-07-06 10:26:44.741808+03	2018-07-06 10:26:44.741853+03	Client38
39	2018-07-06 10:26:46.731982+03	2018-07-06 10:26:46.732004+03	Client39
40	2018-07-06 10:26:49.552338+03	2018-07-06 10:26:49.552398+03	Client40
41	2018-07-06 10:26:51.694742+03	2018-07-06 10:26:51.694784+03	Client41
42	2018-07-06 10:26:53.106927+03	2018-07-06 10:26:53.106958+03	Client42
43	2018-07-06 10:26:54.618117+03	2018-07-06 10:26:54.618193+03	Client43
44	2018-07-06 10:26:56.817615+03	2018-07-06 10:26:56.817675+03	Client44
45	2018-07-06 10:26:58.46208+03	2018-07-06 10:26:58.462104+03	Client45
46	2018-07-06 10:27:00.122203+03	2018-07-06 10:27:00.122249+03	Client46
47	2018-07-06 10:27:01.666041+03	2018-07-06 10:27:01.666103+03	Client47
48	2018-07-06 10:27:03.774447+03	2018-07-06 10:27:03.774471+03	Client48
49	2018-07-06 10:27:05.821368+03	2018-07-06 10:27:05.821425+03	Client49
50	2018-07-06 10:27:08.611479+03	2018-07-06 10:27:08.611512+03	Client50
\.


--
-- Data for Name: main_location; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_location (id, created, modified, name, country, geopoint, radius, shapefile, description, lft, rght, tree_id, level, location_type_id, parent_id) FROM stdin;
1	2018-07-06 10:36:45.627041+03	2018-07-06 10:36:45.627074+03	Nairobi	KE	0101000020E6100000FEFFFFFFFFAF93BFDBA6E4F3FF9B983F	40.0000	\N	Nairobi!!!	1	4	1	0	1	\N
2	2018-07-06 10:37:38.681311+03	2018-07-06 10:37:38.681335+03	Hurlingham	KE	\N	\N	0106000020E61000000100000001030000000100000005000000FFFFFFFFFF7195BF9BB4BEFAFFA1923FFFFFFFFFFFF8A5BFCD67FBFFFFDF503F0B433A014E6C5ABFC5BDA8BA89058EBFD78638689B01823F698AF412511F8C3FFFFFFFFFFF7195BF9BB4BEFAFFA1923F	Lorem ipsum dolor amet unicorn meh paleo banjo distillery twee. Flannel meggings cold-pressed, raw denim listicle poutine organic literally cornhole cloud bread vaporware ugh. Paleo chia glossier tbh, put a bird on it tacos direct trade venmo. Neutra farm-to-table prism authentic pork belly iPhone tofu kickstarter brooklyn salvia cliche single-origin coffee knausgaard migas.\r\n\r\nFranzen keffiyeh pickled, everyday carry narwhal pabst ennui adaptogen organic vaporware vape portland food truck vegan bicycle rights. Kogi kickstarter schlitz woke, intelligentsia literally cronut kombucha pour-over locavore. Salvia sartorial intelligentsia tacos chambray palo santo banjo. Actually everyday carry snackwave biodiesel swag deep v. Knausgaard hot chicken hashtag asymmetrical disrupt fashion axe. Chicharrones DIY tattooed kale chips chillwave seitan fashion axe scenester lumbersexual locavore jianbing green juice air plant blog fingerstache.\r\n\r\nBlue bottle chambray roof party yuccie cray coloring book hoodie pinterest succulents food truck prism. Hashtag air plant cornhole, retro everyday carry meggings activated charcoal seitan readymade. Meditation mixtape +1 locavore, artisan venmo retro PBR&B slow-carb man bun hella craft beer enamel pin yr microdosing. Pork belly tousled YOLO etsy sriracha cardigan lomo. Keytar butcher tacos blue bottle, coloring book kale chips you probably haven't heard of them tattooed 8-bit kogi.\r\n\r\nOccupy raclette af authentic. YOLO microdosing polaroid, selfies air plant fingerstache iceland hoodie trust fund whatever cornhole actually kitsch. Intelligentsia vaporware hoodie taxidermy, selfies cold-pressed YOLO. Banjo fixie lumbersexual hoodie. Pinterest vaporware humblebrag mixtape lumbersexual hexagon. Roof party fingerstache artisan neutra gochujang. Normcore sartorial 90's, neutra humblebrag health goth forage franzen taxidermy keffiyeh kale chips taiyaki try-hard master cleanse.\r\n\r\nTbh glossier poke etsy gochujang semiotics blue bottle XOXO flexitarian flannel edison bulb. Scenester irony sriracha etsy heirloom schlitz crucifix palo santo bitters sartorial synth locavore four dollar toast +1 green juice. +1 meh yr master cleanse, hammock VHS enamel pin four loko normcore raw denim. Scenester selvage vape poke, ethical chambray chartreuse cray chillwave humblebrag whatever waistcoat.\r\n\r\nOh. You need a little dummy text for your mockup? How quaint.\r\n\r\nI bet you’re still using Bootstrap too…	2	3	1	1	2	1
\.


--
-- Data for Name: main_locationtype; Type: TABLE DATA; Schema: public; Owner: sol
--

COPY public.main_locationtype (id, created, modified, name) FROM stdin;
1	2018-07-06 10:36:44.393313+03	2018-07-06 10:36:44.393333+03	City
2	2018-07-06 10:37:37.429037+03	2018-07-06 10:37:37.429057+03	Area
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

COPY public.main_task (id, created, modified, target_object_id, name, description, start, "end", timing_rule, total_submission_target, user_submission_target, status, estimated_time, required_expertise, lft, rght, tree_id, level, client_id, created_by_id, parent_id, target_content_type_id) FROM stdin;
1	2018-07-06 10:34:14.236472+03	2018-07-06 10:34:14.236521+03	1	Awesome Task	Awesome Task Description was here.... I promise.	2018-07-06 10:34:14+03	2018-07-08 12:00:00+03	FREQ=DAILY;INTERVAL=1	\N	500	a	01:00:00	4	1	2	1	0	1	3	\N	16
2	2018-07-06 10:35:39.777683+03	2018-07-06 10:35:39.77771+03	2	Chill Task	Sup?	2018-07-06 10:35:39+03	2018-07-31 12:00:00+03	FREQ=DAILY;INTERVAL=1	\N	100	a	02:30:00	3	1	2	2	0	14	3	\N	16
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
1	2018-07-06 10:34:26.297314+03	2018-07-06 10:34:26.297336+03	2018-07-06	10:34:14	23:59:59.999999	1
2	2018-07-06 10:34:26.297388+03	2018-07-06 10:34:26.297417+03	2018-07-07	10:34:14	23:59:59.999999	1
3	2018-07-06 10:34:26.297455+03	2018-07-06 10:34:26.297462+03	2018-07-08	10:34:14	23:59:59.999999	1
4	2018-07-06 10:35:51.501827+03	2018-07-06 10:35:51.50185+03	2018-07-06	10:35:39	23:59:59.999999	2
5	2018-07-06 10:35:51.501894+03	2018-07-06 10:35:51.501903+03	2018-07-07	10:35:39	23:59:59.999999	2
6	2018-07-06 10:35:51.501927+03	2018-07-06 10:35:51.501934+03	2018-07-08	10:35:39	23:59:59.999999	2
7	2018-07-06 10:35:51.501957+03	2018-07-06 10:35:51.501963+03	2018-07-09	10:35:39	23:59:59.999999	2
8	2018-07-06 10:35:51.501985+03	2018-07-06 10:35:51.501991+03	2018-07-10	10:35:39	23:59:59.999999	2
9	2018-07-06 10:35:51.502013+03	2018-07-06 10:35:51.502019+03	2018-07-11	10:35:39	23:59:59.999999	2
10	2018-07-06 10:35:51.502053+03	2018-07-06 10:35:51.50206+03	2018-07-12	10:35:39	23:59:59.999999	2
11	2018-07-06 10:35:51.502084+03	2018-07-06 10:35:51.502091+03	2018-07-13	10:35:39	23:59:59.999999	2
12	2018-07-06 10:35:51.502115+03	2018-07-06 10:35:51.502123+03	2018-07-14	10:35:39	23:59:59.999999	2
13	2018-07-06 10:35:51.502148+03	2018-07-06 10:35:51.502158+03	2018-07-15	10:35:39	23:59:59.999999	2
14	2018-07-06 10:35:51.502183+03	2018-07-06 10:35:51.502191+03	2018-07-16	10:35:39	23:59:59.999999	2
15	2018-07-06 10:35:51.502215+03	2018-07-06 10:35:51.502222+03	2018-07-17	10:35:39	23:59:59.999999	2
16	2018-07-06 10:35:51.502245+03	2018-07-06 10:35:51.502253+03	2018-07-18	10:35:39	23:59:59.999999	2
17	2018-07-06 10:35:51.502276+03	2018-07-06 10:35:51.502283+03	2018-07-19	10:35:39	23:59:59.999999	2
18	2018-07-06 10:35:51.502307+03	2018-07-06 10:35:51.502314+03	2018-07-20	10:35:39	23:59:59.999999	2
19	2018-07-06 10:35:51.502337+03	2018-07-06 10:35:51.502344+03	2018-07-21	10:35:39	23:59:59.999999	2
20	2018-07-06 10:35:51.502367+03	2018-07-06 10:35:51.502374+03	2018-07-22	10:35:39	23:59:59.999999	2
21	2018-07-06 10:35:51.502398+03	2018-07-06 10:35:51.502405+03	2018-07-23	10:35:39	23:59:59.999999	2
22	2018-07-06 10:35:51.502428+03	2018-07-06 10:35:51.502435+03	2018-07-24	10:35:39	23:59:59.999999	2
23	2018-07-06 10:35:51.502459+03	2018-07-06 10:35:51.502466+03	2018-07-25	10:35:39	23:59:59.999999	2
24	2018-07-06 10:35:51.502489+03	2018-07-06 10:35:51.502496+03	2018-07-26	10:35:39	23:59:59.999999	2
25	2018-07-06 10:35:51.502519+03	2018-07-06 10:35:51.502526+03	2018-07-27	10:35:39	23:59:59.999999	2
26	2018-07-06 10:35:51.502558+03	2018-07-06 10:35:51.502564+03	2018-07-28	10:35:39	23:59:59.999999	2
27	2018-07-06 10:35:51.502585+03	2018-07-06 10:35:51.502592+03	2018-07-29	10:35:39	23:59:59.999999	2
28	2018-07-06 10:35:51.502613+03	2018-07-06 10:35:51.502619+03	2018-07-30	10:35:39	23:59:59.999999	2
29	2018-07-06 10:35:51.50264+03	2018-07-06 10:35:51.502646+03	2018-07-31	10:35:39	23:59:59.999999	2
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
1	2018-07-06 10:27:32.825844+03	2018-07-06 10:27:32.825934+03	7223	4583	Form1	CaJIJNyVTLthgkwmHolx_ocesN5lMEqQqcpovvpmGmt2MxZf5avUmGrklG5eCG5r8rJYAJE3qY14Gfqg19MkHq2C1y5JtYrCur8Y	\N	\N
2	2018-07-06 10:27:34.684932+03	2018-07-06 10:27:34.68497+03	1032	6524	Form2	4RzwpngrNLtXACnBDmZKd5JRUp7nQfSde_6NXZa3sYEtlQKIkA1_1jdWmocFTo0u1iCdO7t-OMbdFeIqzpk8ajrtbdtoeLmp1D0f	\N	\N
3	2018-07-06 10:27:36.414256+03	2018-07-06 10:27:36.414285+03	5046	5182	Form3	PJITY5ufQjHyrkdec84noP9luJWxLlV_5GT-pNdXNf2g1g9H91fDDQeJSXAfrbs1_So0Yiswf2YK3Z-VzQZq65cTLYgsLGi6yNqp	\N	\N
4	2018-07-06 10:27:37.968213+03	2018-07-06 10:27:37.968234+03	3372	6397	Form4	FXOwB0pNIXlHgzo3oh5PBBoexzy2VjkQm-8cjXNpvP-jX4PtGHW0zdLIDwhH47NwhOqDX6-9uR4m5EBMqWUds-6udiOnzWBu_kqD	\N	\N
5	2018-07-06 10:27:39.767839+03	2018-07-06 10:27:39.767861+03	9408	9383	Form5	jdWyW5mVQuMOU057X6ODZOGLScK8DOwhY3ZkwC0QqnaxNuvzSQnNBfhSgfVPAydnfkQh_O51NR0RIGl0JZ7kqprQHgety667eAhz	\N	\N
6	2018-07-06 10:27:42.238509+03	2018-07-06 10:27:42.238533+03	7925	6317	Form6	Xne7EviTHs6LQvE3OEewjYmgKWKh4V5lsJMpioT3v8TWNPBqWzTvMCTCpKB2Aar-t8ascmsEX7RPV091iXkp0UMrfDyf7rALvpq6	\N	\N
7	2018-07-06 10:27:44.113859+03	2018-07-06 10:27:44.113889+03	6160	7700	Form7	0N2FUXSkW2Ef6rBco2n0fFFAXT8j-_YqsPv7bTbTl7j2SDDy_JTjR58YJAuHnrhu_p-sXuxcKo4Du_bFS6Yh0Bm9wJXyqFAreq0v	\N	\N
8	2018-07-06 10:27:45.893545+03	2018-07-06 10:27:45.893582+03	4108	9862	Form8	c3ITIsBtZO29Prw2ccoSbvUrNOEmDI13dawoFD7mN74aV4VO_4yJ3I6mY8HhHjfy_5KP5HG5yEshyhJZNJrFnjAdisQDxreMKvGr	\N	\N
9	2018-07-06 10:27:47.671175+03	2018-07-06 10:27:47.671213+03	9824	4968	Form9	4mGzfe1eOzjEub4bzpHswhOY741OmtSWTNTjM72tYr2t3RI-sl0woSpJumXX4lREiUHbL9cN_hOk25kAu8izCTwpKi9TBkku5B9B	\N	\N
10	2018-07-06 10:27:49.651928+03	2018-07-06 10:27:49.651988+03	9008	1434	Form10	vPNchwVGGtsZmwPFcfXzE8c-4WPcA-761IBsz_xM-1lTkrmvUhbTqbtZtg3YmpHfX8z5KAN-0R_gUHjWhQS0xeShI6G_ElRcf01Q	\N	\N
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
1	2018-07-06 10:24:37.653628+03	2018-07-06 10:30:46.567612+03	\N	davisray	0000000	+254788096605	+254788096605	1	3	1	1
4	2018-07-06 10:31:29.054485+03	2018-07-06 10:32:12.628915+03	\N	onauser	010000	+254788096605	+254788096605	1	4	0	3
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

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 6, true);


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

SELECT pg_catalog.setval('public.main_bounty_id_seq', 2, true);


--
-- Name: main_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sol
--

SELECT pg_catalog.setval('public.main_client_id_seq', 50, true);


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

SELECT pg_catalog.setval('public.main_taskoccurrence_id_seq', 29, true);


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

SELECT pg_catalog.setval('public.ona_xform_id_seq', 10, true);


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
-- Name: main_task_created_by_id_23ce62ed; Type: INDEX; Schema: public; Owner: sol
--

CREATE INDEX main_task_created_by_id_23ce62ed ON public.main_task USING btree (created_by_id);


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
-- Name: main_task main_task_created_by_id_23ce62ed_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: sol
--

ALTER TABLE ONLY public.main_task
    ADD CONSTRAINT main_task_created_by_id_23ce62ed_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


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

