# http://gitlab.gary.pro/formation/aws-basic/blob/0454444e25ad3d3b454ca5e0d29db51bb94141aa/aws-rds-create-db-instance-postgresql.sh


#!/usr/bin/env bash

aws rds create-db-instance \
  --db-instance-identifier "postgresql" \
  --engine postgres \
  --engine-version 11.4 \
  --db-instance-class db.t2.micro \
  --allocated-storage 40 \
  --backup-retention-period 30 \
  --master-username Manrique-IAM \
  --region us-east-1 \


















