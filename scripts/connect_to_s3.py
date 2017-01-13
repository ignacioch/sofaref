import boto3
import logging
from datetime import datetime
from datetime import timedelta

#Method to connect to the S3 bucket and upload the log file /Will be done with cron???
s3 = boto3.resource('s3')
bucket = s3.Bucket('sofaref')

def upload():
	file = open((datetime.now()-timedelta(days=1)).strftime('add_to_table_%d_%m_%Y.log'), 'rb')
	path = 'logs/'+(datetime.now()-timedelta(days=1)).strftime('add_to_table_%d_%m_%Y.log')
	
	s3.Bucket('sofaref').put_object(Key=path, Body=file)


upload()


