import * as Plot from "npm:@observablehq/plot";
import * as d3 from "npm:d3"; 
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
            opacity: 1,
          }),        
          Plot.lineY(dataPlot, {
            x: "edad",
            y: "defunciones",
            stroke: "grey",
            opacity: 1,
            tip:true,
            title: d => `${d.edad} años, ${d3.format(",")(d.defunciones)} personas`
          }),
      ]
    });
  }
