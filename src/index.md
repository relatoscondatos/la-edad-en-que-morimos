---
sql:
  defuncionesPorComuna: data/defuncionesPorComuna.parquet
  defuncionesChilePorEdad: data/defuncionesChilePorEdad.parquet
  defuncionesPorComunaEdad: data/defuncionesPorComunaEdad.parquet
  statsPorComuna: data/percentilesPorComuna.parquet
---

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">


## Distribución de defunciones en Chile (2013 a 2024)


```sql id=dataDefuncionesChilePorEdad
SELECT *
FROM defuncionesChilePorEdad  
```

```js
import {buildDistChart} from "./components/distributionChart.js";
```


```js
buildDistChart(dataDefuncionesChilePorEdad)
```

## Defunciones por comuna

```js
const comuna = view(Inputs.select(_.map(dataComunas.toArray(),d => d.comuna), { label: "Comuna"}));
```

```js
const dataComuna = _.chain([...dataDefuncionesPorComunaEdad])
      .filter((d) => d.comuna == comuna)
      .sortBy((d) => d.edad)
      .value()
```

```sql id=dataStataPorComuna display
SELECT *
FROM statsPorComuna 
WHERE comuna = ${comuna}
```


```js
buildDistChart(dataComuna)
```

```js
Inputs.table(dataComuna)
```

```sql id=dataDefuncionesPorComunaEdad
SELECT *
FROM defuncionesPorComunaEdad  

```

```sql id=dataComunas
SELECT DISTINCT comuna
FROM statsPorComuna  
WHERE n >= 1000
ORDER BY comuna
```


```sql id=dataDefuncionesPorComuna
SELECT *
FROM defuncionesPorComuna  
ORDER BY defunciones DESC
```







```js
function getCurve(options) {
  const comuna = (options && options.comuna) || "Chile";
  const sexo = (options && options.sexo) || null;

  if (false) {

  } else {
    return _.chain([...dataDefuncionesPorComunaEdad])
      .filter((d) => d.comuna == comuna)
      .sortBy((d) => d.edad)
      .value();
  }
}
````

```js
function buildChartCurve(options) {
  const comuna = (options && options.comuna) || "Chile";
  const sexo = (options && options.sexo) || null;
  const mark = (options && options.mark) || null;
  const title = (options && options.title) || comuna;
  const subtitle = (options && options.subtitle) || null;

  const dataPlot = getCurve({ comuna: comuna, sexo: sexo });

  const max = _.chain(dataPlot)
    .map((d) => d.defunciones)
    .max()
    .value();


 

  return Plot.plot({
    title,
    subtitle,
    marginLeft: 50,
    marks: [
      ,
      Plot.areaY(dataPlot, {
        x: "edad",
        y: "defunciones",
        fill: (d) => "curva",
        opacity: 1
      }),
    ]
  });
}
```