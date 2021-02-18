import datetime
import time
import pytz

# Config File
import ApiConfig as cfg

# TheHive4Py Imports
from thehive4py.api import TheHiveApi
from thehive4py.models import *
from thehive4py.query import *

#Cortex Imports
from cortex4py.api import Api

#APIs Connection
hiveServer = cfg.ApiConfig["TheHiveHost"] + ":" + cfg.ApiConfig["TheHivePort"]
hiveKey = cfg.ApiConfig["TheHiveApiKey"]
apiH = TheHiveApi(hiveServer, hiveKey)

cortexServer = cfg.ApiConfig["CortexHost"] + ":" + cfg.ApiConfig["CortexPort"]
cortexKey = cfg.ApiConfig["CortexApiKey"]
apiC = Api(cortexServer, cortexKey)
