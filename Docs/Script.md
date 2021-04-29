# Script XOAR:

El script de inteligencia de amenazas se compone de cuatro archivos archivos *.py*, la mayoría de estos son archivos de configuración. El archivo principal, es el archivo **TheHive.py**. A continuación se realiza una explicación de cada uno de estos archivos.

## ApiConfig

El archivo ApiConfig contiene información importante para el correcto funcionamiento del script, en este archivo se encuentran las claves de ambas Apis (TheHive y Cortex), además el CORTEX-ID que tengamos configurado en nuestra infraestructura, este ultimo es necesario para la ejecución de los análisis.

| Parametro | Descripción |
| ------------- | ------------- |
| TheHiveHost  | Host sobre el cual está corriendo TheHive. |
| TheHivePort  | Puerto sobre el cual corre TheHive. | 
| TheHiveApiKey  | ApiKey de TheHive, sin está el servidor nos denegará las peticiones. |
| CortexHost  | Host sobre el cual está corriendo TheHive. |
| CortexPort  | Puerto sobre el cual corre TheHive. | 
| CortexApiKey  | ApiKey de Cortex. |
| CortexId  | Identificador del CORTEX que se encuentra instalado en nuestro equipo. |

A continuación se muestra un ejemplo de configuración del script para una infraestructura en la cual TheHive y Cortex corren sobre la misma maquina que se corre el script. Además, TheHive corre sobre el puerto 9002 y Cortex sobre el 9001, `ApiConfig.py`:

```
ApiConfig = {
    "TheHiveHost": "http://localhost",
    "TheHivePort": "9002",
    "TheHiveApiKey": "FejzI7LCwqljhIiNjEEqbggVdB0yeO0A",
    "CortexHost": "http://localhost",
    "CortexPort": "9001",
    "CortexApiKey": "FXILcJUVKeX5fyniu9ViHTK0tzeVQK4y",
    "CortexId": "CORTEX-SERVER"
}
```

## ApiConnections

Este archivo es utilizado para importar todas las funciones que serán utilizadas en el script, además de generar la conexión con las APIs.

`ApiConnections.py`:

```
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
from cortex4py.query import *

#APIs Connection
hiveServer = cfg.ApiConfig["TheHiveHost"] + ":" + cfg.ApiConfig["TheHivePort"]
hiveKey = cfg.ApiConfig["TheHiveApiKey"]
apiH = TheHiveApi(hiveServer, hiveKey)

cortexServer = cfg.ApiConfig["CortexHost"] + ":" + cfg.ApiConfig["CortexPort"]
cortexKey = cfg.ApiConfig["CortexApiKey"]
apiC = Api(cortexServer, cortexKey)
```

## Modules

En este archivo se encuentran creadas todas las funciones propias que son usadas por el script *TheHive.py*, a continuación se muestra una breve descripción de cada función:

| Función | Descripción |
| ------------- | ------------- |
| Filter  | Se encarga de realizar un filtrado inicial, en el cual se busca no escanear una misma IP repetidamente. |
| CreateCase  | Se crea una caso y se asocia la alerta a este. | 
| CreateCaseObservable  | Se asocian los observables (Ips, dominions) contenidos dentro de las alertas. |
| SearchAnalyzers  | La función busca que analizadores pueden correrle un análisis al observable en cuestión. |
| Logging  | Función encargada de crear los logs, estos son creados en *ApiTheHive.log* | 
| GetReport  | Obtiene los reportes de los análisis que fueron corridos. |
| AnalyzeReport  | Analiza los reportes obtenidos y determina si el observable representa un riesgo. |
| SendNotification  | Envia las notificaciones a Telegram. |

`Modules.py`:

```
#Api Connections
from ApiConnections import *

def Filter(alerts):

    filtered_alerts = []
    artifacts = []

    for alert in alerts:

        for artifact in alert['artifacts']:
            if not artifact['data'] in artifacts:
                artifacts.append(artifact['data'])
                filtered_alerts.append(alert)

    msg = "Se realizó el filtrado. De " +  str(len(alerts)) + " alertas se crearon " + str(len(filtered_alerts)) + " casos, los demás observables se encuentran repetidos"
    Logging("[INFO]",msg)

    return filtered_alerts

def CreateCase(alert):
 
    tasks = [
        CaseTask(title='Revisión', status='Waiting', flag=True)
    ]

    customFields = CustomFieldHelper()\
        .add_boolean('booleanField', True)\
        .add_string('businessImpact', 'HIGH')\
        .add_date('occurDate', int(time.time())*1000)\
        .add_number('cvss', 9)\
        .build()

    artifacts = ""
    for artifact in alert['artifacts']:
        artifacts += "*" + artifact['data'] + "* " 

    title_case = alert['id']
    case = Case(title=title_case,
                tlp=3,
                flag=True,
                tags=['TheHive4Py', artifacts],
                description='N/A',
                tasks=tasks,
                customFields=customFields)

    case_id = None
    response = apiH.create_case(case)

    if response.status_code == 201:
        case_id = response.json()['id']
        case_number = response.json()['caseId']
        case_title = response.json()['title']
        msg = "Se creó correctamente el caso numero " +  str(case_number) + " con id " + case_id
        Logging("[INFO]",msg)

    else:
        Logging("[ERROR]","No fue posible crear el caso, la Api falló")

    return case_id, case_title

def CreateCaseObservable(artifact, case_id, case_title):

    try:
        caseObservable = CaseObservable(dataType=artifact['dataType'],
                                data=artifact['data'],
                                tlp=artifact['tlp'],
                                ioc=artifact['ioc'],
                                tags=artifact['tags'],
                                message=artifact['message']
                                )

    except KeyError as e:
        caseObservable = CaseObservable(dataType=artifact['dataType'],
                                data=artifact['data'],
                                tlp=artifact['tlp'],
                                ioc=False,
                                tags=artifact['tags'],
                                message=artifact['message']
                                )

    response = apiH.create_case_observable(case_id, caseObservable)

    if response.status_code == 201:

        artifact_id = response.json()['id']
        msg = "Se asoció correctamente el observable " + artifact['data'] + " con el caso " + case_title
        Logging("[INFO]",msg)
        return artifact_id

    else:

        msg = "No fue posible crear el observable para el caso " + case_title + ", la Api falló"
        Logging("[ERROR]",msg)
        return None

def SearchAnalyzers(data_type):

    analyzers = apiC.analyzers.get_by_type(data_type)
    return analyzers

def Logging(title, message):

    date = time.strftime("%a %d-%m-%y %H:%M:%S")
    LogFile = open("ApiTheHive.log", "a+")
    Log = "ApiTheHive: " + date + " " + title + " " + message
    print(Log)
    LogFile.write(Log + "\n")
    LogFile.close()

def GetReport(job_id):

    job = apiC.jobs.get_by_id(job_id)

    if job.json()['status'] == "Success":

        report = apiC.jobs.get_report(job.id).report
        msg = "Se corrió el análisis correctamente, status: " + job.json()['status'] + ", obteniendo reporte para el análisis"
        Logging("[INFO]",msg)
        return report

    else:
     
        msg = "El análisis que se intentaba correr falló, se recomienda validar que la configuración de Cortex se encuentre bien"
        Logging("[ERROR]",msg)
        return None

def AnalyzeReport(score, analyzer):

    if analyzer == 'VirusTotal_GetReport_3_0':
        
        score = score.split()[0]
        return score

    elif analyzer == 'OTXQuery_2_0':
    
        return score

    elif analyzer == 'DShield_lookup_1_0':

        score = score.split()
        score = int(score[0]) + int(score[3]) + int(score[6]) 
        return score        

    else:
 
        msg = "El analizador " + analyzer + " todavía no cuenta con un método para el análisis de sus reportes"
        Logging("[ERROR]",msg)


def SendNotification(analysis_score, dataType, observable):

    BOT_TOKEN="1628114474:AAHO9LvKHts2wTKAn2LR0LQPtVfqaW0iYqs"
    URL="https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    GROUP_ID="-552607247"
    MENSAJE="[Linea Directa][XOAR]: Se han detectado comportamientos sospechosos provenientes de la " + dataType + " " +  observable + ", la " + dataType + " se encuentra reportada por " + str(analysis_score) + " motores."
    TEXT = "curl -s -X POST "  + URL + " -d chat_id=" + GROUP_ID + " -d text=\""
    TEXT2 = "\" > /dev/null"

    cmd =   TEXT + MENSAJE + TEXT2
    os.system(cmd)

    msg = "Enviando notificación a Telegram"
    Logging("[INFO]",msg)
```

## TheHive

Es el Core principal del script, se encarga de darle el flujo necesario a todas las funciones que se encuentran creadas.

#### Diagrama de flujo:

![0_0](https://user-images.githubusercontent.com/79227109/116622173-e2373200-a909-11eb-93ac-6622abcc8039.png)

`TheHive.py`:

```
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
from cortex4py.query import *

#APIs Connection
hiveServer = cfg.ApiConfig["TheHiveHost"] + ":" + cfg.ApiConfig["TheHivePort"]
hiveKey = cfg.ApiConfig["TheHiveApiKey"]
apiH = TheHiveApi(hiveServer, hiveKey)

cortexServer = cfg.ApiConfig["CortexHost"] + ":" + cfg.ApiConfig["CortexPort"]
cortexKey = cfg.ApiConfig["CortexApiKey"]
apiC = Api(cortexServer, cortexKey)
```
