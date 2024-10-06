CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA admin;


CREATE TABLE admin.users (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
	email text NOT NULL UNIQUE,
	password varchar(90) NOT NULL,

	CONSTRAINT user_id_pkey PRIMARY KEY ("id")
);


INSERT INTO "admin".users
(email, password)
VALUES('admin@admin.com',
'$2a$12$LztVT05UMXaDjZaB23SKve75DL.i9b.FO/hGAF0ZbQk8phb/sri0u');
