-- Table: veritas.bureau_person_details

-- DROP TABLE IF EXISTS veritas.bureau_person_details;

CREATE SEQUENCE veritas.bureau_person_details_id_seq START 1;


CREATE TABLE IF NOT EXISTS veritas.bureau_person_details
(
    id integer NOT NULL DEFAULT nextval('veritas.bureau_person_details_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    date_of_birth date,
    age integer,
    gender character varying COLLATE pg_catalog."default",
    bureau_score character varying COLLATE pg_catalog."default",
    score_date date,
    pan character varying COLLATE pg_catalog."default",
    voter_id character varying COLLATE pg_catalog."default",
    drivers_id character varying COLLATE pg_catalog."default",
    uid character varying COLLATE pg_catalog."default",
    enquiry_6months integer,
    enq_calculation_datetime timestamp without time zone,
    any_unsecured_loan_before boolean,
    created_datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    passport_id character varying COLLATE pg_catalog."default",
    ration_id character varying COLLATE pg_catalog."default",
    application_id integer,
    enquiry_6months_unsecured integer,
    any_written_off_in_last_24months boolean,
    written_off_principal_amount integer,
    written_off_total_amount integer,
    parsed_date timestamp without time zone,
    any_hl_lap_running boolean,
    usl_gl_in_last_12months boolean,
    bureau_vintage_in_months integer,
    bureau_calculation_datetime timestamp without time zone,
    CONSTRAINT bureau_person_details_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS veritas.bureau_person_details
    OWNER to postgres;