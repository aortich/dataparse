create database listings

create table jobs(job_id BIGSERIAL PRIMARY KEY, title VARCHAR(255), city VARCHAR(255), state VARCHAR(255), salary_string VARCHAR(50), salary_low INTEGER, salary_high INTEGER, salary_avg INTEGER, job_description VARCHAR(2048), tags VARCHAR(2048) )

select * from jobs