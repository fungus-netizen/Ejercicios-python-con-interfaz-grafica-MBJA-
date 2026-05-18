// variables globales, se destruyen antes de crear nuevos charts para evitar errores de Chart.js al reutilizar canvas
let chartBarras = null;
let chartDonut = null;
let chartPoligono = null;

async function leerCSV(ruta){ // devuelve un array de objetos con claves según el header del CSV
  const res = await fetch(ruta);
  const texto = await res.text();
  return Papa.parse(texto, {header:true, dynamicTyping:true}).data; // papaparse -> agarra claves del header y convierte a numero sino string
} // dynamictyping se encarga de convertir

function limpiarDatos(datos, nombreVar){ // devuelve un array con los valores de la variable, filtrando nulos, 'NA' y no num
  return datos.map(d=>d[nombreVar]).filter(v=>v!==null && v!==undefined && v!=='NA' && !(Number.isNaN(v)));
}

function calcularFrecuencias(datosArray, bins=null){ // si no num, da frecuencias categoricas, si num, da clases con frecuencias absolutas
  const esNumerico = datosArray.every(v=>typeof v === 'number');
  if(!esNumerico){
    const mapa = {};
    datosArray.forEach(v=>{ mapa[v]=(mapa[v]||0)+1 }); // cuenta frecuencia de cada valor categorico
    const items = Object.keys(mapa).map(k=>({label:k, valor:mapa[k]}));
    return {tipo:'categorico', items};
  }

  // obtiene min, max, n, k, ancho, clases con li, ls, etiqueta y frecuencia
  const min = Math.min(...datosArray);
  const max = Math.max(...datosArray);
  const n = datosArray.length;
  const k = bins || Math.ceil(Math.sqrt(n));
  const ancho = (max - min) / k;
  const clases = [];

  for(let i=0;i<k;i++){ // calcula limite inferior, superior, etiqueta y frecuencia inicial de cada clase
    const li = min + i*ancho;
    const ls = i===k-1? max : li + ancho;
    clases.push({li, ls, etiqueta:`${li.toFixed(2)} - ${ls.toFixed(2)}`, frecuencia:0});
  }

  datosArray.forEach(v=>{ // asigna cada valor a su clase correspondiente y suma frecuencia
    const idx = Math.min(Math.floor((v - min)/ancho), k-1);
    clases[idx].frecuencia++;
  });
  return {tipo:'numerico', clases};
}

function frecuenciasAcumuladas(clases){ // suma frecuencias
  let acum = 0;
  return clases.map(c=>{ acum += c.frecuencia; return {...c, acumulada:acum}; });
}

function calcularMedia(datosArray){ // media
  const s = datosArray.reduce((a,b)=>a+b,0);
  return s / datosArray.length;
}

function calcularMediana(datosArray){ // mediana
  const a = [...datosArray].sort((x,y)=>x-y);
  const n = a.length;
  if(n%2===1) return a[(n-1)/2];
  return (a[n/2 -1] + a[n/2]) / 2;
}

function calcularModa(datosArray){ // moda
  const mapa = {};
  datosArray.forEach(v=>mapa[v]=(mapa[v]||0)+1);
  let max=0, moda=null;
  Object.keys(mapa).forEach(k=>{ if(mapa[k]>max){max=mapa[k]; moda=k} });
  return moda;
}

function renderizarTablaAcumulada(clases){ // renderiza tabla de frecuencias acumuladas, asume que cada clase ya la calculo previamente
  const tabla = document.getElementById('tabla-acumulada');
  tabla.innerHTML = '<tr><th>Clase</th><th>Frecuencia</th><th>Acumulada</th></tr>' +
    clases.map(c=>`<tr><td>${c.etiqueta}</td><td>${c.frecuencia}</td><td>${c.acumulada}</td></tr>`).join(''); // genera filas con clase, frecuencia y acumulada
}

function mostrarMedidasHTML(media, mediana, moda){ // muestra los valores en sus widgets correspondientes
  const mediaEl = document.querySelector('#medida-media .valor');
  const medianaEl = document.querySelector('#medida-mediana .valor');
  const modaEl = document.querySelector('#medida-moda .valor');
  const mediaText = (typeof media === 'number' && !Number.isNaN(media)) ? media.toFixed(3) : 'N/A';
  const medianaText = (typeof mediana === 'number' && !Number.isNaN(mediana)) ? mediana : 'N/A';
  const modaText = (moda !== null && moda !== undefined) ? moda : 'N/A';
  if(mediaEl) mediaEl.textContent = mediaText;
  if(medianaEl) medianaEl.textContent = medianaText;
  if(modaEl) modaEl.textContent = modaText;
}

function destruirCharts(){ // destruye charts y asigna null al reutilizar canvas
  if(chartBarras){ chartBarras.destroy(); chartBarras = null; }
  if(chartDonut){ chartDonut.destroy(); chartDonut = null; }
  if(chartPoligono){ chartPoligono.destroy(); chartPoligono = null; }
}

function graficarBarrasChart(clases){ // grafica barras 
  const ctx = document.getElementById('barrasCanvas').getContext('2d');
  const labels = clases.map(c=>c.etiqueta);
  const data = clases.map(c=>c.frecuencia);
  chartBarras = new Chart(ctx, {
    type: 'bar',
    data: {labels, datasets:[{label:'Frecuencia', data, backgroundColor:'#4c78a8'}]},
    options: {responsive:true, maintainAspectRatio:false}
  });
}

function graficarDonutChart(items){ // donan
  const ctx = document.getElementById('donutCanvas').getContext('2d');
  const labels = items.map(i=>i.label);
  const data = items.map(i=>i.valor);
  const colores = ['#4c78a8','#f28e2b','#e15759','#76b7b2','#59a14f','#b07aa1','#ff9da7']; // color por segmento
  chartDonut = new Chart(ctx, {
    type: 'doughnut',
    data:{labels, datasets:[{data, backgroundColor:colores}]},
    options:{responsive:true, maintainAspectRatio:false}
  });
}

function graficarPoligonoChart(clases){ // Poligono frecuencoias
  const ctx = document.getElementById('poligonoCanvas').getContext('2d');
  const labels = clases.map(c=>c.etiqueta);
  const data = clases.map(c=>c.frecuencia);
  chartPoligono = new Chart(ctx, {
    type: 'line',
    data:{labels, datasets:[{label:'Frecuencia', data, fill:false, borderColor:'#59a14f'}]},
    options:{responsive:true, maintainAspectRatio:false}
  });
}

async function procesarRenderizar(){ // hace todo, lee, procesa, renderiza etc.
  const selector = document.getElementById('selector-variable');
  const variable = selector.value;
  const datos = await leerCSV('datos.csv'); // await para 100% que se cargen los datos
  const lista = limpiarDatos(datos, variable);

  document.getElementById('titulo-barras').textContent = `Frecuencias absolutas de ${variable}`;
  document.getElementById('titulo-donut').textContent = `Frecuencias relativas de ${variable}`;
  document.getElementById('titulo-poligono').textContent = `Polígono de frecuencias de ${variable}`;
  document.getElementById('titulo-acumulada').textContent = `Frecuencia acumulada de ${variable}`;
  // las medidas en su propio container

  destruirCharts(); 

  const frec = calcularFrecuencias(lista); // obtiene frecuencias categoricas o numericas segun corresponda
  if(frec.tipo==='categorico'){
    const clasesCat = frec.items.map(i=>({etiqueta:i.label, frecuencia:i.valor}));
    graficarBarrasChart(clasesCat);
    graficarDonutChart(frec.items);
    graficarPoligonoChart(clasesCat);
    const clasesAcum = frecuenciasAcumuladas(clasesCat);
    renderizarTablaAcumulada(clasesAcum);
    mostrarMedidasHTML(NaN,'N/A','N/A');
  } else {
    const clases = frec.clases;
    graficarBarrasChart(clases);
    const items = clases.map(c=>({label:c.etiqueta, valor:c.frecuencia}));
    graficarDonutChart(items);
    graficarPoligonoChart(clases);
    const clasesAcum = frecuenciasAcumuladas(clases);
    renderizarTablaAcumulada(clasesAcum);
    const media = calcularMedia(lista);
    const mediana = calcularMediana(lista);
    const moda = calcularModa(lista);
    mostrarMedidasHTML(media, mediana, moda);
  }
}

document.getElementById('selector-variable').addEventListener('change', ()=>procesarRenderizar()); // cuando cambia el selector, vuelve a procesar y renderizar todo
document.addEventListener('DOMContentLoaded', ()=>procesarRenderizar());
