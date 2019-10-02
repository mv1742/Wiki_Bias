# 1. s2conflict_urls

EXPLAIN ANALYZE CREATE table s2conflict_urls AS SELECT * FROM refs_cleaned_url LEFT JOIN conflict ON(refs_cleaned_url.id=conflict.entity_id)
ORDER BY ratio;


# 2. Table Groupby_Article  DONE

EXPLAIN ANALYZE CREATE table Groupby_Article AS SELECT id, entity_title, ratio, reverted, nofedits FROM s2conflict 
     WHERE ratio IS NOT NULL GROUP BY id, entity_title, ratio, reverted, nofedits ORDER BY reverted DESC;

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

# s2c_large_edits 
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


# FILTER URLS UPPER_BOUND_RATIO

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
  order by count desc

# 1.5 STDs:
# SELECT 36679
# 4STDs:
# SELECT 867


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

# FILTER URLS UPPER_BOUND_RATIO

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








