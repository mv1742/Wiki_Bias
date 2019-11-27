CREATE TABLE timeseries2 AS SELECT time_stamp, entity_id, reverts_ind, bots_ind FROM article_new WHERE reverts IS NOT NULL and nofedits is not null;
ALTER TABLE timeseries2 ADD COLUMN date_holder TIMESTAMP;
UPDATE timeseries2 SET date_holder = time_stamp::TIMESTAMP;

# Create materialized view using window functions

# RATE OF CHANGE
CREATE MATERIALIZED VIEW rate_of_change_day_t2 AS
select entity_id,date_trunc('day', date_holder) as day, count(entity_id) as edits, sum(reverts_ind) as reverts
from timeseries2
group by entity_id, day order by entity_id asc, day asc;

CREATE MATERIALIZED VIEW rate_of_change_month_t2 AS
select entity_id,date_trunc('month', date_holder) as month, count(entity_id) as edits, sum(reverts_ind) as reverts
from timeseries2
group by entity_id, month order by entity_id asc, month asc;

CREATE MATERIALIZED VIEW rate_of_change_year_t2 AS
select entity_id,date_trunc('year', date_holder) as year, count(entity_id) as edits, sum(reverts_ind) as reverts
from timeseries2
group by entity_id, year order by entity_id asc, year asc;

# CUMULATIVE TIME SERIES

CREATE MATERIALIZED VIEW cumulative_day as
SELECT entity_id, day, SUM(edits) OVER (PARTITION BY entity_id ORDER BY day) AS edits_sum, SUM(reverts) OVER (PARTITION BY entity_id ORDER BY day) AS reverts_sum
FROM   rate_of_change_day_t2 ;

CREATE MATERIALIZED VIEW cumulative_month as
SELECT entity_id, month, SUM(edits) OVER (PARTITION BY entity_id ORDER BY month) AS edits_sum, SUM(reverts) OVER (PARTITION BY entity_id ORDER BY month) AS reverts_sum
FROM   rate_of_change_month_t2;

CREATE MATERIALIZED VIEW cumulative_year as
SELECT entity_id, year, SUM(edits) OVER (PARTITION BY entity_id ORDER BY year) AS edits_sum, SUM(reverts) OVER (PARTITION BY entity_id ORDER BY year) AS reverts_sum
FROM   rate_of_change_year_t2;

# Migrate to TimescaleDB

CREATE TABLE rate_of_change_month_t2_chunks (LIKE rate_of_change_month_t2INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);

select create_hypertable('rate_of_change_month_t2_chunks', 'month');
INSERT INTO timeseries2_nochunks SELECT * FROM rate_of_change_month_t2;

create materialized view rate_month as select g. entity_title, r.* from rate_of_change_month_t2 r join groupby_article_large_edits g on r.entity_id = g.id;






