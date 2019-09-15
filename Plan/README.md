# Planning

# More Ideas
## Add more metrics...?
- Sentiment from Gdelt dataset
If time allows, references will have a score derived from Gdelt dataset which provides sentiment analysis scores for each data source. Data sources will then be ranked from 0 - neutral sentiment, to -1, 1 (positive/negative).

-------------------

# TASKS
- Read from s3 with python put in Postgres [instructions]


# DONE
- Connect shh to EC2 Instance
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
- Install Python, pip, and the EB CLI on Linux
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html
- Put Data in s3. 
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
- Create postgreSQL database
https://docs.aws.amazon.com/cli/latest/reference/rds/create-db-instance.html
- Could have used command, but had a permission issue (needs policy)  [link](https://github.com/mv1742/Wiki_Bias/blob/master/AWS/aws-rds-create-db-instance-postgresql.sh)
