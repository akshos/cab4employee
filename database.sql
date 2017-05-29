create table employee (
	eid varchar(20),
	first_name varchar(30),
	last_name varchar(30),
	date_of_reg date,
	contact_num decimal(10),
	account_id varchar(20),
	time_in time,
	time_out time,
	primary key(eid),
	foreign key(account_id) references accounts(aid)
);

create table employee_address (
	eid varchar(20),
	house_num varchar(20),
	street_name varchar(20),
	city varchar(20),
	primary key(eid),foreign key (eid) references employee (eid)
);

create table accounts (
	aid varchar(20),
	name varchar(20),
	primary key(aid)
);

create table cabs (
	cid varchar(20),
	c_model varchar(20),
	did varchar(20) references drivers(did),
	primary key(cid),
	foreign key (c_model) references carbrands (c_model)
);

create table carbrands (
	c_model varchar(20),
	c_brand varchar(20),
	primary key(c_model)
);

create table drivers (
	did varchar(20),
	name varchar(20),
	contact_number decimal,
	rating decimal,
	primary key (did)
);

create table allocations (
	aid varchar(20),
	eid varchar(20) references employee (eid),
	cid varchar(20) references cabs (cid),
	did varchar(20) references drivers(did),
	atime time,
	change_flag boolean,
	iftaken boolean,
	primary key (aid)
);
