#!/usr/bin/env python
# -*- codinge: utf-8 -*-

from time import sleep
import json

# Config File
import ApiConfig as cfg

#Api Connections
from ApiConnections import *

#Modules Import 
from Modules import *

Logging("[INFO]","Comienza la ejecución del script")

cortex_id = cfg.ApiConfig["CortexId"]

#date = datetime.datetime.now()
#date = date.strftime("%d/%m/%Y %H:%M:%S")
date = "09/02/2021 15:24:00"
date = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M:%S") -  datetime.timedelta(minutes=30)
time_tuple = date.timetuple()
timestamp = int(time.mktime(time_tuple)*1000)

query = Gte('date', timestamp)
response = apiH.find_alerts(query=query, sort=['-createdAt'], range='all')
alerts = response.json()

if response.status_code == 200:
    alerts = Filter(alerts)

    try:

        for alert in alerts:
            case_id = CreateCase(alert)
            artifacts = alert['artifacts']

            for artifact in artifacts:
                artifact_id = CreateCaseObservable(artifact, case_id)
                analyzers = SearchAnalyzers(artifact['dataType'])
                    
                for analyzer in analyzers:
                    analyzer_id = analyzer.analyzerDefinitionId
                    response = apiH.run_analyzer(cortex_id, artifact_id, analyzer_id)
		    
                    if response.status_code == 200:
                        msg = "Se corrió correctamente el análisis " + analyzer_id  + " del observable " + artifact['data'] + " del caso " + case_id 
                        Logging("[INFO]",msg)
                        
                        if analyzer_id == "VirusTotal_GetReport_3_0":
                            sleep(25)                        

                    else:
                        msg = "Ocurrió un error al intetar correr el análisis " + analyzer_id  + " del observable " + artifact['data'] + " del caso " + case_id
                        Logging("[ERROR]",msg)

    except CaseException as e:
        msg = "Ocurrió fallo al intentar crear caso para la alerta con id: " + alert['id']
        Logging("[ERROR]",msg)

else:
    Logging("[ERROR]","Tu petición para listar las alertas falló")
