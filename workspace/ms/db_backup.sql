--
-- PostgreSQL database cluster dump
--

\connect postgres

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE pi;
ALTER ROLE pi WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION PASSWORD 'md5b6d60186c406458f8028cab4d9ed7d57';
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION;






--
-- Database creation
--

CREATE DATABASE msdb WITH TEMPLATE = template0 OWNER = postgres;
REVOKE ALL ON DATABASE msdb FROM PUBLIC;
REVOKE ALL ON DATABASE msdb FROM postgres;
GRANT ALL ON DATABASE msdb TO postgres;
GRANT ALL ON DATABASE msdb TO pi;
GRANT CONNECT,TEMPORARY ON DATABASE msdb TO PUBLIC;
REVOKE ALL ON DATABASE template1 FROM PUBLIC;
REVOKE ALL ON DATABASE template1 FROM postgres;
GRANT ALL ON DATABASE template1 TO postgres;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect msdb

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO pi;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO pi;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO pi;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO pi;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO pi;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO pi;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO pi;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO pi;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO pi;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO pi;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO pi;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO pi;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: dbkeeper_msuser; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE dbkeeper_msuser (
    id integer NOT NULL,
    work_phone character varying(20) NOT NULL,
    mobile_phone character varying(20) NOT NULL,
    other_phone character varying(20) NOT NULL,
    note text NOT NULL,
    organization_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.dbkeeper_msuser OWNER TO pi;

--
-- Name: dbkeeper_msuser_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE dbkeeper_msuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dbkeeper_msuser_id_seq OWNER TO pi;

--
-- Name: dbkeeper_msuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE dbkeeper_msuser_id_seq OWNED BY dbkeeper_msuser.id;


--
-- Name: dbkeeper_msuser_teams; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE dbkeeper_msuser_teams (
    id integer NOT NULL,
    msuser_id integer NOT NULL,
    team_id integer NOT NULL
);


ALTER TABLE public.dbkeeper_msuser_teams OWNER TO pi;

--
-- Name: dbkeeper_msuser_teams_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE dbkeeper_msuser_teams_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dbkeeper_msuser_teams_id_seq OWNER TO pi;

--
-- Name: dbkeeper_msuser_teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE dbkeeper_msuser_teams_id_seq OWNED BY dbkeeper_msuser_teams.id;


--
-- Name: dbkeeper_organization; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE dbkeeper_organization (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    type smallint NOT NULL,
    CONSTRAINT dbkeeper_organization_type_check CHECK ((type >= 0))
);


ALTER TABLE public.dbkeeper_organization OWNER TO pi;

--
-- Name: dbkeeper_organization_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE dbkeeper_organization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dbkeeper_organization_id_seq OWNER TO pi;

--
-- Name: dbkeeper_organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE dbkeeper_organization_id_seq OWNED BY dbkeeper_organization.id;


--
-- Name: dbkeeper_setting; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE dbkeeper_setting (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    value text NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.dbkeeper_setting OWNER TO pi;

--
-- Name: dbkeeper_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE dbkeeper_setting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dbkeeper_setting_id_seq OWNER TO pi;

--
-- Name: dbkeeper_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE dbkeeper_setting_id_seq OWNED BY dbkeeper_setting.id;


--
-- Name: dbkeeper_team; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE dbkeeper_team (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    pass_code character varying(50) NOT NULL,
    reg_code character varying(32) NOT NULL,
    registered integer NOT NULL,
    organization_id integer NOT NULL
);


ALTER TABLE public.dbkeeper_team OWNER TO pi;

--
-- Name: dbkeeper_team_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE dbkeeper_team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dbkeeper_team_id_seq OWNER TO pi;

--
-- Name: dbkeeper_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE dbkeeper_team_id_seq OWNED BY dbkeeper_team.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE django_admin_log (
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


ALTER TABLE public.django_admin_log OWNER TO pi;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO pi;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO pi;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO pi;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO pi;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO pi;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO pi;

--
-- Name: piservice_pievent; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE piservice_pievent (
    id integer NOT NULL,
    "time" timestamp with time zone NOT NULL,
    type smallint NOT NULL,
    status smallint NOT NULL,
    data text,
    message character varying(1000) NOT NULL,
    pi_id integer,
    team_id integer
);


ALTER TABLE public.piservice_pievent OWNER TO pi;

--
-- Name: piservice_pievent_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE piservice_pievent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.piservice_pievent_id_seq OWNER TO pi;

--
-- Name: piservice_pievent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE piservice_pievent_id_seq OWNED BY piservice_pievent.id;


--
-- Name: piservice_pistation; Type: TABLE; Schema: public; Owner: pi; Tablespace: 
--

CREATE TABLE piservice_pistation (
    id integer NOT NULL,
    host character varying(60) NOT NULL,
    station_type character varying(20) NOT NULL,
    station_id character varying(20) NOT NULL,
    serial_num character varying(50) NOT NULL,
    url character varying(200) NOT NULL,
    last_activity timestamp with time zone NOT NULL,
    joined_id integer
);


ALTER TABLE public.piservice_pistation OWNER TO pi;

--
-- Name: piservice_pistation_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

CREATE SEQUENCE piservice_pistation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.piservice_pistation_id_seq OWNER TO pi;

--
-- Name: piservice_pistation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pi
--

ALTER SEQUENCE piservice_pistation_id_seq OWNED BY piservice_pistation.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_msuser ALTER COLUMN id SET DEFAULT nextval('dbkeeper_msuser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_msuser_teams ALTER COLUMN id SET DEFAULT nextval('dbkeeper_msuser_teams_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_organization ALTER COLUMN id SET DEFAULT nextval('dbkeeper_organization_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_setting ALTER COLUMN id SET DEFAULT nextval('dbkeeper_setting_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_team ALTER COLUMN id SET DEFAULT nextval('dbkeeper_team_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY piservice_pievent ALTER COLUMN id SET DEFAULT nextval('piservice_pievent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pi
--

ALTER TABLE ONLY piservice_pistation ALTER COLUMN id SET DEFAULT nextval('piservice_pistation_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
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
19	Can add organization	7	add_organization
20	Can change organization	7	change_organization
21	Can delete organization	7	delete_organization
22	Can add team	8	add_team
23	Can change team	8	change_team
24	Can delete team	8	delete_team
25	Can add ms user	9	add_msuser
26	Can change ms user	9	change_msuser
27	Can delete ms user	9	delete_msuser
28	Can add setting	10	add_setting
29	Can change setting	10	change_setting
30	Can delete setting	10	delete_setting
31	Can add pi station	11	add_pistation
32	Can change pi station	11	change_pistation
33	Can delete pi station	11	delete_pistation
34	Can add pi event	12	add_pievent
35	Can change pi event	12	change_pievent
36	Can delete pi event	12	delete_pievent
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('auth_permission_id_seq', 36, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$24000$wMwuFrNw7Ie2$yLLVEL3e+kPDbMR3GfPxRHk0LbyX69pGL9Nr7zOLLbU=	2016-02-14 13:35:33.908361+00	t	pi			pi@nowhere.com	t	t	2016-02-13 19:47:35.067929+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: dbkeeper_msuser; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY dbkeeper_msuser (id, work_phone, mobile_phone, other_phone, note, organization_id, user_id) FROM stdin;
\.


--
-- Name: dbkeeper_msuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('dbkeeper_msuser_id_seq', 1, false);


--
-- Data for Name: dbkeeper_msuser_teams; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY dbkeeper_msuser_teams (id, msuser_id, team_id) FROM stdin;
\.


--
-- Name: dbkeeper_msuser_teams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('dbkeeper_msuser_teams_id_seq', 1, false);


--
-- Data for Name: dbkeeper_organization; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY dbkeeper_organization (id, name, type) FROM stdin;
1	Palm Bay	1
2	Holy Trinity	1
4	Bayside	1
5	Melbourne	1
6	Titusville	1
7	Edgewood	1
8	HarrisTesters	1
\.


--
-- Name: dbkeeper_organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('dbkeeper_organization_id_seq', 1, true);


--
-- Data for Name: dbkeeper_setting; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY dbkeeper_setting (id, name, value, description) FROM stdin;
1	1_READ_ME	Master Server Setting Table Contents	The Master Server operation is configured through a variety of values stored in the Setting table.  The values are captured here in case the Setting table needs to be reconstructed.  This file is created by saving the Setting table to a CSV file and importing it into Excel.
2	DOCK_PARAMS	{"min_dock": 0.01, "sim_time": 45, "max_dock": 0.1, "init_vel": 0.0, "sets": [{"a_fore": 0.09, "f_rate": 0.7, "tape_id": 1, "tape_len": 10.0, "a_aft": 0.15, "f_qty": 20.0}, {"a_fore": 0.1, "f_rate": 0.8, "tape_id": 2, "tape_len": 12.0, "a_aft": 0.16, "f_qty": 21.0}]}	Competition parameters for the Dock challenge
3	DOCK_SIM_PLAYBACK_TIME_S	45	The maximum replay time, in seconds, for the Dock simulation
4	DOCK_TEST_HOST	http://192.168.4.37:8080	URL of the host that runs the FlightService Dock test server that is accessible by the students
5	LAUNCH_PARAMS	[[["red_v1", "1.2", "1", "1"], ["red_v2", "2", "2", "2"], ["red_v3", "3", "3", "3"], ["red_c", "4"]], [["green_v1", "11", "11", "11"], ["green_v2", "22", "22", "22"], ["green_v3", "33", "33", "33"], ["green_c", "44"]], [["blue_v1", "111", "111", "111"], ["blue_v2", "222", "222", "222"], ["blue_v3", "333", "333", "333"], ["blue_c", "444"]]]	Competition parameters for the Launch challenge
7	RETURN_PARAMS	[["Station 1", 1, 0, 0, 0, 0, 0], ["Station 2", 999, 2, 0, 0, 0, 0], ["Station 3", 0, 0, 3, 0, 0, 0], ["Station 4", 0, 0, 0, 4, 0, 0], ["Station 5", 0, 0, 0, 0, 5, 0], ["Station 6", 0, 0, 0, 0, 0, 6]]	Competition parameters for the Return challenge
8	SECURE_ERROR_DISTRIBUTION	[ 1, -1 ]	A list represented as a JSON array that contains error deltas that will be chosen at random and added to tone values to introduce errors in the data.  Construct the list to represent the distribution of errors that you desire.  For example, [ 1, 1, -1, -1, 2 ] would result in 40% of the errors deviating from the correct value by 1, 40% by -1, and 20% by 2.
9	SECURE_NUM_INDUCED_ERRORS	1	The number of errors injected into the Secure tone sequence.  Using the current 3x3 arrangement of values, 1 is the maximum number of induced errors guaranteed to be recoverable.
10	STATION_IPS	127.0.0.1\r\n192.168.1.1\r\n192.168.4.39\r\n192.168.4.65\r\n192.168.4.59\r\n192.168.1.104	IP address of competition stations.
11	STATION_SERIAL_NUMS	1234567\r\nabcdefg\r\n1234\r\n0000000072da1490\r\n000000001183fe50\r\n00000000c131aba0\r\n000000003cafb6a9	List of station serial numbers
12	STATION_STATUS_REFRESH_INTERVAL_MS	5000	
6	LAUNCH_TEST_DATA	{ "Melbourne": [[28.090004, -80.619985], [28.089966, -80.619876], [28.089892, -80.619948], [28.089896, -80.619816]], "Bayside": [[27.95171, -80.675075], [27.951812, -80.675102], [27.951757, -80.674973], [27.951652, -80.674997]], "Titusville": [[28.591602, -80.805232], [28.591508, -80.805202], [28.591613, -80.805368], [28.591481, -80.805332]], "Palm Bay": [[28.047726, -80.616002], [28.047797, -80.616034], [28.047747, -80.616102], [28.04778, -80.615947]], "Holy Trinity": [[28.201382, -80.667228], [28.201463, -80.667337], [28.201378, -80.667379], [28.20132, -80.6673]], "Edgewood": [[28.201382, -80.667228], [28.201463, -80.667337], [28.201378, -80.667379], [28.20132, -80.6673]], "HarrisTesters": [[28.201382, -80.667228], [28.201463, -80.667337], [28.201378, -80.667379], [28.20132, -80.6673]]   }	School test data points for student testing
\.


--
-- Name: dbkeeper_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('dbkeeper_setting_id_seq', 12, true);


--
-- Data for Name: dbkeeper_team; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY dbkeeper_team (id, name, pass_code, reg_code, registered, organization_id) FROM stdin;
1	Team42	nkj03		0	1
7	Syntax Errors	exo12		0	2
8	Infamous	fxq15		0	2
9	Leeroy MMM Jenkins	iyt06		0	2
10	Salty Pledges	awd12		0	2
11	Squad 100/100	fbc11		0	2
12	Nova	rgl05		0	2
13	Shale Pirates	dmr03		0	1
15	Unlucky	qox08		0	1
16	Hyrulian Coders	nig14		0	4
17	Mos Eisley Coders	ctm04		0	4
18	All Star	jrr14		0	4
19	Lord Gaben	ojo08		0	4
20	Shia Surprise!	ygk11		0	4
21	A	dkt03		0	4
22	A-Team	cdm04		0	5
23	.batV3	iho00		0	5
24	Blue Eyes White Mamba	gpn05		0	5
25	Code Breakers	qtq06		0	5
26	Coding Goats	gnm02		0	5
27	PC Master Race	hig08		0	5
28	ByteMe  0	gmf10		0	5
29	Code Wafle	dbq07		0	6
30	Office Fans	egr14		0	6
31	Black Stallion	fzp00		0	6
32	Team 1	jfl12		0	7
33	Team 2	qur08		0	7
34	Team 3	xkg10		0	7
35	Team 4	nwl01		0	7
14	Gentoomen	jsw04		0	1
6	Test4	bkl09	55c7d041fff322de	38	8
\.


--
-- Name: dbkeeper_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('dbkeeper_team_id_seq', 1, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2016-02-14 01:16:40.10827+00	3	2016-02-13 20:05:49.521865+00:00: Team 'Test4' Registered with brata_version 'm.brata_version'. Assigned reg_code 36f9deab6dec8529.	3		12	1
2	2016-02-14 01:16:40.178138+00	4	2016-02-13 20:15:22.026017+00:00: Station '192.168.4.39' (dock01) sent a Join message	3		12	1
3	2016-02-14 01:16:40.212522+00	5	2016-02-13 20:21:23.175663+00:00: Dock using [TAPE=1] [AFT=0.150] [FORE=0.090] [FUEL=20.00] [F-RATE=00.70]	3		12	1
4	2016-02-14 16:08:33.000557+00	6	LAUNCH_TEST_DATA	2	Changed value.	10	1
5	2016-02-14 16:11:32.503873+00	6	LAUNCH_TEST_DATA	2	Changed value.	10	1
6	2016-02-14 17:16:00.251961+00	6	LAUNCH_TEST_DATA	2	Changed value.	10	1
7	2016-02-14 20:10:44.661019+00	38	2016-02-14 13:39:49.876429+00:00: Team 'Test4' Registered with brata_version 'm.brata_version'. Assigned reg_code 55c7d041fff322de.	3		12	1
8	2016-02-14 20:10:45.410923+00	39	2016-02-14 13:40:57.802850+00:00: Failed to retrieve Station using station_id 'dock02' from the database	3		12	1
9	2016-02-14 20:10:45.550979+00	40	2016-02-14 13:44:56.347305+00:00: Station '192.168.1.104' (dock02) sent a Join message	3		12	1
10	2016-02-14 20:10:45.580089+00	41	2016-02-14 13:45:22.436194+00:00: Dock using [TAPE=1] [AFT=0.150] [FORE=0.090] [FUEL=20.00] [F-RATE=00.70]	3		12	1
11	2016-02-14 20:10:45.610621+00	42	2016-02-14 14:08:21.280661+00:00: Dock using [TAPE=2] [AFT=0.160] [FORE=0.100] [FUEL=21.00] [F-RATE=00.80]	3		12	1
12	2016-02-14 20:11:02.359523+00	43	2016-02-14 14:44:29.651674+00:00: Docking Parameters received!	3		12	1
13	2016-02-14 20:11:03.116685+00	44	2016-02-14 14:45:32.821632+00:00: Submit msg received from dock02	3		12	1
14	2016-02-14 20:11:03.257332+00	45	2016-02-14 14:46:17.148683+00:00: Docking latches engaged! Continue to next Challenge!	3		12	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 14, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	dbkeeper	organization
8	dbkeeper	team
9	dbkeeper	msuser
10	dbkeeper	setting
11	piservice	pistation
12	piservice	pievent
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('django_content_type_id_seq', 12, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2016-02-14 12:29:21.044637+00
2	auth	0001_initial	2016-02-14 12:29:35.191372+00
3	admin	0001_initial	2016-02-14 12:29:35.885571+00
4	admin	0002_logentry_remove_auto_add	2016-02-14 12:29:36.331184+00
5	contenttypes	0002_remove_content_type_name	2016-02-14 12:29:37.462187+00
6	auth	0002_alter_permission_name_max_length	2016-02-14 12:29:39.305878+00
7	auth	0003_alter_user_email_max_length	2016-02-14 12:29:39.874717+00
8	auth	0004_alter_user_username_opts	2016-02-14 12:29:40.23819+00
9	auth	0005_alter_user_last_login_null	2016-02-14 12:29:40.612053+00
10	auth	0006_require_contenttypes_0002	2016-02-14 12:29:40.672821+00
11	auth	0007_alter_validators_add_error_messages	2016-02-14 12:29:41.087216+00
12	dbkeeper	0001_initial	2016-02-14 12:29:45.643708+00
13	piservice	0001_initial	2016-02-14 12:29:47.021755+00
14	sessions	0001_initial	2016-02-14 12:29:47.298003+00
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('django_migrations_id_seq', 14, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
waob97rib8ss9bd2qojjmdq4ow58g3i5	Mjg2MWE5MGJlMmI1NGE2MzE5OGVkMjk0NWZlOWEwODAwNzMzZmZkZTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI4ZDYzNTc3MTBhOWFiNjFjZjY5NGI5MDA5MjlmYzAwOGFhMWUwZGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-02-27 19:49:11.860088+00
ncdk1i85lhwjchhpkfo9jgi2821q5c1f	Mjg2MWE5MGJlMmI1NGE2MzE5OGVkMjk0NWZlOWEwODAwNzMzZmZkZTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI4ZDYzNTc3MTBhOWFiNjFjZjY5NGI5MDA5MjlmYzAwOGFhMWUwZGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-02-28 01:13:17.723134+00
lggy1xw44l4evksteca9x3fgfncx65ij	Mjg2MWE5MGJlMmI1NGE2MzE5OGVkMjk0NWZlOWEwODAwNzMzZmZkZTp7Il9hdXRoX3VzZXJfaGFzaCI6ImI4ZDYzNTc3MTBhOWFiNjFjZjY5NGI5MDA5MjlmYzAwOGFhMWUwZGYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=	2016-02-28 13:35:33.955097+00
\.


--
-- Data for Name: piservice_pievent; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY piservice_pievent (id, "time", type, status, data, message, pi_id, team_id) FROM stdin;
1	2016-02-13 18:47:44.075221+00	3	1	\N	Organization 'HarrisTesters' added	\N	\N
2	2016-02-13 18:48:22.477005+00	5	1	\N	Team 'Team42' added	\N	1
\.


--
-- Name: piservice_pievent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('piservice_pievent_id_seq', 45, true);


--
-- Data for Name: piservice_pistation; Type: TABLE DATA; Schema: public; Owner: pi
--

COPY piservice_pistation (id, host, station_type, station_id, serial_num, url, last_activity, joined_id) FROM stdin;
1	192.168.4.39	Dock	dock01	0000000072da1490	http://192.168.4.39:5000/rpi	2016-02-13 20:15:22.204089+00	\N
2	192.168.1.104	Dock	dock02	000000003cafb6a9	http://192.168.1.104:5000/rpi	2016-02-14 13:44:56.488369+00	\N
\.


--
-- Name: piservice_pistation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pi
--

SELECT pg_catalog.setval('piservice_pistation_id_seq', 2, true);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: dbkeeper_msuser_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_msuser
    ADD CONSTRAINT dbkeeper_msuser_pkey PRIMARY KEY (id);


--
-- Name: dbkeeper_msuser_teams_msuser_id_e90e3195_uniq; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_msuser_teams
    ADD CONSTRAINT dbkeeper_msuser_teams_msuser_id_e90e3195_uniq UNIQUE (msuser_id, team_id);


--
-- Name: dbkeeper_msuser_teams_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_msuser_teams
    ADD CONSTRAINT dbkeeper_msuser_teams_pkey PRIMARY KEY (id);


--
-- Name: dbkeeper_msuser_user_id_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_msuser
    ADD CONSTRAINT dbkeeper_msuser_user_id_key UNIQUE (user_id);


--
-- Name: dbkeeper_organization_name_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_organization
    ADD CONSTRAINT dbkeeper_organization_name_key UNIQUE (name);


--
-- Name: dbkeeper_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_organization
    ADD CONSTRAINT dbkeeper_organization_pkey PRIMARY KEY (id);


--
-- Name: dbkeeper_setting_name_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_setting
    ADD CONSTRAINT dbkeeper_setting_name_key UNIQUE (name);


--
-- Name: dbkeeper_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_setting
    ADD CONSTRAINT dbkeeper_setting_pkey PRIMARY KEY (id);


--
-- Name: dbkeeper_team_name_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_team
    ADD CONSTRAINT dbkeeper_team_name_key UNIQUE (name);


--
-- Name: dbkeeper_team_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY dbkeeper_team
    ADD CONSTRAINT dbkeeper_team_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: piservice_pievent_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY piservice_pievent
    ADD CONSTRAINT piservice_pievent_pkey PRIMARY KEY (id);


--
-- Name: piservice_pistation_pkey; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY piservice_pistation
    ADD CONSTRAINT piservice_pistation_pkey PRIMARY KEY (id);


--
-- Name: piservice_pistation_serial_num_key; Type: CONSTRAINT; Schema: public; Owner: pi; Tablespace: 
--

ALTER TABLE ONLY piservice_pistation
    ADD CONSTRAINT piservice_pistation_serial_num_key UNIQUE (serial_num);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: dbkeeper_msuser_26b2345e; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_msuser_26b2345e ON dbkeeper_msuser USING btree (organization_id);


--
-- Name: dbkeeper_msuser_teams_330938fc; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_msuser_teams_330938fc ON dbkeeper_msuser_teams USING btree (msuser_id);


--
-- Name: dbkeeper_msuser_teams_f6a7ca40; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_msuser_teams_f6a7ca40 ON dbkeeper_msuser_teams USING btree (team_id);


--
-- Name: dbkeeper_organization_name_e74b2765_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_organization_name_e74b2765_like ON dbkeeper_organization USING btree (name varchar_pattern_ops);


--
-- Name: dbkeeper_setting_name_fbbc4c5d_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_setting_name_fbbc4c5d_like ON dbkeeper_setting USING btree (name varchar_pattern_ops);


--
-- Name: dbkeeper_team_26b2345e; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_team_26b2345e ON dbkeeper_team USING btree (organization_id);


--
-- Name: dbkeeper_team_name_0f5c4d65_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX dbkeeper_team_name_0f5c4d65_like ON dbkeeper_team USING btree (name varchar_pattern_ops);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: piservice_pievent_e34c8b0e; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX piservice_pievent_e34c8b0e ON piservice_pievent USING btree (pi_id);


--
-- Name: piservice_pievent_f6a7ca40; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX piservice_pievent_f6a7ca40 ON piservice_pievent USING btree (team_id);


--
-- Name: piservice_pistation_a2228edb; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX piservice_pistation_a2228edb ON piservice_pistation USING btree (joined_id);


--
-- Name: piservice_pistation_serial_num_53abd3dd_like; Type: INDEX; Schema: public; Owner: pi; Tablespace: 
--

CREATE INDEX piservice_pistation_serial_num_53abd3dd_like ON piservice_pistation USING btree (serial_num varchar_pattern_ops);


--
-- Name: auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dbkeeper_m_organization_id_ca39aced_fk_dbkeeper_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_msuser
    ADD CONSTRAINT dbkeeper_m_organization_id_ca39aced_fk_dbkeeper_organization_id FOREIGN KEY (organization_id) REFERENCES dbkeeper_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dbkeeper_msuser_teams_msuser_id_6be2fd60_fk_dbkeeper_msuser_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_msuser_teams
    ADD CONSTRAINT dbkeeper_msuser_teams_msuser_id_6be2fd60_fk_dbkeeper_msuser_id FOREIGN KEY (msuser_id) REFERENCES dbkeeper_msuser(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dbkeeper_msuser_teams_team_id_572600bf_fk_dbkeeper_team_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_msuser_teams
    ADD CONSTRAINT dbkeeper_msuser_teams_team_id_572600bf_fk_dbkeeper_team_id FOREIGN KEY (team_id) REFERENCES dbkeeper_team(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dbkeeper_msuser_user_id_7f7e987a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_msuser
    ADD CONSTRAINT dbkeeper_msuser_user_id_7f7e987a_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dbkeeper_t_organization_id_f1bd4411_fk_dbkeeper_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY dbkeeper_team
    ADD CONSTRAINT dbkeeper_t_organization_id_f1bd4411_fk_dbkeeper_organization_id FOREIGN KEY (organization_id) REFERENCES dbkeeper_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piservice_pievent_pi_id_3ad0ce19_fk_piservice_pistation_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY piservice_pievent
    ADD CONSTRAINT piservice_pievent_pi_id_3ad0ce19_fk_piservice_pistation_id FOREIGN KEY (pi_id) REFERENCES piservice_pistation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piservice_pievent_team_id_30a187a8_fk_dbkeeper_team_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY piservice_pievent
    ADD CONSTRAINT piservice_pievent_team_id_30a187a8_fk_dbkeeper_team_id FOREIGN KEY (team_id) REFERENCES dbkeeper_team(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piservice_pistation_joined_id_146b1deb_fk_piservice_pievent_id; Type: FK CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY piservice_pistation
    ADD CONSTRAINT piservice_pistation_joined_id_146b1deb_fk_piservice_pievent_id FOREIGN KEY (joined_id) REFERENCES piservice_pievent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

