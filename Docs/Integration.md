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
| CORTEX-ID  | Nombre de identificación del servidor de Cortex, esto es importante dado que es un parametro que se debe pasar para correr análisis  |
| url  | URL del servidor de Cortex  | 
| key  | ApiKey de Cortex  |

La ApiKey de Cortex la encontramos ingresando al portal e iniciando sesión con el usuario administrador, luego de esto se debe ingresar a la pestaña `Users` dar clic en **Reveal** en el usuario orgadmin, dado que el usuario administrador no puede ejecutar analizadores, solo gestionar usuarios. El resultado debe ser algo similar a esto (La Api Key está subrayada en amarillo}:

![apikyc](https://user-images.githubusercontent.com/79227109/108570932-f8f35400-72dc-11eb-961e-c732b25ff955.PNG)

### Ejemplo de configuración:
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

## Integración de TheHive y MISP
La integración de estos dos softwares nos permitirá publicar observables en MISP desde TheHive y viceversa.

Para realizar la integración de estas dos herramientas solo es necesario agregar la siguiente configuración al archivo de configuración de TheHive, generalmente este archivo se encuentra en `/etc/thehive/applications.conf`:

```
play.modules.enabled += connectors.misp.MispConnector

misp {
  interval = 10m
  "<MISP-ID>" {
  url = "<misp-url>:<misp-port>"
  key = "<misp-apikey>"
  max-attributes = 1000
  max-size = 1 MiB
  max-age = 7 days
  }
}
```

Para realizar una integración exitosa, es necesario entender el significado de los siguientes parametros:

| Parametro | Descripción |
| ------------- | ------------- |
| interval  | Intervalo de tiempo entra la importación de 2 eventos  |
| MISP-ID  | Nombre de identificación del servidor de MISP, esto es importante dado que es un parametro que se debe pasar para correr análisis  |
| url  | URL del servidor de MISP  | 
| key  | ApiKey de MISP  |
| max-attributes  | Máximo número de atributos de los eventos importados  |
| max-size | Tamaño máximo del JSON del evento |
| max-age | Valor de la última fecha de publicación, en el caso de ejemplo se tiene configurado que importe los eventos de hacer **7 días** |

La ApiKey de MISP la encontramos ingresando al portal e iniciando sesión con el usuario administrador, luego de esto se debe ingresar a la pestaña `Administration/List users`. para tomar la ApiKey de algún usuario, debemos dar clic en el simbolo del **ojo**. El resultado debe ser algo similar a esto (La Api Key está subrayada en amarillo}:

![MISP apik](https://user-images.githubusercontent.com/79227109/108774500-bbd1d080-752d-11eb-8166-13dfff856633.PNG)

### Ejemplo de configuración:
En el siguiente ejemplo se muestra la integración de un servidor de MISP que se encuentra instalado en el mismo host que se encuentra el TheHive:

```
play.modules.enabled += connectors.misp.MispConnector

misp {
  interval = 10m
  "<MISP-ALIGO>" {
  url = "https://127.0.0.1:8443"
  key = "7RztDXL3dqUnFhZCMV7RzxTl1HAuDQbBMon90hxf"
  max-attributes = 1000
  max-size = 1 MiB
  max-age = 7 days
  }
}
```

### Error en la integración:
Aún siguiendo de manera correcta los pasos descritos anteriormente en esta guía, al iniciar sesión en TheHive e ir a la pestaña `Administrator/About` nos encontraremos que la integración falló, el error debe verse de la siguiente manera:

<p align="center" width="100%">
    <img width="50%" src="https://user-images.githubusercontent.com/79227109/108775980-c725fb80-752f-11eb-9252-68c3742ccf33.PNG"> 
</p>
