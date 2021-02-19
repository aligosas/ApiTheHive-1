# Creación de reglas ElastAlert
Para el reenvío de alertas del XOC a nuestra plataforma se utiliza la herramienta **ElastAlert Kibana Plugin** que es capaz de consumir la Api de TheHive, este plugin nos perimite la creación de reglas para obtener eventos por indice especifico que se encuentran almacenados en **ElasticSearch**.

Antes de intentar crear una regla ElastAlert que consuma la Api de TheHive se requiere tener claro los siguientes parametros:

| Parametro | Descripción |
| ------------- | ------------- |
| es_host  | Hostname del servidor en el que se encuentra el servicio elasticsearch  |
| es_port  | Puerto por el cual se consume el servicio elasticsearch  | 
| name  | Nombre de nuestra regla de ElastAlert  |
| type  | preguntar | 
| index  | Index de los eventos que nos interesa reenviar a la plataforma de TheHive  |
| filter  | Contenido de la celda  | 
| hive_connection  | Parametros necesarios para la conexión con la Api de TheHive |
| hive_alert_config  | Estructura de las alertas que se crearan en TheHive  | 
| hive_observable_data_mapping  | Asignación de los observables, es decir la información que requiere ser analizada  | 

Para crear una regla ElastAlert se debe ingresar al Dashboard de Kibana y en el menu de opciones buscamos el plugin llamado **ElastAlert**, se debe observar algo similar a la imagen, damos clic en **Create Rule**:

![ElastAlert](https://user-images.githubusercontent.com/79227109/108474622-9e66e300-725d-11eb-88d7-7aad32227ce8.PNG)

### Ejemplo de creación de regla ElastAlert:


```
es_host: elasticsearch
es_port: 9200
name: thehive_fortiweb
type: frequency
index: fortiweb-*
num_events: 1
timeframe:
    seconds: 20
    #minutes: 5
filter:
- query:
    query_string:
      query: "attack_type: SQL Injection"
alert: hivealerter
hive_connection:
  hive_host: http://192.168.100.105
  hive_port: 9002
  hive_apikey: RUFwC9kuj3Dc4OCtBxoOnzn93jjoXbTI

hive_alert_config:
  type: 'external'
  source: 'elastalert'
  description: '{rule[name]}'
  severity: 2
  tags: ['{rule[name]}', '{match[attack_type]}', '{match[src_ip]}']
  tlp: 3
  status: 'New'
  follow: True

hive_observable_data_mapping:
    - ip: "{match[src_ip]}"
```
