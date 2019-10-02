CREATE TABLE wikirefs (
id serial PRIMARY KEY,
article VARCHAR (255),
page_id NUMBER (255),
template VARCHAR (255),
template_original VARCHAR (255),
title VARCHAR (255),
url VARCHAR (255));

ALTER TABLE article_conflict
RENAME COLUMN "sum(reverts)" TO reverts;

ALTER TABLE article_conflict
RENAME COLUMN "sum(nofedits)" TO nofedits;

CREATE TABLE conflict AS SELECT *, CAST(reverts AS float)/nofedits as ratio FROM article_conflict;

EXPLAIN ANALYZE CREATE table s2conflict AS SELECT * FROM table_references LEFT JOIN conflict ON(table_references.id=conflict.entity_id)
ORDER BY ratio;


SELECT t.id, t.entity_title, ratio CTID FROM public.s2conflict t
WHERE ratio IS NOT NULL GROUP BY id, entity_title, ratio ORDER BY ratio DESC

LIMIT 501

#TOP REVERTED

SELECT t.id, t.entity_title, ratio CTID FROM public.s2conflict t
     WHERE ratio IS NOT NULL GROUP BY id, entity_title, ratio ORDER BY ratio DESC
     LIMIT 501

#TOP RATIO


SELECT t.id, t.entity_title, ratio CTID FROM public.s2conflict t
     WHERE ratio IS NOT NULL GROUP BY id, entity_title, ratio ORDER BY ratio DESC
     LIMIT 501

             CREATE TABLE domains AS SELECT *, LEFT(SUBSTRING(url, 
       (CASE WHEN CHARINDEX('//',url)=0 
            THEN 5 
            ELSE  CHARINDEX('//',url) + 2
            END), 35),
       (CASE 
       WHEN CHARINDEX('/', SUBSTRING(url, CHARINDEX('//', url) + 2, 35))=0 
       THEN LEN(url) 
       else CHARINDEX('/', SUBSTRING(url, CHARINDEX('//', url) + 2, 35))- 1
       END)
       ) AS 'Domain' FROM s2conflict_urls;
