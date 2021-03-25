![68747470733a2f2f746865686976652d70726f6a6563742e6f72672f696d672f6c6f676f2e706e67](https://user-images.githubusercontent.com/79227109/112504054-6c173c80-8d59-11eb-846c-331494e11b03.png)

# Metodos TheHive4py

### 1. Find Alerts: 

Este método es utilizado para traer las alertas que se están enviando a TheHive, esto con el fin de trabajar con base a estas, la estructura del método es la siguiente: `find_alerts(query=query, sort=['-createdAt'], range='all')`

| Parámetro | Descripción |
| ------------- | ------------- |
| query  | Consulta utilizada para traer alertas en especifico, es decir que cumplan con ciertas condiciones  |
| sort  | Lista de campos para ordenar el resultado. Prefije el nombre del campo con `-` para orden descendente y `+` para orden ascendente  | 
| range | Un rango que describe el número de filas que se devolverán.  |

#### Ejemplo:

```
query = Gte('date', fecha)
response = apiH.find_alerts(query=query, sort=['-createdAt'], range='all')
```

Dónde **fecha**, en formato timestamp, es el dato utilizado como criterio para la toma de las alertas, la función <Gte> se encarga  de tomar las alertas en las que la fecha sea mayor a **fecha**. Se toman todas las alertas que cumplan con la consulta indicada, en orden descendente.

En este link se encuentra una explicación de las demás consultas que pueden ser utilizadas: [Consultas de TheHive4py](https://thehive-project.github.io/TheHive4py/reference/query/)

### 2. Create Case: 

Este método es utilizado para crear casos y posteriormente asociar los observables de las alertas con estos, con el fin de poder correr análisis sobre los observables contenidos dentro de estas, la sintaxis de este metodo es el siguiente: `create_case(case)`.Al metodo se le debe enviar un objeto tipo Case (La construcción del caso), el cuál requiere los siguientes parametros:

#### Tareas:

Para crear un caso, primero es necesario definir las tareas que este contiene, se entiende como tarea la labor que debe realizar el analista con base a la alerta recibida.

```
tasks = [ 
        CaseTask(title=<titulo de la tarea>, status=<Estado de la tarea: (Waiting, Done)>, flag=True)
        ]
```

Un buen ejemplo para la creación de esta puede ser:

```
tasks = [ 
        CaseTask(title='Revisión', status='Waiting', flag=True)
        ]
```

#### Campos personalizados:

En este apartado se crean otros campos personalizados, que no son tan relevantes, en estos campos se configura la relevancia del caso y la fecha en la que este fue creado, perfectamente se puede dejar la variable configurada de la siguiente manera:

```
customFields = CustomFieldHelper()\
              .add_boolean('booleanField', True)\
              .add_string('businessImpact', 'HIGH')\
              .add_date('occurDate', int(time.time())*1000)\
              .add_number('cvss', 9)\
              .build()
```

#### Objeto Case:

El objeto Case se encarga de realizar la construcción del Caso, relaciona la tarea anteriormente configurada y rellena los campos personalizados, con esto ya se tiene un caso, sin embargo no asocia el caso a la alerta u observables.

```
case = Case(title=title_case,
        tlp=3,
        flag=True,
        tags=['TheHive4Py'],
        description='N/A',
        tasks=tasks,
        customFields=customFields)
```

#### Ejemplo:

```
tasks = [
        CaseTask(title='Revisión', status='Waiting', flag=True)
]

customFields = CustomFieldHelper()\
        .add_boolean('booleanField', True)\
        .add_string('businessImpact', 'HIGH')\
         .add_date('occurDate', int(time.time())*1000)\
        .add_number('cvss', 9)\
        .build()

case = Case(title='Caso de prueba',
        tlp=3,
        flag=True,
        tags=['TheHive4Py', artifacts],
        description='N/A',
        tasks=tasks,
        customFields=customFields)

response = apiH.create_case(case)
```

### 3. Create Case Observable: 

Para asociar el caso creado anteriormente con los observables contenidos en las alertas recibidas es necesario utilizar este método, la sintaxis del metodo es la siguiente: `create_case_observable(case_id, caseObservable)`, a este metodo es necesario enviarle los siguientes dos parametros:

| Parámetro | Descripción |
| ------------- | ------------- |
| Case id  | ID del caso creado anteriormente, a este caso se asociarán los observables contenidos en las alertas  |
| Case observable | Para asociar los observables con un caso es necesario definir un objeto caseObservable.  | 

#### Objeto caseObservable:

En este objeto simplemente se rellenan algunos campos para la asociación del observable, los datos más relevantes son el tipo y el contenido del observable (ip, dominio, hash, archivo, entre otros.) 

```
caseObservable = CaseObservable(dataType=<Tipo de dato>,
                                data=<Obserbable>,
                                tlp=<tlp>,
                                ioc=<¿El dato es un ioc? True o False>,
                                tags=<Etiquetas>,
                                message=<Mensaje>
                                )
```


#### Ejemplo:

En el siguiente ejemplo se observa la forma para relacionar un observable con un caso creado anteriormente, a la función de la api es necesario enviarle como parametros el objeto caseObservable creado y el id del caso al cuál se le asignará el observable.

```
caseObservable = CaseObservable(dataType='ip',
                                data='8.8.8.8',
                                tlp=3,
                                ioc=False,
                                tags='Dominio malicioso',
                                message='Mensaje de prueba'
                                )
                                
response = apiH.create_case_observable(case_id, caseObservable)
```
