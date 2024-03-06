-- Table: public.aviary_types

-- DROP TABLE IF EXISTS public.aviary_types;

CREATE TABLE IF NOT EXISTS public.aviary_types
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT aviary_types_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.aviary_types
    OWNER to postgres;



-- Table: public.aviaries

-- DROP TABLE IF EXISTS public.aviaries;

CREATE TABLE IF NOT EXISTS public.aviaries
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    type_id bigint NOT NULL,
    CONSTRAINT aviaries_pkey PRIMARY KEY (id),
    CONSTRAINT aviary_type FOREIGN KEY (type_id)
        REFERENCES public.aviary_types (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.aviaries
    OWNER to postgres;


-- Table: public.animal_types

-- DROP TABLE IF EXISTS public.animal_types;

CREATE TABLE IF NOT EXISTS public.animal_types
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    description character varying(1500) COLLATE pg_catalog."default",
    CONSTRAINT "AnimalType_pkey" PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.animal_types
    OWNER to postgres;



-- Table: public.animals

-- DROP TABLE IF EXISTS public.animals;

CREATE TABLE IF NOT EXISTS public.animals
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    description character varying(1500) COLLATE pg_catalog."default",
    type_id bigint NOT NULL,
    aviary_id bigint NULL,
    CONSTRAINT animals_pkey PRIMARY KEY (id),
    CONSTRAINT animal_type FOREIGN KEY (type_id)
        REFERENCES public.animal_types (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	CONSTRAINT aviaries FOREIGN KEY (aviary_id)
        REFERENCES public.aviaries (id) MATCH SIMPLE
		ON UPDATE NO ACTION
        ON DELETE NO ACTION

)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.animals
    OWNER to postgres;
