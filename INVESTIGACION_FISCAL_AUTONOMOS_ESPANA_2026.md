# Investigacion Fiscal Exhaustiva: Autonomos en Espana 2026

> Documento de referencia para el desarrollo de una web de ayuda al autonomo espanol.
> Fecha de investigacion: 15 de marzo de 2026.

---

## INDICE

1. [Sistema de Cotizacion (Cuota de Autonomos)](#1-sistema-de-cotizacion-cuota-de-autonomos-2026)
2. [IRPF para Autonomos](#2-irpf-para-autonomos)
3. [Tramos Estatales del IRPF](#3-tramos-estatales-del-irpf-2026)
4. [Escalas Autonomicas del IRPF por Comunidad](#4-escalas-autonomicas-del-irpf-por-comunidad-autonoma)
5. [Regimenes de Estimacion (Directa vs Modulos)](#5-regimenes-de-estimacion)
6. [IVA para Autonomos](#6-iva-para-autonomos)
7. [Gastos Deducibles en IRPF](#7-gastos-deducibles-en-irpf)
8. [Deducciones Autonomicas por Comunidad](#8-deducciones-autonomicas-por-comunidad-autonoma)
9. [Calendario Fiscal](#9-calendario-fiscal-2026)
10. [VERI*FACTU y Facturacion Electronica](#10-verifactu-y-facturacion-electronica)
11. [Datos Utiles para la Web](#11-datos-utiles-para-la-web)
12. [Fuentes](#12-fuentes)

---

## 1. Sistema de Cotizacion (Cuota de Autonomos) 2026

### Como funciona

Desde enero de 2023 (Real Decreto-ley 13/2022), los autonomos cotizan por **ingresos reales**, no por libre eleccion de base. El sistema tiene un periodo de transicion de 9 anos (hasta 2032).

En 2026 se mantienen las mismas cuotas que en 2025 (prorroga aprobada por el Consejo de Ministros), salvo la subida del MEI (+0,1%).

### Tabla de cuotas 2026 (15 tramos)

| Tramo | Ingresos netos mensuales | Cuota minima mensual | Base minima | Base maxima |
|-------|--------------------------|----------------------|-------------|-------------|
| 1 | <= 670 EUR | 200 EUR | 653,59 EUR | 950,98 EUR |
| 2 | 670 - 900 EUR | 220 EUR | 718,95 EUR | 950,98 EUR |
| 3 | 900 - 1.166,70 EUR | 260 EUR | 849,67 EUR | 950,98 EUR |
| 4 | 1.166,70 - 1.300 EUR | 291 EUR | 950,98 EUR | 950,98 EUR |
| 5 | 1.300 - 1.500 EUR | 294 EUR | 960,78 EUR | 960,78 EUR |
| 6 | 1.500 - 1.700 EUR | 294 EUR | 960,78 EUR | 960,78 EUR |
| 7 | 1.700 - 1.850 EUR | 350 EUR | 1.143,79 EUR | 1.143,79 EUR |
| 8 | 1.850 - 2.030 EUR | 350 EUR | 1.143,79 EUR | 1.209,15 EUR |
| 9 | 2.030 - 2.330 EUR | 350 EUR | 1.143,79 EUR | 1.274,51 EUR |
| 10 | 2.330 - 2.760 EUR | 390 EUR | 1.274,51 EUR | 1.372,55 EUR |
| 11 | 2.760 - 3.190 EUR | 390 EUR | 1.274,51 EUR | 1.468,36 EUR |
| 12 | 3.190 - 3.620 EUR | 390 EUR | 1.274,51 EUR | 1.633,99 EUR |
| 13 | 3.620 - 4.050 EUR | 420 EUR | 1.372,55 EUR | 1.732,03 EUR |
| 14 | 4.050 - 6.000 EUR | 500 EUR | 1.633,99 EUR | 4.720,50 EUR |
| 15 | > 6.000 EUR | 590 EUR | 1.928,10 EUR | 4.720,50 EUR |

### Datos clave

- **Base minima general**: 950,98 EUR/mes
- **Base maxima general**: 4.720,50 EUR/mes
- **Tipo de cotizacion total**: 31,20% de la base elegida
- **MEI 2026**: 0,9% (incluido en el 31,20%). El autonomo lo asume integramente.
- **Tarifa plana nuevos autonomos**: 80 EUR/mes durante 12 meses. Prorrogable 12 meses mas si ingresos netos < SMI.
- **Cambios de base**: hasta 6 veces al ano, con efectos bimestrales.
- **Regularizacion anual**: si cotizaste de menos, pagas la diferencia; si de mas, te devuelven.

### Formula de calculo

```
Cuota mensual = Base de cotizacion elegida (dentro del tramo) x 31,20%
```

### Calculo de ingresos netos (rendimiento neto)

```
Rendimiento neto = Ingresos totales - Gastos deducibles
Rendimiento neto mensual = Rendimiento neto anual / 12
```

---

## 2. IRPF para Autonomos

### Conceptos fundamentales

- El IRPF es un impuesto **progresivo** sobre la renta de las personas fisicas.
- Se aplica sobre el **beneficio neto** (ingresos - gastos deducibles), NO sobre la facturacion bruta.
- Se compone de **dos tramos**: estatal (~50%) y autonomico (~50%).
- El tipo efectivo real es MENOR que el tipo marginal del tramo mas alto.
- **Minimo personal y familiar 2026**: 5.550 EUR (aumenta con edad >65/75, discapacidad, hijos/dependientes).

### Retenciones en facturas

| Tipo de autonomo | Retencion |
|-------------------|-----------|
| Profesional (seccion 2a/3a IAE) | **15%** |
| Nuevo autonomo (primeros 3 anos) | **7%** |
| Empresario (seccion 1a IAE) | **No retiene** en sus facturas |

### Pagos fraccionados trimestrales

- **Modelo 130** (estimacion directa): 20% del beneficio neto acumulado - retenciones - pagos anteriores
- **Modelo 131** (modulos): segun indices de la orden ministerial

---

## 3. Tramos Estatales del IRPF 2026

### Base imponible general (escala estatal)

| Base liquidable | Tipo estatal | Tipo acumulado estatal |
|-----------------|-------------|----------------------|
| 0 - 12.450 EUR | 9,50% | 9,50% |
| 12.450 - 20.200 EUR | 12,00% | - |
| 20.200 - 35.200 EUR | 15,00% | - |
| 35.200 - 60.000 EUR | 18,50% | - |
| 60.000 - 300.000 EUR | 22,50% | - |
| > 300.000 EUR | 24,50% | - |

> Nota: Los "tramos totales" que habitualmente se publican (19%, 24%, 30%, 37%, 45%, 47%) son la SUMA del estatal + el autonomico de referencia. Cada CCAA puede modificar su parte.

### Base del ahorro (comun a toda Espana)

| Base liquidable del ahorro | Tipo |
|----------------------------|------|
| 0 - 6.000 EUR | 19% |
| 6.000 - 50.000 EUR | 21% |
| 50.000 - 200.000 EUR | 23% |
| 200.000 - 300.000 EUR | 27% |
| > 300.000 EUR | 28% |

---

## 4. Escalas Autonomicas del IRPF por Comunidad Autonoma

### Tabla resumen comparativa

| Comunidad Autonoma | N tramos | Tipo min. auton. | Tipo max. auton. | Tipo max. agregado (est+aut) |
|---------------------|----------|------------------|------------------|-------------------------------|
| **Madrid** | 5 | 8,50% | 20,50% | 45,00% |
| **Cataluna** | 8 | 10,50% | 25,50% | 50,00% |
| **Andalucia** | 5 | 9,50% | 22,50% | 47,00% |
| **C. Valenciana** | 10+ | 9,50% | 29,50% | 54,00% |
| **Galicia** | 5 | 9,00% | 22,50% | 47,00% |
| **Aragon** | 9 | 9,50% | 25,50% | 50,00% |
| **Castilla y Leon** | 5 | 9,00% | 21,50% | 46,00% |
| **Castilla-La Mancha** | 5 | 9,50% | 22,50% | 47,00% |
| **Extremadura** | 9 | 8,00% | 25,00% | 49,50% |
| **Illes Balears** | 9 | 9,00% | 24,75% | 49,25% |
| **Canarias** | 7 | 9,00% | 26,00% | 50,00%(*)  |
| **Region de Murcia** | 5 | 9,50% | 22,50% | 47,00% |
| **Asturias** | 8 | 9,00% | 26,00% | 50,00%(*)  |
| **Cantabria** | 6 | 8,50% | 24,50% | 49,00% |
| **La Rioja** | 7 | 8,00% | 27,00% | 51,50% |
| **Navarra** (foral) | Propio | Propio | Propio | 52,00% |
| **Pais Vasco** (foral) | Propio | Propio | Propio | 49,00% |

> (*) Valores aproximados. Consultar normativa especifica.

### Detalle: Comunidad de Madrid

| Base liquidable | Tipo autonomico |
|-----------------|-----------------|
| 0 - 12.960 EUR | 8,50% |
| 12.960 - 19.500 EUR | 10,70% |
| 19.500 - 35.500 EUR | 12,80% |
| 35.500 - 60.000 EUR | 17,40% |
| > 60.000 EUR | 20,50% |

Madrid aplica deflactacion y es la comunidad con menor presion fiscal en IRPF. Rebaja adicional de 0,5 puntos prevista para 2027.

### Detalle: Cataluna (8 tramos desde 2025)

| Base liquidable | Tipo autonomico |
|-----------------|-----------------|
| 0 - 12.450 EUR | 10,50% |
| 12.450 - 17.707 EUR | 12,00% |
| 17.707 - 21.000 EUR | 14,00% |
| 21.000 - 33.007 EUR | 15,00% |
| 33.007 - 53.407 EUR | 18,80% |
| 53.407 - 90.000 EUR | 21,50% |
| 90.000 - 120.000 EUR | 23,50% |
| > 120.000 EUR | 25,50% |

> Nota: Cataluna redujo de 9 a 8 tramos en 2025 (Decreto ley 5/2025). El tipo del primer tramo se redujo del 10,5% al 9,5% para bases hasta 12.450 EUR en un primer momento pero luego se mantuvo. Verificar normativa exacta publicada.

### Detalle: Andalucia (5 tramos)

| Base liquidable | Tipo autonomico |
|-----------------|-----------------|
| 0 - 12.450 EUR | 9,50% |
| 12.450 - 20.200 EUR | 12,00% |
| 20.200 - 35.200 EUR | 15,00% |
| 35.200 - 60.000 EUR | 18,50% |
| > 60.000 EUR | 22,50% |

### Regimen foral: Pais Vasco y Navarra

- **Navarra**: IRPF foral propio, tipo maximo agregado ~52%.
- **Pais Vasco** (Alava, Bizkaia, Gipuzkoa): IRPF foral propio por Territorio Historico. Deflactacion del 2% aplicada en 2025. Tipos muy reducidos para rentas bajas segun numero de descendientes (hasta 1%).
- Estos territorios NO se rigen por el catálogo de IRPF del regimen comun.

### Regimen especial: Ceuta y Melilla

- Deduccion del **60%** sobre la cuota integra correspondiente a rentas obtenidas en Ceuta/Melilla.
- Ademas, en IVA no aplica: se usa **IPSI** (Impuesto sobre la Produccion, los Servicios y la Importacion).

### Regimen especial: Canarias

- No aplica IVA: se usa **IGIC** (Impuesto General Indirecto Canario), tipo general **7%**.
- En IRPF: escala autonomica propia con deflactacion.
- Reserva para Inversiones en Canarias (RIC): permite deducir beneficios no distribuidos destinados a inversion.

---

## 5. Regimenes de Estimacion

### 5.1 Estimacion Directa Simplificada (la mas comun)

- **Requisito**: facturacion < 600.000 EUR/ano
- **Calculo**: Ingresos reales - Gastos reales = Beneficio neto
- **Gastos de dificil justificacion**: 5% del rendimiento neto, maximo 2.000 EUR (sin necesidad de facturas)
- **Contabilidad**: libros de ingresos, gastos y bienes de inversion
- **Amortizaciones**: segun tablas de Hacienda simplificadas
- **Modelo trimestral**: 130

### 5.2 Estimacion Directa Normal

- **Obligatoria** si facturacion > 600.000 EUR/ano
- **Contabilidad completa** segun Plan General de Contabilidad y Codigo de Comercio
- **NO aplica** el 5% de gastos de dificil justificacion
- **Amortizaciones**: segun opciones del Impuesto de Sociedades
- **Modelo trimestral**: 130

### 5.3 Estimacion Objetiva (Modulos)

- **Calculo**: rendimiento "teorico" basado en indicadores (m2 local, empleados, potencia electrica, etc.)
- **Limite**: facturacion < 250.000 EUR (< 125.000 EUR si destinatario es empresario/profesional)
- **Solo actividades incluidas en la Orden Ministerial**: comercio minorista, bares, restaurantes, peluquerias, transporte, agricultura...
- **Riesgo**: puedes pagar impuestos aunque tengas perdidas
- **Modelo trimestral**: 131
- **IVA**: regimen simplificado de IVA (complementario)
- **Futuro incierto**: el Gobierno estudia eliminar los modulos

### Cambio de regimen

- Si renuncias a modulos para pasar a estimacion directa, no puedes volver en **3 anos**.
- Nuevas altas: estimacion directa simplificada por defecto (salvo que se elija modulos expresamente).

---

## 6. IVA para Autonomos

### Tipos de IVA vigentes en 2026

| Tipo | Porcentaje | Aplicacion |
|------|-----------|------------|
| **General** | 21% | Mayoria de productos y servicios |
| **Reducido** | 10% | Alimentos no basicos, transporte, hosteleria, reformas vivienda habitual, etc. |
| **Superreducido** | 4% | Pan, leche, huevos, frutas, verduras, medicamentos, libros, productos discapacidad |

### Regimenes especiales de IVA

1. **Regimen General**: el mas habitual. Declarar mediante modelo 303 (trimestral) + 390 (resumen anual).
2. **Regimen Simplificado**: para autonomos en modulos. IVA calculado por indices objetivos.
3. **Recargo de Equivalencia**: comerciantes minoristas. No presentan declaraciones de IVA; proveedores cobran recargo adicional (5,2% general, 1,4% reducido, 0,5% superreducido).
4. **Criterio de Caja**: IVA se declara al cobrar (no al facturar). Limite: facturacion < 2.000.000 EUR.
5. **Agricultura, Ganaderia y Pesca**: regimen compensatorio.
6. **Bienes Usados, Arte, Antiguedades**: regimen especifico.
7. **Agencias de Viaje**: margen de beneficio.
8. **Ventanilla Unica (OSS/IOSS)**: ventas online transfronterizas.
9. **Grupo de Entidades**: voluntario, para grupos empresariales.
10. **Regimen de Franquicia** (en desarrollo): liberaria de declarar IVA a autonomos con ingresos < 85.000 EUR. Aun no implementado.

### Actividades exentas de IVA (art. 20 Ley IVA)

- Ensenanza reglada y clases particulares de materias oficiales
- Sanidad (medicos, dentistas, psicologos, fisioterapeutas)
- Servicios sociales, culturales, deportivos (sin animo de lucro)
- Alquiler de vivienda para uso residencial
- Seguros y operaciones financieras

### Territorios con impuesto indirecto propio

| Territorio | Impuesto | Tipo general |
|------------|----------|-------------|
| **Canarias** | IGIC | 7% |
| **Ceuta** | IPSI | 0,5% - 10% |
| **Melilla** | IPSI | 0,5% - 10% |

---

## 7. Gastos Deducibles en IRPF

### Requisitos generales (3 reglas de Hacienda)

1. **Vinculacion**: el gasto debe estar directamente relacionado con la actividad economica
2. **Justificacion**: debe contar con factura oficial a nombre del autonomo
3. **Imputacion temporal**: debe corresponder al ano fiscal declarado

### Catalogo de gastos deducibles

#### Cuota de autonomos (Seguridad Social)
- **100% deducible** en IRPF

#### Suministros del hogar (si se trabaja desde casa)
```
Formula: (m2 actividad / m2 totales vivienda) x 30% de la factura
```
- Aplica a: luz, agua, internet, gas, telefono fijo
- Tambien deducibles proporcionalmente: IBI, comunidad de propietarios, seguro del hogar

#### Telefono movil
- **50%** si uso mixto (personal + profesional) - criterio consolidado AEAT
- **100%** si linea exclusivamente profesional

#### Dietas y manutencion
| Concepto | Espana | Extranjero |
|----------|--------|-----------|
| Sin pernocta | 26,67 EUR/dia | 48,05 EUR/dia |
| Con pernocta | 53,34 EUR/dia | 91,35 EUR/dia |

Requisitos: pago electronico, en establecimiento de hosteleria, en municipio distinto al domicilio.

#### Vehiculo
- **100% deducible** solo si uso exclusivamente profesional (transportistas, taxistas, repartidores, agentes comerciales)
- **IVA**: 50% deducible si uso afecto (presuncion legal)
- **IRPF**: Hacienda exige prueba de uso exclusivo (muy restrictivo)
- **Kilometraje**: 0,26 EUR/km en 2026 (sin IVA), justificando motivo del desplazamiento

#### Seguros medicos privados
- Hasta **500 EUR/persona** (autonomo + familia)
- Discapacidad: hasta **1.500 EUR/persona**

#### Formacion
- 100% deducible si directamente relacionada con la actividad
- Incluye: cursos, certificaciones, libros tecnicos, congresos, plataformas online
- NO deducible: idiomas genericos o formacion personal sin conexion

#### Equipos informaticos (amortizacion)
- < 300 EUR: deduccion directa al 100%
- > 300 EUR: amortizacion lineal, coeficiente maximo **25%** (4 anos) para equipos informaticos
- Mobiliario: 10% (10 anos)
- Software: 33% (3 anos)

#### Otros gastos deducibles
- Alquiler de local/oficina: 100%
- Material de oficina y consumibles: 100%
- Servicios profesionales (gestoria, abogado, notario): 100%
- Publicidad y marketing: 100%
- Cuotas de colegios profesionales: 100% (hasta 500 EUR)
- Seguros de responsabilidad civil: 100%
- Gastos financieros (intereses prestamos para actividad): 100%
- Vestuario profesional obligatorio (uniformes, EPIs): 100%
- Software y suscripciones profesionales: 100%
- Hosting, dominio, herramientas cloud: 100%

#### Gastos de dificil justificacion (solo Estimacion Directa Simplificada)
- **5% del rendimiento neto previo**, maximo **2.000 EUR/ano**
- Sin necesidad de facturas

### Gastos NO deducibles

- Multas y sanciones administrativas
- Donaciones y liberalidades (salvo Ley de Mecenazgo)
- Perdidas en el juego
- IVA ya deducido en modelo 303
- Gastos con empresas en paraisos fiscales
- Gastos sin justificante valido (mas alla del 5%)
- Ropa no profesional

---

## 8. Deducciones Autonomicas por Comunidad Autonoma

### IMPORTANTE: Diferencia entre "gastos deducibles" y "deducciones autonomicas"

- **Gastos deducibles**: reducen la base imponible (ingresos - gastos = beneficio). Comunes a toda Espana.
- **Deducciones autonomicas**: reducen directamente la **cuota** (el impuesto a pagar). Varian por CCAA.

> El borrador de la AEAT frecuentemente NO incluye todas las deducciones autonomicas. Hay que revisarlo y anadir las que correspondan manualmente.

---

### 8.1 Comunidad de Madrid

**Presion fiscal**: la mas baja de Espana. Deflactacion aplicada.

Deducciones destacadas:
- **Nacimiento/adopcion**: 721,70 EUR por hijo (incrementos en multiples)
- **Adopcion internacional**: 721,70 EUR por hijo
- **Acogimiento menores**: 618,60 - 927,90 EUR segun orden
- **Acogimiento mayores 65+ / discapacidad**: 1.546,50 EUR/persona
- **Alquiler vivienda jovenes (<35 anos)**: hasta 1.000 EUR
- **Gastos educativos**: uniformes, ensenanza de idiomas, guarderias
- **Inversion empresas nueva creacion (business angel)**: 50% sobre base max 100.000 EUR
- **Cuotas partidos politicos**: 20% sobre max 600 EUR

### 8.2 Cataluna

Deducciones destacadas:
- Nacimiento/adopcion de hijos
- Alquiler vivienda habitual
- Donativos a entidades catalanas
- Rehabilitacion vivienda habitual
- Inversion empresas nueva creacion
- Intereses prestamos estudios master/doctorado

### 8.3 Andalucia

Deducciones destacadas:
- **Empleados de hogar**: para padres con hijos a cargo
- **Discapacidad conyugue (>=65%)**: 100 EUR (limite BI 25.000 EUR individual / 30.000 EUR conjunta)
- **Libros de texto y material escolar**
- **Guarderias**: gastos de custodia menores 3 anos
- **Eficiencia energetica en vivienda**
- **Donativos medioambientales**: entidades publicas andaluzas
- **Donativos entidades sin animo de lucro**: inscritas en registros andaluces
- **Vivienda habitual jovenes (<35 anos)**

### 8.4 Comunitat Valenciana

**Presion fiscal**: la mas alta de Espana (tipo maximo 54%). Compensa con catalogo amplio de deducciones.

Deducciones destacadas:
- Nacimiento/adopcion/acogimiento
- Familia numerosa y monoparental
- Discapacidad
- Alquiler vivienda habitual
- Guarderias y centros de educacion infantil
- Eficiencia energetica
- Donativos medioambientales
- **Nuevas (2026)**: gastos sanitarios y practica deportiva/habitos saludables (DL 1/2026)
- Deducciones especiales por DANA

### 8.5 Galicia

Deducciones destacadas:
- Nacimiento/adopcion de hijos
- Libros de texto
- Empleados de hogar
- Guarderias
- Eficiencia energetica
- Viudedad
- Discapacidad/dependencia
- Alquiler vivienda habitual

### 8.6 Aragon

Deducciones destacadas:
- **Nacimiento 1er/2do hijo**: 100-200 EUR (mas si municipio <10.000 hab.)
- **Zona de despoblacion**: 600-720 EUR por nacimiento
- **Hijo con discapacidad >=33%**: deduccion adicional (+20% si zona despoblacion)
- **Libros de texto y material escolar**
- **Guarderias menores de 3 anos**
- **Alquiler vivienda habitual**
- Limite BI: 23.000 EUR individual / 35.000 EUR conjunta para maximas deducciones

### 8.7 Castilla y Leon

Deducciones destacadas:
- Familia (nacimiento, adopcion, familia numerosa)
- Vivienda (adquisicion, alquiler, rehabilitacion)
- Discapacidad
- Cuidado de hijos menores de 4 anos
- Inversion empresas nueva creacion

### 8.8 Castilla-La Mancha

Deducciones destacadas:
- **Libros de texto, idiomas, gastos educativos**
- **Donaciones I+D+i**
- **Donaciones cooperacion internacional**
- **Patrimonio cultural**: donativos de bienes culturales
- **Alquiler vivienda**: 15% para <36 anos (BI max 12.500 EUR ind. / 25.000 EUR conjunta)
- **Familias numerosas/monoparentales**: alquiler sin limite edad
- **Nacimiento/adopcion**: 100 EUR 1er hijo, 500 EUR si 2 hijos en el ano
- **Despoblacion**: hasta 25% del IRPF por residencia en zonas escasamente pobladas
- **Vivienda zona rural**: adquisicion o rehabilitacion
- **Inversion en sociedades mercantiles** (constitucion/ampliacion capital)
- **Economia social**

### 8.9 Extremadura

Deducciones destacadas:
- Nacimiento/adopcion de hijos
- Alquiler vivienda habitual
- **Nuevas tecnologias y energias renovables**
- **Rehabilitacion inmuebles historicos**
- **Inversion empresas agrarias**
- **Proyectos aldeas modelo**
- **Residencia en municipios <3.000 habitantes**

### 8.10 Illes Balears

Deducciones destacadas:
- **Nacimiento/adopcion**: 800 EUR (1o), 1.000 EUR (2o), 1.200 EUR (3o), 1.400 EUR (4o+)
- Limite BI: 52.800 EUR individual / 84.480 EUR conjunta
- **Sostenibilidad vivienda**
- **Donativos investigacion**
- **Fomento lengua catalana**
- **Material escolar**
- **Alquiler vivienda**

### 8.11 Canarias

Deducciones destacadas:
- Catalogo amplio
- Deducciones por enfermedad
- **Reserva para Inversiones en Canarias (RIC)**: potente herramienta para reinvertir beneficios
- IGIC en lugar de IVA (tipo general 7%)
- Zona Especial Canaria (ZEC): tipo reducido Impuesto Sociedades (4%)

### 8.12 Region de Murcia

Deducciones destacadas:
- **Dispositivos ahorro de agua domesticos**
- **Gastos acceso a Internet**
- **Libros de texto, idiomas, gastos educativos**
- **Cuidado hijos <3 anos**
- **Mayores dependientes**
- **Personas con discapacidad**
- Deflactacion automatica si IPC >3%

### 8.13 Principado de Asturias

Deducciones destacadas:
- **Arrendamiento vivienda habitual**
- **Vivienda habitual jovenes** (adquisicion/rehabilitacion)
- **Vivienda discapacitados** (adquisicion/adecuacion)
- **Certificacion gestion forestal sostenible**
- **Residencia en concejos con riesgo de despoblacion**
- **Formacion para incorporacion al mercado laboral**
- **Vehiculos electricos**
- **Transporte publico** (zonas despoblacion)
- **Ayudas por ELA**

### 8.14 Cantabria

Deducciones destacadas:
- Nacimiento/adopcion de hijos
- Gastos educativos y guarderia
- Familias numerosas y monoparentales
- **Donativos a fundaciones / Fondo Cantabria Coopera**
- **Traslado por estudios en zonas rurales con reto demografico**
- **Alquiler vivienda en zonas con reto demografico**

### 8.15 La Rioja

Deducciones destacadas:
- Hijos menores de 3 anos
- **Vivienda en pequenos municipios** (adquisicion/construccion/rehabilitacion)
- Escuelas infantiles
- Acogimiento familiar
- **Jovenes emancipados**: gastos Internet, luz y gas domestico
- **Bicicletas de pedaleo no asistido**
- **Vehiculos electricos**

### 8.16 Navarra (Regimen Foral)

- IRPF propio con normativa foral
- Tipo maximo agregado: ~52%
- Consultar Hacienda Foral de Navarra

### 8.17 Pais Vasco (Regimen Foral)

- IRPF propio por Territorio Historico (Alava, Bizkaia, Gipuzkoa)
- Tipos muy reducidos para rentas bajas (hasta 1% segun descendientes)
- Deflactacion del 2% en 2025
- Consultar Diputaciones Forales

### 8.18 Ceuta y Melilla

- **Deduccion del 60%** de la cuota integra por rentas obtenidas alli
- Impacto directo e inmediato en el impuesto a pagar
- IPSI en lugar de IVA

---

## 9. Calendario Fiscal 2026

### Obligaciones trimestrales

| Trimestre | Periodo | Plazo presentacion | Plazo domiciliacion |
|-----------|---------|--------------------|--------------------|
| 4T 2025 | Oct-Dic 2025 | 1-30 enero 2026 | Hasta 27 enero |
| 1T 2026 | Ene-Mar 2026 | 1-20 abril 2026 | Hasta 15 abril |
| 2T 2026 | Abr-Jun 2026 | 1-20 julio 2026 | Hasta 15 julio |
| 3T 2026 | Jul-Sep 2026 | 1-20 octubre 2026 | Hasta 15 octubre |

### Modelos trimestrales

| Modelo | Concepto | Quien lo presenta |
|--------|----------|-------------------|
| **303** | Autoliquidacion IVA | Todos los autonomos sujetos a IVA |
| **130** | Pago fraccionado IRPF | Autonomos en estimacion directa |
| **131** | Pago fraccionado IRPF | Autonomos en modulos |
| **111** | Retenciones e ingresos a cuenta | Si tienes empleados o profesionales |
| **115** | Retenciones alquileres | Si alquilas local/oficina |

### Declaraciones anuales

| Modelo | Concepto | Plazo |
|--------|----------|-------|
| **100** | Declaracion de la Renta | 8 abril - 30 junio 2026 (ejercicio 2025) |
| **390** | Resumen anual IVA | 1-30 enero 2026 |
| **190** | Resumen anual retenciones | 1-30 enero 2026 |
| **347** | Operaciones con terceros >3.005,06 EUR | Febrero 2026 |
| **349** | Operaciones intracomunitarias | Segun periodicidad |

### Regla de oro

> "Domicilia el dia 15; presenta el dia 20" (en enero: domicilia el 25, presenta el 30)

Incluso sin cuota a ingresar, la declaracion debe presentarse.

---

## 10. VERI*FACTU y Facturacion Electronica

### Situacion actual (marzo 2026)

| Obligacion | Plazo original | Plazo actual |
|------------|----------------|-------------|
| **VERI*FACTU para sociedades** | 1 julio 2026 | **1 julio 2027** (aplazado) |
| **VERI*FACTU para autonomos** | 1 julio 2026 | **1 julio 2027** (aplazado) |
| **Factura electronica B2B (Ley Crea y Crece)** | Pendiente de reglamento | Grandes empresas: ~2027. Resto: ~2027-2028 |

### Que es VERI*FACTU

Sistema de la AEAT que exige que los programas de facturacion generen registros de alta encadenados (hash + firma electronica) por cada factura, garantizando su integridad e inmodificabilidad.

Dos modalidades:
1. **VERI*FACTU**: remision automatica de registros a la AEAT + codigo QR + leyenda "Factura verificable en la sede de la AEAT"
2. **No VERI*FACTU**: sin remision automatica, pero con firma electronica, registro de eventos y conservacion reforzada

### Quien NO esta afectado

- Quien solo usa un programa para emitir y conservar facturas (sin funcionalidad de registro adicional)
- Quienes ya estan en SII (Suministro Inmediato de Informacion)

### Herramienta gratuita de la AEAT

La AEAT facilitara un aplicativo simplificado gratuito en su Sede Electronica para autonomos con pocas facturas, que devolvera factura imprimible con QR.

### Sanciones

- Fabricantes/comercializadores de software: hasta 150.000 EUR
- Empresas y autonomos: hasta 50.000 EUR

---

## 11. Datos Utiles para la Web

### Funcionalidades sugeridas basadas en la investigacion

1. **Calculadora de cuota de autonomo**: input ingresos netos mensuales -> output cuota mensual segun tramo
2. **Calculadora de IRPF por CCAA**: input beneficio neto + CCAA -> output impuesto total (estatal + autonomico)
3. **Comparador fiscal entre CCAA**: mismos ingresos, ver cuanto pagas en cada comunidad
4. **Simulador de gastos deducibles**: input gastos del autonomo -> cuanto se ahorra en la declaracion
5. **Checklist de deducciones autonomicas**: segun CCAA, mostrar todas las deducciones aplicables
6. **Calendario fiscal con alertas**: recordatorios de plazos de presentacion
7. **Calculadora de retenciones en facturas**: profesional vs empresario, nuevo autonomo
8. **Simulador estimacion directa vs modulos**: que regimen conviene mas
9. **Generador de presupuesto fiscal anual**: proyeccion de impuestos segun facturacion prevista

### Datos de entrada que necesita la web

Para un usuario de la web, los datos minimos necesarios para calcular todo serian:

```
- Comunidad autonoma de residencia
- Ciudad/municipio (para deducciones por despoblacion)
- Tipo de actividad (epigrafe IAE / seccion)
- Regimen de estimacion (directa simplificada / normal / modulos)
- Facturacion bruta anual
- Lista de gastos deducibles (categorizado)
- Situacion personal: estado civil, hijos, discapacidad, edad
- Tipo de vivienda: propia/alquiler, m2 totales, m2 actividad
- Vehiculo: tiene/no, uso exclusivo profesional
- Empleados: si/no
- Nuevo autonomo: si/no (para tarifa plana y retencion 7%)
```

### Formulas clave para implementar

```
# Rendimiento neto
rendimiento_neto = ingresos_brutos - gastos_deducibles

# Si Estimacion Directa Simplificada:
gastos_dificil_justif = min(rendimiento_neto * 0.05, 2000)
rendimiento_neto_reducido = rendimiento_neto - gastos_dificil_justif

# Base imponible
base_imponible = rendimiento_neto_reducido - cuota_autonomos_anual

# Base liquidable
base_liquidable = base_imponible - minimo_personal_familiar

# Cuota integra = aplicar escala estatal + escala autonomica a base_liquidable

# Cuota liquida = cuota_integra - deducciones_autonomicas - deducciones_estatales

# A devolver/pagar = cuota_liquida - retenciones_soportadas - pagos_fraccionados

# Cuota autonomo mensual
tramo = buscar_tramo(rendimiento_neto / 12)
cuota_autonomo = base_minima_tramo * 0.3120
```

---

## 12. Fuentes

### Fuentes oficiales
- [Agencia Tributaria - IRPF Deducciones autonomicas](https://sede.agenciatributaria.gob.es/Sede/vivienda-otros-inmuebles/irpf-deducciones-autonomicas.html)
- [Agencia Tributaria - Manual practico de Renta](https://sede.agenciatributaria.gob.es/Sede/Ayuda/24Manual/100/deducciones-autonomicas.html)
- [Agencia Tributaria - Regimenes de tributacion IVA](https://sede.agenciatributaria.gob.es/Sede/iva/regimenes-tributacion-iva.html)
- [Agencia Tributaria - VERI*FACTU](https://sede.agenciatributaria.gob.es/Sede/iva/sistemas-informaticos-facturacion-verifactu/cuestiones-generales.html)
- [Seguridad Social - Simulador cuota autonomo](https://portal.seg-social.gob.es/wps/portal/importass/importass/tramites/simuladorRETAPublico)
- [Ministerio de Hacienda - Tributacion Autonomica 2025](https://www.hacienda.gob.es/sgfal/financiacionterritorial/autonomica/capitulo-i-tributacion-autonomica-2025.pdf)
- [REAF Economistas - Panorama 2025](https://economistas.es/Contenido/REAF/Informes/Panorama%202025.pdf)
- [Comunidad de Madrid - IRPF](https://www.comunidad.madrid/servicios/atencion-contribuyente/irpf-0)
- [Agencia Tributaria de Cataluna](https://atc.gencat.cat/es/tributs/irpf/)
- [Junta de Andalucia - Escala autonomica](https://www.juntadeandalucia.es/organismos/economiahaciendayfondoseuropeos/areas/tributos-juego/tributos/paginas/escalaautonomica.html)

### Fuentes de referencia
- [InfoAutonomos - Cuota de autonomos](https://www.infoautonomos.com/seguridad-social/cuota-de-autonomos-cuanto-se-paga/)
- [InfoAutonomos - Gastos deducibles](https://www.infoautonomos.com/fiscalidad/gastos-deducibles-autonomos-irpf-estimacion-directa/)
- [InfoAutonomos - Calendario fiscal](https://www.infoautonomos.com/fiscalidad/calendario-fiscal-autonomo-pyme/)
- [InfoAutonomos - Retenciones](https://www.infoautonomos.com/fiscalidad/las-retenciones-y-los-autonomos/)
- [Holded - Cuota autonomos](https://www.holded.com/es/blog/cuota-autonomos)
- [Holded - Gastos deducibles](https://www.holded.com/es/blog/gastos-deducibles-irpf-los-autonomos)
- [Holded - Calendario fiscal](https://www.holded.com/es/blog/calendario-fiscal)
- [TaxDown - Tablas y tramos IRPF](https://taxdown.es/irpf/tabla-tramos)
- [TaxDown - Deducciones fiscales autonomos](https://taxdown.es/informacion-autonomos/deducciones-fiscales)
- [Wolters Kluwer - Tramos IRPF 2026](https://www.wolterskluwer.com/es-es/expert-insights/tramos-retenciones-irpf-2026-novedades)
- [Wolters Kluwer - Cuotas autonomos 2026](https://www.wolterskluwer.com/es-es/expert-insights/cuotas-autonomos-2026)
- [BBVA - IRPF autonomo](https://www.bbva.es/finanzas-vistazo/ae/financiacion/irpf-autonomo.html)
- [Cuentica - Calendario fiscal 2026](https://cuentica.com/asesoria/calendario-fiscal-2026-autonomos-empresas/)
- [Fiscaliza - Cuota autonomos 2026](https://fiscaliza.es/guias/autonomos/cuota-autonomos-seguridad-social-2026.html)
- [Baron Seguros - Cotizacion autonomos 2026](https://baronseguros.com/cotizacion-autonomos-2026/)
- [INEAF - Deducciones por CCAA 2026](https://www.ineaf.es/tribuna/deducciones-renta-por-comunidad-autonoma/)
- [OCU - Deducciones autonomicas](https://www.ocu.org/dinero/renta-impuestos/informe/deducciones-autonomicas)
- [Declarando - Factura electronica](https://declarando.es/factura-electronica)
- [Copilot Gestoria - 47 gastos deducibles](https://copilotgestoria.com/blog/gastos-deducibles-autonomos-2026-guia-definitiva)

---

> **Disclaimer**: Este documento es una recopilacion de informacion publica con fines de desarrollo de software. No constituye asesoramiento fiscal profesional. Los datos pueden variar y deben verificarse con la normativa vigente y fuentes oficiales. Ultima actualizacion: 15 de marzo de 2026.
