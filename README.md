![Banner](https://user-images.githubusercontent.com/79227109/108462615-e3cde500-724a-11eb-8748-aa9a99645856.png)

# Inteligencia de amenazas
Una plataforma de inteligencia de amenazas automatiza el procesamiento y análisis de datos de múltiples fuentes mejorando la seguridad de SIEM.  Esto alivia la sobrecarga del personal proporcionándoles un medio eficaz de análisis en tiempo real. De este modo, los equipos de seguridad pueden responder con mayor rapidez y precisión a las amenazas.
 
# Documentación  
Para la contrucción de la plataforma de inteligencia de amenazas se hizo uso de tres softwares open source, estos son: TheHive, Cortex y MISP. Con la integración de estas tecnologías se puede realizar la automatización de la gestión de los incidentes de seguridad, además mejora la confiabilidad y eficiencia de los reportes de amenazas generados para nuestros clientes.

Cada tecnología utilizada en el desarrollo de este proyecto cumple una función especifica para garantizar el correcto funcionamiento del proyecto, TheHive es una plataforma diseñada para facilitar la vida de los SOC, CSIRT, CERT y cualquier profesional de seguridad de la información que se ocupe de incidentes de seguridad que deban ser investigados y tomados medidas. rápidamente. 


![TheHive](https://user-images.githubusercontent.com/79227109/108465251-aae43f00-724f-11eb-8164-927e7af56013.PNG)


Cortex es una herramienta que  permite analizar observables que se han recopilado, a escala, consultando una sola herramienta en lugar de varias, los objetos observables, como direcciones IP y de correo electrónico, URL, nombres de dominio, archivos o hashes, se pueden analizar uno por uno o en modo masivo mediante una interfaz web.


![Cortex](https://user-images.githubusercontent.com/79227109/108465273-b20b4d00-724f-11eb-8c57-6fc07b07ea6b.PNG)


MISP es una plataforma de inteligencia contra amenazas especialmente utilizada para la compartición, almacenaje y correlación de Indicadores de compromiso, persiguiendo tener una comunidad colaborativa sobre amenazas existentes, cuyo objetivo es ayudar a mejorar las contramedidas utilizadas contra los ataques dirigidos y establecer acciones preventivas y de detección.


![MISP](https://user-images.githubusercontent.com/79227109/108465287-b7689780-724f-11eb-890c-0823d30cf19b.PNG)


Junto con MISP, Cortex es el compañero perfecto para TheHive . TheHive le permite analizar decenas o cientos de observables en unos pocos clics aprovechando una o varias instancias de Cortex según sus necesidades de OPSEC y requisitos de rendimiento. Además, TheHive viene con un motor de plantillas de informes que le permite ajustar la salida de los analizadores Cortex a su gusto en lugar de tener que crear sus propios analizadores JSON para la salida Cortex.

TheHive y Cortex cuentan con un cliente API cada uno, ambos son consumidos a través de modulos de python, esto permite la creación de un script que ayude a la automatización ce estas tareas que deben ser ejecutadas por el FronEnd, lo cuál hace que el proceso de gestión de incidentes sea aún más eficientes.

El flujo de trabajo de nuestra plataforma consiste en el reenvío de logs de nuestros controles a TheHive a través de ElastAlert, para este procedimiento lo más importante es la elección de observables que contienen las alertas (Es decir, la información relevante que merece ser analizada), luego de reenviadas las alertas a TheHive se crean casos en los cuales se corren analisis a los observables, esto dependiendo de que tipo de observables sean (Ip, dominio, hash, file) los analizadores utilizados para correr estos analisis son los que se encuentran contenidos en Cortex, todo esto se puede hacer desde TheHive gracias a la posibilidad de integración de estas dos herramientas, basado en los resultados obtenidos en los análisis tenemos la opción de ejecutar **reponders**, un responder es un programa que toma la entrada JSON y realiza una acción y produce un resultado básico de esa acción.  


<p align="center" width="100%">
    <img width="80%" src="https://user-images.githubusercontent.com/79227109/108469498-54c6ca00-7256-11eb-9797-6535ff5d0253.png"> 
</p>

## Guías
- [Documentación de TheHive](https://github.com/TheHive-Project/TheHiveDocs)
- [Documentación de Cortex](https://github.com/TheHive-Project/Cortex)
- [Documentación de MISP](https://www.circl.lu/doc/misp/)
- [Creación de reglas ElastAlert](https://github.com/AligoXOC/ApiTheHive/blob/main/Docs/elastalert.md)
- [Integración TheHive/Cortex/MISP](https://github.com/AligoXOC/ApiTheHive/blob/main/Docs/Integration.md)
- [TheHive API](https://github.com/AligoXOC/ApiTheHive/blob/main/Docs/TheHiveApi.md)
- [Cortex API](https://github.com/AligoXOC/ApiTheHive/blob/main/Docs/CortexApi.md)
- [Script Threat Intelligence](https://github.com/AligoXOC/ApiTheHive/blob/main/Docs/Script.md)
