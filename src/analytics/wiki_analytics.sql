# 1. s2conflict_urls

EXPLAIN ANALYZE CREATE table s2conflict_urls_pageviews AS SELECT * FROM pageviews2 LEFT JOIN s2conflict_urls ON(pageviews2.curr_title=s2conflict_urls.entity_title)
ORDER BY ratio;


# 2. Table Groupby_Article  DONE

EXPLAIN ANALYZE CREATE table Groupby_Article AS SELECT id, entity_title, ratio, reverts, nofedits FROM s2conflict 
     WHERE ratio IS NOT NULL GROUP BY id, entity_title, ratio, reverts, nofedits ORDER BY reverts DESC;

# Filter Relevant edits
# s2c_large_edits

EXPLAIN ANALYZE CREATE table Groupby_Article AS SELECT id, entity_title, ratio, reverts, nofedits FROM s2c_large_edits 
     WHERE ratio IS NOT NULL GROUP BY id, entity_title, ratio, reverts, nofedits ORDER BY reverts DESC;

# 3. Table URLCOUNT
#	A. Extract URL
CREATE table urlcount AS select distinct(host), count(host)
    from (select substring(url from '.*://([^/]*)') as host from s2conflict_urls) t1
  where t1.host != ''
  group by host
  order by count desc

# FILTER URLS WITH EDITS
CREATE TABLE s2conflict_urls_with_edit_history AS SELECT * FROM s2conflict_urls WHERE ratio IS NOT NULL;

## FIRST FILTER RELEVANT EDITS
# EXPLORE DATA FIRST
# SELECT round(AVG(reverts)) as avg, MIN(reverts), MAX(reverts) FROM s2conflict_urls_with_edit_history; 
# avg | min | max
#-----+-----+------
#  42 |   0 | 3522
# (1 row)
SELECT round(AVG(ratio)) as avg, MIN(ratio), MAX(ratio) FROM s2conflict_urls_with_edit_history; 
# avg | min | max
#-----+-----+-----
#   0 |   0 |   1
[source](https://www.gab.lc/articles/average_ignoring_extremes_outliers/)

# s2c_large_edits 0.5 STD!
CREATE table s2c_large_edits AS
WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 0.5) as upper_bound, AVG(reverts) as av_reverts
    FROM s2conflict_urls_with_edit_history
)
select * FROM s2conflict_urls_with_edit_history
where reverts > (SELECT av_reverts FROM bounds);

ALL: SELECT 15270784, ABOVE REV AVERAGE: SELECT 1947902.

s2c_large_edits 
SELECT round(AVG(ratio)) as avg, MIN(ratio), MAX(ratio) FROM s2c_large_edits;
        avg         |         min         |        max        |    stddev_samp     |       stddev       |     stddev_pop
--------------------+---------------------+-------------------+--------------------+--------------------+--------------------
 0.0955473907965123 | 0.00393111194309247 | 0.776699029126214 | 0.0516400146363824 | 0.0516400146363824 | 0.0516400013810899


# FILTER URLS LOWER_BOUND_RATIO

CREATE table Groupby_url_reverts AS
select distinct(host), count(host), CAST(AVG(reverts) AS FLOAT)
    from (select *, substring(url from '.*://([^/]*)') as host from s2conflict_urls_with_edit_history) t1 
  where host != ''
  group by host
  order by count desc;
SELECT 1091137


CREATE table Groupby_url_ratio AS
select distinct(host), count(host) AS host_count, CAST(AVG(ratio) AS FLOAT) AS ratio_av
    from (select *, substring(url from '.*://([^/]*)') as host from s2conflict_urls_with_edit_history) t1 
  where host != ''
  group by host
  order by host_count desc;
SELECT 1091137


SELECT STDDEV(count) as std_host_count, round(AVG(count)) as host_avg, MIN(count) as host_min, MAX(count) as host_max, round(AVG(avg)) as avg_reverts, STDDEV(avg) as stdev_reverts, MIN(avg) as min_reverts, MAX(avg) as max_reverts FROM Groupby_url_reverts;
 std_host_count  | host_avg | host_min | host_max | avg_reverts |  stdev_reverts   | min_reverts | max_reverts
------------------+----------+----------+----------+-------------+------------------+-------------+-------------
 536.361558401490 |       12 |        1 |   410281 |          38 | 146.973545566755 |           0 |        3522


SELECT STDDEV(host_count) as std_host_count, round(AVG(host_count)) as host_avg, MIN(host_count) as host_min, MAX(host_count) as host_max, STDDEV(ratio_av) as stdev_ratio, AVG(ratio_av) as avg_ratio, MIN(ratio_av) as min_ratio, MAX(ratio_av) as max_ratio FROM Groupby_url_ratio;
  std_host_count  | host_avg | host_min | host_max |    stdev_ratio    |     avg_ratio     | min_ratio |     max_ratio
------------------+----------+----------+----------+-------------------+-------------------+-----------+-------------------
 536.361558401490 |       12 |        1 |   410281 | 0.036954956703525 | 0.026362976608395 |         0 | 0.982539682539682


CREATE table Groupby_url_reverts_relevant AS
WITH bounds AS (
    SELECT (AVG(count) + STDDEV_SAMP(count) * 0.5) as upper_bound FROM Groupby_url_reverts)
select * FROM Groupby_url_reverts 
where count > (SELECT upper_bound FROM bounds);
# SELECT 4842

CREATE table Groupby_url_ratio_relevant AS
WITH bounds AS (
    SELECT (AVG(host_count) + STDDEV_SAMP(host_count) * 0.5) as upper_bound FROM Groupby_url_ratio)
select * FROM Groupby_url_ratio
where host_count > (SELECT upper_bound FROM bounds);

#SELECT 4842
SELECT STDDEV(count) as std_host_count, round(AVG(count)) as host_avg, MIN(count) as host_min, MAX(count) as host_max, round(AVG(avg)) as avg_reverts, STDDEV(avg) as stdev_reverts, MIN(avg) as min_reverts, MAX(avg) as max_reverts FROM Groupby_url_reverts_relevant;
  std_host_count   | host_avg | host_min | host_max | avg_reverts |  stdev_reverts   | min_reverts |   max_reverts
-------------------+----------+----------+----------+-------------+------------------+-------------+------------------
 7882.980951014345 |     1634 |      281 |   410281 |          37 | 42.6253820394668 |           0 | 482.337786259542


SELECT STDDEV(host_count) as std_host_count, round(AVG(host_count)) as host_avg, MIN(host_count) as host_min, MAX(host_count) as host_max, STDDEV(ratio_av) as stdev_ratio, AVG(ratio_av) as avg_ratio, MIN(ratio_av) as min_ratio, MAX(ratio_av) as max_ratio FROM Groupby_url_ratio_relevant;

  std_host_count   | host_avg | host_min | host_max |    stdev_ratio    |     avg_ratio     | min_ratio |     max_ratio
-------------------+----------+----------+----------+-------------------+-------------------+-----------+-------------------
 7882.980951014345 |     1634 |      281 |   410281 | 0.015547830721196 | 0.025486845477976 |         0 | 0.119337545612111


CREATE table Source_Score_reverts AS
WITH bounds AS (
    SELECT (AVG(avg) + STDDEV_SAMP(avg)* 4) as upper_bound,
	(AVG(avg) + STDDEV_SAMP(avg) * 1) as med_low_bound,
	(AVG(avg) - STDDEV_SAMP(avg) * 1) as lower_bound FROM Groupby_url_reverts_relevant)
select *, (case when (avg < (SELECT lower_bound FROM bounds)) then 1 when (avg > (SELECT lower_bound FROM bounds) and avg < (SELECT med_low_bound FROM BOUNDS)) then 2
			when (avg > (SELECT med_low_bound FROM BOUNDS) and avg < (SELECT upper_bound FROM BOUNDS)) then 3 when (avg > (SELECT upper_bound FROM BOUNDS)) then 4 end) as rating
from Groupby_url_reverts_relevant;


CREATE table Source_Score_ratio AS
WITH bounds AS (
    SELECT (AVG(ratio_av) + STDDEV_SAMP(ratio_av)* 4) as upper_bound,
	(AVG(ratio_av) + STDDEV_SAMP(ratio_av) * 1) as med_low_bound,
	(AVG(ratio_av) - STDDEV_SAMP(ratio_av) * 1) as lower_bound FROM Groupby_url_ratio_relevant)
select *, (case when (ratio_av < (SELECT lower_bound FROM bounds)) then 1 when (ratio_av > (SELECT lower_bound FROM bounds) and ratio_av < (SELECT med_low_bound FROM BOUNDS)) then 2
			when (ratio_av > (SELECT med_low_bound FROM BOUNDS) and ratio_av < (SELECT upper_bound FROM BOUNDS)) then 3 when (ratio_av > (SELECT upper_bound FROM BOUNDS)) then 4 end) as rating
from Groupby_url_ratio_relevant;
# SELECT 4842


