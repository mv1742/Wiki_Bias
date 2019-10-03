# Add pageviews, replace underscore '_'
UPDATE pageviews2 SET curr_title  = replace(curr_title, '_', ' ');

EXPLAIN ANALYZE CREATE table article_pageviews AS SELECT * FROM groupby_article_large_edits LEFT JOIN pageviews2 ON(groupby_article_large_edits.entity_title = pageviews2.curr_title)
ORDER BY ratio;
