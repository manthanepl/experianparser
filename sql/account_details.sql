-- Table: veritas.cais_account_details

-- DROP TABLE IF EXISTS veritas.cais_account_details;

CREATE SEQUENCE veritas.cais_account_details_id_seq START 1;




CREATE TABLE IF NOT EXISTS veritas.cais_account_details
(
    id integer NOT NULL DEFAULT nextval('veritas.cais_account_details_id_seq'::regclass),
    date_reported date,
    loan_type character varying COLLATE pg_catalog."default",
    secured boolean,
    cash_credit boolean,
    overdraft boolean,
    hl_lap boolean,
    active boolean,
    date_opened date,
    payment_start_date date,
    ownership_type character varying COLLATE pg_catalog."default",
    payment_tenure_in_months integer,
    last_payment_date date,
    interest_rate numeric,
    member_short_name character varying COLLATE pg_catalog."default",
    emi_amount numeric,
    collateral_type character varying COLLATE pg_catalog."default",
    payment_frequency integer,
    payment_end_date date,
    high_credit_amount numeric,
    actual_payment_amount numeric,
    payment_history character varying COLLATE pg_catalog."default",
    remaining_balance numeric,
    date_closed date,
    index character varying COLLATE pg_catalog."default",
    account_holder_id integer NOT NULL DEFAULT nextval('veritas.cais_account_details_account_holder_id_seq'::regclass),
    collateral_value numeric,
    credit_card_credit_limit numeric,
    credit_card_cash_limit numeric,
    account_number character varying COLLATE pg_catalog."default",
    amount_overdue numeric,
    credit_facility_status character varying COLLATE pg_catalog."default",
    wo_amount_total numeric,
    wo_amount_principal numeric,
    suit_filed character varying COLLATE pg_catalog."default",
    settlement_amount numeric,
    source_name character varying COLLATE pg_catalog."default",
    source_table_id integer,
    written_off boolean,
    written_off_date date,
    loan_vintage_in_months integer,
    vintage_calculation_date date,
    CONSTRAINT cais_account_details_pkey PRIMARY KEY (id),
    CONSTRAINT account_holder_id FOREIGN KEY (account_holder_id)
        REFERENCES veritas.bureau_person_details (id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS veritas.cais_account_details
    OWNER to postgres;