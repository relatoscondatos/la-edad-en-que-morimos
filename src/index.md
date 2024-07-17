---
sql:
  defuncionesPorComuna: data/defuncionesPorComuna.parquet
  defuncionesChilePorEdad: data/defuncionesChilePorEdad.parquet
  defuncionesPorComunaEdad: data/defuncionesPorComunaEdad.parquet
  statsPorComuna: data/percentilesPorComuna.parquet
---
# ¿La edad en que morimos depende de dónde vivimos?
## Explorando las desigualdades en la edad de defunción en Chile

## Distribución de edad de defunción en Chile

Esta página utiliza datos de las defunciones en Chile entre 2014 y 2023 (10 años), publicados por el Departamento de Estadísticas e Información en Salud (DEIS) del Ministerio de Salud de Chile.


<div class="grid grid-cols-1">
  <div class="card grid-colspan-1">
  <h2>Distribución de edad de defunciones en Chile</h2>
  <h3>Datos de años 2014 a 2023</h3>

  ${
    resize((width) =>
      buildChartCurve(dataDefuncionesChilePorEdad.toArray(),{
      p50:statsChile.p50, 
      p25:statsChile.p25, 
      p75:statsChile.p75, 
      max:maxChile,
      mark:null,
      width:640,
      height:320
})
    ) 
  }
  </div>  
  </div>  

La curva de distribución muestra cómo se agrupa una mayor cantidad de personas fallecidas en edades más avanzadas.

Ordenamos a todas las personas fallecidas por edad y las dividimos en dos grupos iguales; la **mediana** es la edad que divide al 50% con mayor edad y al 50% con menor edad. En Chile, la **mediana** de la edad de fallecimiento es de ${statsChile.p50} años.

También podemos dividir la población en cuatro grupos (25% cada uno) y obtener así los cuartiles. El **primer cuartil** (percentil 25) incluye a las personas que fallecieron a una edad menor a ${statsChile.p25} años, y el **tercer cuartil** (percentil 75) incluye a las personas que fallecieron a una edad menor a ${statsChile.p75} años.


<div class="grid grid-cols-2">
 
  <div class="card">
  <h2>Mediana</h2>
  <h3>Edad de defunciones en Chile</h3>
  ${
    resize((width) =>
      buildChartCurve(dataDefuncionesChilePorEdad.toArray(),{
      p50:statsChile.p50, 
      p25:statsChile.p25, 
      p75:statsChile.p75, 
      max:maxChile,
      mark:"median",
      width:640,
      height:320
})
    ) 
  }
  </div>
  <div class="card">
  <h2>Cuartiles</h2>
  <h3>Edad de defunciones en Chile</h3>
  ${
    resize((width) =>
      buildChartCurve(dataDefuncionesChilePorEdad.toArray(),{
      p50:statsChile.p50, 
      p25:statsChile.p25, 
      p75:statsChile.p75, 
      max:maxChile,
      mark:"quartiles",
      width:640,
      height:320
})
    ) 
  }
  </div>
</div>

Una manera alternativa de sintetizar cómo se distribuyen las edades es con una barra que representa el rango entre el primer cuartil (25%) y el tercer cuartil (75%). Dentro de la barra se indica la mediana.

<div class="grid grid-cols-2">
 
  <div class="card">
  <h2>Distribución de fallecimientos en Chile</h2>
  <h3>Mediana y rango entre el primer cuartil (25%) y el tercer cuartil (75%)</h3>
  ${buildBoxes([statsChile])}
  </div>

</div>

## Distribución de edad de defunción por comunas

A nivel comunal, muchas comunas tienen una distribución similar a la nacional. A continuación se ilustra la distribución de algunas capitales regionales que son muy similares a la distribución nacional. Sin embargo, otras capitales regionales se distancian más de la distribución nacional.

<div class="grid grid-cols-2">
 
  <div class="card">
  <h2>Capitales Regionales con distribución similar a Chile</h2>
  ${buildBoxes(statsCapitalesRegionales.filter(d => (d.p50 >= statsChile.p50-1) && (d.p50 <= statsChile.p50+1)))}
  </div>
  <div class="card">
  <h2>Capitales Regionales con distribución distinta a Chile</h2>
  ${buildBoxes(statsCapitalesRegionales.filter(d => (d.p50 < statsChile.p50-1) || (d.p50 > statsChile.p50+1) || d.comuna == "Chile"))}
  </div>


</div>


Si observamos todas las comunas (excluyendo las más pequeñas, con menos de 1000 defunciones en 10 años), vemos que hay algunas con una mediana **considerablemente más alta que la nacional** (por ejemplo, ${_.chain([...statsComunasTop]).sortBy(d => +d.p75).sortBy(d => +d.p50).reverse().slice(0,5).map(d => d.comuna).value().join(",")}) y otras con una mediana **considerablemente menor a la nacional** (por ejemplo, ${_.chain([...statsComunasBottom]).sortBy(d => +d.p75).sortBy(d => +d.p50).slice(0,5).map(d => d.comuna).value().join(",")}).

<div class="grid grid-cols-2">
 
  <div class="card">
  <h2>Comunas con mayor edad de fallecimiento</h2>
  ${buildBoxes(statsComunasTop)}
  </div>

  <div class="card">
  <h2>Comunas con menor edad de fallecimiento</h2>
  ${buildBoxes(statsComunasBottom)}
  </div>
</div>



## Consulta por una comuna

Aquí puedes seleccionar una comuna, observar su distribución y compararla con la distribución nacional.
```js
const comuna = view(Inputs.select(_.map(dataComunas.toArray(),d => d.comuna), { label: "Comuna"}));
```

<div class="grid grid-cols-2">
  <div class="card">
  <h2>Mediana</h2>
    <h3>Edad de defunciones en ${comuna}</h3>

  ${
    resize((width) =>
      buildChartCurve(dataComuna,{
      p50:statsComuna.p50, 
      p25:statsComuna.p25, 
      p75:statsComuna.p75, 
      max:maxChile,
      mark:"median",
      width:640,
      height:320
})
    ) 
  }
  </div>
    <div class="card">
      <h2>Cuartiles</h2>
      <h3>Edad de defunciones en ${comuna}</h3>

  ${
    resize((width) =>
      buildChartCurve(dataComuna,{
      p50:statsComuna.p50, 
      p25:statsComuna.p25, 
      p75:statsComuna.p75, 
      max:maxChile,
      mark:"quartiles",
      width:640,
      height:320
})
    ) 
  }
  </div>
</div>

${comparaciónConChile(statsComuna, statsChile)}

<div class="grid grid-cols-2">

  <div class="card">
  <h2>${comuna}</h2>
  ${buildBoxes(statsComunaMasChile)}
  </div>

</div>

## Determinantes sociales de la salud
### Posible explicación de las diferencias

La OMS indica que *"Los determinantes sociales de la salud (DSS) son los factores no médicos que influyen en los resultados de salud. Son las condiciones en las que las personas nacen, crecen, trabajan, viven y envejecen, y el conjunto más amplio de fuerzas y sistemas que moldean las condiciones de la vida diaria." (OMS, 2024)* 

Ejemplos de determinantes sociales de la salud:
* Ingreso y protección social
* Educación
* Desempleo e inseguridad laboral
* Condiciones de vida laboral
* Inseguridad alimentaria
* Vivienda, servicios básicos y medio ambiente
* Desarrollo en la primera infancia
* Inclusión social y no discriminación
* Conflicto estructural
* Acceso a servicios de salud asequibles y de calidad decente

Según la OMS, *numerosos estudios sugieren que los DSS representan **entre el 30% y el 55%** de los resultados de salud.*

Más información sobre ***Determinandes sociales de la salud***: 
* [Social determinants of health, OMS](https://www.who.int/health-topics/social-determinants-of-health)
* [Determinantes sociales de la salud, OPS](https://www.paho.org/es/temas/determinantes-sociales-salud)
* [Social determinants of health: the solid facts, 2nd ed, OMS](https://iris.who.int/handle/10665/326568)
* [Fair Society, Healthy Lives (The Marmot Review)](https://www.instituteofhealthequity.org/resources-reports/fair-society-healthy-lives-the-marmot-review)
* [Marmot Review 10 Years On](https://www.instituteofhealthequity.org/resources-reports/marmot-review-10-years-on)


 <div class="card">
  <h2>Fuente de datos</h2>
Departamento de Estadísticas e Información de Salud,  Ministerio de Salud, "Defunciones por Causa"  

* Datos Abiertos | Defunciones
https://deis.minsal.cl/#datosabiertos

* [Defunciones por Causa 1990 - 2021 CIFRAS OFICIALES](https://repositoriodeis.minsal.cl/DatosAbiertos/VITALES/DEFUNCIONES_FUENTE_DEIS_1990_2021_CIFRAS_OFICIALES.zip)
* Defunciones por Causa 2022 - 2024 CIFRAS PRELIMINARES (Actualización semanal):(*Enlace actualizado semanalmente*)  

Organización Mundial de la Salud (OMS). "Social determinants of health." Consultado el 16 de julio de 2024. https://www.who.int/health-topics/social-determinants-of-health.

  </div>


```js
const maxChile = _.chain(dataDefuncionesChilePorEdad.toArray()).map(d => d.edad).value()

const dataComuna = _.chain([...dataDefuncionesPorComunaEdad])
      .filter((d) => d.comuna == comuna)
      .sortBy((d) => d.edad)
      .value()

const statsCapitalesRegionales = [...statsComunas].filter(d => d.comuna.match(/Chile$|Arica$|Iquique$|Antofagasta$|Copiapó$|La Serena$|Valparaíso$|Rancagua$|Talca$|Concepción$|Chillán$|Temuco$|Valdivia$|Puerto Montt$|Coihaique$|Punta Arenas/))

const umbralDiferencia = 2;
```


```js
/*
* buildChartCurve
*/
function buildChartCurve(data,options) {
  const comuna = (options && options.comuna) || "Chile";
  const sexo = (options && options.sexo) || null;
  const mark = (options && options.mark) || null;
  const title = (options && options.title) || null;
  const subtitle = (options && options.subtitle) || null;
  const p50 = (options && options.p50) || null;
  const p25 = (options && options.p25) || null;
  const p75 = (options && options.p75) || null;
  const width = (options && options.width) || 640;
  const height = (options && options.height) || width/2;

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
      text: (d) => d,
      fontSize: 18

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
    width,
    height,
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

      Plot.lineY(dataPlot, {
        x: "edad",
        y: "defunciones",
        stroke: (d) => "curva",
        opacity: 0,
        tip:true,
        title: d => `Edad: ${d.edad} \nDefunciones: ${d3.format(",")(d.defunciones)}`
      }),

      mark == "median" ? medianMark  : mark == "quartiles" ? quartilesMark : []
    ]
  });
}

function buildBoxes(data, options) {
  const dataPlot = data;

  return Plot.plot({
    marginLeft: 100,

    x: {
      domain: [50, 95]
    },

    y:{
      domain: _.chain([...dataPlot]).sortBy(d => d.p75).sortBy(d => d.p50).map(d => d.comuna).reverse().value()
    },
    color: {
      domain: ["comuna", "chile"],
      //range: ["blue", "lightgrey"]
    },
    marks: [
      Plot.barX(dataPlot, {
        x1: (d) => d.p25,
        x2: (d) => d.p75,
        y: (d) => d.comuna,
        fill: (d) =>
          d.comuna !== "Chile" ? "comuna" : "chile"
      }),

      Plot.tickX(dataPlot, {
        x: (d) => d.p50,
        y: "comuna",
        stroke: "black",
        //sort: { y: "x" }
      }),
      Plot.barX(dataPlot, {
        x1: (d) => d.p50 - 0.5,
        x2: (d) => d.p50 + 0.5,
        y: (d) => d.comuna,
        insetTop: 5,
        insetBottom: 5,
        fill: "white"
      }),

      Plot.text(dataPlot, {
        x: (d) => d.p50,
        y: "comuna",
        fill: "black",
        text: (d) => d.p50,
        fontSize: 8
      }),
      Plot.text(dataPlot, {
        x: (d) => d.p75,
        y: "comuna",
        fill: "black",
        text: (d) => d.p75,
        textAnchor: "start",
        fontSize: 8
      }),
      Plot.text(dataPlot, {
        x: (d) => d.p25,
        y: "comuna",
        fill: "black",
        text: (d) => d.p25,
        textAnchor: "end",
        fontSize: 8
      }),
      Plot.ruleX([0])
    ]
  });
}

function comparaciónConChile(statsComuna, statsChile) {

  let msg = `${statsComuna.comuna}`
  if (statsComuna.p50 < statsChile.p50 - umbralDiferencia) {
    msg += ` tiene una mediana (${statsComuna.p50}) menor a la de Chile (${statsChile.p50})`
  } else if (statsComuna.p50 > statsChile.p50 + umbralDiferencia) {
    msg += ` tiene una mediana (${statsComuna.p50}) por sobre la de Chile (${statsChile.p50})`

  } else {
    msg += ` tiene una mediana (${statsComuna.p50}) similar a la de Chile (${statsChile.p50})`
  }

  return msg
}
```



```sql id=dataDefuncionesChilePorEdad
SELECT *
FROM defuncionesChilePorEdad  
```

```sql id=[statsChile]
SELECT *
FROM statsPorComuna 
WHERE comuna = 'Chile'
```

```sql id=[statsComuna]
SELECT *
FROM statsPorComuna 
WHERE comuna = ${comuna}
```

```sql id=statsComunaMasChile
SELECT *
FROM statsPorComuna 
WHERE comuna = ${comuna} OR comuna = 'Chile'
```

```sql id=statsComunas
SELECT *
FROM statsPorComuna 
```

```sql id=statsComunasTop
SELECT *
FROM statsPorComuna 
WHERE p50 > 78 AND n > 1000 or comuna = 'Chile'
```

```sql id=statsComunasBottom
SELECT *
FROM statsPorComuna 
WHERE p50 < 74 AND n > 1000 or comuna = 'Chile'
ORDER BY p50 DESC
```

```sql id=statsComunasSimilarAChile
SELECT *
FROM statsPorComuna 
WHERE p50 = ${statsChile.p50} AND p25 = ${statsChile.p25} AND p75 = ${statsChile.p75} AND n > 1000 or comuna = 'Chile'
ORDER BY p50 DESC
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
import {buildDistChart} from "./components/distributionChart.js";

import { es_ES } from "./components/config.js";
d3.formatDefaultLocale(es_ES);
```