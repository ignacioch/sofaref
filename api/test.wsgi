import sys
import site
if sys.version_info[0]<3:       # require python3
 raise Exception("Python3 required! Current (wrong) version: '%s'" % sys.version_info)
site.addsitedir('/home/ubuntu/sofaref/api/myvenv/lib/python3.4/site-packages')
sys.path.insert(0, '/home/ubuntu/sofaref/api/')
from app import app as application

