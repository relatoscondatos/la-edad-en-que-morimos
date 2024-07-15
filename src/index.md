---
sql:
  defuncionesPorComuna: data/defuncionesPorComuna.parquet
  defuncionesChilePorEdad: data/defuncionesChilePorEdad.parquet
  defuncionesPorComunaEdad: data/defuncionesPorComunaEdad.parquet
  statsPorComuna: data/percentilesPorComuna.parquet
---

```js
import {buildDistChart} from "./components/distributionChart.js";
```

## A qué edad muere la gente en Chile
### En base a datos de 2014 a 2023


```sql id=dataDefuncionesChilePorEdad
SELECT *
FROM defuncionesChilePorEdad  
```

```sql id=[statsChile] display
SELECT *
FROM statsPorComuna 
WHERE comuna = 'Chile'
```

```js
const maxChile = _.chain(dataDefuncionesChilePorEdad.toArray()).map(d => d.edad).value()
```

```js
_.chain(dataDefuncionesChilePorEdad.toArray()).map(d => d.defunciones).max().value()
```


```js
buildChartCurve2(dataDefuncionesChilePorEdad.toArray(),{
  p50:statsChile.p50, 
  p25:statsChile.p25, 
  p75:statsChile.p75, 
  max:maxChile,
  mark:null

  })
```

```js
buildChartCurve2(dataDefuncionesChilePorEdad.toArray(),{
  p50:statsChile.p50, 
  p25:statsChile.p25, 
  p75:statsChile.p75, 
  max:maxChile,
  mark:"median"

  })
```

```js
buildChartCurve2(dataDefuncionesChilePorEdad.toArray(),{
  p50:statsChile.p50, 
  p25:statsChile.p25, 
  p75:statsChile.p75, 
  max:maxChile,
    mark:"quartiles"

  })
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

```sql id=[statsComuna]
SELECT *
FROM statsPorComuna 
WHERE comuna = ${comuna}
```


```js
buildChartCurve2(dataComuna,{
  p50:statsComuna.p50,
  p25:statsComuna.p25,
  p75:statsComuna.p75,
  max:maxChile,
  mark:"quartiles"
  })
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
```

```js
function buildChartCurve(data,options) {
  const comuna = (options && options.comuna) || "Chile";
  const sexo = (options && options.sexo) || null;
  const p50 = (options && options.p50) || null;
  const title = (options && options.title) || comuna;
  const subtitle = (options && options.subtitle) || null;

  const dataPlot = data

  const max = _.chain(dataPlot)
    .map((d) => d.defunciones)
    .max()
    .value();

  return Plot.plot({
    title,
    subtitle,
    marginLeft: 50,
    marks: [
      Plot.areaY(dataPlot, {
        x: "edad",
        y: "defunciones",
        fill: (d) => "curva",
        opacity: 1
      }),      
      Plot.ruleX([p50]),
    ]
  });
}
```

```js
function buildChartCurve2(data,options) {
  const comuna = (options && options.comuna) || "Chile";
  const sexo = (options && options.sexo) || null;
  const mark = (options && options.mark) || null;
  const title = (options && options.title) || null;
  const subtitle = (options && options.subtitle) || null;
  const p50 = (options && options.p50) || null;
  const p25 = (options && options.p25) || null;
  const p75 = (options && options.p75) || null;

  const dataPlot = data;

  const maxX = (options && options.max) || _.chain(dataPlot)
    .map((d) => d.edad)
    .max()
    .value();

   const maxY =  _.chain(dataPlot)
    .map((d) => d.defunciones)
    .max()
    .value();;


  
  const data_25_75 = dataPlot.filter(
    (d) => d.edad >= p25 && d.edad <= p75
  );
  

  const medianMark = [
    Plot.ruleX([p50], {stroke:"#DDD", strokeWidth:3}),
    Plot.text([p50], {
      x: (d) => d,
      y: d => maxY,
      dy: -10,
      text: (d) => d,
      fill:"black",
      fontSize: 18

    }),
    Plot.text([p50], {
      x: (d) => d,
      y: 0,
      dy: -15,
      dx: -10,
      text: (d) => "50%",
      textAnchor: "end",
      fontSize: 18,

      fill: "white"
    }),
    Plot.text([p50], {
      x: (d) => d,
      y: 0,
      dy: -15,
      dx: 10,
      text: (d) => "50%",
      textAnchor: "start",
      fontSize: 18,
      fill: "white"
    })
  ];

  const quartilesMark = [
    Plot.areaY(data_25_75, {
      x: "edad",
      y: "defunciones",
      fill: (d) => "intercuartil",
      opacity: 1
    }),

    Plot.ruleX([p25, p50, p75]),
    Plot.text([p25, p50, p75], {
      x: (d) => d,
      y: maxY,
      dy: -10,
      text: (d) => d
    }),
    Plot.text([(p25 + p50) / 2, (p75 + p50) / 2], {
      x: (d) => d,
      y: 0,
      dy: -10,
      text: (d) => "25%",
      fill: "white",
      fontSize: 18
    }),
    Plot.text([p25], {
      x: (d) => d,
      y: 0,
      dy: -10,
      dx: -10,
      text: (d) => "25%",
      textAnchor: "end",
      fill: "white",
      fontSize: 18
    }),
    Plot.text([p75], {
      x: (d) => d,
      y: 0,
      dy: -10,
      dx: 10,
      text: (d) => "25%",
      textAnchor: "start",
      fill: "white",
      fontSize: 18
    })
  ];

  return Plot.plot({
    title,
    subtitle,
    marginLeft: 50,
    x:{domain:[0,120]},
    //color: { range: colorCuartiles },
    marks: [
      Plot.areaY(dataPlot, {
        x: "edad",
        y: "defunciones",
        fill: (d) => "curva",
        opacity: 1
      }),

      mark == "median" ? medianMark  : mark == "quartiles" ? quartilesMark : []
    ]
  });
}
```



```js
import { es_ES } from "./components/config.js";
d3.formatDefaultLocale(es_ES);
```