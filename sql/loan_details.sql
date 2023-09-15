-- Table: veritas.loan_emi_details

-- DROP TABLE IF EXISTS veritas.loan_emi_details;

CREATE SEQUENCE veritas.loan_emi_details_id_seq START 1;


CREATE TABLE IF NOT EXISTS veritas.loan_emi_details
(
    id integer NOT NULL DEFAULT nextval('veritas.loan_emi_details_id_seq'::regclass),
    loan_id integer NOT NULL DEFAULT nextval('veritas.loan_emi_details_loan_id_seq'::regclass),
    account_holder_id integer NOT NULL DEFAULT nextval('veritas.loan_emi_details_account_holder_id_seq'::regclass),
    emi_dpd character varying COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    payment_status character varying COLLATE pg_catalog."default",
    CONSTRAINT loan_emi_details_pkey PRIMARY KEY (id),
    CONSTRAINT account_holder_id FOREIGN KEY (account_holder_id)
        REFERENCES veritas.bureau_person_details (id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT loan_id FOREIGN KEY (loan_id)
        REFERENCES veritas.cais_account_details (id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS veritas.loan_emi_details
    OWNER to postgres;