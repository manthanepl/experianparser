-- Table: veritas.enquiries_details

-- DROP TABLE IF EXISTS veritas.enquiries_details;

CREATE SEQUENCE veritas.enquiries_details_id_seq START 1;

CREATE TABLE IF NOT EXISTS veritas.enquiries_details
(
    id integer NOT NULL DEFAULT nextval('veritas.enquiries_details_id_seq'::regclass),
    "member_short_name" character varying COLLATE pg_catalog."default",
    "enquiry_purpose" character varying COLLATE pg_catalog."default",
    "enquiry_amount" integer NOT NULL,
    "enquiry_date" date,
    index character varying COLLATE pg_catalog."default",
    account_holder_id integer NOT NULL,
    secured boolean,
    CONSTRAINT enquiries_details_pkey PRIMARY KEY (id),
    CONSTRAINT account_holder_id FOREIGN KEY (account_holder_id)
        REFERENCES veritas.bureau_person_details (id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS veritas.enquiries_details
    OWNER to postgres;