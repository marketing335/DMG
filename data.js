// ============================================================
// DATOS FISCALES AUTONOMOS ESPANA 2026
// ============================================================

const CUOTAS_AUTONOMO = [
  { min: 0,    max: 670,     cuota: 200, baseMin: 653.59,  baseMax: 950.98 },
  { min: 670,  max: 900,     cuota: 220, baseMin: 718.95,  baseMax: 950.98 },
  { min: 900,  max: 1166.70, cuota: 260, baseMin: 849.67,  baseMax: 950.98 },
  { min: 1166.70, max: 1300, cuota: 291, baseMin: 950.98,  baseMax: 950.98 },
  { min: 1300, max: 1500,    cuota: 294, baseMin: 960.78,  baseMax: 960.78 },
  { min: 1500, max: 1700,    cuota: 294, baseMin: 960.78,  baseMax: 960.78 },
  { min: 1700, max: 1850,    cuota: 350, baseMin: 1143.79, baseMax: 1143.79 },
  { min: 1850, max: 2030,    cuota: 350, baseMin: 1143.79, baseMax: 1209.15 },
  { min: 2030, max: 2330,    cuota: 350, baseMin: 1143.79, baseMax: 1274.51 },
  { min: 2330, max: 2760,    cuota: 390, baseMin: 1274.51, baseMax: 1372.55 },
  { min: 2760, max: 3190,    cuota: 390, baseMin: 1274.51, baseMax: 1468.36 },
  { min: 3190, max: 3620,    cuota: 390, baseMin: 1274.51, baseMax: 1633.99 },
  { min: 3620, max: 4050,    cuota: 420, baseMin: 1372.55, baseMax: 1732.03 },
  { min: 4050, max: 6000,    cuota: 500, baseMin: 1633.99, baseMax: 4720.50 },
  { min: 6000, max: Infinity,cuota: 590, baseMin: 1928.10, baseMax: 4720.50 },
];

const TIPO_COTIZACION = 31.20; // %
const TARIFA_PLANA = 80; // EUR/mes
const MEI_2026 = 0.9; // %

// ============================================================
// TRAMOS IRPF ESTATAL (parte estatal ~50%)
// ============================================================

const TRAMOS_ESTATALES = [
  { hasta: 12450,    tipo: 9.50 },
  { hasta: 20200,    tipo: 12.00 },
  { hasta: 35200,    tipo: 15.00 },
  { hasta: 60000,    tipo: 18.50 },
  { hasta: 300000,   tipo: 22.50 },
  { hasta: Infinity, tipo: 24.50 },
];

// ============================================================
// TRAMOS IRPF AUTONOMICOS POR CCAA
// ============================================================

const COMUNIDADES = {
  madrid: {
    nombre: "Comunidad de Madrid",
    tramos: [
      { hasta: 12960,    tipo: 8.50 },
      { hasta: 19500,    tipo: 10.70 },
      { hasta: 35500,    tipo: 12.80 },
      { hasta: 60000,    tipo: 17.40 },
      { hasta: Infinity, tipo: 20.50 },
    ],
    tipoMaxAgregado: 45.00,
    notas: "Deflactacion aplicada. Menor presion fiscal de Espana. Rebaja de 0,5 puntos prevista para 2027.",
  },
  cataluna: {
    nombre: "Cataluna",
    tramos: [
      { hasta: 12450,    tipo: 10.50 },
      { hasta: 17707,    tipo: 12.00 },
      { hasta: 21000,    tipo: 14.00 },
      { hasta: 33007,    tipo: 15.00 },
      { hasta: 53407,    tipo: 18.80 },
      { hasta: 90000,    tipo: 21.50 },
      { hasta: 120000,   tipo: 23.50 },
      { hasta: Infinity, tipo: 25.50 },
    ],
    tipoMaxAgregado: 50.00,
    notas: "8 tramos desde 2025 (Decreto ley 5/2025). Tipos altos en rentas elevadas.",
  },
  andalucia: {
    nombre: "Andalucia",
    tramos: [
      { hasta: 12450,    tipo: 9.50 },
      { hasta: 20200,    tipo: 12.00 },
      { hasta: 35200,    tipo: 15.00 },
      { hasta: 60000,    tipo: 18.50 },
      { hasta: Infinity, tipo: 22.50 },
    ],
    tipoMaxAgregado: 47.00,
    notas: "Escala similar a la estatal de referencia. Posicion intermedia.",
  },
  valencia: {
    nombre: "Comunitat Valenciana",
    tramos: [
      { hasta: 12450,    tipo: 9.50 },
      { hasta: 17707,    tipo: 11.90 },
      { hasta: 20200,    tipo: 13.90 },
      { hasta: 33007,    tipo: 18.00 },
      { hasta: 53407,    tipo: 22.50 },
      { hasta: 65000,    tipo: 24.50 },
      { hasta: 80000,    tipo: 25.50 },
      { hasta: 120000,   tipo: 27.50 },
      { hasta: 175000,   tipo: 28.50 },
      { hasta: Infinity, tipo: 29.50 },
    ],
    tipoMaxAgregado: 54.00,
    notas: "Mayor presion fiscal de Espana. Tipo maximo agregado del 54%. Amplio catalogo de deducciones para compensar.",
  },
  galicia: {
    nombre: "Galicia",
    tramos: [
      { hasta: 12450,    tipo: 9.00 },
      { hasta: 20200,    tipo: 11.50 },
      { hasta: 35200,    tipo: 14.50 },
      { hasta: 60000,    tipo: 18.50 },
      { hasta: Infinity, tipo: 22.50 },
    ],
    tipoMaxAgregado: 47.00,
    notas: "Deflacto los 3 primeros tramos en 2022. Tipo minimo del 9%.",
  },
  aragon: {
    nombre: "Aragon",
    tramos: [
      { hasta: 12450,    tipo: 9.50 },
      { hasta: 14000,    tipo: 11.00 },
      { hasta: 20200,    tipo: 13.00 },
      { hasta: 25000,    tipo: 15.20 },
      { hasta: 35200,    tipo: 16.50 },
      { hasta: 50000,    tipo: 19.00 },
      { hasta: 60000,    tipo: 21.00 },
      { hasta: 70000,    tipo: 22.50 },
      { hasta: Infinity, tipo: 25.50 },
    ],
    tipoMaxAgregado: 50.00,
    notas: "9 tramos, busca mayor progresividad. Deflactacion aplicada en 2025.",
  },
  castilla_leon: {
    nombre: "Castilla y Leon",
    tramos: [
      { hasta: 12450,    tipo: 9.00 },
      { hasta: 20200,    tipo: 12.00 },
      { hasta: 35200,    tipo: 14.00 },
      { hasta: 53407,    tipo: 18.50 },
      { hasta: Infinity, tipo: 21.50 },
    ],
    tipoMaxAgregado: 46.00,
    notas: "5 tramos. Tipo maximo relativamente moderado (21,5%).",
  },
  castilla_mancha: {
    nombre: "Castilla-La Mancha",
    tramos: [
      { hasta: 12450,    tipo: 9.50 },
      { hasta: 20200,    tipo: 12.00 },
      { hasta: 35200,    tipo: 15.00 },
      { hasta: 60000,    tipo: 18.50 },
      { hasta: Infinity, tipo: 22.50 },
    ],
    tipoMaxAgregado: 47.00,
    notas: "Deducciones significativas por despoblacion (hasta 25% del IRPF).",
  },
  extremadura: {
    nombre: "Extremadura",
    tramos: [
      { hasta: 12450,    tipo: 8.00 },
      { hasta: 15000,    tipo: 10.50 },
      { hasta: 20200,    tipo: 13.00 },
      { hasta: 25000,    tipo: 15.50 },
      { hasta: 35200,    tipo: 17.00 },
      { hasta: 45000,    tipo: 19.00 },
      { hasta: 60000,    tipo: 21.00 },
      { hasta: 80000,    tipo: 23.00 },
      { hasta: Infinity, tipo: 25.00 },
    ],
    tipoMaxAgregado: 49.50,
    notas: "9 tramos. Tipo minimo bajo (8%) pero maximo elevado (25%).",
  },
  baleares: {
    nombre: "Illes Balears",
    tramos: [
      { hasta: 10000,    tipo: 9.00 },
      { hasta: 12450,    tipo: 9.00 },
      { hasta: 18000,    tipo: 11.25 },
      { hasta: 20200,    tipo: 13.25 },
      { hasta: 30000,    tipo: 14.75 },
      { hasta: 40000,    tipo: 17.25 },
      { hasta: 50000,    tipo: 19.25 },
      { hasta: 70000,    tipo: 21.50 },
      { hasta: Infinity, tipo: 24.75 },
    ],
    tipoMaxAgregado: 49.25,
    notas: "9 tramos. Reduccion de 0,5 puntos en bases <= 30.000 EUR (desde 2024).",
  },
  canarias: {
    nombre: "Canarias",
    tramos: [
      { hasta: 12450,    tipo: 9.00 },
      { hasta: 17707,    tipo: 11.50 },
      { hasta: 20200,    tipo: 14.00 },
      { hasta: 33007,    tipo: 15.00 },
      { hasta: 53407,    tipo: 19.50 },
      { hasta: 90000,    tipo: 23.50 },
      { hasta: Infinity, tipo: 26.00 },
    ],
    tipoMaxAgregado: 50.00,
    notas: "IGIC en lugar de IVA (7%). Reserva para Inversiones en Canarias (RIC). ZEC con IS al 4%.",
  },
  murcia: {
    nombre: "Region de Murcia",
    tramos: [
      { hasta: 12450,    tipo: 9.50 },
      { hasta: 20200,    tipo: 12.00 },
      { hasta: 35200,    tipo: 15.00 },
      { hasta: 60000,    tipo: 18.50 },
      { hasta: Infinity, tipo: 22.50 },
    ],
    tipoMaxAgregado: 47.00,
    notas: "Deflactacion automatica si IPC >3% (Ley 9/2025).",
  },
  asturias: {
    nombre: "Principado de Asturias",
    tramos: [
      { hasta: 12450,    tipo: 9.00 },
      { hasta: 17707,    tipo: 12.00 },
      { hasta: 20200,    tipo: 14.00 },
      { hasta: 33007,    tipo: 15.00 },
      { hasta: 53407,    tipo: 19.50 },
      { hasta: 70000,    tipo: 22.50 },
      { hasta: 90000,    tipo: 24.50 },
      { hasta: Infinity, tipo: 26.00 },
    ],
    tipoMaxAgregado: 50.00,
    notas: "Tipo minimo reducido al 9% desde 2025. 8 tramos.",
  },
  cantabria: {
    nombre: "Cantabria",
    tramos: [
      { hasta: 12450,    tipo: 8.50 },
      { hasta: 20200,    tipo: 11.50 },
      { hasta: 35200,    tipo: 15.00 },
      { hasta: 46000,    tipo: 18.50 },
      { hasta: 65000,    tipo: 22.00 },
      { hasta: Infinity, tipo: 24.50 },
    ],
    tipoMaxAgregado: 49.00,
    notas: "6 tramos. Tipo minimo bajo (8,5%).",
  },
  la_rioja: {
    nombre: "La Rioja",
    tramos: [
      { hasta: 12450,    tipo: 8.00 },
      { hasta: 15000,    tipo: 10.60 },
      { hasta: 20200,    tipo: 14.00 },
      { hasta: 25000,    tipo: 16.50 },
      { hasta: 35200,    tipo: 18.00 },
      { hasta: 60000,    tipo: 19.50 },
      { hasta: Infinity, tipo: 27.00 },
    ],
    tipoMaxAgregado: 51.50,
    notas: "7 tramos. Tipo maximo autonómico elevado (27%), solo para >60.000 EUR.",
  },
  navarra: {
    nombre: "Navarra (Regimen Foral)",
    tramos: [
      { hasta: 4484,     tipo: 13.00 },
      { hasta: 8968,     tipo: 22.00 },
      { hasta: 17452,    tipo: 25.00 },
      { hasta: 29889,    tipo: 28.00 },
      { hasta: 45427,    tipo: 35.50 },
      { hasta: 77658,    tipo: 40.00 },
      { hasta: 116487,   tipo: 45.00 },
      { hasta: 311023,   tipo: 49.00 },
      { hasta: Infinity, tipo: 52.00 },
    ],
    tipoMaxAgregado: 52.00,
    esForal: true,
    notas: "IRPF foral propio (no se suma estatal + autonomico). Tipo unico foral.",
  },
  pais_vasco: {
    nombre: "Pais Vasco (Regimen Foral)",
    tramos: [
      { hasta: 17360,    tipo: 23.00 },
      { hasta: 34720,    tipo: 28.00 },
      { hasta: 52080,    tipo: 35.00 },
      { hasta: 69440,    tipo: 40.00 },
      { hasta: 86800,    tipo: 45.00 },
      { hasta: 173600,   tipo: 49.00 },
      { hasta: Infinity, tipo: 49.00 },
    ],
    tipoMaxAgregado: 49.00,
    esForal: true,
    notas: "IRPF foral propio (Bizkaia). Cada Territorio Historico tiene su escala. Deflactacion del 2% en 2025.",
  },
};

// ============================================================
// TRAMOS BASE DEL AHORRO (comun a toda Espana)
// ============================================================

const TRAMOS_AHORRO = [
  { hasta: 6000,     tipo: 19 },
  { hasta: 50000,    tipo: 21 },
  { hasta: 200000,   tipo: 23 },
  { hasta: 300000,   tipo: 27 },
  { hasta: Infinity, tipo: 28 },
];

// ============================================================
// RETENCIONES
// ============================================================

const RETENCIONES = {
  profesionalGeneral: 15,
  nuevoAutonomo: 7,     // primeros 3 años
  empresario: 0,         // seccion 1a IAE
  alquilerLocal: 19,
  modulosAgricola: 2,
};

// ============================================================
// GASTOS DEDUCIBLES - LIMITES Y PORCENTAJES
// ============================================================

const GASTOS_DEDUCIBLES = {
  cuotaAutonomos: { porcentaje: 100, descripcion: "Cuota mensual Seguridad Social" },
  suministrosHogar: {
    porcentaje: 30,
    descripcion: "Luz, agua, internet, gas (proporcion m2 afectos x 30%)",
    formula: "(m2_actividad / m2_totales) * 0.30 * factura"
  },
  telefonoMixto: { porcentaje: 50, descripcion: "Movil uso personal + profesional" },
  telefonoExclusivo: { porcentaje: 100, descripcion: "Linea exclusivamente profesional" },
  dietaSinPernocta: { limiteEspana: 26.67, limiteExtranjero: 48.05 },
  dietaConPernocta: { limiteEspana: 53.34, limiteExtranjero: 91.35 },
  kmVehiculo: 0.26, // EUR/km sin IVA
  seguroMedico: { limitePorPersona: 500, limiteDiscapacidad: 1500 },
  gastosDificilJustificacion: { porcentaje: 5, limite: 2000 },
  amortizaciones: {
    equiposInformaticos: { coeficiente: 25, anos: 4 },
    mobiliario: { coeficiente: 10, anos: 10 },
    software: { coeficiente: 33, anos: 3 },
    vehiculo: { coeficiente: 16, anos: 6.25 },
    maquinaria: { coeficiente: 12, anos: 8 },
    utillaje: { coeficiente: 30, anos: 3.33 },
  },
  cuotasColegiosProfesionales: { limite: 500 },
};

// ============================================================
// MINIMOS PERSONALES Y FAMILIARES 2026
// ============================================================

const MINIMOS = {
  personal: 5550,
  mayor65: 6700,       // +1150
  mayor75: 8100,       // +1400 adicional
  discapacidad33_65: 3000,
  discapacidadMas65: 12000,
  primerHijo: 2400,
  segundoHijo: 2700,
  tercerHijo: 4000,
  cuartoYSiguientes: 4500,
  hijoMenor3: 2800,    // adicional
  ascendienteMayor65: 1150,
  ascendienteMayor75: 2550, // 1150 + 1400
};

// ============================================================
// DEDUCCIONES AUTONOMICAS POR CCAA
// ============================================================

const DEDUCCIONES_AUTONOMICAS = {
  madrid: {
    nombre: "Comunidad de Madrid",
    deducciones: [
      { id: "mad_nacimiento", nombre: "Nacimiento o adopcion de hijo", importe: 721.70, tipo: "fija", categoria: "familia", detalle: "Por cada hijo. Incrementos en partos multiples." },
      { id: "mad_adopcion_int", nombre: "Adopcion internacional", importe: 721.70, tipo: "fija", categoria: "familia", detalle: "Por cada hijo adoptado internacionalmente." },
      { id: "mad_acogimiento", nombre: "Acogimiento de menores", importeMin: 618.60, importeMax: 927.90, tipo: "variable", categoria: "familia", detalle: "Segun orden del menor acogido." },
      { id: "mad_acogimiento_mayores", nombre: "Acogimiento mayores 65+ o discapacidad", importe: 1546.50, tipo: "fija", categoria: "familia", detalle: "Por cada persona acogida no remuneradamente." },
      { id: "mad_alquiler_joven", nombre: "Alquiler vivienda jovenes (<35)", importeMax: 1000, tipo: "hasta", categoria: "vivienda", detalle: "Deduccion por alquiler de vivienda habitual." },
      { id: "mad_gastos_educativos", nombre: "Gastos educativos", porcentaje: 15, tipo: "porcentaje", categoria: "educacion", detalle: "Uniformes, ensenanza de idiomas, guarderias." },
      { id: "mad_business_angel", nombre: "Inversion empresas nueva creacion", porcentaje: 50, tipo: "porcentaje", categoria: "emprendimiento", detalle: "50% sobre base max 100.000 EUR/ano.", baseMax: 100000 },
      { id: "mad_partidos", nombre: "Cuotas partidos politicos", porcentaje: 20, tipo: "porcentaje", categoria: "otros", detalle: "20% sobre max 600 EUR.", baseMax: 600 },
    ]
  },
  cataluna: {
    nombre: "Cataluna",
    deducciones: [
      { id: "cat_nacimiento", nombre: "Nacimiento o adopcion", importe: 150, tipo: "fija", categoria: "familia", detalle: "Por cada hijo nacido o adoptado." },
      { id: "cat_alquiler", nombre: "Alquiler vivienda habitual", porcentaje: 10, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 300 EUR (600 EUR si discapacidad). Limite renta.", baseMax: 3000 },
      { id: "cat_donativos", nombre: "Donativos entidades catalanas", porcentaje: 15, tipo: "porcentaje", categoria: "donativos", detalle: "Donativos a entidades de fomento lengua catalana." },
      { id: "cat_rehabilitacion", nombre: "Rehabilitacion vivienda habitual", porcentaje: 1.5, tipo: "porcentaje", categoria: "vivienda", detalle: "1,5% de las cantidades invertidas." },
      { id: "cat_interes_estudios", nombre: "Intereses prestamos master/doctorado", importe: 3000, tipo: "hasta", categoria: "educacion", detalle: "Intereses de prestamos para estudios de master y doctorado." },
    ]
  },
  andalucia: {
    nombre: "Andalucia",
    deducciones: [
      { id: "and_empleada_hogar", nombre: "Empleados del hogar", porcentaje: 15, tipo: "porcentaje", categoria: "familia", detalle: "Para padres con derecho a minimo por descendientes.", baseMax: 500 },
      { id: "and_discapacidad_conyuge", nombre: "Discapacidad conyugue >=65%", importe: 100, tipo: "fija", categoria: "discapacidad", detalle: "Limite BI: 25.000 ind. / 30.000 conjunta." },
      { id: "and_libros_texto", nombre: "Libros de texto y material escolar", importeMax: 150, tipo: "hasta", categoria: "educacion", detalle: "Por hijo en edad escolar. Segun renta." },
      { id: "and_guarderia", nombre: "Gastos de guarderia", porcentaje: 15, tipo: "porcentaje", categoria: "familia", detalle: "Custodia menores de 3 anos." },
      { id: "and_eficiencia", nombre: "Eficiencia energetica vivienda", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Obras de mejora energetica." },
      { id: "and_donativos_medioamb", nombre: "Donativos medioambientales", porcentaje: 10, tipo: "porcentaje", categoria: "donativos", detalle: "A entidades publicas andaluzas." },
      { id: "and_vivienda_joven", nombre: "Vivienda habitual jovenes (<35)", porcentaje: 5, tipo: "porcentaje", categoria: "vivienda", detalle: "Adquisicion primera vivienda." },
    ]
  },
  valencia: {
    nombre: "Comunitat Valenciana",
    deducciones: [
      { id: "val_nacimiento", nombre: "Nacimiento/adopcion/acogimiento", importe: 270, tipo: "fija", categoria: "familia", detalle: "Por cada hijo. Incrementos multiples." },
      { id: "val_familia_numerosa", nombre: "Familia numerosa", importe: 300, tipo: "fija", categoria: "familia", detalle: "Categoria general. 600 EUR especial." },
      { id: "val_monoparental", nombre: "Familia monoparental", importe: 300, tipo: "fija", categoria: "familia", detalle: "300 EUR por contribuyente." },
      { id: "val_discapacidad", nombre: "Discapacidad", importe: 179, tipo: "fija", categoria: "discapacidad", detalle: ">=33%. Incrementos segun grado." },
      { id: "val_alquiler", nombre: "Alquiler vivienda habitual", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 550 EUR. Requisitos de renta." },
      { id: "val_guarderia", nombre: "Guarderias 0-3 anos", porcentaje: 15, tipo: "porcentaje", categoria: "familia", detalle: "Gastos de custodia en centros autorizados." },
      { id: "val_eficiencia", nombre: "Eficiencia energetica", porcentaje: 20, tipo: "porcentaje", categoria: "vivienda", detalle: "Instalaciones autoconsumo, placas solares, etc." },
      { id: "val_sanitarios", nombre: "Gastos sanitarios (nueva 2026)", porcentaje: 100, tipo: "porcentaje", categoria: "salud", detalle: "DL 1/2026. Gastos sanitarios no cubiertos." },
      { id: "val_deporte", nombre: "Actividades deportivas (nueva 2026)", porcentaje: 100, tipo: "porcentaje", categoria: "salud", detalle: "DL 1/2026. Practica deportiva y habitos saludables." },
      { id: "val_dana", nombre: "Deducciones especiales DANA", importe: 0, tipo: "variable", categoria: "otros", detalle: "Deducciones extraordinarias por afectados DANA." },
    ]
  },
  galicia: {
    nombre: "Galicia",
    deducciones: [
      { id: "gal_nacimiento", nombre: "Nacimiento/adopcion", importe: 360, tipo: "fija", categoria: "familia", detalle: "Por cada hijo." },
      { id: "gal_libros", nombre: "Libros de texto", importeMax: 150, tipo: "hasta", categoria: "educacion", detalle: "Por hijo en edad escolar." },
      { id: "gal_empleada_hogar", nombre: "Empleados del hogar", porcentaje: 30, tipo: "porcentaje", categoria: "familia", detalle: "Cuidado hijos." },
      { id: "gal_guarderia", nombre: "Guarderia", porcentaje: 30, tipo: "porcentaje", categoria: "familia", detalle: "Gastos de guarderia." },
      { id: "gal_eficiencia", nombre: "Eficiencia energetica", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Obras de mejora." },
      { id: "gal_viudedad", nombre: "Viudedad", importe: 300, tipo: "fija", categoria: "familia", detalle: "Contribuyentes viudos." },
      { id: "gal_alquiler", nombre: "Alquiler vivienda habitual", porcentaje: 10, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 300 EUR. Menores de 35 anos." },
    ]
  },
  aragon: {
    nombre: "Aragon",
    deducciones: [
      { id: "ara_nacimiento_1", nombre: "Nacimiento 1er hijo", importe: 100, tipo: "fija", categoria: "familia", detalle: "200 EUR si BI <23.000 ind. Hasta 720 EUR en zona despoblacion." },
      { id: "ara_nacimiento_2", nombre: "Nacimiento 2o hijo", importe: 150, tipo: "fija", categoria: "familia", detalle: "300 EUR si BI <23.000 ind." },
      { id: "ara_discapacidad_hijo", nombre: "Hijo con discapacidad >=33%", importe: 200, tipo: "fija", categoria: "discapacidad", detalle: "+20% si zona de despoblacion." },
      { id: "ara_libros", nombre: "Libros de texto y material escolar", importeMax: 75, tipo: "hasta", categoria: "educacion", detalle: "Por hijo. Segun nivel de renta." },
      { id: "ara_guarderia", nombre: "Guarderia menores de 3 anos", porcentaje: 15, tipo: "porcentaje", categoria: "familia", detalle: "Gastos de custodia." },
      { id: "ara_alquiler", nombre: "Alquiler vivienda habitual", porcentaje: 10, tipo: "porcentaje", categoria: "vivienda", detalle: "Para menores de 35 anos o con discapacidad." },
      { id: "ara_despoblacion", nombre: "Residencia en zona despoblacion", importe: 600, tipo: "fija", categoria: "territorio", detalle: "Hasta 720 EUR en riesgo extremo." },
    ]
  },
  castilla_leon: {
    nombre: "Castilla y Leon",
    deducciones: [
      { id: "cyl_familia_numerosa", nombre: "Familia numerosa", importe: 500, tipo: "fija", categoria: "familia", detalle: "Categoria general. Incrementos." },
      { id: "cyl_nacimiento", nombre: "Nacimiento/adopcion", importe: 710, tipo: "fija", categoria: "familia", detalle: "Por cada hijo." },
      { id: "cyl_vivienda", nombre: "Adquisicion vivienda habitual", porcentaje: 7.5, tipo: "porcentaje", categoria: "vivienda", detalle: "Jovenes <36 anos en municipios rurales." },
      { id: "cyl_alquiler", nombre: "Alquiler vivienda", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Jovenes menores de 36 anos." },
      { id: "cyl_cuidado_hijos", nombre: "Cuidado hijos <4 anos", importeMax: 1320, tipo: "hasta", categoria: "familia", detalle: "Por gastos de cuidado infantil." },
      { id: "cyl_empresa", nombre: "Inversion empresas nueva creacion", porcentaje: 20, tipo: "porcentaje", categoria: "emprendimiento", detalle: "Hasta 10.000 EUR de base." },
    ]
  },
  castilla_mancha: {
    nombre: "Castilla-La Mancha",
    deducciones: [
      { id: "clm_nacimiento", nombre: "Nacimiento/adopcion", importe: 100, tipo: "fija", categoria: "familia", detalle: "1er hijo. 500 EUR si 2 hijos en el ano." },
      { id: "clm_libros", nombre: "Libros de texto e idiomas", importeMax: 150, tipo: "hasta", categoria: "educacion", detalle: "Gastos educativos." },
      { id: "clm_idi", nombre: "Donaciones I+D+i", porcentaje: 15, tipo: "porcentaje", categoria: "donativos", detalle: "Investigacion y desarrollo." },
      { id: "clm_cooperacion", nombre: "Cooperacion internacional", porcentaje: 15, tipo: "porcentaje", categoria: "donativos", detalle: "Donativos a ONG cooperacion." },
      { id: "clm_alquiler_joven", nombre: "Alquiler vivienda <36 anos", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "BI max 12.500 ind. / 25.000 conjunta." },
      { id: "clm_despoblacion", nombre: "Residencia zona despoblada", porcentaje: 25, tipo: "porcentaje", categoria: "territorio", detalle: "Hasta 25% del IRPF por residencia efectiva." },
      { id: "clm_inversion_social", nombre: "Inversion en economia social", porcentaje: 20, tipo: "porcentaje", categoria: "emprendimiento", detalle: "Participaciones en cooperativas, etc." },
      { id: "clm_vivienda_rural", nombre: "Vivienda en zona rural", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Adquisicion o rehabilitacion." },
    ]
  },
  extremadura: {
    nombre: "Extremadura",
    deducciones: [
      { id: "ext_nacimiento", nombre: "Nacimiento/adopcion", importe: 300, tipo: "fija", categoria: "familia", detalle: "Por hijo." },
      { id: "ext_alquiler", nombre: "Alquiler vivienda habitual", porcentaje: 5, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 300 EUR." },
      { id: "ext_renovables", nombre: "Energias renovables", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Inversion en nuevas tecnologias y renovables." },
      { id: "ext_historicos", nombre: "Rehabilitacion inmuebles historicos", porcentaje: 5, tipo: "porcentaje", categoria: "vivienda", detalle: "Patrimonio historico." },
      { id: "ext_agraria", nombre: "Inversion empresa agraria", porcentaje: 20, tipo: "porcentaje", categoria: "emprendimiento", detalle: "Empresas agrarias extremenas." },
      { id: "ext_aldea_modelo", nombre: "Proyectos aldeas modelo", porcentaje: 15, tipo: "porcentaje", categoria: "territorio", detalle: "Inversion en aldeas modelo." },
      { id: "ext_municipio_pequeno", nombre: "Residencia municipio <3.000 hab.", importe: 300, tipo: "fija", categoria: "territorio", detalle: "Residencia habitual en pequenos municipios." },
    ]
  },
  baleares: {
    nombre: "Illes Balears",
    deducciones: [
      { id: "bal_nacimiento_1", nombre: "Nacimiento 1er hijo", importe: 800, tipo: "fija", categoria: "familia", detalle: "BI max 52.800 ind. / 84.480 conjunta." },
      { id: "bal_nacimiento_2", nombre: "Nacimiento 2o hijo", importe: 1000, tipo: "fija", categoria: "familia", detalle: "" },
      { id: "bal_nacimiento_3", nombre: "Nacimiento 3er hijo", importe: 1200, tipo: "fija", categoria: "familia", detalle: "" },
      { id: "bal_nacimiento_4", nombre: "Nacimiento 4o+ hijo", importe: 1400, tipo: "fija", categoria: "familia", detalle: "" },
      { id: "bal_sostenibilidad", nombre: "Sostenibilidad vivienda", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Mejoras sostenibilidad." },
      { id: "bal_investigacion", nombre: "Donativos investigacion", porcentaje: 25, tipo: "porcentaje", categoria: "donativos", detalle: "Entidades de investigacion." },
      { id: "bal_catalan", nombre: "Fomento lengua catalana", porcentaje: 15, tipo: "porcentaje", categoria: "donativos", detalle: "Donativos a entidades." },
      { id: "bal_material_escolar", nombre: "Material escolar", importeMax: 200, tipo: "hasta", categoria: "educacion", detalle: "Libros y material." },
      { id: "bal_alquiler", nombre: "Alquiler vivienda", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 530 EUR." },
    ]
  },
  canarias: {
    nombre: "Canarias",
    deducciones: [
      { id: "can_nacimiento", nombre: "Nacimiento/adopcion", importe: 200, tipo: "fija", categoria: "familia", detalle: "Por hijo." },
      { id: "can_enfermedad", nombre: "Gastos de enfermedad", porcentaje: 10, tipo: "porcentaje", categoria: "salud", detalle: "Gastos medicos no cubiertos." },
      { id: "can_familia_numerosa", nombre: "Familia numerosa", importe: 500, tipo: "fija", categoria: "familia", detalle: "Categoria general." },
      { id: "can_discapacidad", nombre: "Discapacidad", importe: 300, tipo: "fija", categoria: "discapacidad", detalle: ">=33%." },
      { id: "can_alquiler", nombre: "Alquiler vivienda", porcentaje: 15, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 500 EUR." },
      { id: "can_guarderia", nombre: "Gastos guarderia", porcentaje: 15, tipo: "porcentaje", categoria: "familia", detalle: "Menores de 3 anos." },
      { id: "can_ric", nombre: "Reserva Inversiones Canarias (RIC)", porcentaje: 100, tipo: "porcentaje", categoria: "emprendimiento", detalle: "Beneficios no distribuidos para inversion." },
    ]
  },
  murcia: {
    nombre: "Region de Murcia",
    deducciones: [
      { id: "mur_agua", nombre: "Dispositivos ahorro de agua", porcentaje: 20, tipo: "porcentaje", categoria: "vivienda", detalle: "Dispositivos domesticos." },
      { id: "mur_internet", nombre: "Gastos acceso a Internet", porcentaje: 10, tipo: "porcentaje", categoria: "otros", detalle: "Linea de internet en vivienda." },
      { id: "mur_libros", nombre: "Libros texto, idiomas, educacion", importeMax: 120, tipo: "hasta", categoria: "educacion", detalle: "Material educativo." },
      { id: "mur_hijos_3", nombre: "Cuidado hijos <3 anos", porcentaje: 15, tipo: "porcentaje", categoria: "familia", detalle: "Gastos guarderia/cuidadores." },
      { id: "mur_dependientes", nombre: "Mayores dependientes", importe: 100, tipo: "fija", categoria: "familia", detalle: "Ascendientes dependientes." },
      { id: "mur_discapacidad", nombre: "Personas con discapacidad", importe: 120, tipo: "fija", categoria: "discapacidad", detalle: "A cargo del contribuyente." },
    ]
  },
  asturias: {
    nombre: "Principado de Asturias",
    deducciones: [
      { id: "ast_alquiler", nombre: "Arrendamiento vivienda habitual", porcentaje: 10, tipo: "porcentaje", categoria: "vivienda", detalle: "Hasta 500 EUR." },
      { id: "ast_vivienda_joven", nombre: "Vivienda habitual jovenes", porcentaje: 5, tipo: "porcentaje", categoria: "vivienda", detalle: "Adquisicion/rehabilitacion." },
      { id: "ast_discapacidad_viv", nombre: "Vivienda discapacitados", porcentaje: 3, tipo: "porcentaje", categoria: "discapacidad", detalle: "Adquisicion/adecuacion." },
      { id: "ast_forestal", nombre: "Gestion forestal sostenible", porcentaje: 30, tipo: "porcentaje", categoria: "territorio", detalle: "Certificacion forestal." },
      { id: "ast_despoblacion", nombre: "Residencia concejos despoblacion", importe: 500, tipo: "fija", categoria: "territorio", detalle: "Concejos con riesgo." },
      { id: "ast_formacion", nombre: "Formacion laboral", porcentaje: 30, tipo: "porcentaje", categoria: "educacion", detalle: "Incorporacion al mercado laboral." },
      { id: "ast_electrico", nombre: "Vehiculo electrico", porcentaje: 15, tipo: "porcentaje", categoria: "otros", detalle: "Compra de vehiculo electrico." },
      { id: "ast_transporte", nombre: "Transporte publico (despoblacion)", porcentaje: 15, tipo: "porcentaje", categoria: "territorio", detalle: "Residentes en zonas despoblacion." },
      { id: "ast_ela", nombre: "Subvenciones/ayudas ELA", porcentaje: 100, tipo: "porcentaje", categoria: "salud", detalle: "Enfermos de ELA." },
    ]
  },
  cantabria: {
    nombre: "Cantabria",
    deducciones: [
      { id: "cnt_nacimiento", nombre: "Nacimiento/adopcion", importe: 300, tipo: "fija", categoria: "familia", detalle: "Por hijo." },
      { id: "cnt_educativos", nombre: "Gastos educativos y guarderia", porcentaje: 15, tipo: "porcentaje", categoria: "educacion", detalle: "Incluye guarderia." },
      { id: "cnt_familia_numerosa", nombre: "Familia numerosa", importe: 300, tipo: "fija", categoria: "familia", detalle: "Categoria general." },
      { id: "cnt_monoparental", nombre: "Familia monoparental", importe: 200, tipo: "fija", categoria: "familia", detalle: "Familia monoparental." },
      { id: "cnt_donativos", nombre: "Donativos fundaciones / Cantabria Coopera", porcentaje: 15, tipo: "porcentaje", categoria: "donativos", detalle: "Donativos a fundaciones cantabras." },
      { id: "cnt_traslado_rural", nombre: "Traslado estudios zona rural", importeMax: 1000, tipo: "hasta", categoria: "territorio", detalle: "Municipios con reto demografico." },
      { id: "cnt_alquiler_rural", nombre: "Alquiler vivienda zona rural", porcentaje: 10, tipo: "porcentaje", categoria: "territorio", detalle: "Zonas con reto demografico." },
    ]
  },
  la_rioja: {
    nombre: "La Rioja",
    deducciones: [
      { id: "rio_hijos_3", nombre: "Hijos menores de 3 anos", importe: 150, tipo: "fija", categoria: "familia", detalle: "Por cada hijo <3." },
      { id: "rio_vivienda_rural", nombre: "Vivienda en pequenos municipios", porcentaje: 5, tipo: "porcentaje", categoria: "vivienda", detalle: "Adquisicion/construccion/rehabilitacion." },
      { id: "rio_escuela_infantil", nombre: "Escuela infantil", porcentaje: 30, tipo: "porcentaje", categoria: "familia", detalle: "Gastos en escuelas infantiles autorizadas." },
      { id: "rio_acogimiento", nombre: "Acogimiento familiar", importe: 300, tipo: "fija", categoria: "familia", detalle: "Por acogimiento de menores." },
      { id: "rio_internet_joven", nombre: "Internet jovenes emancipados", porcentaje: 30, tipo: "porcentaje", categoria: "otros", detalle: "Gastos de acceso a Internet." },
      { id: "rio_suministros_joven", nombre: "Luz y gas jovenes emancipados", porcentaje: 15, tipo: "porcentaje", categoria: "otros", detalle: "Suministros domesticos." },
      { id: "rio_bicicleta", nombre: "Bicicleta pedaleo no asistido", porcentaje: 15, tipo: "porcentaje", categoria: "otros", detalle: "Compra de bicicleta no electrica." },
      { id: "rio_electrico", nombre: "Vehiculo electrico", porcentaje: 15, tipo: "porcentaje", categoria: "otros", detalle: "Compra de vehiculo electrico." },
    ]
  },
  navarra: {
    nombre: "Navarra (Regimen Foral)",
    deducciones: [
      { id: "nav_info", nombre: "Normativa foral propia", importe: 0, tipo: "info", categoria: "otros", detalle: "Navarra tiene su propia Hacienda Foral con deducciones especificas. Consultar Hacienda Foral de Navarra." },
    ]
  },
  pais_vasco: {
    nombre: "Pais Vasco (Regimen Foral)",
    deducciones: [
      { id: "pv_info", nombre: "Normativa foral propia", importe: 0, tipo: "info", categoria: "otros", detalle: "Cada Territorio Historico (Alava, Bizkaia, Gipuzkoa) tiene sus propias deducciones. Consultar Diputaciones Forales." },
    ]
  },
};

// ============================================================
// CALENDARIO FISCAL 2026
// ============================================================

const CALENDARIO_FISCAL = [
  { fecha: "2026-01-27", modelo: "Varios", descripcion: "Ultimo dia domiciliacion 4T 2025", tipo: "domiciliacion" },
  { fecha: "2026-01-30", modelo: "303/130/131/390/190", descripcion: "Declaraciones 4T 2025 + resumen anual IVA + retenciones", tipo: "trimestral" },
  { fecha: "2026-02-28", modelo: "347", descripcion: "Declaracion operaciones con terceros >3.005,06 EUR", tipo: "anual" },
  { fecha: "2026-04-08", modelo: "100", descripcion: "Inicio campana Renta 2025", tipo: "renta" },
  { fecha: "2026-04-15", modelo: "Varios", descripcion: "Ultimo dia domiciliacion 1T 2026", tipo: "domiciliacion" },
  { fecha: "2026-04-20", modelo: "303/130/131", descripcion: "Declaraciones 1T 2026 (IVA + IRPF)", tipo: "trimestral" },
  { fecha: "2026-06-30", modelo: "100", descripcion: "Fin campana Renta 2025", tipo: "renta" },
  { fecha: "2026-07-15", modelo: "Varios", descripcion: "Ultimo dia domiciliacion 2T 2026", tipo: "domiciliacion" },
  { fecha: "2026-07-20", modelo: "303/130/131", descripcion: "Declaraciones 2T 2026 (IVA + IRPF)", tipo: "trimestral" },
  { fecha: "2026-10-15", modelo: "Varios", descripcion: "Ultimo dia domiciliacion 3T 2026", tipo: "domiciliacion" },
  { fecha: "2026-10-20", modelo: "303/130/131", descripcion: "Declaraciones 3T 2026 (IVA + IRPF)", tipo: "trimestral" },
];

// ============================================================
// TIPOS IVA
// ============================================================

const TIPOS_IVA = {
  general: 21,
  reducido: 10,
  superreducido: 4,
  recargo_general: 5.2,
  recargo_reducido: 1.4,
  recargo_superreducido: 0.5,
};

// ============================================================
// CATEGORIAS DE GASTOS PARA SIMULADOR
// ============================================================

const CATEGORIAS_GASTOS = [
  { id: "cuota_ss", nombre: "Cuota autonomos (Seguridad Social)", deduccion: 100, iva: false, icono: "shield" },
  { id: "alquiler_local", nombre: "Alquiler local/oficina/coworking", deduccion: 100, iva: true, icono: "building" },
  { id: "suministros", nombre: "Suministros hogar (luz, agua, gas, internet)", deduccion: 30, iva: true, icono: "zap", nota: "Proporcion m2 afectos x 30%" },
  { id: "telefono", nombre: "Telefono movil", deduccion: 50, iva: true, icono: "phone", nota: "50% si uso mixto, 100% si exclusivo" },
  { id: "material_oficina", nombre: "Material de oficina y consumibles", deduccion: 100, iva: true, icono: "package" },
  { id: "equipos", nombre: "Equipos informaticos", deduccion: 100, iva: true, icono: "monitor", nota: "Amortizacion 25% anual si >300 EUR" },
  { id: "software", nombre: "Software y suscripciones", deduccion: 100, iva: true, icono: "code" },
  { id: "hosting", nombre: "Hosting, dominio, cloud", deduccion: 100, iva: true, icono: "cloud" },
  { id: "publicidad", nombre: "Publicidad y marketing", deduccion: 100, iva: true, icono: "megaphone" },
  { id: "formacion", nombre: "Formacion profesional", deduccion: 100, iva: true, icono: "book" },
  { id: "gestoria", nombre: "Gestoria/asesor fiscal/abogado", deduccion: 100, iva: true, icono: "briefcase" },
  { id: "seguros_rc", nombre: "Seguros (RC, local, actividad)", deduccion: 100, iva: false, icono: "shield" },
  { id: "seguro_medico", nombre: "Seguro medico privado", deduccion: 100, iva: false, icono: "heart", nota: "Max 500 EUR/persona (1500 discapacidad)" },
  { id: "dietas", nombre: "Dietas y manutencion", deduccion: 100, iva: true, icono: "utensils", nota: "26,67 EUR/dia (sin pernocta)" },
  { id: "desplazamientos", nombre: "Desplazamientos profesionales", deduccion: 100, iva: true, icono: "car", nota: "0,26 EUR/km o transporte publico" },
  { id: "vehiculo", nombre: "Vehiculo (uso exclusivo profesional)", deduccion: 100, iva: true, icono: "truck", nota: "Solo si uso 100% profesional" },
  { id: "colegio_profesional", nombre: "Colegio profesional", deduccion: 100, iva: false, icono: "award", nota: "Hasta 500 EUR" },
  { id: "otros", nombre: "Otros gastos vinculados a actividad", deduccion: 100, iva: true, icono: "more" },
];
