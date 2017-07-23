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
	first_name varchar(20),
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
	direction varchar(10),
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

create table requests (
	eid varchar(20),
	req_date date,
	time_in time,
	time_out time,
	constraint pk_request primary key (eid,req_date)
);

Employee Table

insert into employee values('emp01','Gokul','Santosh','03-05-01','9677332189','acc01','09:00:00','18:00:00','gokulsan');
insert into employee values('emp02','Rohan','Thomas','04-08-04','7013678809','acc02','19:00:00','03:00:00','rohthomas');
insert into employee values('emp03','Dale','Sabu','25-06-01','9546003257','acc02','19:00:00','03:00:00','dalesabu');
insert into employee values('emp04','Bharat','Gopal','02-07-07','9856628910','acc03','09:00:00','18:00:00','bharatgpl');
insert into employee values('emp05','Shawn','Dodricks','16-11-08','7015789052','acc01','09:00:00','18:00:00','shrodricks');
insert into employee values('emp06','Vivek','Hari','20-04-10','7043801256','acc02','19:00:00','03:00:00','vivekhari');
insert into employee values('emp07','Philip','Yohan','27-09-06','9492145765','acc01','09:00:00','18:00:00','philyohan');
insert into employee values('emp08','Anju','Sujith','15-06-04','7017905523','acc03','09:00:00','18:00:00','ansujith');
insert into employee values('emp09','Nivin','Vinod','16-02-07','9328865415','acc01','09:00:00','18:00:00','nivinod');
insert into employee values('emp10','Jithin','Joseph','25-07-11','8547206978','acc03','09:00:00','18:00:00','jithjoseph');
insert into employee values('emp11','Wifred','Iwin','02-08-05','9876123550','acc02','19:00:00','03:00:00','wiliwin');
insert into employee values('emp12','Navina','Mohan','09-12-07','9823710065','acc02','19:00:00','03:00:00','navmohan');
insert into employee values('emp13','Manaswini','Shivakumar','26-03-08','9037220302','acc01','09:00:00','18:00:00','manshivkumar');
insert into employee values('emp14','Tina','Mathews','16-07-15','9447318764','acc03','09:00:00','18:00:00','tinamath');
insert into employee values('emp15','Anakha','Krishna','24-03-13','8033121270','acc02','19:00:00','03:00:00','krisanakha');
insert into employee values('emp16','Anu','Thomas','29-03-13','8032112127','acc03','19:00:00','03:00:00','anuanu');
insert into employee values('emp17','Golu','Sri','09-05-01','9077332189','acc03','09:00:00','18:00:00','golus');
insert into employee values('emp18','Aneesh','Krishnankutty','24-02-13','8033121271','acc03','19:00:00','03:00:00','aneeshkutty');
insert into employee values('emp19','Arul','Jyothi','27-03-13','80321121279','acc03','19:00:00','03:00:00','arul');
insert into employee values('emp20','Girija','Sam','20-05-01','9076332189','acc03','09:00:00','18:00:00','giri');
insert into employee values('emp21','Giri','Kutty','24-02-12','8022121271','acc03','19:00:00','03:00:00','gkutty');
insert into employee values('emp22','Arun','Lalu','27-03-10','8011112127','acc03','19:00:00','03:00:00','arunlu');
insert into employee values('emp23','Lalu','Manuel','20-05-11','9444332189','acc02','09:00:00','18:00:00','manlu');
insert into employee values('emp24','Manuel','Mathew','24-07-13','8022331271','acc03','19:00:00','03:00:00','mattman');
insert into employee values('emp25','Kiran','Jose','11-03-10','8000110127','acc03','19:00:00','03:00:00','kijo');
insert into employee values('emp26','Jose','Prakash','2-10-10','9444300089','acc02','09:00:00','18:00:00','jopra');
insert into employee values('emp27','Prakash','Raj','4-07-13','8022301271','acc01','19:00:00','03:00:00','praraj');
insert into employee values('emp28','John','James','1-07-10','9991110127','acc03','19:00:00','03:00:00','joja');
insert into employee values('emp29','James','Singh','3-09-10','8544300089','acc02','09:00:00','18:00:00','jasi');
insert into employee values('emp30','Raman','Kutty','2-07-13','9492301271','acc01','19:00:00','03:00:00','raku');
insert into employee values('','','','','','','','','');

CABS

insert into cabs values('KL-01-AU-3068', 'Grandi10', 4, 5);
insert into cabs values('KL-01-GK-1965', 'i10', 4, 4);
insert into cabs values('KL-03-KL-6593', 'Swift', 4, 4);
insert into cabs values('KL-21-LJ-8557', 'Santro', 4, 4);
insert into cabs values('KL-06-IJ-9981', 'Ertiga', 4, 5);
insert into cabs values('KL-12-XV-5471', 'Celerio', 4, 5);
insert into cabs values('KL-01-LM-3258', 'i10', 4, 4);
insert into cabs values('KL-02-CV-1010', 'GrandI10', 4, 5);
insert into cabs values('KL-08-MN-4687', 'Swift', 4, 5);
insert into cabs values('KL-02-DG-6479', 'Celerio', 4, 5);
insert into cabs values('KL-01-FZ-1254', 'Xcent', 4, 5);
insert into cabs values('KL-15-NO-5201', 'Indica', 4, 3);
insert into cabs values('KL-22-QW-4702', 'Xcent', 4, 5);
insert into cabs values('KL-16-ES-2014', 'Ertiga', 4, 5);
insert into cabs values('KL-02-ER-7210', 'Innova', 7, 5);
insert into cabs values('KL-01-PM-9751', 'GrandI10', 4, 5);
insert into cabs values('KL-17-JK-5579', 'Indica', 4, 3);
insert into cabs values('KL-07-AQ-6475', 'Santro', 4, 4);
insert into cabs values('KL-09-GF-2564', 'Celerio', 4, 5);
insert into cabs values('KL-01-HT-3224', 'Innova', 7, 5);

Login

insert into login values( 'dota', 'chunin', 'agency' );
insert into login values( 'akshos', 'kannan', 'admin' );
insert into login values( 'arul', 'arul', 'emp' );

Employee Address

eid, house_num, street_name, postal_code(int), city
insert into employee_address values( '', '', '', , '' )

insert into employee_address values('emp01', 'TC_44/1661_URA_Lane', 'Eastfort', 'Trivandrum', 695023 );
insert into employee_address values('emp02', 'GA-01_PD_ROAD', 'Eastfort', 'Trivandrum', 695023 );
insert into employee_address values('emp03', 'RAJA_BHAVAN-01', 'Eastfort', 'Trivandrum', 695023 );
insert into employee_address values('emp04', 'Estate_Road', 'Pappanamcode', 'Trivandrum', 695018 );
insert into employee_address values('emp05', 'Kovil_Road', 'Pappanamcode', 'Trivandrum', 695018 );
insert into employee_address values('emp06', 'Manvila_Foundation', 'Pmg_Jn', 'Trivandrum', 695033 );
insert into employee_address values('emp07', 'IB_towers_road', 'Pappanamcode', 'Trivandrum', 695018 );
insert into employee_address values('emp08', 'TC_55/1983_Residency', 'Nemom', 'Trivandrum', 695020 );
insert into employee_address values('emp09', 'Arcade_Residency', 'SS_kovil_road', 'Trivandrum', 695001 );
insert into employee_address values('emp10', 'Flat_14_b(Pe)_heera', 'Ullor', 'Trivandrum', 695011 );
insert into employee_address values('emp11', 'Annas_Arcade', 'SS_kovil_road', 'Trivandrum', 695001);
insert into employee_address values('emp12', 'GOVT_HOST_ROAD', 'Thycaud', 'Trivandrum', 695014);
insert into employee_address values('emp13', 'Flat_3_a(Pe)_heera', 'Ullor', 'Trivandrum', 695011 );
insert into employee_address values('emp14', 'Opp_Brigade_lane', 'Ullor', 'Trivandrum', 695011 );
insert into employee_address values('emp15', 'Amabala_agency_street', 'Nemom', 'Trivandrum', 695020 );
insert into employee_address values('emp16', 'Mascot_Hotel_lane', 'Pmg_Jn', 'Trivandrum', 695033 );
insert into employee_address values('emp17', 'Police_Quaters-palayam', 'Pmg_Jn', 'Trivandrum', 695033 );
insert into employee_address values('emp18', 'Opp_Thycaud_P.O', 'Thycaud', 'Trivandrum', 695014);
insert into employee_address values('emp19', 'Aryanivas_lane', 'SS_kovil_road', 'Trivandrum', 695001);
insert into employee_address values('emp20', 'Loyola_Road', 'Sreekaryam', 'Trivandrum', 695017);
insert into employee_address values('emp21', 'EG-Clg_Road', 'Thycaud', 'Trivandrum', 695014);
insert into employee_address values('emp22', 'Vikhas_Road', 'Sreekaryam', 'Trivandrum', 695017);
insert into employee_address values('emp23', 'Quinton_Road', 'Ullor', 'Trivandrum', 695011);
insert into employee_address values('emp24', 'Puthan_Street', 'EastFort', 'Trivandrum', 695023);
insert into employee_address values('emp25', 'Govt_HSS_road', 'PTP_Nagar', 'Trivandrum', 695038);
insert into employee_address values('emp26', 'Water_AP_Road', 'PTP_Nagar', 'Trivandrum', 695038);
insert into employee_address values('emp27', 'Water_Works', 'Nemom', 'Trivandrum', 695020 );
insert into employee_address values('emp28', 'Power_House', 'Nemom', 'Trivandrum', 695020 );
insert into employee_address values('emp29', 'Kp-34_Church_lane ', 'PTP_Nagar', 'Trivandrum', 695038);
insert into employee_address values('emp30', 'Vihar_lane', 'Pothencode', 'Trivandrum', 695584);



