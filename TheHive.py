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

ReportFile = open("Report.log", "a+")

#date = datetime.datetime.now()
#date = date.strftime("%d/%m/%Y %H:%M:%S")
date = "09/01/2021 15:24:00"
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
            case_id, case_title = CreateCase(alert)
            artifacts = alert['artifacts']

            for artifact in artifacts:
                artifact_id = CreateCaseObservable(artifact, case_id, case_title)
                analyzers = SearchAnalyzers(artifact['dataType'])
                ReportFile.write("Observable: " + artifact['data'] + "\n")
                    
                for analyzer in analyzers:
                    analyzer_id = analyzer.analyzerDefinitionId
                    response = apiH.run_analyzer(cortex_id, artifact_id, analyzer_id)

                    job_id = response.json()['cortexJobId']

                    if response.status_code == 200:
                        msg = "Se lanzó el análisis " + analyzer_id  + " al observable " + artifact['data'] + " del caso " + case_id 
                        Logging("[INFO]",msg)
                        sleep(10)

                        report = GetReport(job_id)
                        try:
                            ReportFile.write(analyzer_id + ": " + report['summary']['taxonomies'][0]['value']  + "\n")
                        except:
                            ReportFile.write("Falló el análisis \n")

                    else:
                        msg = "Ocurrió un error al intetar correr el análisis " + analyzer_id  + " del observable " + artifact['data'] + " del caso " + case_id
                        Logging("[ERROR]",msg)

                    ReportFile.write("\n")

    except CaseException as e:
        msg = "Ocurrió fallo al intentar crear caso para la alerta con id: " + alert['id']
        Logging("[ERROR]",msg)

else:
    Logging("[ERROR]","Tu petición para listar las alertas falló")

ReportFile.close()
