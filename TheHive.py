#!/usr/bin/env python
# -*- codinge: utf-8 -*-

import json

# Config File
import ApiConfig as cfg

#Api Connections
from ApiConnections import *

#Modules Import 
from Modules import *

Logging("[INFO]","Comienza la ejecución del script")

cortex_id = cfg.ApiConfig["CortexId"]

response = apiH.find_alerts(sort=['-createdAt'], range='all')
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
                    response_json = response.json()
		    
                    if response.status_code == 200:
                        msg = "Se corrió correctamente el análisis " + analyzer_id  + " del observable " + artifact['data'] + " del caso " + case_id 
                        Logging("[INFO]",msg)

                    else:
                        msg = "Ocurrió un error al intetar correr el análisis " + analyzer_id  + " del observable " + artifact['data'] + " del caso " + case_id
                        Logging("[ERROR]",msg)

    except CaseException as e:
        msg = "Ocurrió fallo al intentar crear caso para la alerta con id: " + alert['id']
        Logging("[ERROR]",msg)

else:
    Logging("[ERROR]","Tu petición para listar las alertas falló")
