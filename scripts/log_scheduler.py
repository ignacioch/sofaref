from datetime import datetime
from threading import Timer
from connect_to_s3 import upload


#Code to run the next day the upload script to push to the S3 bucket the logs of the previous day
#In order to run it every day it should be called from connect_to_s3
#Preferrably done with cron in unix
x=datetime.today()
date = datetime.now().date().strftime('%d_%m_%Y')
print(date)
y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

t = Timer(secs, upload)
t.start()