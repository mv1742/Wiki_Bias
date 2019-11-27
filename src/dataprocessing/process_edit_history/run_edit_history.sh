#!/bin/bash
for i in 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
do
   echo="$i"
   spark-submit --master spark://ec2-35-168-228-143.compute-1.amazonaws.com:7077 --jars postgresql-42.2.8.jar --packages com.databricks:spark-xml_2.11:0.6.0,org.postgresql:postgresql:42.2.5 edit_history.py stub$i article_fixed 01/01/2002 $i
done
