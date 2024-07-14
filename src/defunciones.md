---
sql:
  defuncionesPorEdadComunaYSexo: ./data/dataDefuncionesPorEdadComunaYSexo_2014_2023.parquet
---


<div class="hero2">
  <h1>Distribución de defunciones en Chile</h1>
</div>


```sql
SELECT comuna, 
    sum(defunciones) as defunciones 
FROM defuncionesPorEdadComunaYSexo  
GROUP BY comuna

```