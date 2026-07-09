# Pipeline DataMart Chile S.A.

## Descripción del proyecto

Este proyecto corresponde al examen final de la asignatura. El objetivo es construir un pipeline de datos completo para la empresa ficticia DataMart Chile S.A., una cadena de retail online con operaciones en Santiago, Valparaíso y Concepción.

El pipeline procesa el archivo `ventas_datamart.csv`, el cual contiene errores intencionales como duplicados, formatos de fecha inconsistentes, valores inválidos, categorías mezcladas y reglas de negocio incumplidas.

## Etapas del pipeline

El pipeline está dividido en 4 etapas principales:

1. Ingesta de datos
2. Limpieza y transformación
3. Validación estructural y semántica
4. Carga a base de datos

## Estructura del proyecto

```text
datamart_pipeline/
│
├── data/
│   ├── raw/
│   ├── clean/
│   ├── validated/
│   └── errors/
│
├── logs/
├── database/
│
├── ventas_datamart.csv
├── ingesta.py
├── limpieza.py
├── validacion.py
├── carga.py
├── main.py
├── requirements.txt
└── README.md