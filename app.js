// ============================================================
// MOTOR DE CALCULO FISCAL + UI
// ============================================================

// --- MOTOR DE CALCULO ---

function calcularCuotaAutonomo(ingresosNetosMensuales) {
  for (const tramo of CUOTAS_AUTONOMO) {
    if (ingresosNetosMensuales <= tramo.max) {
      return {
        tramo: tramo,
        cuotaMinima: tramo.cuota,
        cuotaAnual: tramo.cuota * 12,
        baseMin: tramo.baseMin,
        baseMax: tramo.baseMax,
        rangoIngresos: `${tramo.min.toFixed(0)} - ${tramo.max === Infinity ? '+' : tramo.max.toFixed(0)} EUR`,
      };
    }
  }
  const ultimo = CUOTAS_AUTONOMO[CUOTAS_AUTONOMO.length - 1];
  return { tramo: ultimo, cuotaMinima: ultimo.cuota, cuotaAnual: ultimo.cuota * 12, baseMin: ultimo.baseMin, baseMax: ultimo.baseMax, rangoIngresos: `> ${ultimo.min} EUR` };
}

function calcularIRPFTramos(baseLiquidable, tramos) {
  let cuota = 0;
  let restante = baseLiquidable;
  let anterior = 0;
  const desglose = [];

  for (const tramo of tramos) {
    if (restante <= 0) break;
    const baseTramo = Math.min(restante, tramo.hasta - anterior);
    const cuotaTramo = baseTramo * tramo.tipo / 100;
    desglose.push({
      desde: anterior,
      hasta: Math.min(tramo.hasta, anterior + baseTramo),
      tipo: tramo.tipo,
      base: baseTramo,
      cuota: cuotaTramo,
    });
    cuota += cuotaTramo;
    restante -= baseTramo;
    anterior = tramo.hasta;
  }

  return { cuota, desglose, tipoEfectivo: baseLiquidable > 0 ? (cuota / baseLiquidable * 100) : 0 };
}

function calcularIRPFCompleto(beneficioNeto, comunidadId, opciones = {}) {
  const comunidad = COMUNIDADES[comunidadId];
  if (!comunidad) return null;

  const cuotaSSAnual = opciones.cuotaSSAnual || 0;
  const minimoPersonal = opciones.minimoPersonal || MINIMOS.personal;

  // Reduccion por cuota SS
  let baseImponible = beneficioNeto - cuotaSSAnual;
  if (baseImponible < 0) baseImponible = 0;

  // Gastos dificil justificacion (solo EDS)
  let gastosDJ = 0;
  if (opciones.estimacionDirectaSimplificada !== false) {
    gastosDJ = Math.min(baseImponible * 0.05, 2000);
    baseImponible -= gastosDJ;
  }

  // Base liquidable
  let baseLiquidable = baseImponible - minimoPersonal;
  if (baseLiquidable < 0) baseLiquidable = 0;

  // Calcular parte estatal y autonomica
  let estatal, autonomica;
  if (comunidad.esForal) {
    // Regimen foral: la escala es unica (no se suma estatal)
    autonomica = calcularIRPFTramos(baseLiquidable, comunidad.tramos);
    estatal = { cuota: 0, desglose: [], tipoEfectivo: 0 };
  } else {
    estatal = calcularIRPFTramos(baseLiquidable, TRAMOS_ESTATALES);
    autonomica = calcularIRPFTramos(baseLiquidable, comunidad.tramos);
  }

  const cuotaTotal = estatal.cuota + autonomica.cuota;
  const tipoEfectivoTotal = beneficioNeto > 0 ? (cuotaTotal / beneficioNeto * 100) : 0;

  // Retenciones ya pagadas
  const retencionesAnuales = opciones.retencionesAnuales || 0;
  const pagosFraccionados = opciones.pagosFraccionados || 0;

  const resultadoRenta = cuotaTotal - retencionesAnuales - pagosFraccionados;

  return {
    beneficioNeto,
    cuotaSSAnual,
    gastosDificilJustificacion: gastosDJ,
    baseImponible: baseImponible + gastosDJ, // antes de DJ
    baseImponibleReducida: baseImponible,
    minimoPersonal,
    baseLiquidable,
    estatal,
    autonomica,
    cuotaTotal,
    tipoEfectivoTotal,
    retencionesAnuales,
    pagosFraccionados,
    resultadoRenta,
    comunidad: comunidad.nombre,
    esForal: !!comunidad.esForal,
  };
}

function compararComunidades(beneficioNeto, opciones = {}) {
  const resultados = [];
  for (const [id, comunidad] of Object.entries(COMUNIDADES)) {
    const resultado = calcularIRPFCompleto(beneficioNeto, id, opciones);
    resultados.push({
      id,
      nombre: comunidad.nombre,
      cuotaTotal: resultado.cuotaTotal,
      tipoEfectivo: resultado.tipoEfectivoTotal,
      diferencia: 0,
      tipoMaxAgregado: comunidad.tipoMaxAgregado,
      notas: comunidad.notas,
    });
  }

  resultados.sort((a, b) => a.cuotaTotal - b.cuotaTotal);
  const min = resultados[0].cuotaTotal;
  resultados.forEach(r => r.diferencia = r.cuotaTotal - min);

  return resultados;
}

function calcularGastosDeducibles(gastos, m2Total, m2Actividad) {
  let totalDeducible = 0;
  let totalIVADeducible = 0;
  const desglose = [];

  for (const gasto of gastos) {
    const cat = CATEGORIAS_GASTOS.find(c => c.id === gasto.categoria);
    if (!cat) continue;

    let importeDeducible = gasto.importe;
    let porcentajeAplicado = cat.deduccion;

    // Suministros hogar: formula especial
    if (gasto.categoria === 'suministros' && m2Total > 0) {
      const proporcionM2 = m2Actividad / m2Total;
      importeDeducible = gasto.importe * proporcionM2 * 0.30;
      porcentajeAplicado = Math.round(proporcionM2 * 30 * 100) / 100;
    } else {
      importeDeducible = gasto.importe * (cat.deduccion / 100);
    }

    // Limites especiales
    if (gasto.categoria === 'seguro_medico') {
      const personas = gasto.personas || 1;
      const limite = personas * GASTOS_DEDUCIBLES.seguroMedico.limitePorPersona;
      importeDeducible = Math.min(importeDeducible, limite);
    }
    if (gasto.categoria === 'colegio_profesional') {
      importeDeducible = Math.min(importeDeducible, GASTOS_DEDUCIBLES.cuotasColegiosProfesionales.limite);
    }

    const ivaDeducible = cat.iva ? gasto.importe * 0.21 : 0;

    totalDeducible += importeDeducible;
    totalIVADeducible += ivaDeducible;

    desglose.push({
      categoria: cat.nombre,
      importeOriginal: gasto.importe,
      importeDeducible,
      porcentajeAplicado,
      ivaDeducible,
      nota: cat.nota || '',
    });
  }

  return { totalDeducible, totalIVADeducible, desglose };
}

function calcularPagoFraccionado(beneficioAcumulado, retencionesAcumuladas, pagosAnteriores) {
  const cuota = beneficioAcumulado * 0.20;
  const resultado = cuota - retencionesAcumuladas - pagosAnteriores;
  return Math.max(0, resultado);
}

// --- UTILIDADES ---

function formatEUR(n) {
  return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(n);
}

function formatPct(n) {
  return n.toFixed(2) + '%';
}

function esc(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// --- UI ---

let activeSection = 'cuota';

function init() {
  setupNavigation();
  setupCuotaCalculator();
  setupIRPFCalculator();
  setupComparador();
  setupGastos();
  setupDeducciones();
  renderCalendario();
  showSection('cuota');
}

function setupNavigation() {
  document.querySelectorAll('[data-section]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      showSection(btn.dataset.section);
    });
  });
}

function showSection(id) {
  activeSection = id;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('[data-section]').forEach(b => b.classList.remove('active'));

  const section = document.getElementById('sec-' + id);
  if (section) section.classList.add('active');

  document.querySelectorAll(`[data-section="${id}"]`).forEach(b => b.classList.add('active'));

  // Close mobile menu
  const nav = document.querySelector('.nav-links');
  if (nav) nav.classList.remove('open');
}

// --- CALCULADORA CUOTA AUTONOMO ---

function setupCuotaCalculator() {
  const form = document.getElementById('form-cuota');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    calcularCuota();
  });

  const input = document.getElementById('ingresos-netos');
  if (input) input.addEventListener('input', debounce(calcularCuota, 300));

  // Render tabla de tramos
  renderTablaTramos();
}

function calcularCuota() {
  const input = document.getElementById('ingresos-netos');
  const tarifaPlana = document.getElementById('tarifa-plana');
  const resultDiv = document.getElementById('resultado-cuota');
  if (!input || !resultDiv) return;

  const ingresosAnuales = parseFloat(input.value) || 0;
  const ingresosMensuales = ingresosAnuales / 12;
  const esTarifaPlana = tarifaPlana && tarifaPlana.checked;

  if (ingresosAnuales <= 0) {
    resultDiv.innerHTML = '<p class="hint">Introduce tus ingresos netos anuales para calcular.</p>';
    return;
  }

  const resultado = calcularCuotaAutonomo(ingresosMensuales);

  if (esTarifaPlana) {
    resultDiv.innerHTML = `
      <div class="result-cards">
        <div class="result-card highlight">
          <span class="result-label">Cuota mensual (Tarifa Plana)</span>
          <span class="result-value">${formatEUR(TARIFA_PLANA)}</span>
        </div>
        <div class="result-card">
          <span class="result-label">Cuota anual</span>
          <span class="result-value">${formatEUR(TARIFA_PLANA * 12)}</span>
        </div>
        <div class="result-card save">
          <span class="result-label">Ahorro vs cuota normal</span>
          <span class="result-value">${formatEUR((resultado.cuotaMinima - TARIFA_PLANA) * 12)}/ano</span>
        </div>
        <div class="result-card">
          <span class="result-label">Tu tramo real</span>
          <span class="result-value">${resultado.rangoIngresos}/mes</span>
        </div>
        <div class="result-card">
          <span class="result-label">Cuota que pagarias sin tarifa plana</span>
          <span class="result-value">${formatEUR(resultado.cuotaMinima)}/mes</span>
        </div>
      </div>
    `;
  } else {
    resultDiv.innerHTML = `
      <div class="result-cards">
        <div class="result-card highlight">
          <span class="result-label">Cuota mensual minima</span>
          <span class="result-value">${formatEUR(resultado.cuotaMinima)}</span>
        </div>
        <div class="result-card">
          <span class="result-label">Cuota anual</span>
          <span class="result-value">${formatEUR(resultado.cuotaAnual)}</span>
        </div>
        <div class="result-card">
          <span class="result-label">Ingresos mensuales</span>
          <span class="result-value">${formatEUR(ingresosMensuales)}</span>
        </div>
        <div class="result-card">
          <span class="result-label">Tramo</span>
          <span class="result-value">${resultado.rangoIngresos}/mes</span>
        </div>
        <div class="result-card">
          <span class="result-label">Base cotizacion min.</span>
          <span class="result-value">${formatEUR(resultado.baseMin)}</span>
        </div>
        <div class="result-card">
          <span class="result-label">Base cotizacion max.</span>
          <span class="result-value">${formatEUR(resultado.baseMax)}</span>
        </div>
      </div>
      <p class="hint">Tipo de cotizacion: ${TIPO_COTIZACION}% (incluye MEI ${MEI_2026}%). Puedes cambiar de base hasta 6 veces al ano.</p>
    `;
  }
}

function renderTablaTramos() {
  const container = document.getElementById('tabla-tramos-cuota');
  if (!container) return;

  let html = `<table class="data-table">
    <thead><tr>
      <th>Tramo</th><th>Ingresos netos/mes</th><th>Cuota min./mes</th><th>Cuota/ano</th><th>Base min.</th><th>Base max.</th>
    </tr></thead><tbody>`;

  CUOTAS_AUTONOMO.forEach((t, i) => {
    html += `<tr>
      <td>${i + 1}</td>
      <td>${t.min.toFixed(0)} - ${t.max === Infinity ? '+ EUR' : t.max.toFixed(0) + ' EUR'}</td>
      <td><strong>${formatEUR(t.cuota)}</strong></td>
      <td>${formatEUR(t.cuota * 12)}</td>
      <td>${formatEUR(t.baseMin)}</td>
      <td>${formatEUR(t.baseMax)}</td>
    </tr>`;
  });

  html += '</tbody></table>';
  container.innerHTML = html;
}

// --- CALCULADORA IRPF ---

function setupIRPFCalculator() {
  const form = document.getElementById('form-irpf');
  if (!form) return;

  // Populate CCAA selector
  const select = document.getElementById('ccaa-irpf');
  if (select) {
    for (const [id, c] of Object.entries(COMUNIDADES)) {
      const opt = document.createElement('option');
      opt.value = id;
      opt.textContent = c.nombre;
      select.appendChild(opt);
    }
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    calcularIRPF();
  });
}

function calcularIRPF() {
  const beneficio = parseFloat(document.getElementById('beneficio-neto').value) || 0;
  const ccaa = document.getElementById('ccaa-irpf').value;
  const cuotaSSMensual = parseFloat(document.getElementById('cuota-ss-irpf').value) || 0;
  const retenciones = parseFloat(document.getElementById('retenciones-irpf').value) || 0;
  const hijos = parseInt(document.getElementById('hijos-irpf').value) || 0;
  const nuevoAutonomo = document.getElementById('nuevo-autonomo-irpf');
  const resultDiv = document.getElementById('resultado-irpf');

  if (!resultDiv || !ccaa || beneficio <= 0) {
    if (resultDiv) resultDiv.innerHTML = '<p class="hint">Rellena los campos para calcular.</p>';
    return;
  }

  // Calcular minimo personal + familiar
  let minimo = MINIMOS.personal;
  if (hijos >= 1) minimo += MINIMOS.primerHijo;
  if (hijos >= 2) minimo += MINIMOS.segundoHijo;
  if (hijos >= 3) minimo += MINIMOS.tercerHijo;
  if (hijos >= 4) minimo += MINIMOS.cuartoYSiguientes * (hijos - 3);

  const resultado = calcularIRPFCompleto(beneficio, ccaa, {
    cuotaSSAnual: cuotaSSMensual * 12,
    minimoPersonal: minimo,
    retencionesAnuales: retenciones,
    estimacionDirectaSimplificada: true,
  });

  if (!resultado) return;

  const esForal = resultado.esForal;

  let html = `
    <div class="result-cards">
      <div class="result-card highlight">
        <span class="result-label">IRPF total a pagar</span>
        <span class="result-value">${formatEUR(resultado.cuotaTotal)}</span>
      </div>
      <div class="result-card ${resultado.resultadoRenta < 0 ? 'save' : 'warning'}">
        <span class="result-label">Resultado Renta (${resultado.resultadoRenta < 0 ? 'A DEVOLVER' : 'A PAGAR'})</span>
        <span class="result-value">${formatEUR(Math.abs(resultado.resultadoRenta))}</span>
      </div>
      <div class="result-card">
        <span class="result-label">Tipo efectivo real</span>
        <span class="result-value">${formatPct(resultado.tipoEfectivoTotal)}</span>
      </div>
      <div class="result-card">
        <span class="result-label">Comunidad</span>
        <span class="result-value">${esc(resultado.comunidad)}</span>
      </div>
    </div>

    <h4>Desglose del calculo</h4>
    <table class="data-table compact">
      <tbody>
        <tr><td>Beneficio neto anual</td><td class="right">${formatEUR(resultado.beneficioNeto)}</td></tr>
        <tr><td>(-) Cuota SS anual</td><td class="right">-${formatEUR(resultado.cuotaSSAnual)}</td></tr>
        <tr><td>(-) Gastos dificil justif. (5%)</td><td class="right">-${formatEUR(resultado.gastosDificilJustificacion)}</td></tr>
        <tr><td>(-) Minimo personal/familiar</td><td class="right">-${formatEUR(resultado.minimoPersonal)}</td></tr>
        <tr class="total"><td><strong>Base liquidable</strong></td><td class="right"><strong>${formatEUR(resultado.baseLiquidable)}</strong></td></tr>
      </tbody>
    </table>`;

  if (!esForal) {
    html += `
    <h4>Cuota estatal (${formatPct(resultado.estatal.tipoEfectivo)} efectivo)</h4>
    <table class="data-table compact">
      <thead><tr><th>Tramo</th><th>Tipo</th><th>Base</th><th>Cuota</th></tr></thead>
      <tbody>`;
    resultado.estatal.desglose.forEach(d => {
      html += `<tr>
        <td>${formatEUR(d.desde)} - ${formatEUR(d.hasta)}</td>
        <td>${formatPct(d.tipo)}</td>
        <td class="right">${formatEUR(d.base)}</td>
        <td class="right">${formatEUR(d.cuota)}</td>
      </tr>`;
    });
    html += `<tr class="total"><td colspan="3"><strong>Total estatal</strong></td><td class="right"><strong>${formatEUR(resultado.estatal.cuota)}</strong></td></tr>`;
    html += '</tbody></table>';
  }

  html += `
    <h4>Cuota ${esForal ? 'foral' : 'autonomica'} (${formatPct(resultado.autonomica.tipoEfectivo)} efectivo)</h4>
    <table class="data-table compact">
      <thead><tr><th>Tramo</th><th>Tipo</th><th>Base</th><th>Cuota</th></tr></thead>
      <tbody>`;
  resultado.autonomica.desglose.forEach(d => {
    html += `<tr>
      <td>${formatEUR(d.desde)} - ${formatEUR(d.hasta)}</td>
      <td>${formatPct(d.tipo)}</td>
      <td class="right">${formatEUR(d.base)}</td>
      <td class="right">${formatEUR(d.cuota)}</td>
    </tr>`;
  });
  html += `<tr class="total"><td colspan="3"><strong>Total ${esForal ? 'foral' : 'autonomica'}</strong></td><td class="right"><strong>${formatEUR(resultado.autonomica.cuota)}</strong></td></tr>`;
  html += '</tbody></table>';

  html += `
    <h4>Resultado final</h4>
    <table class="data-table compact">
      <tbody>
        <tr><td>Cuota integra total</td><td class="right">${formatEUR(resultado.cuotaTotal)}</td></tr>
        <tr><td>(-) Retenciones soportadas</td><td class="right">-${formatEUR(resultado.retencionesAnuales)}</td></tr>
        <tr class="total ${resultado.resultadoRenta < 0 ? 'save' : 'warning'}">
          <td><strong>${resultado.resultadoRenta < 0 ? 'A DEVOLVER' : 'A INGRESAR'}</strong></td>
          <td class="right"><strong>${formatEUR(Math.abs(resultado.resultadoRenta))}</strong></td>
        </tr>
      </tbody>
    </table>`;

  resultDiv.innerHTML = html;
}

// --- COMPARADOR CCAA ---

function setupComparador() {
  const form = document.getElementById('form-comparador');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    calcularComparador();
  });
}

function calcularComparador() {
  const beneficio = parseFloat(document.getElementById('beneficio-comparador').value) || 0;
  const resultDiv = document.getElementById('resultado-comparador');
  if (!resultDiv || beneficio <= 0) return;

  const ingresosMensuales = beneficio / 12;
  const cuotaSS = calcularCuotaAutonomo(ingresosMensuales);

  const resultados = compararComunidades(beneficio, {
    cuotaSSAnual: cuotaSS.cuotaAnual,
    minimoPersonal: MINIMOS.personal,
    estimacionDirectaSimplificada: true,
  });

  const masCara = resultados[resultados.length - 1];
  const masBarata = resultados[0];
  const diferencia = masCara.cuotaTotal - masBarata.cuotaTotal;

  let html = `
    <div class="result-cards">
      <div class="result-card save">
        <span class="result-label">Donde menos pagas</span>
        <span class="result-value">${esc(masBarata.nombre)}</span>
        <span class="result-detail">${formatEUR(masBarata.cuotaTotal)} (${formatPct(masBarata.tipoEfectivo)})</span>
      </div>
      <div class="result-card warning">
        <span class="result-label">Donde mas pagas</span>
        <span class="result-value">${esc(masCara.nombre)}</span>
        <span class="result-detail">${formatEUR(masCara.cuotaTotal)} (${formatPct(masCara.tipoEfectivo)})</span>
      </div>
      <div class="result-card highlight">
        <span class="result-label">Diferencia maxima</span>
        <span class="result-value">${formatEUR(diferencia)}</span>
        <span class="result-detail">al ano, por el mismo beneficio</span>
      </div>
    </div>

    <h4>Ranking completo (de menor a mayor IRPF)</h4>
    <table class="data-table">
      <thead><tr>
        <th>#</th><th>Comunidad</th><th>IRPF anual</th><th>Tipo efectivo</th><th>Diferencia vs mejor</th><th>Tipo max. agregado</th>
      </tr></thead><tbody>`;

  resultados.forEach((r, i) => {
    const barWidth = masBarata.cuotaTotal > 0 ? Math.round(r.cuotaTotal / masCara.cuotaTotal * 100) : 0;
    html += `<tr class="${i === 0 ? 'row-best' : i === resultados.length - 1 ? 'row-worst' : ''}">
      <td>${i + 1}</td>
      <td><strong>${esc(r.nombre)}</strong></td>
      <td>
        <div class="bar-cell">
          <div class="bar" style="width:${barWidth}%"></div>
          <span>${formatEUR(r.cuotaTotal)}</span>
        </div>
      </td>
      <td>${formatPct(r.tipoEfectivo)}</td>
      <td class="${r.diferencia > 0 ? 'text-danger' : 'text-success'}">${r.diferencia > 0 ? '+' : ''}${formatEUR(r.diferencia)}</td>
      <td>${formatPct(r.tipoMaxAgregado)}</td>
    </tr>`;
  });

  html += '</tbody></table>';
  resultDiv.innerHTML = html;
}

// --- GASTOS DEDUCIBLES ---

let gastosLista = [];

function setupGastos() {
  const addBtn = document.getElementById('btn-add-gasto');
  const calcBtn = document.getElementById('btn-calc-gastos');
  const selectCat = document.getElementById('gasto-categoria');

  if (selectCat) {
    CATEGORIAS_GASTOS.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat.id;
      opt.textContent = cat.nombre;
      selectCat.appendChild(opt);
    });
  }

  if (addBtn) {
    addBtn.addEventListener('click', () => {
      const cat = document.getElementById('gasto-categoria').value;
      const importe = parseFloat(document.getElementById('gasto-importe').value) || 0;
      const frecuencia = document.getElementById('gasto-frecuencia').value;

      if (!cat || importe <= 0) return;

      let importeAnual = importe;
      if (frecuencia === 'mensual') importeAnual = importe * 12;
      if (frecuencia === 'trimestral') importeAnual = importe * 4;

      gastosLista.push({ categoria: cat, importe: importeAnual, importeOriginal: importe, frecuencia });
      renderGastosLista();
      document.getElementById('gasto-importe').value = '';
    });
  }

  if (calcBtn) {
    calcBtn.addEventListener('click', calcularGastosUI);
  }
}

function renderGastosLista() {
  const container = document.getElementById('gastos-lista');
  if (!container) return;

  if (gastosLista.length === 0) {
    container.innerHTML = '<p class="hint">Anade gastos para ver el desglose.</p>';
    return;
  }

  let html = '<table class="data-table compact"><thead><tr><th>Gasto</th><th>Importe</th><th>Frecuencia</th><th>Anual</th><th></th></tr></thead><tbody>';
  gastosLista.forEach((g, i) => {
    const cat = CATEGORIAS_GASTOS.find(c => c.id === g.categoria);
    html += `<tr>
      <td>${cat ? esc(cat.nombre) : g.categoria}</td>
      <td>${formatEUR(g.importeOriginal)}</td>
      <td>${g.frecuencia}</td>
      <td>${formatEUR(g.importe)}</td>
      <td><button class="btn-small btn-danger" onclick="eliminarGasto(${i})">X</button></td>
    </tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

function eliminarGasto(i) {
  gastosLista.splice(i, 1);
  renderGastosLista();
}

function calcularGastosUI() {
  const m2Total = parseFloat(document.getElementById('m2-total').value) || 100;
  const m2Actividad = parseFloat(document.getElementById('m2-actividad').value) || 0;
  const ingresos = parseFloat(document.getElementById('ingresos-gastos').value) || 0;
  const ccaa = document.getElementById('ccaa-gastos').value;
  const resultDiv = document.getElementById('resultado-gastos');

  if (!resultDiv) return;

  const resultado = calcularGastosDeducibles(gastosLista, m2Total, m2Actividad);

  // Gastos dificil justificacion
  const rendimientoNeto = ingresos - resultado.totalDeducible;
  const gastosDJ = Math.min(Math.max(rendimientoNeto, 0) * 0.05, 2000);

  // Calcular ahorro fiscal
  let ahorroFiscal = 0;
  if (ccaa && ingresos > 0) {
    const sinGastos = calcularIRPFCompleto(ingresos, ccaa, { minimoPersonal: MINIMOS.personal });
    const conGastos = calcularIRPFCompleto(Math.max(0, rendimientoNeto), ccaa, { minimoPersonal: MINIMOS.personal });
    if (sinGastos && conGastos) {
      ahorroFiscal = sinGastos.cuotaTotal - conGastos.cuotaTotal;
    }
  }

  let html = `
    <div class="result-cards">
      <div class="result-card highlight">
        <span class="result-label">Total gastos deducibles</span>
        <span class="result-value">${formatEUR(resultado.totalDeducible)}</span>
      </div>
      <div class="result-card">
        <span class="result-label">Gastos dificil justificacion (5%)</span>
        <span class="result-value">${formatEUR(gastosDJ)}</span>
      </div>
      <div class="result-card save">
        <span class="result-label">Ahorro fiscal estimado en IRPF</span>
        <span class="result-value">${formatEUR(ahorroFiscal)}</span>
      </div>
      <div class="result-card">
        <span class="result-label">IVA deducible estimado</span>
        <span class="result-value">${formatEUR(resultado.totalIVADeducible)}</span>
      </div>
    </div>

    <h4>Desglose por gasto</h4>
    <table class="data-table">
      <thead><tr><th>Concepto</th><th>Importe</th><th>% deducible</th><th>Deducible</th><th>IVA deducible</th></tr></thead>
      <tbody>`;

  resultado.desglose.forEach(d => {
    html += `<tr>
      <td>${esc(d.categoria)}${d.nota ? ' <small>(' + esc(d.nota) + ')</small>' : ''}</td>
      <td>${formatEUR(d.importeOriginal)}</td>
      <td>${d.porcentajeAplicado}%</td>
      <td>${formatEUR(d.importeDeducible)}</td>
      <td>${formatEUR(d.ivaDeducible)}</td>
    </tr>`;
  });

  html += `<tr class="total">
    <td colspan="3"><strong>Total</strong></td>
    <td><strong>${formatEUR(resultado.totalDeducible)}</strong></td>
    <td><strong>${formatEUR(resultado.totalIVADeducible)}</strong></td>
  </tr>`;
  html += '</tbody></table>';

  resultDiv.innerHTML = html;
}

// --- DEDUCCIONES AUTONOMICAS ---

function setupDeducciones() {
  const select = document.getElementById('ccaa-deducciones');
  if (!select) return;

  for (const [id, d] of Object.entries(DEDUCCIONES_AUTONOMICAS)) {
    const opt = document.createElement('option');
    opt.value = id;
    opt.textContent = d.nombre;
    select.appendChild(opt);
  }

  select.addEventListener('change', renderDeducciones);
}

function renderDeducciones() {
  const ccaa = document.getElementById('ccaa-deducciones').value;
  const resultDiv = document.getElementById('resultado-deducciones');
  if (!resultDiv || !ccaa) return;

  const datos = DEDUCCIONES_AUTONOMICAS[ccaa];
  const comunidad = COMUNIDADES[ccaa];
  if (!datos) return;

  const categorias = {};
  datos.deducciones.forEach(d => {
    if (!categorias[d.categoria]) categorias[d.categoria] = [];
    categorias[d.categoria].push(d);
  });

  const catNames = {
    familia: 'Familia y natalidad',
    vivienda: 'Vivienda',
    educacion: 'Educacion',
    emprendimiento: 'Emprendimiento e inversion',
    discapacidad: 'Discapacidad',
    donativos: 'Donativos',
    territorio: 'Territorio y despoblacion',
    salud: 'Salud',
    otros: 'Otros',
  };

  let html = `
    <div class="ccaa-header">
      <h3>${esc(datos.nombre)}</h3>
      ${comunidad ? `<p class="ccaa-notas">${esc(comunidad.notas)}</p>` : ''}
      ${comunidad ? `<p>Tipo maximo agregado: <strong>${formatPct(comunidad.tipoMaxAgregado)}</strong></p>` : ''}
    </div>
    <div class="deducciones-grid">`;

  for (const [catId, deducciones] of Object.entries(categorias)) {
    html += `<div class="deduccion-category">
      <h4>${catNames[catId] || catId}</h4>
      <div class="deduccion-list">`;

    deducciones.forEach(d => {
      let importeStr = '';
      if (d.tipo === 'fija') importeStr = formatEUR(d.importe);
      else if (d.tipo === 'hasta') importeStr = 'hasta ' + formatEUR(d.importeMax || d.importe);
      else if (d.tipo === 'porcentaje') importeStr = d.porcentaje + '%';
      else if (d.tipo === 'variable') importeStr = d.importeMin ? formatEUR(d.importeMin) + ' - ' + formatEUR(d.importeMax) : 'Variable';
      else if (d.tipo === 'info') importeStr = 'Info';

      html += `<div class="deduccion-item">
        <div class="deduccion-header">
          <span class="deduccion-nombre">${esc(d.nombre)}</span>
          <span class="deduccion-importe">${importeStr}</span>
        </div>
        <p class="deduccion-detalle">${esc(d.detalle)}</p>
      </div>`;
    });

    html += '</div></div>';
  }

  html += '</div>';
  resultDiv.innerHTML = html;
}

// --- CALENDARIO FISCAL ---

function renderCalendario() {
  const container = document.getElementById('calendario-contenido');
  if (!container) return;

  const hoy = new Date();

  let html = '<div class="calendario-grid">';

  CALENDARIO_FISCAL.forEach(evento => {
    const fecha = new Date(evento.fecha);
    const isPast = fecha < hoy;
    const isNear = !isPast && (fecha - hoy) < 30 * 24 * 60 * 60 * 1000;

    const tipoClass = {
      trimestral: 'tipo-trimestral',
      domiciliacion: 'tipo-domiciliacion',
      anual: 'tipo-anual',
      renta: 'tipo-renta',
    }[evento.tipo] || '';

    html += `<div class="calendario-item ${isPast ? 'past' : ''} ${isNear ? 'near' : ''} ${tipoClass}">
      <div class="cal-fecha">
        <span class="cal-dia">${fecha.getDate()}</span>
        <span class="cal-mes">${fecha.toLocaleDateString('es-ES', { month: 'short' }).toUpperCase()}</span>
      </div>
      <div class="cal-info">
        <span class="cal-modelo">${esc(evento.modelo)}</span>
        <span class="cal-desc">${esc(evento.descripcion)}</span>
      </div>
      <span class="cal-badge ${evento.tipo}">${evento.tipo}</span>
    </div>`;
  });

  html += '</div>';

  // Add modelo info
  html += `
    <h4 style="margin-top:2rem">Modelos que presenta un autonomo tipico</h4>
    <table class="data-table">
      <thead><tr><th>Modelo</th><th>Que es</th><th>Frecuencia</th><th>Quien lo presenta</th></tr></thead>
      <tbody>
        <tr><td><strong>303</strong></td><td>Autoliquidacion IVA</td><td>Trimestral</td><td>Todos sujetos a IVA</td></tr>
        <tr><td><strong>130</strong></td><td>Pago fraccionado IRPF</td><td>Trimestral</td><td>Estimacion directa</td></tr>
        <tr><td><strong>131</strong></td><td>Pago fraccionado IRPF</td><td>Trimestral</td><td>Modulos</td></tr>
        <tr><td><strong>111</strong></td><td>Retenciones trabajadores</td><td>Trimestral</td><td>Si tienes empleados</td></tr>
        <tr><td><strong>115</strong></td><td>Retenciones alquileres</td><td>Trimestral</td><td>Si alquilas local</td></tr>
        <tr><td><strong>100</strong></td><td>Declaracion de la Renta</td><td>Anual (abr-jun)</td><td>Todos</td></tr>
        <tr><td><strong>390</strong></td><td>Resumen anual IVA</td><td>Anual (enero)</td><td>Todos sujetos a IVA</td></tr>
        <tr><td><strong>190</strong></td><td>Resumen anual retenciones</td><td>Anual (enero)</td><td>Si retienes</td></tr>
        <tr><td><strong>347</strong></td><td>Operaciones >3.005 EUR</td><td>Anual (febrero)</td><td>Si facturas >3.005 a un cliente</td></tr>
      </tbody>
    </table>
    <div class="tip-box">
      <strong>Regla de oro:</strong> Domicilia el dia 15; presenta el dia 20. En enero: domicilia el 25, presenta el 30. Aunque no tengas cuota a ingresar, DEBES presentar las declaraciones.
    </div>`;

  container.innerHTML = html;
}

// --- UTILIDADES UI ---

function debounce(fn, ms) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), ms);
  };
}

// Hamburger menu toggle
function toggleMenu() {
  const nav = document.querySelector('.nav-links');
  if (nav) nav.classList.toggle('open');
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', init);
