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

CREATE table LOWER_B_RATIO_large_edits AS

WITH bounds AS (
    SELECT (AVG(ratio) - STDDEV_SAMP(ratio) * 1.5) as lower_bound,
           (AVG(ratio) + STDDEV_SAMP(ratio) * 1.5) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where ratio < (SELECT lower_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc

# SELECT 5712

# 1.5 STDs:
# SELECT 36679
# 4STDs:
# SELECT 867

CREATE table UPPER_4STDs_RATIO_large_edits AS

WITH bounds AS (
    SELECT (AVG(ratio) - STDDEV_SAMP(ratio) * 1.5) as lower_bound,
           (AVG(ratio) + STDDEV_SAMP(ratio) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where ratio > (SELECT upper_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;


# FILTER URLS 

CREATE table LOWER_MED_2_5_STDs_RATIO_large_edits AS
WITH bounds AS (
    SELECT (AVG(ratio) - STDDEV_SAMP(ratio) * 1.5) as lower_bound,
	   (AVG(ratio) + STDDEV_SAMP(ratio) * 1) as med_bound,
           (AVG(ratio) + STDDEV_SAMP(ratio) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where ratio > (SELECT lower_bound FROM bounds) AND ratio < (SELECT med_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;

CREATE table MED_Upper_3_STDs_RATIO_large_edits AS
WITH bounds AS (
    SELECT (AVG(ratio) - STDDEV_SAMP(ratio) * 1.5) as lower_bound,
	   (AVG(ratio) + STDDEV_SAMP(ratio) * 1) as med_bound,
           (AVG(ratio) + STDDEV_SAMP(ratio) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where ratio > (SELECT med_bound FROM bounds) AND ratio < (SELECT upper_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;
SELECT 55535




SELECT round(AVG(reverts)) as avg, MIN(reverts), MAX(reverts), STDDEV_SAMP(ratio), STDDEV(ratio), STDDEV_POP(ratio)  FROM s2c_large_edits;
postgres=# SELECT round(AVG(reverts)) as avg, MIN(reverts), MAX(reverts), STDDEV_SAMP(reverts), STDDEV(reverts), STDDEV_POP(reverts)  FROM s2c_large_edits;
# avg | min | max  |   stddev_samp    |      stddev      |    stddev_pop
#-----+-----+------+------------------+------------------+------------------
# 302 |  42 | 3522 | 400.815723821479 | 400.815723821479 | 400.815620937510

# FILTER URLS LOWER_BOUND_RATIO

CREATE table LOWER_B_REVERTS_large_edits AS

WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 0.5) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where reverts < (SELECT lower_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc

# SELECT 174731

# FILTER URLS UPPER_BOUND_REVERTS

CREATE table UPPER_4STDs_REVERTS_large_edits AS

WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where reverts > (SELECT upper_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;

# SELECT 6890
CREATE table UPPER_REVERTS_large_edits AS

WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 0.5) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where reverts > (SELECT upper_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;

# SELECT 59005


# FILTER URLS UPPER_BOUND_REVERTS

CREATE table UPPER_4STDs_REVERTS_large_edits AS

WITH bounds AS (
    SELECT (AVG(reverts) + STDDEV_SAMP(reverts) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where reverts > (SELECT upper_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;

# SELECT 6890


CREATE table LOWER_MED_2_5_STDs_REVERTS_large_edits AS
WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
	   (AVG(reverts) + STDDEV_SAMP(reverts) * 1) as med_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where reverts > (SELECT lower_bound FROM bounds) AND reverts < (SELECT med_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;

CREATE table MED_Upper_3_STDs_REVERTS_large_edits AS
WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
	   (AVG(reverts) + STDDEV_SAMP(reverts) * 1) as med_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 4) as upper_bound
    FROM s2c_large_edits 
)
select distinct(host), count(host)
    from (select *, substring(url from '.*://([^/]*)') as host from s2c_large_edits 
where reverts > (SELECT med_bound FROM bounds) AND reverts < (SELECT upper_bound FROM bounds)) t1
  where t1.host != ''
  group by host
  order by count desc;

CREATE tble 

## ADD ID: 

ALTER TABLE LOWER_B_RATIO_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE LOWER_MED_2_5_STDs_RATIO_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE MED_Upper_3_STDs_RATIO_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE UPPER_4STDs_RATIO_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE LOWER_B_REVERTS_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE LOWER_MED_2_5_STDs_REVERTS_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE MED_Upper_3_STDs_REVERTS_large_edits ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE UPPER_4STDs_REVERTS_large_edits ADD COLUMN id SERIAL PRIMARY KEY;

ALTER TABLE LOWER_B_RATIO_large_edits 
RENAME COLUMN count_LOWER_B_RATIO to count_lb;

ALTER TABLE LOWER_MED_2_5_STDs_RATIO_large_edits 
RENAME COLUMN count_LOWER_MED_2_5_STDs_RATIO to count_lm;

ALTER TABLE MED_Upper_3_STDs_RATIO_large_edits 
RENAME COLUMN count_MED_Upper_3_STDs_RATIO to count_mu;

ALTER TABLE UPPER_4STDs_RATIO_large_edits 
RENAME COLUMN count_UPPER_4STDs_RATIO to count_u;


ALTER TABLE LOWER_B_REVERTS_large_edits 
RENAME COLUMN count to count_lb;

ALTER TABLE LOWER_MED_2_5_STDs_REVERTS_large_edits 
RENAME COLUMN count_LOWER_MED_2_5_STDs_REVERTS to count_lm;

ALTER TABLE MED_Upper_3_STDs_REVERTS_large_edits 
RENAME COLUMN count_MED_Upper_3_STDs_REVERTS to count_mu;

ALTER TABLE UPPER_4STDs_REVERTS_large_edits 
RENAME COLUMN count_UPPER_4STDs_REVERTS to count_u;

ALTER TABLE LOWER_B_RATIO_large_edits
RENAME COLUMN host TO host_lb;

ALTER TABLE LOWER_MED_2_5_STDs_RATIO_large_edits
RENAME COLUMN host TO host_lm;

ALTER TABLE MED_Upper_3_STDs_RATIO_large_edits
RENAME COLUMN host TO host_mu;

ALTER TABLE UPPER_4STDs_RATIO_large_edits
RENAME COLUMN host TO host_u;

ALTER TABLE LOWER_B_REVERTS_large_edits
RENAME COLUMN host TO host_lb;

ALTER TABLE LOWER_MED_2_5_STDs_REVERTS_large_edits
RENAME COLUMN host TO host_lm;

ALTER TABLE MED_Upper_3_STDs_REVERTS_large_edits
RENAME COLUMN host TO host_mu;

ALTER TABLE UPPER_4STDs_REVERTS_large_edits
RENAME COLUMN host TO host_u;



# Merge lb and lm 
CREATE table JOINED_table1 AS SELECT A.*, B.host_lb, B.count_lb FROM LOWER_MED_2_5_STDs_RATIO_large_edits AS A 
FULL OUTER JOIN LOWER_B_RATIO_large_edits AS B 
ON A.host_lm=B.host_lb;
SELECT 192787


CREATE table JOINED_table1 AS SELECT A.*, B.host_lb, B.count_lb FROM LOWER_MED_2_5_STDs_RATIO_large_edits AS A 
FULL OUTER JOIN LOWER_B_RATIO_large_edits AS B 
ON A.host_lm=B.host_lb;
SELECT 192787

CREATE table JOINED_table1_2 AS Select count_lm, count_lb, Case
        When host_lm IS NULL Then host_lb
        Else host_lm End
        AS host
From JOINED_table1;
SELECT 192787

# Merge mu and table_1_2 
CREATE table JOINED_table2 AS (SELECT * FROM MED_Upper_3_STDs_RATIO_large_edits FULL OUTER JOIN JOINED_table1_2
ON (MED_Upper_3_STDs_RATIO_large_edits.host_mu=JOINED_table1_2.host));
SELECT 220248

CREATE table JOINED_table2_2 AS 
Select table2.count_mu, table2.count_lm, table2.count_lb, Case
        When table2.host IS NULL Then table2.host_mu
        Else table2.host End
        AS host
From JOINED_table2 AS table2;
SELECT 220445

# Merge u and table_2_2 
CREATE table JOINED_table3 AS (SELECT * FROM UPPER_4STDs_RATIO_large_edits FULL OUTER JOIN JOINED_table2_2
ON (UPPER_4STDs_RATIO_large_edits.host_u=JOINED_table2_2.host));


# Joined_Table3
CREATE table JOINED_table3 AS (SELECT * FROM UPPER_4STDs_RATIO_large_edits FULL OUTER JOIN JOINED_table2_2
ON (UPPER_4STDs_RATIO_large_edits.host_u=JOINED_table2_2.host));
SELECT 220445

CREATE table JOINED_table3_2 AS 
Select table3.count_u, table3.count_mu, table3.count_lm, table3.count_lb, Case
        When table3.host IS NULL Then table3.host_u
        Else table3.host End
        AS host
From JOINED_table3 AS table3;

UPDATE JOINED_table3_2 SET count_mu = 0 WHERE count_mu IS NULL;
UPDATE JOINED_table3_2 SET count_lm = 0 WHERE count_lm IS NULL;
UPDATE JOINED_table3_2 SET count_lb = 0 WHERE count_lb IS NULL;
UPDATE JOINED_table3_2 SET count_u = 0 WHERE count_u IS NULL;


JOINED_table3 

# SELECT COALESCE(count_mu, 0 ),COALESCE(count_lm, 0 ),COALESCE(count_lb, 0 ),COALESCE(count_u, 0 ) FROM JOINED_table3;

CREATE table JOINED_distribution AS
SELECT host, count_u, count_mu, count_lm, count_lb,
        count_u * 100.0 / (select SUM(count_u) FROM JOINED_table3) as count_u_percent,
        count_mu * 100.0 / (select SUM(count_mu) FROM JOINED_table3) as count_mu_percent,
        count_lm * 100.0 / (select SUM(count_lm) FROM JOINED_table3) as count_lm_percent,
        count_lb * 100.0 / (select SUM(count_lb) FROM JOINED_table3) as count_lb_percent
FROM JOINED_table3
GROUP BY host, count_u, count_mu, count_lm, count_lb;
SELECT 220252

ALTER TABLE JOINED_distribution 
ADD conflict_score_dist float;
ADD conflict_score_count float;

UPDATE JOINED_distribution SET conflict_score_count = (count_u - count_lb)/NULLIF(count_lb,0);
UPDATE 220445


ALTER TABLE JOINED_distribution 
ADD conflict_score_distribution float;

UPDATE JOINED_distribution SET conflict_score_dist = (count_u_percent - count_lb_percent)/NULLIF(count_lb_percent,0);
UPDATE 220252

UPDATE JOINED_distribution SELECT WHERE FROM JOINED_distribution;

CREATE table distribution_conflict_score AS
SELECT * FROM JOINED_distribution where conflict_score in not null;
SELECT 5712


SELECT round(AVG(reverts)) as avg, MIN(reverts), MAX(reverts), STDDEV_SAMP(ratio), STDDEV(ratio), STDDEV_POP(ratio)  FROM s2c_large_edits;


### Calculate distribution along sources


# host, count_u, count_mu, count_lm, count_lb, to be finished
CREATE table SOURCE_Rating_distribution AS
SELECT host, count_u AS A, count_mu AS B, count_lm AS C, count_lb AS D, (count_u + count_mu + count_lm + count_lb) AS TOTAL, (count_u + count_mu + count_lm + count_lb)/4 AS AVERAGE, 
	SQRT(  
  (A-AVERAGE)(B-AVERAGE) + C*C + D*D)/4  - (A+B+C+D)*(A+B+C+D)/4/4) AS sd
  FROM JOINED_table3;
