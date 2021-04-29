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

Para realizar una integración exitosa, es necesario entender el significado de los siguientes parametros:

| Parametro | Descripción |
| ------------- | ------------- |
| CORTEX-ID  | Nombre de identificación del servidor de Cortex, esto es importante dado que es un parametro que se debe pasar para correr análisis  |
| url  | URL del servidor de Cortex  | 
| key  | ApiKey de Cortex  |

La ApiKey de Cortex la encontramos ingresando al portal e iniciando sesión con el usuario administrador, luego de esto se debe ingresar a la pestaña `Users` dar clic en **Reveal** en el usuario orgadmin, dado que el usuario administrador no puede ejecutar analizadores, solo gestionar usuarios. El resultado debe ser algo similar a esto (La Api Key está subrayada en amarillo}:

![apikyc](https://user-images.githubusercontent.com/79227109/108570932-f8f35400-72dc-11eb-961e-c732b25ff955.PNG)

#### Ejemplo de configuración:
En el siguiente ejemplo se muestra la integración de un servidor de Cortex que se encuentra instalado en el mismo host que se encuentra el TheHive:

```
play.modules.enabled += connectors.cortex.CortexConnector

cortex {
  "CORTEX-ALIGO" {
  url = "http://127.0.0.1:9001"
  key = "59kn3AMItpJEouvqKgP8PkzpQfSAmUBn"
  }
}
```

Es necesario reiniciar el servicio de TheHive, usando el comando: `service thehive restart`.
