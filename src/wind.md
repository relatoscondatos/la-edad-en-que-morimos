---
toc: false
---

# San Francisco wind

This example accesses near real-time wind data using R and Python data loaders, and uses GitHub actions to automatically rebuild and deploy to GitHub pages every 2 hours.

The R and Py data loaders are redundant; this is a pedagogical example to test GH actions for both.

**Data:** NOAA Tides and Currents, [CO-OPS API](https://api.tidesandcurrents.noaa.gov/api/prod/)



## Using data from Python data loader

Data loader: `src/data/wind.csv.py`

```js echo
const windPy = await FileAttachment("./data/wind.csv").csv({ typed: true });
```

```js
function windyPyChart(width) {
  return Plot.plot({
    width: width,
    x: { domain: directions, label: "Wind direction" },
    marks: [
      Plot.barY(
        windPy,
        Plot.groupX({ y: "count" }, { x: "windDirAbb", fill: "#008BFF" })
      ),
      Plot.ruleY([0]),
    ],
  });
}
```



<div class="grid grid-cols-4">
  <div class="card grid-colspan-2">${Inputs.table(windPy, {rows: 17.5})}</div>
  <div class="card grid-colspan-2">${resize(width => windyPyChart(width))}</div>
</div>