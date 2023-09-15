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
    any_unsecured_loan_before boolean,
    passport_id character varying COLLATE pg_catalog."default",
    ration_id character varying COLLATE pg_catalog."default",
    application_id integer,
    enquiry_6months_unsecured integer,
    any_written_off_in_last_24months boolean,
    written_off_principal_amount integer,
    written_off_total_amount integer,
    any_hl_lap_running boolean,
    usl_gl_in_last_12months integer,
    bureau_vintage_in_months integer,
    bureau_source character varying COLLATE pg_catalog."default",
    max_dpd_in_6months integer,
    other_dpds_in_last_2years integer,
    gl_cc_kcc_el_dpd_in_last_year integer,
    max_dpd_in_one_year integer,
    enq_calculation_datetime_ist timestamp without time zone,
    enq_calculation_datetime_utc timestamp without time zone,
    parsed_date_ist timestamp without time zone,
    parsed_date_utc timestamp without time zone,
    bureau_calculation_datetime_ist timestamp without time zone,
    bureau_calculation_datetime_utc timestamp without time zone,
    CONSTRAINT bureau_person_details_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS veritas.bureau_person_details
    OWNER to postgres;