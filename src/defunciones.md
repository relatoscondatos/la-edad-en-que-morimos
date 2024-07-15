---
sql:
  defuncionesPorComuna: data/defuncionesPorComuna.parquet
  defuncionesChilePorEdad: data/defuncionesChilePorEdad.parquet
  defuncionesPorComunaEdad: data/defuncionesPorComunaEdad.parquet
---

## Defunciones (formato fuente)

```sql id=dataDefuncionesChilePorEdad
SELECT *
FROM defuncionesChilePorEdad  
```

```js
buildDistChart(dataDefuncionesChilePorEdad)
```

## Defunciones por comuna

```sql
SELECT *
FROM defuncionesPorComuna  
LIMIT 10
```

## Defunciones por comuna y edad

```sql
SELECT *
FROM defuncionesPorComunaEdad  
LIMIT 10
```

```sql id=dataDefuncionesPorComunaEdad
SELECT *
FROM defuncionesPorComunaEdad  

```

```sql id=dataDefuncionesPorComuna
SELECT *
FROM defuncionesPorComuna  
ORDER BY defunciones DESC
```

<div class="hero2">
  <h1>Distribución de defunciones en Chile</h1>
</div>

<div class="card">${plot1}</div>


```js
display([...dataDefuncionesPorComunaEdad])
```

```js
display(getCurve({comuna:"Las Condes"}))
```
```js
display(buildChartCurve({comuna:"Providencia"}))
```

```js
display(buildChartCurve({comuna:"Las Condes"}))
```

```js
display(buildChartCurve({comuna:"Renca"}))
```



```js
const plot1 = Plot.plot({
  title: `Defunciones por comuna`,
  marginLeft:100,

  width: width,
  
  marks: [
    Plot.barX(dataDefuncionesPorComuna, {
      x: "defunciones",
      y: "comuna",
      sort:{y:"x",reverse:true, limit:50}
    }),
  ],
});
display(plot1)
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
function buildDistChart(data) {

  const dataPlot = data;

  const max = _.chain(dataPlot)
    .map((d) => d.defunciones)
    .max()
    .value();

  return Plot.plot({
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