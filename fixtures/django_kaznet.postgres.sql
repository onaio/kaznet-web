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
    timing_rule text NOT NULL,
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
-- Name: main_task_locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.main_task_locations (
    id integer NOT NULL,
    task_id integer NOT NULL,
    location_id integer NOT NULL
);


ALTER TABLE public.main_task_locations OWNER TO postgres;

--
-- Name: main_task_locations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.main_task_locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_task_locations_id_seq OWNER TO postgres;

--
-- Name: main_task_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.main_task_locations_id_seq OWNED BY public.main_task_locations.id;


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
-- Name: main_task_locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_locations ALTER COLUMN id SET DEFAULT nextval('public.main_task_locations_id_seq'::regclass);


--
-- Name: main_task_segment_rules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_segment_rules ALTER COLUMN id SET DEFAULT nextval('public.main_task_segment_rules_id_seq'::regclass);


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
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	SxtvJUfzKiBCkShSIypGTKYdsDZeETomuxCycLsWUVnCwIANpcXCyYiEAIPPfvcKQXAStHUlwmKfZicZCYKZvvgCOjapTwGdkXVqNXPyRdEWfnwwUocRdjPYEHhmAgsj	\N	f	onauser	Ona	Tech	tech+kaznet@ona.io	f	t	2018-06-21 12:13:29+03
1	pbkdf2_sha256$100000$ho9fAO6eBc4L$8Mjc9noBmhYKXr/g/Johi9CbutvCe34rUAv0U0VavcA=	2018-06-21 12:16:15+03	t	mosh			kelvin@jayanoris.com	t	t	2018-06-21 12:09:10+03
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
c45541bd1613b7f44d351b15ae315857ee3fd75e	2018-06-21 12:09:10.44775+03	1
a3e12e35672a57227a87e1bbf8c5fb9c468b6782	2018-06-21 12:13:29.822245+03	2
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2018-06-21 12:22:09.801798+03	1	Awesome Task - 1	2	[{"changed": {"fields": ["target_content_type", "target_object_id", "name", "description", "end", "timing_rule", "total_submission_target", "user_submission_target", "status", "estimated_time", "locations", "client"]}}]	24	1
2	2018-06-21 12:24:20.128098+03	2	Location 2 - 2	2	[{"changed": {"fields": ["target_content_type", "target_object_id", "description", "start", "timing_rule", "total_submission_target", "user_submission_target", "status", "estimated_time", "locations", "client", "required_expertise"]}}]	24	1
3	2018-06-21 12:25:06.258321+03	2	Kill Bill - 2	2	[{"changed": {"fields": ["name"]}}]	24	1
4	2018-06-21 12:25:22.218133+03	1	Task 2 bounty is Money('150000', 'KES')	1	[{"added": {}}]	17	1
5	2018-06-21 12:25:31.647553+03	2	Task 1 bounty is Money('55', 'KES')	1	[{"added": {}}]	17	1
6	2018-06-21 12:27:31.309077+03	1	Kenya - Location 1	2	[{"changed": {"fields": ["country", "geopoint", "radius", "description", "location_type"]}}]	19	1
7	2018-06-21 12:27:54.089482+03	2	Location 2	2	[{"changed": {"fields": ["geopoint", "radius", "description", "location_type"]}}]	19	1
8	2018-06-21 12:28:38.061926+03	2	onauser	2	[{"changed": {"fields": ["username", "email"]}}, {"changed": {"name": "Profile", "object": "Ona Tech's profile", "fields": ["role"]}}]	4	1
9	2018-06-21 12:29:09.385387+03	1	example.com	2	[{"changed": {"fields": ["name"]}}]	7	1
10	2018-06-21 12:45:16.144577+03	1	mosh	2	[{"changed": {"name": "Profile", "object": "kelvin@jayanoris.com's profile", "fields": ["role"]}}]	4	1
11	2018-06-21 12:54:17.007118+03	1	mosh	2	[{"changed": {"fields": ["password"]}}]	4	1
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
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2018-06-21 12:03:12.630828+03
2	auth	0001_initial	2018-06-21 12:03:12.732461+03
3	account	0001_initial	2018-06-21 12:03:12.799785+03
4	account	0002_email_max_length	2018-06-21 12:03:12.809675+03
5	admin	0001_initial	2018-06-21 12:03:12.831286+03
6	admin	0002_logentry_remove_auto_add	2018-06-21 12:03:12.843551+03
7	contenttypes	0002_remove_content_type_name	2018-06-21 12:03:12.870039+03
8	auth	0002_alter_permission_name_max_length	2018-06-21 12:03:12.878239+03
9	auth	0003_alter_user_email_max_length	2018-06-21 12:03:12.891781+03
10	auth	0004_alter_user_username_opts	2018-06-21 12:03:12.904282+03
11	auth	0005_alter_user_last_login_null	2018-06-21 12:03:12.918694+03
12	auth	0006_require_contenttypes_0002	2018-06-21 12:03:12.920647+03
13	auth	0007_alter_validators_add_error_messages	2018-06-21 12:03:12.934454+03
14	auth	0008_alter_user_username_max_length	2018-06-21 12:03:12.953527+03
15	auth	0009_alter_user_last_name_max_length	2018-06-21 12:03:12.968184+03
16	authtoken	0001_initial	2018-06-21 12:03:12.988938+03
17	authtoken	0002_auto_20160226_1747	2018-06-21 12:03:13.03488+03
18	main	0001_initial	2018-06-21 12:03:13.4573+03
19	ona	0001_initial	2018-06-21 12:03:13.596968+03
20	sessions	0001_initial	2018-06-21 12:03:13.614862+03
21	sites	0001_initial	2018-06-21 12:03:13.630641+03
22	sites	0002_alter_domain_unique	2018-06-21 12:03:13.64276+03
23	socialaccount	0001_initial	2018-06-21 12:03:13.753527+03
24	socialaccount	0002_token_max_lengths	2018-06-21 12:03:13.825545+03
25	socialaccount	0003_extra_data_default_dict	2018-06-21 12:03:13.835704+03
26	users	0001_initial	2018-06-21 12:03:13.892204+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
20nsmov16316fk4ix7en4t3qjhin0dxe	MzAzZGIwMThmNDE1OGI5MWQ0MWZlYmUwN2QwYTk5NDM0ODhiMWE0Yjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjOWVkMjkzMjQ2ZTE2Mjg1N2IzNWI3NjlkYmUxMzVmMDU4YzNlZTEwIn0=	2018-07-05 12:54:17.03235+03
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	Kaznet
\.


--
-- Data for Name: main_bounty; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_bounty (id, created, amount, task_id) FROM stdin;
1	2018-06-21 12:25:22.213014+03	150000.00	2
2	2018-06-21 12:25:31.642649+03	55.00	1
\.


--
-- Data for Name: main_client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_client (id, created, modified, name) FROM stdin;
1	2018-06-21 12:14:07.197562+03	2018-06-21 12:14:07.197628+03	Client 1
2	2018-06-21 12:14:07.202191+03	2018-06-21 12:14:07.202285+03	Client 2
3	2018-06-21 12:14:07.205737+03	2018-06-21 12:14:07.20582+03	Client 3
4	2018-06-21 12:14:07.209231+03	2018-06-21 12:14:07.209291+03	Client 4
5	2018-06-21 12:14:07.212627+03	2018-06-21 12:14:07.212689+03	Client 5
6	2018-06-21 12:14:07.215392+03	2018-06-21 12:14:07.215434+03	Client 6
7	2018-06-21 12:14:07.21781+03	2018-06-21 12:14:07.217848+03	Client 7
8	2018-06-21 12:14:07.220328+03	2018-06-21 12:14:07.220385+03	Client 8
9	2018-06-21 12:14:07.222966+03	2018-06-21 12:14:07.223009+03	Client 9
10	2018-06-21 12:14:07.225927+03	2018-06-21 12:14:07.225984+03	Client 10
11	2018-06-21 12:14:07.229774+03	2018-06-21 12:14:07.229852+03	Client 11
12	2018-06-21 12:14:07.233893+03	2018-06-21 12:14:07.23397+03	Client 12
13	2018-06-21 12:14:07.235838+03	2018-06-21 12:14:07.235861+03	Client 13
14	2018-06-21 12:14:07.237694+03	2018-06-21 12:14:07.237718+03	Client 14
15	2018-06-21 12:14:07.239423+03	2018-06-21 12:14:07.239442+03	Client 15
16	2018-06-21 12:14:07.240978+03	2018-06-21 12:14:07.240997+03	Client 16
17	2018-06-21 12:14:07.242445+03	2018-06-21 12:14:07.242464+03	Client 17
18	2018-06-21 12:14:07.243811+03	2018-06-21 12:14:07.243829+03	Client 18
19	2018-06-21 12:14:07.245084+03	2018-06-21 12:14:07.245109+03	Client 19
20	2018-06-21 12:14:07.246597+03	2018-06-21 12:14:07.24662+03	Client 20
21	2018-06-21 12:14:07.247902+03	2018-06-21 12:14:07.247923+03	Client 21
22	2018-06-21 12:14:07.249174+03	2018-06-21 12:14:07.24919+03	Client 22
23	2018-06-21 12:14:07.25042+03	2018-06-21 12:14:07.250435+03	Client 23
24	2018-06-21 12:14:07.251888+03	2018-06-21 12:14:07.251921+03	Client 24
25	2018-06-21 12:14:07.253713+03	2018-06-21 12:14:07.253735+03	Client 25
26	2018-06-21 12:14:07.255579+03	2018-06-21 12:14:07.255597+03	Client 26
27	2018-06-21 12:14:07.257211+03	2018-06-21 12:14:07.257228+03	Client 27
28	2018-06-21 12:14:07.258957+03	2018-06-21 12:14:07.258974+03	Client 28
29	2018-06-21 12:14:07.260634+03	2018-06-21 12:14:07.26065+03	Client 29
30	2018-06-21 12:14:07.262337+03	2018-06-21 12:14:07.262359+03	Client 30
31	2018-06-21 12:14:07.264435+03	2018-06-21 12:14:07.264501+03	Client 31
32	2018-06-21 12:14:07.265938+03	2018-06-21 12:14:07.26596+03	Client 32
33	2018-06-21 12:14:07.267432+03	2018-06-21 12:14:07.267481+03	Client 33
34	2018-06-21 12:14:07.269212+03	2018-06-21 12:14:07.269243+03	Client 34
35	2018-06-21 12:14:07.270948+03	2018-06-21 12:14:07.270979+03	Client 35
36	2018-06-21 12:14:07.272642+03	2018-06-21 12:14:07.272671+03	Client 36
37	2018-06-21 12:14:07.274239+03	2018-06-21 12:14:07.274267+03	Client 37
38	2018-06-21 12:14:07.276036+03	2018-06-21 12:14:07.276065+03	Client 38
39	2018-06-21 12:14:07.277664+03	2018-06-21 12:14:07.27769+03	Client 39
40	2018-06-21 12:14:07.279323+03	2018-06-21 12:14:07.279348+03	Client 40
41	2018-06-21 12:14:07.281139+03	2018-06-21 12:14:07.281166+03	Client 41
42	2018-06-21 12:14:07.282781+03	2018-06-21 12:14:07.282807+03	Client 42
43	2018-06-21 12:14:07.284152+03	2018-06-21 12:14:07.284172+03	Client 43
44	2018-06-21 12:14:07.285471+03	2018-06-21 12:14:07.285493+03	Client 44
45	2018-06-21 12:14:07.286938+03	2018-06-21 12:14:07.286961+03	Client 45
46	2018-06-21 12:14:07.29125+03	2018-06-21 12:14:07.291277+03	Client 46
47	2018-06-21 12:14:07.292805+03	2018-06-21 12:14:07.292831+03	Client 47
48	2018-06-21 12:14:07.294262+03	2018-06-21 12:14:07.294288+03	Client 48
49	2018-06-21 12:14:07.295727+03	2018-06-21 12:14:07.295752+03	Client 49
50	2018-06-21 12:14:07.297203+03	2018-06-21 12:14:07.29723+03	Client 50
51	2018-06-21 12:14:07.298752+03	2018-06-21 12:14:07.298778+03	Client 51
52	2018-06-21 12:14:07.300219+03	2018-06-21 12:14:07.300239+03	Client 52
53	2018-06-21 12:14:07.301634+03	2018-06-21 12:14:07.301653+03	Client 53
54	2018-06-21 12:14:07.303085+03	2018-06-21 12:14:07.303112+03	Client 54
55	2018-06-21 12:14:07.30497+03	2018-06-21 12:14:07.304992+03	Client 55
56	2018-06-21 12:14:07.306575+03	2018-06-21 12:14:07.306611+03	Client 56
57	2018-06-21 12:14:07.308354+03	2018-06-21 12:14:07.308382+03	Client 57
58	2018-06-21 12:14:07.309852+03	2018-06-21 12:14:07.309871+03	Client 58
59	2018-06-21 12:14:07.31129+03	2018-06-21 12:14:07.31131+03	Client 59
60	2018-06-21 12:14:07.312888+03	2018-06-21 12:14:07.312916+03	Client 60
61	2018-06-21 12:14:07.314442+03	2018-06-21 12:14:07.314472+03	Client 61
62	2018-06-21 12:14:07.31604+03	2018-06-21 12:14:07.316069+03	Client 62
63	2018-06-21 12:14:07.317647+03	2018-06-21 12:14:07.317677+03	Client 63
64	2018-06-21 12:14:07.319172+03	2018-06-21 12:14:07.319196+03	Client 64
65	2018-06-21 12:14:07.320646+03	2018-06-21 12:14:07.320673+03	Client 65
66	2018-06-21 12:14:07.322087+03	2018-06-21 12:14:07.322113+03	Client 66
67	2018-06-21 12:14:07.323567+03	2018-06-21 12:14:07.323593+03	Client 67
68	2018-06-21 12:14:07.328115+03	2018-06-21 12:14:07.328145+03	Client 68
69	2018-06-21 12:14:07.329718+03	2018-06-21 12:14:07.329746+03	Client 69
\.


--
-- Data for Name: main_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_location (id, created, modified, name, country, geopoint, radius, shapefile, description, lft, rght, tree_id, level, location_type_id, parent_id) FROM stdin;
1	2018-06-21 12:14:30.215276+03	2018-06-21 12:27:31.287941+03	Location 1	KE	0101000020E6100000FEFFFF58740DA6BFEF432709740DA63F	2000.0000	\N	This is the description.	2842	4297	544	4831	1	\N
2	2018-06-21 12:14:30.260298+03	2018-06-21 12:27:54.060863+03	Location 2		0101000020E6100000FDFF7FE9FF55B3BF86AA821E1773A83F	140.0000	\N	Another description.	4103	8746	3878	2974	1	\N
\.


--
-- Data for Name: main_locationtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_locationtype (id, created, modified, name) FROM stdin;
1	2018-06-21 12:26:58.573869+03	2018-06-21 12:26:58.57392+03	Market
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

COPY public.main_task (id, created, modified, target_object_id, name, description, start, "end", timing_rule, total_submission_target, user_submission_target, status, estimated_time, required_expertise, lft, rght, tree_id, level, client_id, parent_id, target_content_type_id) FROM stdin;
1	2018-06-21 12:15:45.349936+03	2018-06-21 12:22:09.703447+03	1	Awesome Task	This is pure joy.	2018-06-21 12:15:45+03	2019-01-30 12:17:40+03	RRULE:FREQ=DAILY;INTERVAL=10;COUNT=12	100	100	a	4 days 01:15:20	1	3555	9063	3988	9593	7	\N	16
2	2018-06-21 12:15:45.3637+03	2018-06-21 12:25:06.164454+03	2	Kill Bill	The best and most delicious task ever.	2018-08-17 12:15:45+03	\N	RRULE:FREQ=DAILY;INTERVAL=1;COUNT=500	200	2	s	00:00:19	3	4988	1077	1593	6130	2	\N	16
\.


--
-- Data for Name: main_task_locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_task_locations (id, task_id, location_id) FROM stdin;
1	1	1
2	2	2
\.


--
-- Data for Name: main_task_segment_rules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_task_segment_rules (id, task_id, segmentrule_id) FROM stdin;
\.


--
-- Data for Name: main_taskoccurrence; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.main_taskoccurrence (id, created, modified, date, start_time, end_time, task_id) FROM stdin;
1	2018-06-21 12:22:09.763588+03	2018-06-21 12:22:09.76361+03	2018-06-21	12:22:09	23:59:59.999999	1
2	2018-06-21 12:22:09.763659+03	2018-06-21 12:22:09.763668+03	2018-07-01	12:22:09	23:59:59.999999	1
3	2018-06-21 12:22:09.763692+03	2018-06-21 12:22:09.763699+03	2018-07-11	12:22:09	23:59:59.999999	1
4	2018-06-21 12:22:09.76372+03	2018-06-21 12:22:09.763727+03	2018-07-21	12:22:09	23:59:59.999999	1
5	2018-06-21 12:22:09.763749+03	2018-06-21 12:22:09.763755+03	2018-07-31	12:22:09	23:59:59.999999	1
6	2018-06-21 12:22:09.763776+03	2018-06-21 12:22:09.763782+03	2018-08-10	12:22:09	23:59:59.999999	1
7	2018-06-21 12:22:09.763803+03	2018-06-21 12:22:09.763822+03	2018-08-20	12:22:09	23:59:59.999999	1
8	2018-06-21 12:22:09.763845+03	2018-06-21 12:22:09.763852+03	2018-08-30	12:22:09	23:59:59.999999	1
9	2018-06-21 12:22:09.763873+03	2018-06-21 12:22:09.763879+03	2018-09-09	12:22:09	23:59:59.999999	1
10	2018-06-21 12:22:09.763899+03	2018-06-21 12:22:09.763906+03	2018-09-19	12:22:09	23:59:59.999999	1
11	2018-06-21 12:22:09.763926+03	2018-06-21 12:22:09.763932+03	2018-09-29	12:22:09	23:59:59.999999	1
12	2018-06-21 12:22:09.763953+03	2018-06-21 12:22:09.763959+03	2018-10-09	12:22:09	23:59:59.999999	1
513	2018-06-21 12:25:06.192735+03	2018-06-21 12:25:06.192756+03	2018-06-21	12:25:06	23:59:59.999999	2
514	2018-06-21 12:25:06.192794+03	2018-06-21 12:25:06.192801+03	2018-06-22	12:25:06	23:59:59.999999	2
515	2018-06-21 12:25:06.192823+03	2018-06-21 12:25:06.192829+03	2018-06-23	12:25:06	23:59:59.999999	2
516	2018-06-21 12:25:06.192848+03	2018-06-21 12:25:06.192854+03	2018-06-24	12:25:06	23:59:59.999999	2
517	2018-06-21 12:25:06.192873+03	2018-06-21 12:25:06.192879+03	2018-06-25	12:25:06	23:59:59.999999	2
518	2018-06-21 12:25:06.192899+03	2018-06-21 12:25:06.192905+03	2018-06-26	12:25:06	23:59:59.999999	2
519	2018-06-21 12:25:06.192924+03	2018-06-21 12:25:06.19293+03	2018-06-27	12:25:06	23:59:59.999999	2
520	2018-06-21 12:25:06.192948+03	2018-06-21 12:25:06.192954+03	2018-06-28	12:25:06	23:59:59.999999	2
521	2018-06-21 12:25:06.192972+03	2018-06-21 12:25:06.192978+03	2018-06-29	12:25:06	23:59:59.999999	2
522	2018-06-21 12:25:06.192996+03	2018-06-21 12:25:06.193002+03	2018-06-30	12:25:06	23:59:59.999999	2
523	2018-06-21 12:25:06.19302+03	2018-06-21 12:25:06.193026+03	2018-07-01	12:25:06	23:59:59.999999	2
524	2018-06-21 12:25:06.193044+03	2018-06-21 12:25:06.19305+03	2018-07-02	12:25:06	23:59:59.999999	2
525	2018-06-21 12:25:06.193068+03	2018-06-21 12:25:06.193074+03	2018-07-03	12:25:06	23:59:59.999999	2
526	2018-06-21 12:25:06.193092+03	2018-06-21 12:25:06.193098+03	2018-07-04	12:25:06	23:59:59.999999	2
527	2018-06-21 12:25:06.193116+03	2018-06-21 12:25:06.193122+03	2018-07-05	12:25:06	23:59:59.999999	2
528	2018-06-21 12:25:06.193141+03	2018-06-21 12:25:06.193146+03	2018-07-06	12:25:06	23:59:59.999999	2
529	2018-06-21 12:25:06.193164+03	2018-06-21 12:25:06.19317+03	2018-07-07	12:25:06	23:59:59.999999	2
530	2018-06-21 12:25:06.193189+03	2018-06-21 12:25:06.193194+03	2018-07-08	12:25:06	23:59:59.999999	2
531	2018-06-21 12:25:06.193212+03	2018-06-21 12:25:06.193218+03	2018-07-09	12:25:06	23:59:59.999999	2
532	2018-06-21 12:25:06.193236+03	2018-06-21 12:25:06.193242+03	2018-07-10	12:25:06	23:59:59.999999	2
533	2018-06-21 12:25:06.19326+03	2018-06-21 12:25:06.193266+03	2018-07-11	12:25:06	23:59:59.999999	2
534	2018-06-21 12:25:06.193284+03	2018-06-21 12:25:06.19329+03	2018-07-12	12:25:06	23:59:59.999999	2
535	2018-06-21 12:25:06.193308+03	2018-06-21 12:25:06.193314+03	2018-07-13	12:25:06	23:59:59.999999	2
536	2018-06-21 12:25:06.193332+03	2018-06-21 12:25:06.193338+03	2018-07-14	12:25:06	23:59:59.999999	2
537	2018-06-21 12:25:06.193355+03	2018-06-21 12:25:06.193361+03	2018-07-15	12:25:06	23:59:59.999999	2
538	2018-06-21 12:25:06.193379+03	2018-06-21 12:25:06.193385+03	2018-07-16	12:25:06	23:59:59.999999	2
539	2018-06-21 12:25:06.193403+03	2018-06-21 12:25:06.193409+03	2018-07-17	12:25:06	23:59:59.999999	2
540	2018-06-21 12:25:06.193427+03	2018-06-21 12:25:06.193432+03	2018-07-18	12:25:06	23:59:59.999999	2
541	2018-06-21 12:25:06.19345+03	2018-06-21 12:25:06.193456+03	2018-07-19	12:25:06	23:59:59.999999	2
542	2018-06-21 12:25:06.193474+03	2018-06-21 12:25:06.19348+03	2018-07-20	12:25:06	23:59:59.999999	2
543	2018-06-21 12:25:06.193498+03	2018-06-21 12:25:06.193503+03	2018-07-21	12:25:06	23:59:59.999999	2
544	2018-06-21 12:25:06.193522+03	2018-06-21 12:25:06.193527+03	2018-07-22	12:25:06	23:59:59.999999	2
545	2018-06-21 12:25:06.193545+03	2018-06-21 12:25:06.193551+03	2018-07-23	12:25:06	23:59:59.999999	2
546	2018-06-21 12:25:06.193569+03	2018-06-21 12:25:06.193575+03	2018-07-24	12:25:06	23:59:59.999999	2
547	2018-06-21 12:25:06.193593+03	2018-06-21 12:25:06.193598+03	2018-07-25	12:25:06	23:59:59.999999	2
548	2018-06-21 12:25:06.193616+03	2018-06-21 12:25:06.193622+03	2018-07-26	12:25:06	23:59:59.999999	2
549	2018-06-21 12:25:06.193643+03	2018-06-21 12:25:06.193652+03	2018-07-27	12:25:06	23:59:59.999999	2
550	2018-06-21 12:25:06.193682+03	2018-06-21 12:25:06.193692+03	2018-07-28	12:25:06	23:59:59.999999	2
551	2018-06-21 12:25:06.193723+03	2018-06-21 12:25:06.193733+03	2018-07-29	12:25:06	23:59:59.999999	2
552	2018-06-21 12:25:06.193754+03	2018-06-21 12:25:06.19376+03	2018-07-30	12:25:06	23:59:59.999999	2
553	2018-06-21 12:25:06.193778+03	2018-06-21 12:25:06.193784+03	2018-07-31	12:25:06	23:59:59.999999	2
554	2018-06-21 12:25:06.193819+03	2018-06-21 12:25:06.193825+03	2018-08-01	12:25:06	23:59:59.999999	2
555	2018-06-21 12:25:06.193843+03	2018-06-21 12:25:06.193849+03	2018-08-02	12:25:06	23:59:59.999999	2
556	2018-06-21 12:25:06.193866+03	2018-06-21 12:25:06.193872+03	2018-08-03	12:25:06	23:59:59.999999	2
557	2018-06-21 12:25:06.193891+03	2018-06-21 12:25:06.193896+03	2018-08-04	12:25:06	23:59:59.999999	2
558	2018-06-21 12:25:06.193914+03	2018-06-21 12:25:06.19392+03	2018-08-05	12:25:06	23:59:59.999999	2
559	2018-06-21 12:25:06.193939+03	2018-06-21 12:25:06.193946+03	2018-08-06	12:25:06	23:59:59.999999	2
560	2018-06-21 12:25:06.193965+03	2018-06-21 12:25:06.193971+03	2018-08-07	12:25:06	23:59:59.999999	2
561	2018-06-21 12:25:06.193989+03	2018-06-21 12:25:06.193994+03	2018-08-08	12:25:06	23:59:59.999999	2
562	2018-06-21 12:25:06.194013+03	2018-06-21 12:25:06.194018+03	2018-08-09	12:25:06	23:59:59.999999	2
563	2018-06-21 12:25:06.194036+03	2018-06-21 12:25:06.194042+03	2018-08-10	12:25:06	23:59:59.999999	2
564	2018-06-21 12:25:06.19406+03	2018-06-21 12:25:06.194065+03	2018-08-11	12:25:06	23:59:59.999999	2
565	2018-06-21 12:25:06.194083+03	2018-06-21 12:25:06.194089+03	2018-08-12	12:25:06	23:59:59.999999	2
566	2018-06-21 12:25:06.194106+03	2018-06-21 12:25:06.194112+03	2018-08-13	12:25:06	23:59:59.999999	2
567	2018-06-21 12:25:06.19413+03	2018-06-21 12:25:06.194136+03	2018-08-14	12:25:06	23:59:59.999999	2
568	2018-06-21 12:25:06.194154+03	2018-06-21 12:25:06.19416+03	2018-08-15	12:25:06	23:59:59.999999	2
569	2018-06-21 12:25:06.194178+03	2018-06-21 12:25:06.194183+03	2018-08-16	12:25:06	23:59:59.999999	2
570	2018-06-21 12:25:06.194201+03	2018-06-21 12:25:06.194207+03	2018-08-17	12:25:06	23:59:59.999999	2
571	2018-06-21 12:25:06.194224+03	2018-06-21 12:25:06.19423+03	2018-08-18	12:25:06	23:59:59.999999	2
572	2018-06-21 12:25:06.194248+03	2018-06-21 12:25:06.194254+03	2018-08-19	12:25:06	23:59:59.999999	2
573	2018-06-21 12:25:06.194272+03	2018-06-21 12:25:06.194278+03	2018-08-20	12:25:06	23:59:59.999999	2
574	2018-06-21 12:25:06.194296+03	2018-06-21 12:25:06.194302+03	2018-08-21	12:25:06	23:59:59.999999	2
575	2018-06-21 12:25:06.19432+03	2018-06-21 12:25:06.194326+03	2018-08-22	12:25:06	23:59:59.999999	2
576	2018-06-21 12:25:06.194344+03	2018-06-21 12:25:06.194349+03	2018-08-23	12:25:06	23:59:59.999999	2
577	2018-06-21 12:25:06.194367+03	2018-06-21 12:25:06.194373+03	2018-08-24	12:25:06	23:59:59.999999	2
578	2018-06-21 12:25:06.194391+03	2018-06-21 12:25:06.194397+03	2018-08-25	12:25:06	23:59:59.999999	2
579	2018-06-21 12:25:06.194415+03	2018-06-21 12:25:06.19442+03	2018-08-26	12:25:06	23:59:59.999999	2
580	2018-06-21 12:25:06.194438+03	2018-06-21 12:25:06.194444+03	2018-08-27	12:25:06	23:59:59.999999	2
581	2018-06-21 12:25:06.194462+03	2018-06-21 12:25:06.194468+03	2018-08-28	12:25:06	23:59:59.999999	2
582	2018-06-21 12:25:06.194486+03	2018-06-21 12:25:06.194491+03	2018-08-29	12:25:06	23:59:59.999999	2
583	2018-06-21 12:25:06.194509+03	2018-06-21 12:25:06.194515+03	2018-08-30	12:25:06	23:59:59.999999	2
584	2018-06-21 12:25:06.194545+03	2018-06-21 12:25:06.19455+03	2018-08-31	12:25:06	23:59:59.999999	2
585	2018-06-21 12:25:06.194568+03	2018-06-21 12:25:06.194574+03	2018-09-01	12:25:06	23:59:59.999999	2
586	2018-06-21 12:25:06.194592+03	2018-06-21 12:25:06.194598+03	2018-09-02	12:25:06	23:59:59.999999	2
587	2018-06-21 12:25:06.194615+03	2018-06-21 12:25:06.194621+03	2018-09-03	12:25:06	23:59:59.999999	2
588	2018-06-21 12:25:06.194638+03	2018-06-21 12:25:06.194644+03	2018-09-04	12:25:06	23:59:59.999999	2
589	2018-06-21 12:25:06.194661+03	2018-06-21 12:25:06.194667+03	2018-09-05	12:25:06	23:59:59.999999	2
590	2018-06-21 12:25:06.194684+03	2018-06-21 12:25:06.194689+03	2018-09-06	12:25:06	23:59:59.999999	2
591	2018-06-21 12:25:06.194707+03	2018-06-21 12:25:06.194712+03	2018-09-07	12:25:06	23:59:59.999999	2
592	2018-06-21 12:25:06.19473+03	2018-06-21 12:25:06.194735+03	2018-09-08	12:25:06	23:59:59.999999	2
593	2018-06-21 12:25:06.194752+03	2018-06-21 12:25:06.194758+03	2018-09-09	12:25:06	23:59:59.999999	2
594	2018-06-21 12:25:06.194775+03	2018-06-21 12:25:06.194781+03	2018-09-10	12:25:06	23:59:59.999999	2
595	2018-06-21 12:25:06.194798+03	2018-06-21 12:25:06.194804+03	2018-09-11	12:25:06	23:59:59.999999	2
596	2018-06-21 12:25:06.194821+03	2018-06-21 12:25:06.194827+03	2018-09-12	12:25:06	23:59:59.999999	2
597	2018-06-21 12:25:06.194844+03	2018-06-21 12:25:06.19485+03	2018-09-13	12:25:06	23:59:59.999999	2
598	2018-06-21 12:25:06.194867+03	2018-06-21 12:25:06.194872+03	2018-09-14	12:25:06	23:59:59.999999	2
599	2018-06-21 12:25:06.194889+03	2018-06-21 12:25:06.194895+03	2018-09-15	12:25:06	23:59:59.999999	2
600	2018-06-21 12:25:06.194912+03	2018-06-21 12:25:06.194918+03	2018-09-16	12:25:06	23:59:59.999999	2
601	2018-06-21 12:25:06.194935+03	2018-06-21 12:25:06.19494+03	2018-09-17	12:25:06	23:59:59.999999	2
602	2018-06-21 12:25:06.194958+03	2018-06-21 12:25:06.194963+03	2018-09-18	12:25:06	23:59:59.999999	2
603	2018-06-21 12:25:06.194981+03	2018-06-21 12:25:06.194986+03	2018-09-19	12:25:06	23:59:59.999999	2
604	2018-06-21 12:25:06.195019+03	2018-06-21 12:25:06.195024+03	2018-09-20	12:25:06	23:59:59.999999	2
605	2018-06-21 12:25:06.195042+03	2018-06-21 12:25:06.195047+03	2018-09-21	12:25:06	23:59:59.999999	2
606	2018-06-21 12:25:06.195064+03	2018-06-21 12:25:06.19507+03	2018-09-22	12:25:06	23:59:59.999999	2
607	2018-06-21 12:25:06.195087+03	2018-06-21 12:25:06.195092+03	2018-09-23	12:25:06	23:59:59.999999	2
608	2018-06-21 12:25:06.195109+03	2018-06-21 12:25:06.195115+03	2018-09-24	12:25:06	23:59:59.999999	2
609	2018-06-21 12:25:06.195133+03	2018-06-21 12:25:06.195138+03	2018-09-25	12:25:06	23:59:59.999999	2
610	2018-06-21 12:25:06.195156+03	2018-06-21 12:25:06.195161+03	2018-09-26	12:25:06	23:59:59.999999	2
611	2018-06-21 12:25:06.195179+03	2018-06-21 12:25:06.195184+03	2018-09-27	12:25:06	23:59:59.999999	2
612	2018-06-21 12:25:06.195201+03	2018-06-21 12:25:06.195207+03	2018-09-28	12:25:06	23:59:59.999999	2
613	2018-06-21 12:25:06.195224+03	2018-06-21 12:25:06.19523+03	2018-09-29	12:25:06	23:59:59.999999	2
614	2018-06-21 12:25:06.195247+03	2018-06-21 12:25:06.195253+03	2018-09-30	12:25:06	23:59:59.999999	2
615	2018-06-21 12:25:06.19527+03	2018-06-21 12:25:06.195275+03	2018-10-01	12:25:06	23:59:59.999999	2
616	2018-06-21 12:25:06.195293+03	2018-06-21 12:25:06.195298+03	2018-10-02	12:25:06	23:59:59.999999	2
617	2018-06-21 12:25:06.195316+03	2018-06-21 12:25:06.195321+03	2018-10-03	12:25:06	23:59:59.999999	2
618	2018-06-21 12:25:06.195338+03	2018-06-21 12:25:06.195344+03	2018-10-04	12:25:06	23:59:59.999999	2
619	2018-06-21 12:25:06.195361+03	2018-06-21 12:25:06.195367+03	2018-10-05	12:25:06	23:59:59.999999	2
620	2018-06-21 12:25:06.195384+03	2018-06-21 12:25:06.19539+03	2018-10-06	12:25:06	23:59:59.999999	2
621	2018-06-21 12:25:06.195407+03	2018-06-21 12:25:06.195413+03	2018-10-07	12:25:06	23:59:59.999999	2
622	2018-06-21 12:25:06.19543+03	2018-06-21 12:25:06.195435+03	2018-10-08	12:25:06	23:59:59.999999	2
623	2018-06-21 12:25:06.195453+03	2018-06-21 12:25:06.195458+03	2018-10-09	12:25:06	23:59:59.999999	2
624	2018-06-21 12:25:06.195476+03	2018-06-21 12:25:06.195481+03	2018-10-10	12:25:06	23:59:59.999999	2
625	2018-06-21 12:25:06.195498+03	2018-06-21 12:25:06.195504+03	2018-10-11	12:25:06	23:59:59.999999	2
626	2018-06-21 12:25:06.195521+03	2018-06-21 12:25:06.195527+03	2018-10-12	12:25:06	23:59:59.999999	2
627	2018-06-21 12:25:06.195544+03	2018-06-21 12:25:06.195549+03	2018-10-13	12:25:06	23:59:59.999999	2
628	2018-06-21 12:25:06.195566+03	2018-06-21 12:25:06.195572+03	2018-10-14	12:25:06	23:59:59.999999	2
629	2018-06-21 12:25:06.195589+03	2018-06-21 12:25:06.195595+03	2018-10-15	12:25:06	23:59:59.999999	2
630	2018-06-21 12:25:06.195612+03	2018-06-21 12:25:06.195617+03	2018-10-16	12:25:06	23:59:59.999999	2
631	2018-06-21 12:25:06.195634+03	2018-06-21 12:25:06.19564+03	2018-10-17	12:25:06	23:59:59.999999	2
632	2018-06-21 12:25:06.195657+03	2018-06-21 12:25:06.195663+03	2018-10-18	12:25:06	23:59:59.999999	2
633	2018-06-21 12:25:06.19568+03	2018-06-21 12:25:06.195685+03	2018-10-19	12:25:06	23:59:59.999999	2
634	2018-06-21 12:25:06.195703+03	2018-06-21 12:25:06.195708+03	2018-10-20	12:25:06	23:59:59.999999	2
635	2018-06-21 12:25:06.195726+03	2018-06-21 12:25:06.195731+03	2018-10-21	12:25:06	23:59:59.999999	2
636	2018-06-21 12:25:06.195749+03	2018-06-21 12:25:06.195754+03	2018-10-22	12:25:06	23:59:59.999999	2
637	2018-06-21 12:25:06.195771+03	2018-06-21 12:25:06.195777+03	2018-10-23	12:25:06	23:59:59.999999	2
638	2018-06-21 12:25:06.195794+03	2018-06-21 12:25:06.1958+03	2018-10-24	12:25:06	23:59:59.999999	2
639	2018-06-21 12:25:06.195817+03	2018-06-21 12:25:06.195823+03	2018-10-25	12:25:06	23:59:59.999999	2
640	2018-06-21 12:25:06.19584+03	2018-06-21 12:25:06.195846+03	2018-10-26	12:25:06	23:59:59.999999	2
641	2018-06-21 12:25:06.195863+03	2018-06-21 12:25:06.195869+03	2018-10-27	12:25:06	23:59:59.999999	2
642	2018-06-21 12:25:06.195886+03	2018-06-21 12:25:06.195892+03	2018-10-28	12:25:06	23:59:59.999999	2
643	2018-06-21 12:25:06.195909+03	2018-06-21 12:25:06.195914+03	2018-10-29	12:25:06	23:59:59.999999	2
644	2018-06-21 12:25:06.195932+03	2018-06-21 12:25:06.195937+03	2018-10-30	12:25:06	23:59:59.999999	2
645	2018-06-21 12:25:06.195955+03	2018-06-21 12:25:06.19596+03	2018-10-31	12:25:06	23:59:59.999999	2
646	2018-06-21 12:25:06.195977+03	2018-06-21 12:25:06.195983+03	2018-11-01	12:25:06	23:59:59.999999	2
647	2018-06-21 12:25:06.196+03	2018-06-21 12:25:06.196005+03	2018-11-02	12:25:06	23:59:59.999999	2
648	2018-06-21 12:25:06.196022+03	2018-06-21 12:25:06.196028+03	2018-11-03	12:25:06	23:59:59.999999	2
649	2018-06-21 12:25:06.196045+03	2018-06-21 12:25:06.19605+03	2018-11-04	12:25:06	23:59:59.999999	2
650	2018-06-21 12:25:06.196068+03	2018-06-21 12:25:06.196073+03	2018-11-05	12:25:06	23:59:59.999999	2
651	2018-06-21 12:25:06.19609+03	2018-06-21 12:25:06.196096+03	2018-11-06	12:25:06	23:59:59.999999	2
652	2018-06-21 12:25:06.196113+03	2018-06-21 12:25:06.196118+03	2018-11-07	12:25:06	23:59:59.999999	2
653	2018-06-21 12:25:06.196135+03	2018-06-21 12:25:06.196141+03	2018-11-08	12:25:06	23:59:59.999999	2
654	2018-06-21 12:25:06.196158+03	2018-06-21 12:25:06.196163+03	2018-11-09	12:25:06	23:59:59.999999	2
655	2018-06-21 12:25:06.196195+03	2018-06-21 12:25:06.1962+03	2018-11-10	12:25:06	23:59:59.999999	2
656	2018-06-21 12:25:06.196218+03	2018-06-21 12:25:06.196224+03	2018-11-11	12:25:06	23:59:59.999999	2
657	2018-06-21 12:25:06.196241+03	2018-06-21 12:25:06.196247+03	2018-11-12	12:25:06	23:59:59.999999	2
658	2018-06-21 12:25:06.196264+03	2018-06-21 12:25:06.196269+03	2018-11-13	12:25:06	23:59:59.999999	2
659	2018-06-21 12:25:06.196287+03	2018-06-21 12:25:06.196292+03	2018-11-14	12:25:06	23:59:59.999999	2
660	2018-06-21 12:25:06.19631+03	2018-06-21 12:25:06.196315+03	2018-11-15	12:25:06	23:59:59.999999	2
661	2018-06-21 12:25:06.196333+03	2018-06-21 12:25:06.196338+03	2018-11-16	12:25:06	23:59:59.999999	2
662	2018-06-21 12:25:06.196355+03	2018-06-21 12:25:06.196361+03	2018-11-17	12:25:06	23:59:59.999999	2
663	2018-06-21 12:25:06.196378+03	2018-06-21 12:25:06.196383+03	2018-11-18	12:25:06	23:59:59.999999	2
664	2018-06-21 12:25:06.196401+03	2018-06-21 12:25:06.196406+03	2018-11-19	12:25:06	23:59:59.999999	2
665	2018-06-21 12:25:06.196494+03	2018-06-21 12:25:06.196502+03	2018-11-20	12:25:06	23:59:59.999999	2
666	2018-06-21 12:25:06.196533+03	2018-06-21 12:25:06.196539+03	2018-11-21	12:25:06	23:59:59.999999	2
667	2018-06-21 12:25:06.196558+03	2018-06-21 12:25:06.196564+03	2018-11-22	12:25:06	23:59:59.999999	2
668	2018-06-21 12:25:06.196581+03	2018-06-21 12:25:06.196587+03	2018-11-23	12:25:06	23:59:59.999999	2
669	2018-06-21 12:25:06.196605+03	2018-06-21 12:25:06.196611+03	2018-11-24	12:25:06	23:59:59.999999	2
670	2018-06-21 12:25:06.196629+03	2018-06-21 12:25:06.196634+03	2018-11-25	12:25:06	23:59:59.999999	2
671	2018-06-21 12:25:06.196652+03	2018-06-21 12:25:06.196658+03	2018-11-26	12:25:06	23:59:59.999999	2
672	2018-06-21 12:25:06.196676+03	2018-06-21 12:25:06.196682+03	2018-11-27	12:25:06	23:59:59.999999	2
673	2018-06-21 12:25:06.1967+03	2018-06-21 12:25:06.196705+03	2018-11-28	12:25:06	23:59:59.999999	2
674	2018-06-21 12:25:06.196723+03	2018-06-21 12:25:06.196729+03	2018-11-29	12:25:06	23:59:59.999999	2
675	2018-06-21 12:25:06.196747+03	2018-06-21 12:25:06.196752+03	2018-11-30	12:25:06	23:59:59.999999	2
676	2018-06-21 12:25:06.19677+03	2018-06-21 12:25:06.196775+03	2018-12-01	12:25:06	23:59:59.999999	2
677	2018-06-21 12:25:06.196793+03	2018-06-21 12:25:06.196799+03	2018-12-02	12:25:06	23:59:59.999999	2
678	2018-06-21 12:25:06.196817+03	2018-06-21 12:25:06.196822+03	2018-12-03	12:25:06	23:59:59.999999	2
679	2018-06-21 12:25:06.19684+03	2018-06-21 12:25:06.196846+03	2018-12-04	12:25:06	23:59:59.999999	2
680	2018-06-21 12:25:06.196863+03	2018-06-21 12:25:06.196869+03	2018-12-05	12:25:06	23:59:59.999999	2
681	2018-06-21 12:25:06.196887+03	2018-06-21 12:25:06.196893+03	2018-12-06	12:25:06	23:59:59.999999	2
682	2018-06-21 12:25:06.19691+03	2018-06-21 12:25:06.196916+03	2018-12-07	12:25:06	23:59:59.999999	2
683	2018-06-21 12:25:06.196934+03	2018-06-21 12:25:06.196939+03	2018-12-08	12:25:06	23:59:59.999999	2
684	2018-06-21 12:25:06.196957+03	2018-06-21 12:25:06.196962+03	2018-12-09	12:25:06	23:59:59.999999	2
685	2018-06-21 12:25:06.19698+03	2018-06-21 12:25:06.196986+03	2018-12-10	12:25:06	23:59:59.999999	2
686	2018-06-21 12:25:06.197003+03	2018-06-21 12:25:06.197009+03	2018-12-11	12:25:06	23:59:59.999999	2
687	2018-06-21 12:25:06.197027+03	2018-06-21 12:25:06.197032+03	2018-12-12	12:25:06	23:59:59.999999	2
688	2018-06-21 12:25:06.19705+03	2018-06-21 12:25:06.197056+03	2018-12-13	12:25:06	23:59:59.999999	2
689	2018-06-21 12:25:06.197073+03	2018-06-21 12:25:06.197079+03	2018-12-14	12:25:06	23:59:59.999999	2
690	2018-06-21 12:25:06.197097+03	2018-06-21 12:25:06.197103+03	2018-12-15	12:25:06	23:59:59.999999	2
691	2018-06-21 12:25:06.197121+03	2018-06-21 12:25:06.197127+03	2018-12-16	12:25:06	23:59:59.999999	2
692	2018-06-21 12:25:06.197162+03	2018-06-21 12:25:06.197167+03	2018-12-17	12:25:06	23:59:59.999999	2
693	2018-06-21 12:25:06.197186+03	2018-06-21 12:25:06.197192+03	2018-12-18	12:25:06	23:59:59.999999	2
694	2018-06-21 12:25:06.19721+03	2018-06-21 12:25:06.197216+03	2018-12-19	12:25:06	23:59:59.999999	2
695	2018-06-21 12:25:06.197236+03	2018-06-21 12:25:06.197242+03	2018-12-20	12:25:06	23:59:59.999999	2
696	2018-06-21 12:25:06.197261+03	2018-06-21 12:25:06.197268+03	2018-12-21	12:25:06	23:59:59.999999	2
697	2018-06-21 12:25:06.197288+03	2018-06-21 12:25:06.197294+03	2018-12-22	12:25:06	23:59:59.999999	2
698	2018-06-21 12:25:06.197313+03	2018-06-21 12:25:06.197319+03	2018-12-23	12:25:06	23:59:59.999999	2
699	2018-06-21 12:25:06.197337+03	2018-06-21 12:25:06.197344+03	2018-12-24	12:25:06	23:59:59.999999	2
700	2018-06-21 12:25:06.197363+03	2018-06-21 12:25:06.197369+03	2018-12-25	12:25:06	23:59:59.999999	2
701	2018-06-21 12:25:06.197404+03	2018-06-21 12:25:06.197411+03	2018-12-26	12:25:06	23:59:59.999999	2
702	2018-06-21 12:25:06.19743+03	2018-06-21 12:25:06.197436+03	2018-12-27	12:25:06	23:59:59.999999	2
703	2018-06-21 12:25:06.197455+03	2018-06-21 12:25:06.197461+03	2018-12-28	12:25:06	23:59:59.999999	2
704	2018-06-21 12:25:06.197481+03	2018-06-21 12:25:06.197487+03	2018-12-29	12:25:06	23:59:59.999999	2
705	2018-06-21 12:25:06.197505+03	2018-06-21 12:25:06.197511+03	2018-12-30	12:25:06	23:59:59.999999	2
706	2018-06-21 12:25:06.19753+03	2018-06-21 12:25:06.197536+03	2018-12-31	12:25:06	23:59:59.999999	2
707	2018-06-21 12:25:06.197554+03	2018-06-21 12:25:06.19756+03	2019-01-01	12:25:06	23:59:59.999999	2
708	2018-06-21 12:25:06.197579+03	2018-06-21 12:25:06.197585+03	2019-01-02	12:25:06	23:59:59.999999	2
709	2018-06-21 12:25:06.197604+03	2018-06-21 12:25:06.19761+03	2019-01-03	12:25:06	23:59:59.999999	2
710	2018-06-21 12:25:06.197629+03	2018-06-21 12:25:06.197635+03	2019-01-04	12:25:06	23:59:59.999999	2
711	2018-06-21 12:25:06.197654+03	2018-06-21 12:25:06.197659+03	2019-01-05	12:25:06	23:59:59.999999	2
712	2018-06-21 12:25:06.197678+03	2018-06-21 12:25:06.197684+03	2019-01-06	12:25:06	23:59:59.999999	2
713	2018-06-21 12:25:06.197702+03	2018-06-21 12:25:06.197708+03	2019-01-07	12:25:06	23:59:59.999999	2
714	2018-06-21 12:25:06.197727+03	2018-06-21 12:25:06.197733+03	2019-01-08	12:25:06	23:59:59.999999	2
715	2018-06-21 12:25:06.197751+03	2018-06-21 12:25:06.197758+03	2019-01-09	12:25:06	23:59:59.999999	2
716	2018-06-21 12:25:06.197777+03	2018-06-21 12:25:06.197787+03	2019-01-10	12:25:06	23:59:59.999999	2
717	2018-06-21 12:25:06.197816+03	2018-06-21 12:25:06.197826+03	2019-01-11	12:25:06	23:59:59.999999	2
718	2018-06-21 12:25:06.197856+03	2018-06-21 12:25:06.197866+03	2019-01-12	12:25:06	23:59:59.999999	2
719	2018-06-21 12:25:06.197898+03	2018-06-21 12:25:06.197905+03	2019-01-13	12:25:06	23:59:59.999999	2
720	2018-06-21 12:25:06.197924+03	2018-06-21 12:25:06.19793+03	2019-01-14	12:25:06	23:59:59.999999	2
721	2018-06-21 12:25:06.197949+03	2018-06-21 12:25:06.197955+03	2019-01-15	12:25:06	23:59:59.999999	2
722	2018-06-21 12:25:06.197974+03	2018-06-21 12:25:06.19798+03	2019-01-16	12:25:06	23:59:59.999999	2
723	2018-06-21 12:25:06.198009+03	2018-06-21 12:25:06.19802+03	2019-01-17	12:25:06	23:59:59.999999	2
724	2018-06-21 12:25:06.198054+03	2018-06-21 12:25:06.198065+03	2019-01-18	12:25:06	23:59:59.999999	2
725	2018-06-21 12:25:06.198086+03	2018-06-21 12:25:06.198093+03	2019-01-19	12:25:06	23:59:59.999999	2
726	2018-06-21 12:25:06.198111+03	2018-06-21 12:25:06.198118+03	2019-01-20	12:25:06	23:59:59.999999	2
727	2018-06-21 12:25:06.198137+03	2018-06-21 12:25:06.198143+03	2019-01-21	12:25:06	23:59:59.999999	2
728	2018-06-21 12:25:06.198162+03	2018-06-21 12:25:06.198168+03	2019-01-22	12:25:06	23:59:59.999999	2
729	2018-06-21 12:25:06.198186+03	2018-06-21 12:25:06.198192+03	2019-01-23	12:25:06	23:59:59.999999	2
730	2018-06-21 12:25:06.198229+03	2018-06-21 12:25:06.198235+03	2019-01-24	12:25:06	23:59:59.999999	2
731	2018-06-21 12:25:06.198259+03	2018-06-21 12:25:06.19827+03	2019-01-25	12:25:06	23:59:59.999999	2
732	2018-06-21 12:25:06.1983+03	2018-06-21 12:25:06.198307+03	2019-01-26	12:25:06	23:59:59.999999	2
733	2018-06-21 12:25:06.198326+03	2018-06-21 12:25:06.198332+03	2019-01-27	12:25:06	23:59:59.999999	2
734	2018-06-21 12:25:06.19835+03	2018-06-21 12:25:06.198357+03	2019-01-28	12:25:06	23:59:59.999999	2
735	2018-06-21 12:25:06.198391+03	2018-06-21 12:25:06.198399+03	2019-01-29	12:25:06	23:59:59.999999	2
736	2018-06-21 12:25:06.198418+03	2018-06-21 12:25:06.198424+03	2019-01-30	12:25:06	23:59:59.999999	2
737	2018-06-21 12:25:06.198443+03	2018-06-21 12:25:06.198449+03	2019-01-31	12:25:06	23:59:59.999999	2
738	2018-06-21 12:25:06.198468+03	2018-06-21 12:25:06.198474+03	2019-02-01	12:25:06	23:59:59.999999	2
739	2018-06-21 12:25:06.198493+03	2018-06-21 12:25:06.198499+03	2019-02-02	12:25:06	23:59:59.999999	2
740	2018-06-21 12:25:06.198518+03	2018-06-21 12:25:06.198524+03	2019-02-03	12:25:06	23:59:59.999999	2
741	2018-06-21 12:25:06.198544+03	2018-06-21 12:25:06.198551+03	2019-02-04	12:25:06	23:59:59.999999	2
742	2018-06-21 12:25:06.19858+03	2018-06-21 12:25:06.198592+03	2019-02-05	12:25:06	23:59:59.999999	2
743	2018-06-21 12:25:06.198616+03	2018-06-21 12:25:06.198623+03	2019-02-06	12:25:06	23:59:59.999999	2
744	2018-06-21 12:25:06.19865+03	2018-06-21 12:25:06.198662+03	2019-02-07	12:25:06	23:59:59.999999	2
745	2018-06-21 12:25:06.19869+03	2018-06-21 12:25:06.198697+03	2019-02-08	12:25:06	23:59:59.999999	2
746	2018-06-21 12:25:06.198718+03	2018-06-21 12:25:06.198726+03	2019-02-09	12:25:06	23:59:59.999999	2
747	2018-06-21 12:25:06.198765+03	2018-06-21 12:25:06.198776+03	2019-02-10	12:25:06	23:59:59.999999	2
748	2018-06-21 12:25:06.198798+03	2018-06-21 12:25:06.198809+03	2019-02-11	12:25:06	23:59:59.999999	2
749	2018-06-21 12:25:06.198835+03	2018-06-21 12:25:06.198842+03	2019-02-12	12:25:06	23:59:59.999999	2
750	2018-06-21 12:25:06.198862+03	2018-06-21 12:25:06.198869+03	2019-02-13	12:25:06	23:59:59.999999	2
751	2018-06-21 12:25:06.198894+03	2018-06-21 12:25:06.198906+03	2019-02-14	12:25:06	23:59:59.999999	2
752	2018-06-21 12:25:06.198933+03	2018-06-21 12:25:06.198941+03	2019-02-15	12:25:06	23:59:59.999999	2
753	2018-06-21 12:25:06.198961+03	2018-06-21 12:25:06.198967+03	2019-02-16	12:25:06	23:59:59.999999	2
754	2018-06-21 12:25:06.198989+03	2018-06-21 12:25:06.198996+03	2019-02-17	12:25:06	23:59:59.999999	2
755	2018-06-21 12:25:06.199018+03	2018-06-21 12:25:06.199026+03	2019-02-18	12:25:06	23:59:59.999999	2
756	2018-06-21 12:25:06.199048+03	2018-06-21 12:25:06.199054+03	2019-02-19	12:25:06	23:59:59.999999	2
757	2018-06-21 12:25:06.199075+03	2018-06-21 12:25:06.199082+03	2019-02-20	12:25:06	23:59:59.999999	2
758	2018-06-21 12:25:06.199112+03	2018-06-21 12:25:06.199126+03	2019-02-21	12:25:06	23:59:59.999999	2
759	2018-06-21 12:25:06.199166+03	2018-06-21 12:25:06.199176+03	2019-02-22	12:25:06	23:59:59.999999	2
760	2018-06-21 12:25:06.199207+03	2018-06-21 12:25:06.19922+03	2019-02-23	12:25:06	23:59:59.999999	2
761	2018-06-21 12:25:06.199257+03	2018-06-21 12:25:06.199269+03	2019-02-24	12:25:06	23:59:59.999999	2
762	2018-06-21 12:25:06.199325+03	2018-06-21 12:25:06.199336+03	2019-02-25	12:25:06	23:59:59.999999	2
763	2018-06-21 12:25:06.19936+03	2018-06-21 12:25:06.199367+03	2019-02-26	12:25:06	23:59:59.999999	2
764	2018-06-21 12:25:06.199387+03	2018-06-21 12:25:06.199393+03	2019-02-27	12:25:06	23:59:59.999999	2
765	2018-06-21 12:25:06.199413+03	2018-06-21 12:25:06.19942+03	2019-02-28	12:25:06	23:59:59.999999	2
766	2018-06-21 12:25:06.19944+03	2018-06-21 12:25:06.199447+03	2019-03-01	12:25:06	23:59:59.999999	2
767	2018-06-21 12:25:06.199467+03	2018-06-21 12:25:06.199474+03	2019-03-02	12:25:06	23:59:59.999999	2
768	2018-06-21 12:25:06.199494+03	2018-06-21 12:25:06.199501+03	2019-03-03	12:25:06	23:59:59.999999	2
769	2018-06-21 12:25:06.199537+03	2018-06-21 12:25:06.199557+03	2019-03-04	12:25:06	23:59:59.999999	2
770	2018-06-21 12:25:06.199601+03	2018-06-21 12:25:06.199622+03	2019-03-05	12:25:06	23:59:59.999999	2
771	2018-06-21 12:25:06.199674+03	2018-06-21 12:25:06.199684+03	2019-03-06	12:25:06	23:59:59.999999	2
772	2018-06-21 12:25:06.199791+03	2018-06-21 12:25:06.199805+03	2019-03-07	12:25:06	23:59:59.999999	2
773	2018-06-21 12:25:06.199833+03	2018-06-21 12:25:06.199841+03	2019-03-08	12:25:06	23:59:59.999999	2
774	2018-06-21 12:25:06.199863+03	2018-06-21 12:25:06.199871+03	2019-03-09	12:25:06	23:59:59.999999	2
775	2018-06-21 12:25:06.199894+03	2018-06-21 12:25:06.199901+03	2019-03-10	12:25:06	23:59:59.999999	2
776	2018-06-21 12:25:06.199926+03	2018-06-21 12:25:06.199934+03	2019-03-11	12:25:06	23:59:59.999999	2
777	2018-06-21 12:25:06.199957+03	2018-06-21 12:25:06.199965+03	2019-03-12	12:25:06	23:59:59.999999	2
778	2018-06-21 12:25:06.199993+03	2018-06-21 12:25:06.200001+03	2019-03-13	12:25:06	23:59:59.999999	2
779	2018-06-21 12:25:06.200025+03	2018-06-21 12:25:06.200033+03	2019-03-14	12:25:06	23:59:59.999999	2
780	2018-06-21 12:25:06.200056+03	2018-06-21 12:25:06.200065+03	2019-03-15	12:25:06	23:59:59.999999	2
781	2018-06-21 12:25:06.200088+03	2018-06-21 12:25:06.200096+03	2019-03-16	12:25:06	23:59:59.999999	2
782	2018-06-21 12:25:06.20012+03	2018-06-21 12:25:06.200127+03	2019-03-17	12:25:06	23:59:59.999999	2
783	2018-06-21 12:25:06.200156+03	2018-06-21 12:25:06.200166+03	2019-03-18	12:25:06	23:59:59.999999	2
784	2018-06-21 12:25:06.20019+03	2018-06-21 12:25:06.200197+03	2019-03-19	12:25:06	23:59:59.999999	2
785	2018-06-21 12:25:06.200219+03	2018-06-21 12:25:06.200227+03	2019-03-20	12:25:06	23:59:59.999999	2
786	2018-06-21 12:25:06.200259+03	2018-06-21 12:25:06.200272+03	2019-03-21	12:25:06	23:59:59.999999	2
787	2018-06-21 12:25:06.200314+03	2018-06-21 12:25:06.200328+03	2019-03-22	12:25:06	23:59:59.999999	2
788	2018-06-21 12:25:06.200386+03	2018-06-21 12:25:06.200399+03	2019-03-23	12:25:06	23:59:59.999999	2
789	2018-06-21 12:25:06.200435+03	2018-06-21 12:25:06.200446+03	2019-03-24	12:25:06	23:59:59.999999	2
790	2018-06-21 12:25:06.200476+03	2018-06-21 12:25:06.200488+03	2019-03-25	12:25:06	23:59:59.999999	2
791	2018-06-21 12:25:06.200548+03	2018-06-21 12:25:06.200555+03	2019-03-26	12:25:06	23:59:59.999999	2
792	2018-06-21 12:25:06.200575+03	2018-06-21 12:25:06.200582+03	2019-03-27	12:25:06	23:59:59.999999	2
793	2018-06-21 12:25:06.2006+03	2018-06-21 12:25:06.200606+03	2019-03-28	12:25:06	23:59:59.999999	2
794	2018-06-21 12:25:06.200624+03	2018-06-21 12:25:06.20063+03	2019-03-29	12:25:06	23:59:59.999999	2
795	2018-06-21 12:25:06.200649+03	2018-06-21 12:25:06.200655+03	2019-03-30	12:25:06	23:59:59.999999	2
796	2018-06-21 12:25:06.200675+03	2018-06-21 12:25:06.200681+03	2019-03-31	12:25:06	23:59:59.999999	2
797	2018-06-21 12:25:06.2007+03	2018-06-21 12:25:06.200706+03	2019-04-01	12:25:06	23:59:59.999999	2
798	2018-06-21 12:25:06.200726+03	2018-06-21 12:25:06.200732+03	2019-04-02	12:25:06	23:59:59.999999	2
799	2018-06-21 12:25:06.200752+03	2018-06-21 12:25:06.200758+03	2019-04-03	12:25:06	23:59:59.999999	2
800	2018-06-21 12:25:06.200778+03	2018-06-21 12:25:06.200784+03	2019-04-04	12:25:06	23:59:59.999999	2
801	2018-06-21 12:25:06.200805+03	2018-06-21 12:25:06.200812+03	2019-04-05	12:25:06	23:59:59.999999	2
802	2018-06-21 12:25:06.200833+03	2018-06-21 12:25:06.20084+03	2019-04-06	12:25:06	23:59:59.999999	2
803	2018-06-21 12:25:06.200861+03	2018-06-21 12:25:06.200868+03	2019-04-07	12:25:06	23:59:59.999999	2
804	2018-06-21 12:25:06.200889+03	2018-06-21 12:25:06.200895+03	2019-04-08	12:25:06	23:59:59.999999	2
805	2018-06-21 12:25:06.200917+03	2018-06-21 12:25:06.200924+03	2019-04-09	12:25:06	23:59:59.999999	2
806	2018-06-21 12:25:06.200945+03	2018-06-21 12:25:06.200951+03	2019-04-10	12:25:06	23:59:59.999999	2
807	2018-06-21 12:25:06.200974+03	2018-06-21 12:25:06.200981+03	2019-04-11	12:25:06	23:59:59.999999	2
808	2018-06-21 12:25:06.201003+03	2018-06-21 12:25:06.201011+03	2019-04-12	12:25:06	23:59:59.999999	2
809	2018-06-21 12:25:06.201035+03	2018-06-21 12:25:06.201043+03	2019-04-13	12:25:06	23:59:59.999999	2
810	2018-06-21 12:25:06.201067+03	2018-06-21 12:25:06.201075+03	2019-04-14	12:25:06	23:59:59.999999	2
811	2018-06-21 12:25:06.201097+03	2018-06-21 12:25:06.201104+03	2019-04-15	12:25:06	23:59:59.999999	2
812	2018-06-21 12:25:06.201126+03	2018-06-21 12:25:06.201134+03	2019-04-16	12:25:06	23:59:59.999999	2
813	2018-06-21 12:25:06.201156+03	2018-06-21 12:25:06.201162+03	2019-04-17	12:25:06	23:59:59.999999	2
814	2018-06-21 12:25:06.201184+03	2018-06-21 12:25:06.201191+03	2019-04-18	12:25:06	23:59:59.999999	2
815	2018-06-21 12:25:06.201213+03	2018-06-21 12:25:06.20122+03	2019-04-19	12:25:06	23:59:59.999999	2
816	2018-06-21 12:25:06.201241+03	2018-06-21 12:25:06.201248+03	2019-04-20	12:25:06	23:59:59.999999	2
817	2018-06-21 12:25:06.201269+03	2018-06-21 12:25:06.201276+03	2019-04-21	12:25:06	23:59:59.999999	2
818	2018-06-21 12:25:06.201296+03	2018-06-21 12:25:06.201303+03	2019-04-22	12:25:06	23:59:59.999999	2
819	2018-06-21 12:25:06.201324+03	2018-06-21 12:25:06.201331+03	2019-04-23	12:25:06	23:59:59.999999	2
820	2018-06-21 12:25:06.201352+03	2018-06-21 12:25:06.20136+03	2019-04-24	12:25:06	23:59:59.999999	2
821	2018-06-21 12:25:06.201381+03	2018-06-21 12:25:06.201389+03	2019-04-25	12:25:06	23:59:59.999999	2
822	2018-06-21 12:25:06.201409+03	2018-06-21 12:25:06.201436+03	2019-04-26	12:25:06	23:59:59.999999	2
823	2018-06-21 12:25:06.20146+03	2018-06-21 12:25:06.201467+03	2019-04-27	12:25:06	23:59:59.999999	2
824	2018-06-21 12:25:06.201489+03	2018-06-21 12:25:06.201496+03	2019-04-28	12:25:06	23:59:59.999999	2
825	2018-06-21 12:25:06.201515+03	2018-06-21 12:25:06.201523+03	2019-04-29	12:25:06	23:59:59.999999	2
826	2018-06-21 12:25:06.201545+03	2018-06-21 12:25:06.201553+03	2019-04-30	12:25:06	23:59:59.999999	2
827	2018-06-21 12:25:06.201575+03	2018-06-21 12:25:06.201583+03	2019-05-01	12:25:06	23:59:59.999999	2
828	2018-06-21 12:25:06.201605+03	2018-06-21 12:25:06.201617+03	2019-05-02	12:25:06	23:59:59.999999	2
829	2018-06-21 12:25:06.201656+03	2018-06-21 12:25:06.201668+03	2019-05-03	12:25:06	23:59:59.999999	2
830	2018-06-21 12:25:06.201704+03	2018-06-21 12:25:06.201714+03	2019-05-04	12:25:06	23:59:59.999999	2
831	2018-06-21 12:25:06.201748+03	2018-06-21 12:25:06.201758+03	2019-05-05	12:25:06	23:59:59.999999	2
832	2018-06-21 12:25:06.20179+03	2018-06-21 12:25:06.201802+03	2019-05-06	12:25:06	23:59:59.999999	2
833	2018-06-21 12:25:06.201837+03	2018-06-21 12:25:06.201847+03	2019-05-07	12:25:06	23:59:59.999999	2
834	2018-06-21 12:25:06.201879+03	2018-06-21 12:25:06.201891+03	2019-05-08	12:25:06	23:59:59.999999	2
835	2018-06-21 12:25:06.201922+03	2018-06-21 12:25:06.201929+03	2019-05-09	12:25:06	23:59:59.999999	2
836	2018-06-21 12:25:06.201949+03	2018-06-21 12:25:06.201955+03	2019-05-10	12:25:06	23:59:59.999999	2
837	2018-06-21 12:25:06.201973+03	2018-06-21 12:25:06.20198+03	2019-05-11	12:25:06	23:59:59.999999	2
838	2018-06-21 12:25:06.201998+03	2018-06-21 12:25:06.202004+03	2019-05-12	12:25:06	23:59:59.999999	2
839	2018-06-21 12:25:06.202022+03	2018-06-21 12:25:06.202028+03	2019-05-13	12:25:06	23:59:59.999999	2
840	2018-06-21 12:25:06.202047+03	2018-06-21 12:25:06.202053+03	2019-05-14	12:25:06	23:59:59.999999	2
841	2018-06-21 12:25:06.202072+03	2018-06-21 12:25:06.202078+03	2019-05-15	12:25:06	23:59:59.999999	2
842	2018-06-21 12:25:06.202097+03	2018-06-21 12:25:06.202103+03	2019-05-16	12:25:06	23:59:59.999999	2
843	2018-06-21 12:25:06.202121+03	2018-06-21 12:25:06.202127+03	2019-05-17	12:25:06	23:59:59.999999	2
844	2018-06-21 12:25:06.202147+03	2018-06-21 12:25:06.202153+03	2019-05-18	12:25:06	23:59:59.999999	2
845	2018-06-21 12:25:06.202172+03	2018-06-21 12:25:06.202178+03	2019-05-19	12:25:06	23:59:59.999999	2
846	2018-06-21 12:25:06.202196+03	2018-06-21 12:25:06.202202+03	2019-05-20	12:25:06	23:59:59.999999	2
847	2018-06-21 12:25:06.202222+03	2018-06-21 12:25:06.202228+03	2019-05-21	12:25:06	23:59:59.999999	2
848	2018-06-21 12:25:06.202247+03	2018-06-21 12:25:06.202253+03	2019-05-22	12:25:06	23:59:59.999999	2
849	2018-06-21 12:25:06.202274+03	2018-06-21 12:25:06.202281+03	2019-05-23	12:25:06	23:59:59.999999	2
850	2018-06-21 12:25:06.202301+03	2018-06-21 12:25:06.202307+03	2019-05-24	12:25:06	23:59:59.999999	2
851	2018-06-21 12:25:06.202328+03	2018-06-21 12:25:06.202334+03	2019-05-25	12:25:06	23:59:59.999999	2
852	2018-06-21 12:25:06.202355+03	2018-06-21 12:25:06.202362+03	2019-05-26	12:25:06	23:59:59.999999	2
853	2018-06-21 12:25:06.202384+03	2018-06-21 12:25:06.202391+03	2019-05-27	12:25:06	23:59:59.999999	2
854	2018-06-21 12:25:06.202411+03	2018-06-21 12:25:06.202417+03	2019-05-28	12:25:06	23:59:59.999999	2
855	2018-06-21 12:25:06.202439+03	2018-06-21 12:25:06.202446+03	2019-05-29	12:25:06	23:59:59.999999	2
856	2018-06-21 12:25:06.202467+03	2018-06-21 12:25:06.202474+03	2019-05-30	12:25:06	23:59:59.999999	2
857	2018-06-21 12:25:06.202517+03	2018-06-21 12:25:06.202524+03	2019-05-31	12:25:06	23:59:59.999999	2
858	2018-06-21 12:25:06.202545+03	2018-06-21 12:25:06.202552+03	2019-06-01	12:25:06	23:59:59.999999	2
859	2018-06-21 12:25:06.202586+03	2018-06-21 12:25:06.202596+03	2019-06-02	12:25:06	23:59:59.999999	2
860	2018-06-21 12:25:06.202628+03	2018-06-21 12:25:06.202639+03	2019-06-03	12:25:06	23:59:59.999999	2
861	2018-06-21 12:25:06.20267+03	2018-06-21 12:25:06.202681+03	2019-06-04	12:25:06	23:59:59.999999	2
862	2018-06-21 12:25:06.20271+03	2018-06-21 12:25:06.202717+03	2019-06-05	12:25:06	23:59:59.999999	2
863	2018-06-21 12:25:06.202736+03	2018-06-21 12:25:06.202742+03	2019-06-06	12:25:06	23:59:59.999999	2
864	2018-06-21 12:25:06.202761+03	2018-06-21 12:25:06.202767+03	2019-06-07	12:25:06	23:59:59.999999	2
865	2018-06-21 12:25:06.202785+03	2018-06-21 12:25:06.202792+03	2019-06-08	12:25:06	23:59:59.999999	2
866	2018-06-21 12:25:06.202811+03	2018-06-21 12:25:06.202817+03	2019-06-09	12:25:06	23:59:59.999999	2
867	2018-06-21 12:25:06.202836+03	2018-06-21 12:25:06.202841+03	2019-06-10	12:25:06	23:59:59.999999	2
868	2018-06-21 12:25:06.202876+03	2018-06-21 12:25:06.202883+03	2019-06-11	12:25:06	23:59:59.999999	2
869	2018-06-21 12:25:06.202903+03	2018-06-21 12:25:06.202909+03	2019-06-12	12:25:06	23:59:59.999999	2
870	2018-06-21 12:25:06.202927+03	2018-06-21 12:25:06.202934+03	2019-06-13	12:25:06	23:59:59.999999	2
871	2018-06-21 12:25:06.202953+03	2018-06-21 12:25:06.202959+03	2019-06-14	12:25:06	23:59:59.999999	2
872	2018-06-21 12:25:06.202977+03	2018-06-21 12:25:06.202983+03	2019-06-15	12:25:06	23:59:59.999999	2
873	2018-06-21 12:25:06.203002+03	2018-06-21 12:25:06.203008+03	2019-06-16	12:25:06	23:59:59.999999	2
874	2018-06-21 12:25:06.203027+03	2018-06-21 12:25:06.203033+03	2019-06-17	12:25:06	23:59:59.999999	2
875	2018-06-21 12:25:06.203052+03	2018-06-21 12:25:06.203058+03	2019-06-18	12:25:06	23:59:59.999999	2
876	2018-06-21 12:25:06.203078+03	2018-06-21 12:25:06.203085+03	2019-06-19	12:25:06	23:59:59.999999	2
877	2018-06-21 12:25:06.203104+03	2018-06-21 12:25:06.203111+03	2019-06-20	12:25:06	23:59:59.999999	2
878	2018-06-21 12:25:06.203131+03	2018-06-21 12:25:06.203137+03	2019-06-21	12:25:06	23:59:59.999999	2
879	2018-06-21 12:25:06.203157+03	2018-06-21 12:25:06.203164+03	2019-06-22	12:25:06	23:59:59.999999	2
880	2018-06-21 12:25:06.203184+03	2018-06-21 12:25:06.20319+03	2019-06-23	12:25:06	23:59:59.999999	2
881	2018-06-21 12:25:06.20321+03	2018-06-21 12:25:06.203216+03	2019-06-24	12:25:06	23:59:59.999999	2
882	2018-06-21 12:25:06.203236+03	2018-06-21 12:25:06.203243+03	2019-06-25	12:25:06	23:59:59.999999	2
883	2018-06-21 12:25:06.203263+03	2018-06-21 12:25:06.203269+03	2019-06-26	12:25:06	23:59:59.999999	2
884	2018-06-21 12:25:06.203291+03	2018-06-21 12:25:06.203297+03	2019-06-27	12:25:06	23:59:59.999999	2
885	2018-06-21 12:25:06.203318+03	2018-06-21 12:25:06.203326+03	2019-06-28	12:25:06	23:59:59.999999	2
886	2018-06-21 12:25:06.203346+03	2018-06-21 12:25:06.203352+03	2019-06-29	12:25:06	23:59:59.999999	2
887	2018-06-21 12:25:06.203373+03	2018-06-21 12:25:06.20338+03	2019-06-30	12:25:06	23:59:59.999999	2
888	2018-06-21 12:25:06.203401+03	2018-06-21 12:25:06.203408+03	2019-07-01	12:25:06	23:59:59.999999	2
889	2018-06-21 12:25:06.203428+03	2018-06-21 12:25:06.203435+03	2019-07-02	12:25:06	23:59:59.999999	2
890	2018-06-21 12:25:06.203455+03	2018-06-21 12:25:06.203462+03	2019-07-03	12:25:06	23:59:59.999999	2
891	2018-06-21 12:25:06.2035+03	2018-06-21 12:25:06.203508+03	2019-07-04	12:25:06	23:59:59.999999	2
892	2018-06-21 12:25:06.203528+03	2018-06-21 12:25:06.203536+03	2019-07-05	12:25:06	23:59:59.999999	2
893	2018-06-21 12:25:06.20357+03	2018-06-21 12:25:06.203577+03	2019-07-06	12:25:06	23:59:59.999999	2
894	2018-06-21 12:25:06.203598+03	2018-06-21 12:25:06.203605+03	2019-07-07	12:25:06	23:59:59.999999	2
895	2018-06-21 12:25:06.203627+03	2018-06-21 12:25:06.203634+03	2019-07-08	12:25:06	23:59:59.999999	2
896	2018-06-21 12:25:06.203655+03	2018-06-21 12:25:06.203662+03	2019-07-09	12:25:06	23:59:59.999999	2
897	2018-06-21 12:25:06.203684+03	2018-06-21 12:25:06.203691+03	2019-07-10	12:25:06	23:59:59.999999	2
898	2018-06-21 12:25:06.203713+03	2018-06-21 12:25:06.20372+03	2019-07-11	12:25:06	23:59:59.999999	2
899	2018-06-21 12:25:06.203744+03	2018-06-21 12:25:06.203756+03	2019-07-12	12:25:06	23:59:59.999999	2
900	2018-06-21 12:25:06.203791+03	2018-06-21 12:25:06.203803+03	2019-07-13	12:25:06	23:59:59.999999	2
901	2018-06-21 12:25:06.203835+03	2018-06-21 12:25:06.203847+03	2019-07-14	12:25:06	23:59:59.999999	2
902	2018-06-21 12:25:06.203883+03	2018-06-21 12:25:06.203891+03	2019-07-15	12:25:06	23:59:59.999999	2
903	2018-06-21 12:25:06.203911+03	2018-06-21 12:25:06.203917+03	2019-07-16	12:25:06	23:59:59.999999	2
904	2018-06-21 12:25:06.203937+03	2018-06-21 12:25:06.203943+03	2019-07-17	12:25:06	23:59:59.999999	2
905	2018-06-21 12:25:06.203963+03	2018-06-21 12:25:06.20397+03	2019-07-18	12:25:06	23:59:59.999999	2
906	2018-06-21 12:25:06.203989+03	2018-06-21 12:25:06.203995+03	2019-07-19	12:25:06	23:59:59.999999	2
907	2018-06-21 12:25:06.204014+03	2018-06-21 12:25:06.20402+03	2019-07-20	12:25:06	23:59:59.999999	2
908	2018-06-21 12:25:06.204038+03	2018-06-21 12:25:06.204044+03	2019-07-21	12:25:06	23:59:59.999999	2
909	2018-06-21 12:25:06.204062+03	2018-06-21 12:25:06.204068+03	2019-07-22	12:25:06	23:59:59.999999	2
910	2018-06-21 12:25:06.204101+03	2018-06-21 12:25:06.204107+03	2019-07-23	12:25:06	23:59:59.999999	2
911	2018-06-21 12:25:06.204127+03	2018-06-21 12:25:06.204134+03	2019-07-24	12:25:06	23:59:59.999999	2
912	2018-06-21 12:25:06.204154+03	2018-06-21 12:25:06.20416+03	2019-07-25	12:25:06	23:59:59.999999	2
913	2018-06-21 12:25:06.204179+03	2018-06-21 12:25:06.204186+03	2019-07-26	12:25:06	23:59:59.999999	2
914	2018-06-21 12:25:06.204204+03	2018-06-21 12:25:06.20421+03	2019-07-27	12:25:06	23:59:59.999999	2
915	2018-06-21 12:25:06.204229+03	2018-06-21 12:25:06.204236+03	2019-07-28	12:25:06	23:59:59.999999	2
916	2018-06-21 12:25:06.204256+03	2018-06-21 12:25:06.204262+03	2019-07-29	12:25:06	23:59:59.999999	2
917	2018-06-21 12:25:06.204282+03	2018-06-21 12:25:06.204289+03	2019-07-30	12:25:06	23:59:59.999999	2
918	2018-06-21 12:25:06.204309+03	2018-06-21 12:25:06.204316+03	2019-07-31	12:25:06	23:59:59.999999	2
919	2018-06-21 12:25:06.204338+03	2018-06-21 12:25:06.204344+03	2019-08-01	12:25:06	23:59:59.999999	2
920	2018-06-21 12:25:06.204364+03	2018-06-21 12:25:06.204371+03	2019-08-02	12:25:06	23:59:59.999999	2
921	2018-06-21 12:25:06.204392+03	2018-06-21 12:25:06.204399+03	2019-08-03	12:25:06	23:59:59.999999	2
922	2018-06-21 12:25:06.204418+03	2018-06-21 12:25:06.204466+03	2019-08-04	12:25:06	23:59:59.999999	2
923	2018-06-21 12:25:06.204502+03	2018-06-21 12:25:06.204525+03	2019-08-05	12:25:06	23:59:59.999999	2
924	2018-06-21 12:25:06.204561+03	2018-06-21 12:25:06.204573+03	2019-08-06	12:25:06	23:59:59.999999	2
925	2018-06-21 12:25:06.20461+03	2018-06-21 12:25:06.204622+03	2019-08-07	12:25:06	23:59:59.999999	2
926	2018-06-21 12:25:06.204656+03	2018-06-21 12:25:06.204667+03	2019-08-08	12:25:06	23:59:59.999999	2
927	2018-06-21 12:25:06.204692+03	2018-06-21 12:25:06.204698+03	2019-08-09	12:25:06	23:59:59.999999	2
928	2018-06-21 12:25:06.204718+03	2018-06-21 12:25:06.204725+03	2019-08-10	12:25:06	23:59:59.999999	2
929	2018-06-21 12:25:06.204745+03	2018-06-21 12:25:06.204752+03	2019-08-11	12:25:06	23:59:59.999999	2
930	2018-06-21 12:25:06.204773+03	2018-06-21 12:25:06.20478+03	2019-08-12	12:25:06	23:59:59.999999	2
931	2018-06-21 12:25:06.2048+03	2018-06-21 12:25:06.204806+03	2019-08-13	12:25:06	23:59:59.999999	2
932	2018-06-21 12:25:06.204826+03	2018-06-21 12:25:06.204834+03	2019-08-14	12:25:06	23:59:59.999999	2
933	2018-06-21 12:25:06.204854+03	2018-06-21 12:25:06.20486+03	2019-08-15	12:25:06	23:59:59.999999	2
934	2018-06-21 12:25:06.20488+03	2018-06-21 12:25:06.204887+03	2019-08-16	12:25:06	23:59:59.999999	2
935	2018-06-21 12:25:06.204908+03	2018-06-21 12:25:06.204915+03	2019-08-17	12:25:06	23:59:59.999999	2
936	2018-06-21 12:25:06.20495+03	2018-06-21 12:25:06.204963+03	2019-08-18	12:25:06	23:59:59.999999	2
937	2018-06-21 12:25:06.204995+03	2018-06-21 12:25:06.205007+03	2019-08-19	12:25:06	23:59:59.999999	2
938	2018-06-21 12:25:06.205042+03	2018-06-21 12:25:06.205053+03	2019-08-20	12:25:06	23:59:59.999999	2
939	2018-06-21 12:25:06.205079+03	2018-06-21 12:25:06.205085+03	2019-08-21	12:25:06	23:59:59.999999	2
940	2018-06-21 12:25:06.205105+03	2018-06-21 12:25:06.205111+03	2019-08-22	12:25:06	23:59:59.999999	2
941	2018-06-21 12:25:06.20513+03	2018-06-21 12:25:06.205136+03	2019-08-23	12:25:06	23:59:59.999999	2
942	2018-06-21 12:25:06.205156+03	2018-06-21 12:25:06.205162+03	2019-08-24	12:25:06	23:59:59.999999	2
943	2018-06-21 12:25:06.20518+03	2018-06-21 12:25:06.205186+03	2019-08-25	12:25:06	23:59:59.999999	2
944	2018-06-21 12:25:06.205205+03	2018-06-21 12:25:06.205211+03	2019-08-26	12:25:06	23:59:59.999999	2
945	2018-06-21 12:25:06.20523+03	2018-06-21 12:25:06.205237+03	2019-08-27	12:25:06	23:59:59.999999	2
946	2018-06-21 12:25:06.205255+03	2018-06-21 12:25:06.205261+03	2019-08-28	12:25:06	23:59:59.999999	2
947	2018-06-21 12:25:06.20528+03	2018-06-21 12:25:06.205286+03	2019-08-29	12:25:06	23:59:59.999999	2
948	2018-06-21 12:25:06.205304+03	2018-06-21 12:25:06.20531+03	2019-08-30	12:25:06	23:59:59.999999	2
949	2018-06-21 12:25:06.205329+03	2018-06-21 12:25:06.205334+03	2019-08-31	12:25:06	23:59:59.999999	2
950	2018-06-21 12:25:06.205353+03	2018-06-21 12:25:06.205359+03	2019-09-01	12:25:06	23:59:59.999999	2
951	2018-06-21 12:25:06.205378+03	2018-06-21 12:25:06.205383+03	2019-09-02	12:25:06	23:59:59.999999	2
952	2018-06-21 12:25:06.205402+03	2018-06-21 12:25:06.205408+03	2019-09-03	12:25:06	23:59:59.999999	2
953	2018-06-21 12:25:06.205427+03	2018-06-21 12:25:06.205433+03	2019-09-04	12:25:06	23:59:59.999999	2
954	2018-06-21 12:25:06.205451+03	2018-06-21 12:25:06.205457+03	2019-09-05	12:25:06	23:59:59.999999	2
955	2018-06-21 12:25:06.205475+03	2018-06-21 12:25:06.205481+03	2019-09-06	12:25:06	23:59:59.999999	2
956	2018-06-21 12:25:06.205499+03	2018-06-21 12:25:06.205505+03	2019-09-07	12:25:06	23:59:59.999999	2
957	2018-06-21 12:25:06.205524+03	2018-06-21 12:25:06.20553+03	2019-09-08	12:25:06	23:59:59.999999	2
958	2018-06-21 12:25:06.205548+03	2018-06-21 12:25:06.205554+03	2019-09-09	12:25:06	23:59:59.999999	2
959	2018-06-21 12:25:06.205573+03	2018-06-21 12:25:06.205579+03	2019-09-10	12:25:06	23:59:59.999999	2
960	2018-06-21 12:25:06.205598+03	2018-06-21 12:25:06.205604+03	2019-09-11	12:25:06	23:59:59.999999	2
961	2018-06-21 12:25:06.205623+03	2018-06-21 12:25:06.205629+03	2019-09-12	12:25:06	23:59:59.999999	2
962	2018-06-21 12:25:06.205648+03	2018-06-21 12:25:06.205655+03	2019-09-13	12:25:06	23:59:59.999999	2
963	2018-06-21 12:25:06.205673+03	2018-06-21 12:25:06.205679+03	2019-09-14	12:25:06	23:59:59.999999	2
964	2018-06-21 12:25:06.205698+03	2018-06-21 12:25:06.205704+03	2019-09-15	12:25:06	23:59:59.999999	2
965	2018-06-21 12:25:06.205723+03	2018-06-21 12:25:06.205728+03	2019-09-16	12:25:06	23:59:59.999999	2
966	2018-06-21 12:25:06.205747+03	2018-06-21 12:25:06.205753+03	2019-09-17	12:25:06	23:59:59.999999	2
967	2018-06-21 12:25:06.205772+03	2018-06-21 12:25:06.205778+03	2019-09-18	12:25:06	23:59:59.999999	2
968	2018-06-21 12:25:06.205796+03	2018-06-21 12:25:06.205802+03	2019-09-19	12:25:06	23:59:59.999999	2
969	2018-06-21 12:25:06.205821+03	2018-06-21 12:25:06.205828+03	2019-09-20	12:25:06	23:59:59.999999	2
970	2018-06-21 12:25:06.205846+03	2018-06-21 12:25:06.205852+03	2019-09-21	12:25:06	23:59:59.999999	2
971	2018-06-21 12:25:06.205871+03	2018-06-21 12:25:06.205877+03	2019-09-22	12:25:06	23:59:59.999999	2
972	2018-06-21 12:25:06.205895+03	2018-06-21 12:25:06.205901+03	2019-09-23	12:25:06	23:59:59.999999	2
973	2018-06-21 12:25:06.20592+03	2018-06-21 12:25:06.205926+03	2019-09-24	12:25:06	23:59:59.999999	2
974	2018-06-21 12:25:06.205944+03	2018-06-21 12:25:06.20595+03	2019-09-25	12:25:06	23:59:59.999999	2
975	2018-06-21 12:25:06.205969+03	2018-06-21 12:25:06.205975+03	2019-09-26	12:25:06	23:59:59.999999	2
976	2018-06-21 12:25:06.206007+03	2018-06-21 12:25:06.206019+03	2019-09-27	12:25:06	23:59:59.999999	2
977	2018-06-21 12:25:06.206054+03	2018-06-21 12:25:06.206066+03	2019-09-28	12:25:06	23:59:59.999999	2
978	2018-06-21 12:25:06.206109+03	2018-06-21 12:25:06.206121+03	2019-09-29	12:25:06	23:59:59.999999	2
979	2018-06-21 12:25:06.206151+03	2018-06-21 12:25:06.206162+03	2019-09-30	12:25:06	23:59:59.999999	2
980	2018-06-21 12:25:06.206191+03	2018-06-21 12:25:06.206201+03	2019-10-01	12:25:06	23:59:59.999999	2
981	2018-06-21 12:25:06.206232+03	2018-06-21 12:25:06.206239+03	2019-10-02	12:25:06	23:59:59.999999	2
982	2018-06-21 12:25:06.206257+03	2018-06-21 12:25:06.206263+03	2019-10-03	12:25:06	23:59:59.999999	2
983	2018-06-21 12:25:06.206288+03	2018-06-21 12:25:06.206294+03	2019-10-04	12:25:06	23:59:59.999999	2
984	2018-06-21 12:25:06.206314+03	2018-06-21 12:25:06.20632+03	2019-10-05	12:25:06	23:59:59.999999	2
985	2018-06-21 12:25:06.206338+03	2018-06-21 12:25:06.206345+03	2019-10-06	12:25:06	23:59:59.999999	2
986	2018-06-21 12:25:06.206363+03	2018-06-21 12:25:06.206369+03	2019-10-07	12:25:06	23:59:59.999999	2
987	2018-06-21 12:25:06.206388+03	2018-06-21 12:25:06.206394+03	2019-10-08	12:25:06	23:59:59.999999	2
988	2018-06-21 12:25:06.206413+03	2018-06-21 12:25:06.206419+03	2019-10-09	12:25:06	23:59:59.999999	2
989	2018-06-21 12:25:06.206439+03	2018-06-21 12:25:06.206445+03	2019-10-10	12:25:06	23:59:59.999999	2
990	2018-06-21 12:25:06.206464+03	2018-06-21 12:25:06.20647+03	2019-10-11	12:25:06	23:59:59.999999	2
991	2018-06-21 12:25:06.206488+03	2018-06-21 12:25:06.206494+03	2019-10-12	12:25:06	23:59:59.999999	2
992	2018-06-21 12:25:06.206513+03	2018-06-21 12:25:06.206519+03	2019-10-13	12:25:06	23:59:59.999999	2
993	2018-06-21 12:25:06.206538+03	2018-06-21 12:25:06.206544+03	2019-10-14	12:25:06	23:59:59.999999	2
994	2018-06-21 12:25:06.206564+03	2018-06-21 12:25:06.206571+03	2019-10-15	12:25:06	23:59:59.999999	2
995	2018-06-21 12:25:06.20659+03	2018-06-21 12:25:06.206597+03	2019-10-16	12:25:06	23:59:59.999999	2
996	2018-06-21 12:25:06.206617+03	2018-06-21 12:25:06.206623+03	2019-10-17	12:25:06	23:59:59.999999	2
997	2018-06-21 12:25:06.206643+03	2018-06-21 12:25:06.20665+03	2019-10-18	12:25:06	23:59:59.999999	2
998	2018-06-21 12:25:06.206669+03	2018-06-21 12:25:06.206677+03	2019-10-19	12:25:06	23:59:59.999999	2
999	2018-06-21 12:25:06.206699+03	2018-06-21 12:25:06.206705+03	2019-10-20	12:25:06	23:59:59.999999	2
1000	2018-06-21 12:25:06.206727+03	2018-06-21 12:25:06.206735+03	2019-10-21	12:25:06	23:59:59.999999	2
1001	2018-06-21 12:25:06.206758+03	2018-06-21 12:25:06.206765+03	2019-10-22	12:25:06	23:59:59.999999	2
1002	2018-06-21 12:25:06.206788+03	2018-06-21 12:25:06.206798+03	2019-10-23	12:25:06	23:59:59.999999	2
1003	2018-06-21 12:25:06.206824+03	2018-06-21 12:25:06.206832+03	2019-10-24	12:25:06	23:59:59.999999	2
1004	2018-06-21 12:25:06.206855+03	2018-06-21 12:25:06.206863+03	2019-10-25	12:25:06	23:59:59.999999	2
1005	2018-06-21 12:25:06.206886+03	2018-06-21 12:25:06.206894+03	2019-10-26	12:25:06	23:59:59.999999	2
1006	2018-06-21 12:25:06.206916+03	2018-06-21 12:25:06.206924+03	2019-10-27	12:25:06	23:59:59.999999	2
1007	2018-06-21 12:25:06.206944+03	2018-06-21 12:25:06.206953+03	2019-10-28	12:25:06	23:59:59.999999	2
1008	2018-06-21 12:25:06.206973+03	2018-06-21 12:25:06.20698+03	2019-10-29	12:25:06	23:59:59.999999	2
1009	2018-06-21 12:25:06.207002+03	2018-06-21 12:25:06.207009+03	2019-10-30	12:25:06	23:59:59.999999	2
1010	2018-06-21 12:25:06.20703+03	2018-06-21 12:25:06.207036+03	2019-10-31	12:25:06	23:59:59.999999	2
1011	2018-06-21 12:25:06.207057+03	2018-06-21 12:25:06.207064+03	2019-11-01	12:25:06	23:59:59.999999	2
1012	2018-06-21 12:25:06.207084+03	2018-06-21 12:25:06.207091+03	2019-11-02	12:25:06	23:59:59.999999	2
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
\.


--
-- Data for Name: ona_xform; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ona_xform (id, created, modified, ona_pk, project_id, title, id_string, deleted_at, last_updated) FROM stdin;
1	2018-06-21 12:15:23.170271+03	2018-06-21 12:15:23.170313+03	1903	4328	Form 1	ypQOibC_NvZG0DFiTjwAuzXTjW_g7bEyUGWZA-4kjkBgUZwZ1PA-yqDgtqpx_zBOKfI2dYG46aQiAy01klxMgVR2xhYS3TM3Raei	\N	\N
2	2018-06-21 12:15:23.175198+03	2018-06-21 12:15:23.175232+03	6373	5522	Form 2	5v86TwuBwx5xy7woQDM21HqZBjDzY7-4ceY_hUXyqmZmweY_8PzaN1IxJz0U8sG36P44WYSLNiTZwp4nnevzdBAG-9OfB6FQXxsy	\N	\N
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
2	2018-06-21 12:13:29.817175+03	2018-06-21 12:28:38.055316+03	\N	\N	\N			1	1	0	2
1	2018-06-21 12:09:10.445513+03	2018-06-21 12:45:16.138772+03	\N	\N	\N			1	1	0	1
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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 78, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 2, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 11, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 26, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 26, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: main_bounty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_bounty_id_seq', 2, true);


--
-- Name: main_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_client_id_seq', 69, true);


--
-- Name: main_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_location_id_seq', 2, true);


--
-- Name: main_locationtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_locationtype_id_seq', 1, true);


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

SELECT pg_catalog.setval('public.main_task_id_seq', 2, true);


--
-- Name: main_task_locations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_task_locations_id_seq', 2, true);


--
-- Name: main_task_segment_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_task_segment_rules_id_seq', 1, false);


--
-- Name: main_taskoccurrence_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.main_taskoccurrence_id_seq', 1012, true);


--
-- Name: ona_instance_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ona_instance_id_seq', 1, false);


--
-- Name: ona_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ona_project_id_seq', 1, false);


--
-- Name: ona_xform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ona_xform_id_seq', 2, true);


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

SELECT pg_catalog.setval('public.users_userprofile_id_seq', 2, true);


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
-- Name: main_task_locations main_task_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_pkey PRIMARY KEY (id);


--
-- Name: main_task_locations main_task_locations_task_id_location_id_51dc375b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_task_id_location_id_51dc375b_uniq UNIQUE (task_id, location_id);


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
-- Name: main_task_level_1378e816; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_level_1378e816 ON public.main_task USING btree (level);


--
-- Name: main_task_lft_d860dd9c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_lft_d860dd9c ON public.main_task USING btree (lft);


--
-- Name: main_task_locations_location_id_fb7e3064; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_locations_location_id_fb7e3064 ON public.main_task_locations USING btree (location_id);


--
-- Name: main_task_locations_task_id_39f2e68a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX main_task_locations_task_id_39f2e68a ON public.main_task_locations USING btree (task_id);


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
-- Name: main_task_locations main_task_locations_location_id_fb7e3064_fk_main_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_location_id_fb7e3064_fk_main_location_id FOREIGN KEY (location_id) REFERENCES public.main_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: main_task_locations main_task_locations_task_id_39f2e68a_fk_main_task_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.main_task_locations
    ADD CONSTRAINT main_task_locations_task_id_39f2e68a_fk_main_task_id FOREIGN KEY (task_id) REFERENCES public.main_task(id) DEFERRABLE INITIALLY DEFERRED;


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

