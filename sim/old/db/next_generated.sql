-- SQLite
select * from power where type == 'generated' and timestamp > datetime('2022-02-02 07:20:00+00:00', '+1 seconds') and timestamp <= '2022-02-02 17:05:00' order by timestamp asc