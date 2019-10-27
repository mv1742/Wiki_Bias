  cat files.txt | while read line
do
  spark-submit --master spark://ec2-52-200-116-187.compute-1.amazonaws.com:7077 --jars postgresql-42.2.8.jar --packages com.databricks:spark-xml_2.11:0.6.0,org.postgresql:postgresql:42.2.5 articles.py $line
done
