# Creación de reglas ElastAlert
Para el reenvío de alertas del XOC a la plataforma de ThreatIntelligence utilizamos la herramienta **ElastAlert Kibana Plugin**, esta nos permite crear reglas en las que se configuran diferentes parametros con el fin de enviar alertas especificas, en este caso, se consumirá la Api de TheHive.

Para crear una regla que consuma la Api de TheHive se requiere configurar los siguientes parametros:

<p align="center" width="100%">
| Parametros | Descripción |
| ------------- | ------------- |
| Contenido de la celda  | Contenido de la celda  |
| Contenido de la celda  | Contenido de la celda  | 
</p>


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
