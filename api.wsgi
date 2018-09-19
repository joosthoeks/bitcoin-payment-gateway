

import sys


# require python3:
if sys.version_info[0] < 3:
    raise Exception("Python3 required! Current (wrong) version: '%s'" % sys.version_info)

sys.path.insert(0, '/home/joost/bitcoin-payment-gateway')
from api import app as application

