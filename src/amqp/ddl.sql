create table ip_traffic
(
	event_type varchar(255),
	ip_src varchar(255),
	ip_dst varchar(255),
	port_src varchar(255),
	port_dst integer,
	timestamp_start timestamp,
	timestamp_end timestamp,
	packets integer,
	bytes integer,
	writer_id varchar(255),
	mac_src varchar(255),
	mac_dst varchar(255),
	ip_proto varchar(255),
	src_hostname varchar(255),
	dst_hostname varchar(255)
);

alter table ip_traffic owner to odis;

