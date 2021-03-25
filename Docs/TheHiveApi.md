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

Dónde <fecha>, en formato timestamp, es el dato utilizado como criterio para la toma de las alertas, la función <Gte> se encarga  de tomar las alertas en las que la fecha sea mayor a <fecha>. Se toman todas las alertas que cumplan con la consulta indicada, en orden descendente.

En este link se encuentra una explicación de las demás consultas que pueden ser utilizadas: [Consultas de TheHive4py](https://thehive-project.github.io/TheHive4py/reference/query/)
