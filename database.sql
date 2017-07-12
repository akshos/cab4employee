create table employee (
	eid varchar(20),
	first_name varchar(30),
	last_name varchar(30),
	date_of_reg date,
	contact_num decimal(10),
	account_id varchar(20),
	time_in time,
	time_out time,
	username varchar(20),
	primary key(eid)
);

create table login (
	username varchar(20),
	password varchar(30),
	type varchar(10),
	primary key(username)
);

create table employee_address (
	eid varchar(20),
	house_num varchar(20),
	street_name varchar(20),
	city varchar(20),
	postal_code decimal(20),
	primary key(eid)
);

create table accounts (
	aid varchar(20),
	name varchar(20),
	primary key(aid)
);

create table cabs (
	cid varchar(20),
	c_model varchar(20),
	maxpassengers int(5),
	rating int(1),
	primary key(cid)
);

create table carbrands (
	c_model varchar(20),
	c_brand varchar(20),
	primary key(c_model)
);

create table drivers (
	did varchar(20),
	fitst_name varchar(20),
	last_name varchar(20),
	cid	varchar(20), 
	contact_number decimal,
	rating decimal,
	primary key (did)
);

create table allocations (
	aid varchar(20),
	eid varchar(20),
	cid varchar(20),
	did varchar(20),
	atime time,
	change_flag boolean,
	iftaken boolean,
	primary key (aid)
);

create table allocations_history (
	aid varchar(20),
	eid varchar(20),
	cid varchar(20),
	did varchar(20),
	atime time,
	change_flag boolean,
	iftaken boolean,
	primary key (aid)
);

insert into allocations values( 'A01','E01','C01','D01','00:00:00',0,0 );
insert into allocations values( 'A02','E02','C02','D03','00:00:00',0,0 );
insert into allocations values( 'A03','E03','C03','D02','00:00:00',0,0 );
insert into allocations values( 'A04','E04','C02','D02','00:00:00',0,0 );

