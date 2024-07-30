## Descripción
Este proyecto tiene como objetivo realiza un sistema de recomendación de peliculas similares para esto se tiene que tomar en cuenta el score y la similitud en los titulos de cada pelicula, para hacer esto primero hay que realizar un ETL donde se limpiaran los datos y se realizan algunas transformaciones, despues se hara un EDA para poder ánalizar los datos que tenemos y de esta manera saber que variables nos pueden dar mayor clasificación y asi poder entrenar nuestro modelo de Machine Learning que sera el encargado de darnos las peliculas con mas similitud para por ultimo dar la recomendación de las peliculas que depende de una pelicula ingresada.

![Recomendación](Imagenes/recomendacion.jfif)

# Tabla de contenido 
1. [Introducción](#Descripción)
2. [Instalación y requisitos](#Instalación_y_Requisitos)
3. [Estructura_del_proyecto](#Estructura_del_proyecto)
4. [Uso_y_ejecución](#Uso_y_ejecución)

## Instalación_y_Requisitos
Requisitos 
- Link de render
- link de Github

Installación
1. Python 3.7 o superior
2. pandas
3. numpy
4. matplotlib
5. scikit-learn
6. ingresar a Github https://github.com/GLibardoAlarcon/Proyecto01
7. acceder a la sigiente ruta y descargar df_union.parquet Data/df_union.parquet
3. Acceder a link de fastApi https://proyecto01-1.onrender.com/docs

## Estructura_del_proyecto
- <mark>.venv</mark> Contiene las librerias necesarias para que funcione el proyecto main.py en un entorno virtual pero a nivel local
- <mark>Data</mark> Contiene los archivos que se se utilizarón para el ánalisis y para la aplicación FastApi
- <mark>notebooks</mark> Contiene el archivos .py y ipynb 
- <mark>README</mark> Contenido explicativo e introductorio

## Uso_y_ejecución
1. Ingresa al la primera iteración Uploat_parque donde vas a ingresar el archivo df_union.parquet
2. Ingresa a filmaciones M en esta obción pide ingresar un mes del año y obtendra las filmaciones que se hicierón en ese mes
3. Ingresa a filmaciones D en esta obcion ingresar un dia de la semana y dara como resultado las filmaciones que se hicierón ese día
4. 

