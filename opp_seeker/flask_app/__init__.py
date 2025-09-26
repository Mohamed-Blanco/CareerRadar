
import psycopg2

from opp_seeker.database.database_connection import Database_connection
from opp_seeker.logger import Logger

logger = Logger().get_logger()

SQL_CREATE_TABLES = """  
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 230 (class 1259 OID 16439)
-- Name: job_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_metadata (
    id integer NOT NULL,
    id_original_job bigint,
    location character varying(200),
    sector_travail character varying(200),
    entreprise character varying(200),
    title character varying(200),
    skills jsonb,
    months_of_experience integer,
    date_processement date,
    date_posted date,
    total_skills integer,
    description text,
    job_logo text ,
    search_vector tsvector GENERATED ALWAYS AS ((((((((((setweight(to_tsvector('english'::regconfig, (COALESCE(title, ''::character varying))::text), 'A'::"char") || setweight(to_tsvector('french'::regconfig, (COALESCE(title, ''::character varying))::text), 'A'::"char")) || setweight(to_tsvector('english'::regconfig, COALESCE(description, ''::text)), 'B'::"char")) || setweight(to_tsvector('french'::regconfig, COALESCE(description, ''::text)), 'B'::"char")) || setweight(to_tsvector('english'::regconfig, (COALESCE(location, ''::character varying))::text), 'C'::"char")) || setweight(to_tsvector('french'::regconfig, (COALESCE(location, ''::character varying))::text), 'C'::"char")) || setweight(to_tsvector('english'::regconfig, (COALESCE(sector_travail, ''::character varying))::text), 'D'::"char")) || setweight(to_tsvector('french'::regconfig, (COALESCE(sector_travail, ''::character varying))::text), 'D'::"char")) || setweight(to_tsvector('english'::regconfig, (COALESCE(entreprise, ''::character varying))::text), 'D'::"char")) || setweight(to_tsvector('french'::regconfig, (COALESCE(entreprise, ''::character varying))::text), 'D'::"char"))) STORED
);


ALTER TABLE public.job_metadata OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16438)
-- Name: job_metadata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_metadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_metadata_id_seq OWNER TO postgres;

--
-- TOC entry 3512 (class 0 OID 0)
-- Dependencies: 229
-- Name: job_metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_metadata_id_seq OWNED BY public.job_metadata.id;


--
-- TOC entry 220 (class 1259 OID 16392)
-- Name: job_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_records (
    id integer NOT NULL,
    job_details jsonb,
    date_enregistrement date,
    title character varying(200)
);


ALTER TABLE public.job_records OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16391)
-- Name: job_records_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.job_records_id_seq OWNER TO postgres;

--
-- TOC entry 3513 (class 0 OID 0)
-- Dependencies: 219
-- Name: job_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_records_id_seq OWNED BY public.job_records.id;


--
-- TOC entry 222 (class 1259 OID 16403)
-- Name: jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs (
    id_job integer NOT NULL,
    job_data jsonb,
    title character varying(200),
    date_enregistrement date
);


ALTER TABLE public.jobs OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16402)
-- Name: jobs_id_job_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_id_job_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jobs_id_job_seq OWNER TO postgres;

--
-- TOC entry 3514 (class 0 OID 0)
-- Dependencies: 221
-- Name: jobs_id_job_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_id_job_seq OWNED BY public.jobs.id_job;


--
-- TOC entry 232 (class 1259 OID 16454)
-- Name: jobs_pr; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs_pr (
    id integer NOT NULL,
    original_job integer,
    location character varying(150),
    experience interval,
    sector character varying(300),
    entreprise_name character varying(300),
    demanded_skills jsonb
);


ALTER TABLE public.jobs_pr OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16453)
-- Name: jobs_pr_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_pr_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.jobs_pr_id_seq OWNER TO postgres;

--
-- TOC entry 3515 (class 0 OID 0)
-- Dependencies: 231
-- Name: jobs_pr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_pr_id_seq OWNED BY public.jobs_pr.id;


--
-- TOC entry 224 (class 1259 OID 16414)
-- Name: linkdein_job_ids; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.linkdein_job_ids (
    id integer NOT NULL,
    linkdein_id character varying(200),
    date_creation date,
    found_by_keyword character varying(500)
);


ALTER TABLE public.linkdein_job_ids OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16413)
-- Name: linkdein_job_ids_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.linkdein_job_ids_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.linkdein_job_ids_id_seq OWNER TO postgres;

--
-- TOC entry 3516 (class 0 OID 0)
-- Dependencies: 223
-- Name: linkdein_job_ids_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.linkdein_job_ids_id_seq OWNED BY public.linkdein_job_ids.id;


--
-- TOC entry 226 (class 1259 OID 16423)
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id_student integer NOT NULL,
    skills text[],
    experience integer,
    city character varying(50),
    gender character varying(20)
);


ALTER TABLE public.students OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16422)
-- Name: students_id_student_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_id_student_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.students_id_student_seq OWNER TO postgres;

--
-- TOC entry 3517 (class 0 OID 0)
-- Dependencies: 225
-- Name: students_id_student_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_id_student_seq OWNED BY public.students.id_student;


--
-- TOC entry 228 (class 1259 OID 16432)
-- Name: test_table; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_table (
    id integer NOT NULL,
    test_name character varying(10)
);


ALTER TABLE public.test_table OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16431)
-- Name: test_table_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_table_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_table_id_seq OWNER TO postgres;

--
-- TOC entry 3518 (class 0 OID 0)
-- Dependencies: 227
-- Name: test_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_table_id_seq OWNED BY public.test_table.id;


--
-- TOC entry 3324 (class 2604 OID 16442)
-- Name: job_metadata id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_metadata ALTER COLUMN id SET DEFAULT nextval('public.job_metadata_id_seq'::regclass);


--
-- TOC entry 3319 (class 2604 OID 16395)
-- Name: job_records id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_records ALTER COLUMN id SET DEFAULT nextval('public.job_records_id_seq'::regclass);


--
-- TOC entry 3320 (class 2604 OID 16406)
-- Name: jobs id_job; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs ALTER COLUMN id_job SET DEFAULT nextval('public.jobs_id_job_seq'::regclass);


--
-- TOC entry 3326 (class 2604 OID 16457)
-- Name: jobs_pr id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_pr ALTER COLUMN id SET DEFAULT nextval('public.jobs_pr_id_seq'::regclass);


--
-- TOC entry 3321 (class 2604 OID 16417)
-- Name: linkdein_job_ids id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.linkdein_job_ids ALTER COLUMN id SET DEFAULT nextval('public.linkdein_job_ids_id_seq'::regclass);


--
-- TOC entry 3322 (class 2604 OID 16426)
-- Name: students id_student; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students ALTER COLUMN id_student SET DEFAULT nextval('public.students_id_student_seq'::regclass);


--
-- TOC entry 3323 (class 2604 OID 16435)
-- Name: test_table id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_table ALTER COLUMN id SET DEFAULT nextval('public.test_table_id_seq'::regclass);


--
-- TOC entry 3503 (class 0 OID 16439)
-- Dependencies: 230
-- Data for Name: job_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

--
-- TOC entry 3499 (class 0 OID 16423)
-- Dependencies: 226
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3501 (class 0 OID 16432)
-- Dependencies: 228
-- Data for Name: test_table; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3519 (class 0 OID 0)
-- Dependencies: 229
-- Name: job_metadata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.job_metadata_id_seq', 152, true);


--
-- TOC entry 3520 (class 0 OID 0)
-- Dependencies: 219
-- Name: job_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.job_records_id_seq', 3360, true);


--
-- TOC entry 3521 (class 0 OID 0)
-- Dependencies: 221
-- Name: jobs_id_job_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.jobs_id_job_seq', 1, false);


--
-- TOC entry 3522 (class 0 OID 0)
-- Dependencies: 231
-- Name: jobs_pr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.jobs_pr_id_seq', 1, false);


--
-- TOC entry 3523 (class 0 OID 0)
-- Dependencies: 223
-- Name: linkdein_job_ids_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.linkdein_job_ids_id_seq', 1829, true);


--
-- TOC entry 3524 (class 0 OID 0)
-- Dependencies: 225
-- Name: students_id_student_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_id_student_seq', 1, false);


--
-- TOC entry 3525 (class 0 OID 0)
-- Dependencies: 227
-- Name: test_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_table_id_seq', 1, false);


--
-- TOC entry 3342 (class 2606 OID 16447)
-- Name: job_metadata job_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_metadata
    ADD CONSTRAINT job_metadata_pkey PRIMARY KEY (id);


--
-- TOC entry 3328 (class 2606 OID 16399)
-- Name: job_records job_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_records
    ADD CONSTRAINT job_records_pkey PRIMARY KEY (id);


--
-- TOC entry 3330 (class 2606 OID 16401)
-- Name: job_records job_records_title_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_records
    ADD CONSTRAINT job_records_title_key UNIQUE (title);


--
-- TOC entry 3332 (class 2606 OID 16410)
-- Name: jobs jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id_job);


--
-- TOC entry 3344 (class 2606 OID 16461)
-- Name: jobs_pr jobs_pr_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_pr
    ADD CONSTRAINT jobs_pr_pkey PRIMARY KEY (id);


--
-- TOC entry 3336 (class 2606 OID 16421)
-- Name: linkdein_job_ids linkdein_job_ids_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.linkdein_job_ids
    ADD CONSTRAINT linkdein_job_ids_pkey PRIMARY KEY (id);


--
-- TOC entry 3338 (class 2606 OID 16430)
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id_student);


--
-- TOC entry 3340 (class 2606 OID 16437)
-- Name: test_table test_table_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_table
    ADD CONSTRAINT test_table_pkey PRIMARY KEY (id);


--
-- TOC entry 3346 (class 2606 OID 16463)
-- Name: jobs_pr unique_original_jobs; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_pr
    ADD CONSTRAINT unique_original_jobs UNIQUE (original_job);


--
-- TOC entry 3334 (class 2606 OID 16412)
-- Name: jobs unique_title; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT unique_title UNIQUE (title);


--
-- TOC entry 3347 (class 2606 OID 16448)
-- Name: job_metadata job_metadata_id_original_job_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_metadata
    ADD CONSTRAINT job_metadata_id_original_job_fkey FOREIGN KEY (id_original_job) REFERENCES public.job_records(id);


--
-- TOC entry 3348 (class 2606 OID 16464)
-- Name: jobs_pr jobs_pr_original_job_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_pr
    ADD CONSTRAINT jobs_pr_original_job_fkey FOREIGN KEY (original_job) REFERENCES public.jobs(id_job);


-- Completed on 2025-08-15 18:24:46 CET

--
-- PostgreSQL database dump complete
--

"""

# init db not needed (docker)
# def init_db():
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute(SQL_CREATE_DATABASE)
#             conn.commit()
#
#     except psycopg2.OperationalError as e:
#         logger.error(f"Error: {e}")
#         logger.error("Could not create the database ")
#         conn.rollback()

def init_tables():

    db = Database_connection()
    conn = db.get_connection()
    logger.info("INISTIALIZING THE DATABASE ")
    try:
        with conn.cursor() as cursor:
            cursor.execute(SQL_CREATE_TABLES)
            conn.commit()
        logger.info("DATABASE Created Successfully ")
    except (psycopg2.OperationalError, psycopg2.Error) as e:
        logger.error(f"Error: {e}")
        conn.rollback()
    finally :
        db.release_connection(conn)


init_tables()
logger.critical("Database Initialization is complete ")



