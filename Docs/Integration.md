![DsDNPtzWkAAQ7zy](https://user-images.githubusercontent.com/79227109/108568667-7bc5e000-72d8-11eb-87f3-5b9ab7a91ecd.png)

# Integración de las herramientas
Junto con MISP, Cortex es el compañero perfecto para TheHive. TheHive le permite analizar decenas o cientos de observables en unos pocos clics aprovechando una o varias instancias de Cortex según sus necesidades de OPSEC y requisitos de rendimiento. Además, TheHive viene con un motor de plantillas de informes que le permite ajustar la salida de los analizadores Cortex a su gusto en lugar de tener que crear sus propios analizadores JSON para la salida Cortex.

## Integración de TheHive y Cortex
Uniendo las herramientas TheHive y Cortex podemos tener una plataforma de gestión de incidentes de seguridad que pueda ejecutar análisis y obtener los reportes de estos de una forma sencilla consumiendo los analizadores que nos provee Cortex, además de esto podemos crear respuestas a los resultados de los análisis, esto se logra con los responders que también nos provee este software.

Para realizar la integración de estas dos herramientas solo es necesario agregar la siguiente configuración al archivo de configuración de TheHive, generalmente este archivo se encuentra en `/etc/thehive/applications.conf`:

```
play.modules.enabled += connectors.cortex.CortexConnector

cortex {
  "<CORTEX-ID>" {
  url = "<cortex-url>:<cortex-port>"
  key = "<cortex-apikey>"
  }
}
```

Para realizar una integración exitosa, es necesario entender el significado de los siguientes parametros:

| Parametro | Descripción |
| ------------- | ------------- |
| CORTEX-ID  | Nombre de identificación del servidor de cortex, esto es importante dado que es un parametro que se debe pasar para correr análisis.  |
| url  | URL del servidor de cortex  | 
| key  | ApiKey de Cortex  |

La ApiKey de Cortex la encontramos ingresando al portal e iniciando sesión con el usuario administrador, luego de esto se debe ingresar a la pestaña `Users` dar clic en **Reveal** en el usuario orgadmin, dado que el usuario administrador no puede ejecutar analizadores, solo gestionar usuarios. El resultado debe ser algo similar a esto:

![apikyc](https://user-images.githubusercontent.com/79227109/108570932-f8f35400-72dc-11eb-961e-c732b25ff955.PNG)
