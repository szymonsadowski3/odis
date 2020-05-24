SELECT * FROM ip_traffic ORDER BY timestamp_start ASC;
SELECT * FROM ip_traffic ORDER BY timestamp_start DESC;

SELECT (max(timestamp_start) - min(timestamp_start)) FROM ip_traffic;

SELECT count(1) FROM ip_traffic;

INSERT INTO ip_traffic SELECT event_type
                            ,ip_src
                            ,ip_dst
                            ,port_src
                            ,port_dst
                            ,timestamp_start - INTERVAL '65 days' AS timestamp_start
                            ,timestamp_end
                            ,packets
                            ,bytes
                            ,writer_id
                            ,mac_src
                            ,mac_dst
                            ,ip_proto
                            ,src_hostname
                            ,dst_hostname
                            ,incoming_outgoing
FROM ip_traffic;