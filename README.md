![Banner](https://user-images.githubusercontent.com/79227109/108462615-e3cde500-724a-11eb-8748-aa9a99645856.png)

# Inteligencia de amenazas
Una plataforma de inteligencia de amenazas automatiza el procesamiento y análisis de datos de múltiples fuentes mejorando la seguridad de SIEM.  Esto alivia la sobrecarga del personal proporcionándoles un medio eficaz de análisis en tiempo real. De este modo, los equipos de seguridad pueden responder con mayor rapidez y precisión a las amenazas.
 
# Documentación  
Para la contrucción de la plataforma de inteligencia de amenazas se hizo uso de tres softwares open source, estos son: TheHive, Cortex y MISP. Con la integración de estas tecnologías se puede realizar la automatización de la gestión de los incidentes de seguridad, además mejora la confiabilidad y eficiencia de los reportes de amenazas generados para nuestros clientes.

Cada tecnología utilizada en el desarrollo de este proyecto cumple una función especifica para garantizar el correcto funcionamiento del proyecto, TheHive es una plataforma diseñada para facilitar la vida de los SOC, CSIRT, CERT y cualquier profesional de seguridad de la información que se ocupe de incidentes de seguridad que deban ser investigados y tomados medidas. rápidamente. 

Cortex es una herramienta que  permite analizar observables que se han recopilado, a escala, consultando una sola herramienta en lugar de varias, los objetos observables, como direcciones IP y de correo electrónico, URL, nombres de dominio, archivos o hashes, se pueden analizar uno por uno o en modo masivo mediante una interfaz web.

MISP es una plataforma de inteligencia contra amenazas especialmente utilizada para la compartición, almacenaje y correlación de Indicadores de compromiso, persiguiendo tener una comunidad colaborativa sobre amenazas existentes, cuyo objetivo es ayudar a mejorar las contramedidas utilizadas contra los ataques dirigidos y establecer acciones preventivas y de detección.

Junto con MISP , Cortex es el compañero perfecto para TheHive . TheHive le permite analizar decenas o cientos de observables en unos pocos clics aprovechando una o varias instancias de Cortex según sus necesidades de OPSEC y requisitos de rendimiento. Además, TheHive viene con un motor de plantillas de informes que le permite ajustar la salida de los analizadores Cortex a su gusto en lugar de tener que crear sus propios analizadores JSON para la salida Cortex.

TheHive y Cortex cuentan con un cliente API, los cuales permiten la ejecución 

```
git status
```

`git status`
