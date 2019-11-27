-- 1. Create materialized view from raw data
CREATE  MATERIALIZED VIEW  timeseries2 AS SELECT time_stamp, entity_id, reverts_ind, bots_ind FROM article_new WHERE reverts IS NOT NULL and nofedits is not null;
ALTER  MATERIALIZED VIEW  timeseries2 ADD COLUMN date_holder TIMESTAMP;
UPDATE timeseries2 SET date_holder = time_stamp::TIMESTAMP;

-- 2. Create materialized view using window function - calculate Rate of Change daily, monthly, and yearly
-- 2.1 Calculate Rate of Change daily
CREATE MATERIALIZED VIEW rate_of_change_day_t2 AS
select entity_id,date_trunc('day', date_holder) as day, count(entity_id) as edits, sum(reverts_ind) as reverts
from timeseries2
group by entity_id, day order by entity_id asc, day asc;
-- 2.2 Calculate Rate of Change monthly
CREATE MATERIALIZED VIEW rate_of_change_month_t2 AS
select entity_id,date_trunc('month', date_holder) as month, count(entity_id) as edits, sum(reverts_ind) as reverts
from timeseries2
group by entity_id, month order by entity_id asc, month asc;
-- 2.3 Calculate Rate of Change yearly
CREATE MATERIALIZED VIEW rate_of_change_year_t2 AS
select entity_id,date_trunc('year', date_holder) as year, count(entity_id) as edits, sum(reverts_ind) as reverts
from timeseries2
group by entity_id, year order by entity_id asc, year asc;

-- 3. Migrate to TimescaleDB
CREATE TABLE rate_of_change_month_t2_chunks (LIKE rate_of_change_month_t2INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
select create_hypertable('rate_of_change_month_t2_chunks', 'month');
INSERT INTO timeseries2_nochunks SELECT * FROM rate_of_change_month_t2;

-- 4. Add entity_titles to display in Flask
create materialized view rate_month as select g. entity_title, r.* from rate_of_change_month_t2 r join groupby_article_large_edits g on r.entity_id = g.id;