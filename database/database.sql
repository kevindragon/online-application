
CREATE TABLE admin (id integer primary key, username varchar(50), password varchar(50), create_at datetime);
CREATE TABLE admin_session (session_id varchar(50) unique, username varchar(50), update_time datetime);
CREATE UNIQUE INDEX username ON admin (username);

-- 硕士研究生申请信息
CREATE TABLE master_info (
       id integer primary key, 
       name varchar(50), 
       gender char(3),
       id_number char(18) UNIQUE,
       university varchar(200), 
       major varchar(200), 
       email varchar(100), 
       phone varchar(100), 
       avatar varchar(200)
);
CREATE INDEX master_name ON master_info (`name`);

-- 博士研究生申请信息
CREATE TABLE doctor_info (
       id integer primary key, 
       name varchar(50), 
       gender char(3),
       id_number char(18) UNIQUE,
       university varchar(200), 
       major varchar(200), 
       email varchar(100), 
       phone varchar(100), 
       avatar varchar(200)
);
CREATE INDEX doctor_name ON doctor_info (`name`);
