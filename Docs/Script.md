# Script XOAR:

El script de inteligencia de amenazas se compone de cuatro archivos archivos *.py*, la mayoría de estos son archivos de configuración y un archivo txt. El archivo principal, es el archivo **TheHive.py**. A continuación se realiza una explicación de cada uno de estos archivos.

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

## Fecha.txt
Es el archivo de texto en el cual se almacena la fecha de la ultima alerta que fue procesada. Esto con el objetivo de que en la próxima ejecución del script se procesen únicamente las alertas cuya fecha de creación es igual o mayor a la almacenada. Cabe resaltar que dicho archivo se actualiza cada vez que se ejecuta el script. 

## TheHive

Es el Core principal del script, se encarga de darle el flujo necesario a todas las funciones que se encuentran creadas.

#### Diagrama de flujo:
![diagrama-Page-2 drawio](https://user-images.githubusercontent.com/57953380/139280555-01778a1a-2421-47b2-bbfe-8db1521f64f1.png)

#### Logging:
Los logs se ven de la siguiente manera durante la ejecución del script:
![Captura](https://user-images.githubusercontent.com/79227109/116623460-e2d0c800-a90b-11eb-9b22-d746e2e3d9b8.PNG)

### Crontab task
Para la ejecución automática del script se definió una tarea de crontab que se ejecute cada 30 minutos, con el ánimo de procesar las nuevas alertas que llegan a TheHive en este rango de tiempo. 
Ejecutando el comando ````crontab -e ```` es posible editar el archivo donde se programan las tareas. 
![image](https://user-images.githubusercontent.com/57953380/139323623-9ae0e1b4-dc6c-46ef-b265-ac97ba70393a.png)
Nota: para editar archivos en vim se presiona la tecla "Insert" y para salir "Esc :wq!"
