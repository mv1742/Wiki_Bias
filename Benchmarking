postgres=# explain analyze select * from rate_month where month = '2019-08-01' order by edits desc limit 10;
                                                                  QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=99441.02..99442.17 rows=10 width=64) (actual time=925.554..961.605 rows=10 loops=1)
   ->  Gather Merge  (cost=99441.02..101200.75 rows=15302 width=64) (actual time=925.552..961.582 rows=10 loops=1)
         Workers Planned: 1
         Workers Launched: 1
         ->  Sort  (cost=98441.01..98479.27 rows=15302 width=64) (actual time=909.521..909.577 rows=52 loops=2)
               Sort Key: edits DESC
               Sort Method: quicksort  Memory: 2988kB
               ->  Parallel Seq Scan on rate_month  (cost=0.00..97377.41 rows=15302 width=64) (actual time=0.031..873.761 rows=17582 loops=2)
                     Filter: (month = '2019-08-01 00:00:00'::timestamp without time zone)
                     Rows Removed by Filter: 2966510
 Planning time: 0.086 ms
 Execution time: 961.680 ms
(12 rows)

postgres=# CREATE TABLE rate_month_chunks (LIKE rate_month INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
CREATE TABLE
postgres=# select create_hypertable('rate_month_chunks', 'month');              NOTICE:  adding not-null constraint to column "month"
DETAIL:  Time dimensions cannot have NULL values
^[[A       create_hypertable
--------------------------------
 (7,public,rate_month_chunks,t)
(1 row)

postgres=# INSERT INTO rate_month_chunks SELECT * FROM rate_month;

postgres=# explain analyze select * from rate_month_chunks where month = '2019-08-01' order by edits desc limit 10;
                                                                                    QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=140.96..140.98 rows=10 width=64) (actual time=195.736..195.767 rows=10 loops=1)
   ->  Sort  (cost=140.96..141.34 rows=155 width=64) (actual time=195.733..195.742 rows=10 loops=1)
         Sort Key: _hyper_7_3049_chunk.edits DESC
         Sort Method: top-N heapsort  Memory: 26kB
         ->  Append  (cost=2.59..137.61 rows=155 width=64) (actual time=78.552..166.040 rows=35164 loops=1)
               ->  Bitmap Heap Scan on _hyper_7_3049_chunk  (cost=2.59..137.61 rows=155 width=64) (actual time=78.550..115.044 rows=35164 loops=1)
                     Recheck Cond: (month = '2019-08-01 00:00:00'::timestamp without time zone)
                     Heap Blocks: exact=352
                     ->  Bitmap Index Scan on _hyper_7_3049_chunk_rate_month_chunks_month_idx  (cost=0.00..2.55 rows=155 width=0) (actual time=78.479..78.480 rows=35164 loops=1)
                           Index Cond: (month = '2019-08-01 00:00:00'::timestamp without time zone)
 Planning time: 150.110 ms
 Execution time: 195.824 ms
(12 rows)

Result: Timescale DB is x7 faster with time-based queries