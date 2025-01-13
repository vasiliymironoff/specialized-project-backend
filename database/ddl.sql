CREATE TABLE IF NOT EXISTS public.news
(
    id bigint NOT NULL PRIMARY KEY,
    create_time date NOT NULL,
    description character varying(400) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    category character varying(255),
    path_audio character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying
)
	
CREATE SEQUENCE public.news_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;	

ALTER TABLE public.news
    ALTER COLUMN id SET DEFAULT nextval('public.news_seq'::regclass);
