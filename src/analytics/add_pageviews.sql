# Add pageviews, replace underscore '_'
UPDATE pageviews2 SET curr_title  = replace(curr_title, '_', ' ');
