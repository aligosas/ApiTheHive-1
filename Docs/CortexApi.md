![67854500-2639-11ea-899e-a6db18761db5](https://user-images.githubusercontent.com/79227109/112549684-2d4eaa00-8d8c-11eb-9c6a-7af7bcc117f7.jpg)

# Metodos Cortex4py

### 1. Get analyzers by type: 

Este método es utilizado para saber cuáles de los analizadores que se encuentran configurados en Cortex sirven para analizar el tipo de observable, para esto se debe pasar como parametro al método el tipo de observable (ip, hash, domain, file, entre otros.) La sintaxis es la siguiente: `analyzers.get_by_type(data_type)`

```
analyzers = apiC.analyzers.get_by_type(data_type)
```

#### Ejemplo:

```
analyzers = apiC.analyzers.get_by_type('domain')
```

### 2. Get jobs by id: 

Para Cortex la ejecución de un análisis o un responder es un **job**, Luego de realizar el análisis de los observables es necesario obtener el reporte para poder tomar acciones. La sintaxis es la siguiente: `jobs.get_by_id(job_id)`

```
job = apiC.jobs.get_by_id(job_id)
```

**Nota:** El job_id de un analisis se puede obtener al correr el método **run_analyzer**, el JSON que este retorna contiene un campo llamado **cortexJobId**.

