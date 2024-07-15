import * as Plot from "npm:@observablehq/plot";
import _ from "npm:lodash";


export function buildDistChart(data) {

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
