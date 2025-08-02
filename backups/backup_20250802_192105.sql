--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

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
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    file_name character varying NOT NULL,
    url character varying NOT NULL,
    created_at timestamp without time zone,
    is_deleted boolean NOT NULL,
    deleted_at timestamp without time zone
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: pending_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pending_users (
    id uuid NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    verification_code character varying(6) NOT NULL,
    created_at timestamp without time zone,
    expires_at timestamp without time zone NOT NULL
);


ALTER TABLE public.pending_users OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    is_admin boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, user_id, file_name, url, created_at, is_deleted, deleted_at) FROM stdin;
\.


--
-- Data for Name: pending_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pending_users (id, username, email, password_hash, verification_code, created_at, expires_at) FROM stdin;
d541aec7-6aff-4fcb-b9c0-5fa10da9956a	Prueba	maitegarciacorrea16@gmail.com	$2b$12$Qd/j1ENqZjZ4JpiFh8Ygqe7iMxzPVoEzuETyvcdCA2LHCBlKLoxPW	304054	2025-08-02 16:34:54.851689	2025-08-02 16:49:54.505481
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password, is_admin, created_at) FROM stdin;
9239cf43-20b9-47e4-af64-5393a69fae31	ana	ana@example.com	$2b$12$eUVWRxeFnif0jwVvZVxdDO/3.wfv08LVV4jEfqVMqpUbMKUV34Y0e	f	2025-08-02 16:32:49.518693
\.


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: pending_users pending_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pending_users
    ADD CONSTRAINT pending_users_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_images_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_images_id ON public.images USING btree (id);


--
-- Name: ix_pending_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_pending_users_email ON public.pending_users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: images images_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

