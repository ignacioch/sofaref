from flask import Flask
import logging
import os
from datetime import datetime
#os.chdir('/home/ubuntu/sofaref/api')

logging.basicConfig(filename=datetime.now().strftime('sofaref_%d_%m_%Y.log'),level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
from app import views

