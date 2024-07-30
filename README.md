## Descripción
Este proyecto tiene como objetivo realiza un sistema de recomendación de peliculas similares para esto se tiene que tomar en cuenta el score y la similitud en los titulos de cada pelicula, para hacer esto primero hay que realizar un ETL donde se limpiaran los datos y se realizan algunas transformaciones, despues se hara un EDA para poder ánalizar los datos que tenemos y de esta manera saber que variables nos pueden dar mayor clasificación y asi poder entrenar nuestro modelo de Machine Learning que sera el encargado de darnos las peliculas con mas similitud para por ultimo dar la recomendación de las peliculas que depende de una pelicula ingresada.

![Recomendación](Imagenes/recomendacion.jfif)

# Tabla de contenido 
1. [Introducción](#Descripción)
2. [Instalación y requisitos](#Instalación_y_Requisitos)
2. [Estructura_del_proyecto](#Estructura_del_proyecto)

## Instalación_y_Requisitos
Requisitos 
- Link de render
- link de Github

Psos para su funcionamiento
1. ingresar a Github https://github.com/GLibardoAlarcon/Proyecto01
2. acceder a la sigiente ruta y descargar df_union.parquet Data/df_union.parquet
3. Acceder a link de fastApi https://proyecto01-1.onrender.com/docs
4. Ingresa al la primera iteración Uploat_parque donde vas a ingresar el archivo df_union.parquet
5. Ya iterar con las demas opciones, cada una de ellas te va a pedir un dato que tienes que ingresar para que puedas consumir el Api

## Estructura_del_proyecto
<mark>.venv<mark> Contiene las librerias necesarias para que funcione el proyecto main.py en un entorno virtual pero a nivel local
<mark>Data<mark> Contiene los archivos que se se utilizarón para el ánalisi y para que ingresar a FasApi
<mark>notebooks<mark> Contiene el archivos .py y ipynb 
<mark>README<mark> Contenido explicativo e introductorio

