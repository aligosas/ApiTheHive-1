#!/usr/bin/env python
# -*- codinge: utf-8 -*-

from time import sleep
import json
import sys

# Config File
import ApiConfig as cfg

#Api Connections
from ApiConnections import *

#Modules Import
from Modules import *

Logging("[INFO]","Comienza la ejecución del script")

cortex_id = cfg.ApiConfig["CortexId"]

if len(sys.argv) == 2:
    f = open(sys.argv[1])
    timestamp = f.read()

else:
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
            #print ("alert",alert)

            for artifact in artifacts:
                artifact_id = CreateCaseObservable(artifact, case_id, case_title)
                analyzers = SearchAnalyzers(artifact['dataType'])

                flag = 0
                analysis_score = 0
                for analyzer in analyzers:
                    analyzer_id = analyzer.analyzerDefinitionId
                    response = apiH.run_analyzer(cortex_id, artifact_id, analyzer_id)

                                          
                    #Memoria para conocer ultima alerta procesada
                    fecha = alert["createdAt"]
                    f2 = open("fecha.txt","w")
                    f2.write(str(fecha))
                    f2.close()

                    if response.status_code == 200:
                        msg = "Se lanzó el análisis " + analyzer_id  + " al observable " + artifact['data'] + " del caso " + case_id
                        Logging("[INFO]",msg)
                        sleep(10)


                        try:

                            job_id = response.json()['cortexJobId']
                            report = GetReport(job_id)
                            score = report['summary']['taxonomies'][0]['value']
                            report_response = AnalyzeReport(score, analyzer_id)
                            #print ("report", report)
                            #print ("score", score)
                            #print ("rep response", report_response)
                            analysis_score += int(report_response)
                            
                        except:

                            msg = "La ejecución del análisis falló, probablemente se cumplió el máximo número de análisis del " + analyzer_id
                            Logging("[ERROR]",msg)

                        if report_response == 0 or report_response == "0":
                                flag += 1
                                #print ("flag",flag)
                        #else:
                            #print ("flag no es cero",flag)

                    else:
                        msg = "Ocurrió un error al intetar correr el análisis " + analyzer_id  + " del observable " + artifact['data'] + " del caso " + case_id
                        Logging("[ERROR]",msg)

                alert_type = alert["tags"][1]
                #print ("alert_typeee", alert_type)
                if analysis_score >= 5 and flag <= 1:
                    SendNotification(analysis_score, artifact['dataType'], artifact['data'], alert_type)

    except CaseException as e:
        msg = "Ocurrió fallo al intentar crear caso para la alerta con id: " + alert['id']
        Logging("[ERROR]",msg)

else:
    Logging("[ERROR]","Tu petición para listar las alertas falló")

