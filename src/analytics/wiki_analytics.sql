-- 1. Create Materialized View s2conflict
CREATE materialized view s2conflict AS
select *, ratio_minmaxed + ratio_2_minmaxed as conflict_score from
    (select *, 1.00 * (ratio - MIN(ratio)) / (MAX(ratio)-MIN(ratio)) as ratio_minmax, 1.00 * (ratio_2 - MIN(ratio_2)) / (MAX(ratio_2)-MIN(ratio_2)) as ratio_2_minmax from
        (select *, cast(reverts as float)/cast(len_text as float) as ratio_2
        FROM refs_refs_cats_lens
        LEFT JOIN
                SELECT *, unnest(categories), CAST(reverts AS float)/nofedits as ratio
                FROM article_conflict conflict ON(refs_refs_cats_lens.id=conflict.entity_id)) t1) t2
where conflict_score is not null
ORDER BY conflict_score;

-- 2. Table Groupby_Article
-- 2.1 Group by Article and filter relevant edits (small articles are ignored)
CREATE materialized view groupby_article_len_relevant AS
WITH bounds AS (
    SELECT (AVG(reverts)) as upper_bound FROM s2conflict)
select * FROM (select distinct(id)
                from s2conflict
                group by id) s2conflict_articles
where reverts > (SELECT upper_bound FROM bounds);
-- 2.2. Calculate Conflict Score 1 to 5
CREATE materialized view groupby_articles_Score_ratios AS
WITH bounds AS (
    SELECT (AVG(conflict_score) + STDDEV_SAMP(ratio)* 3) as upper_bound,
	(AVG(conflict_score) + STDDEV_SAMP(conflict_score) * 2) as med_high_bound,
	(AVG(conflict_score)) as med_bound
	(AVG(conflict_score) - STDDEV_SAMP(conflict_score)  * 1) as lower_bound FROM groupby_article_len_relevant)
select *, (case when (conflict_score < (SELECT lower_bound FROM bounds)) then 1 when (conflict_score > (SELECT lower_bound FROM bounds) and conflict_score < (SELECT med_bound FROM BOUNDS)) then 2
			when (conflict_score > (SELECT med_bound FROM BOUNDS) and conflict_score < (SELECT med_high_bound FROM BOUNDS)) then 3 when (conflict_score > (SELECT med_high_bound FROM BOUNDS) and conflict_score < (SELECT upper_bound FROM BOUNDS)) then 4
			when (conflict_score > (SELECT upper_bound FROM BOUNDS)) then 5 end) as rating
from groupby_article_len_relevant;

-- 3. Table Group by URL host
-- 3.1. Extract URL
CREATE materialized view s2conflict_urls AS select distinct(host), count(host)
    from (select substring(url from '.*://([^/]*)') as host from s2conflict) t1
  where t1.host != ''
  group by host
  order by count desc

-- 3.2. Filter URL with Large edits
CREATE materialized view  s2c_urls_large_edits AS
WITH bounds AS (
    SELECT (AVG(reverts) - STDDEV_SAMP(reverts) * 0.5) as lower_bound,
           (AVG(reverts) + STDDEV_SAMP(reverts) * 0.5) as upper_bound, AVG(reverts) as av_reverts
    FROM (SELECT * FROM s2conflict_urls WHERE conflict_score IS NOT NULL) t1
)
select * FROM t1
where reverts > (SELECT av_reverts FROM bounds);