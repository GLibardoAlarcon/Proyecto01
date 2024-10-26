from fastapi import FastAPI, File, UploadFile, HTTPException, Query
import pandas as pd
from babel.dates import format_date
from io import BytesIO 
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from enum import Enum
from typing import List
app = FastAPI()

# Cargar el archivo Parquet
try:
    df_movies = pd.read_parquet('./Data/movies_dataset_f.parquet')
except FileNotFoundError:
    # Si no se carga el archivo parquet envia un mensage de error
    raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado")

# Extraer los meses en idioma español, donde quedan guardados en una variable
meses_disponibles = list(df_movies['release_date'].dropna().apply(lambda x: format_date(x, 'MMMM', locale='es_ES')).unique())
# Extraemos los días unicos del dataset
dias_unicos = list(df_movies['release_date'].apply(lambda x: format_date(x, 'EEEE', locale='es_ES')).unique())
# Extraemos los titulos unicos
Titulos_unicos = list(df_movies['title'].unique())

@app.get("/filmaciones_mes/", tags=['Proyecto_01'])
async def cantidad_filmaciones_mes(
    mes: str = Query(..., description="Selecciona el mes", enum=meses_disponibles)
):
    # Verificar que el archivo se haya cargado correctamente
    if df_movies is None:
        raise HTTPException(status_code=404, detail="No se ha cargado ningún archivo Parquet")

    # Filtrar y contar las filmaciones del mes especificado
    mes_column = df_movies['release_date'].apply(lambda x: format_date(x, 'MMMM', locale='es_ES'))
    conteo = (mes_column == mes).sum()

    # Mensaje de respuesta
    respuesta = {
        "cantidad_peliculas": int(conteo),
        "mensaje": f"Cantidad de películas estrenadas en el mes de {mes}"
    }
    
    return respuesta

@app.get("/Filmaciones D", tags=['Proyecto_01'])
# Creamos la función
async def cantidad_filmaciones_dia(dia: str = Query(..., description="Seleccione el día", enum = dias_unicos)):

     # Verificar que el archivo se haya cargado correctamente
    if df_movies is None:
        raise HTTPException(status_code=404, detail="No se ha cargado ningún archivo Parquet")
    # Filtrar y contar las filmaciones por día
    dias_column = df_movies['release_date'].apply(lambda x: format_date(x, 'EEEE', locale='es_ES'))
    conteo = (dias_column == dia).sum()
    # Mensage de respuesta
    return  {
        "Cantidad de peliculas": int(conteo),
        "Mensaje": f"Cantidad de películas estrenadas en el día {dia}"
    }



@app.get("/Score Titulo", tags=['Proyecto_01'])
# Función para el score por filmación
async def score_titulo(Titulo: str):
     # Verificar que el archivo se haya cargado correctamente
    if df_movies is None:
        raise HTTPException(status_code=404, detail="No se ha cargado ningún archivo Parquet")
         # ciclo para recorrer cada uno de los titulos
    for i in range(0, len(df_movies)):
             # Si el titulo es el mismo que el ingresado nos guarda la información en cada una de las variables
             if df_movies['title'][i] == Titulo:
                popularity = df_movies['popularity'][i]
                year = df_movies['release_year'][i]
                Variable = {"La pelicula": Titulo, "Fue estrenada en el año": str(year), "Con un score/popularidad de": str(popularity)}

    return Variable

@app.get("/Votos por titulo", tags=['Proyecto_01'])
# Creamos la función
async def votos_titulo(Titulo: str):
    # Si no encuentra el titulo solicitado
    Variable = {"El dato ingresado es incorrecto o no": "se encuentra en nuestra base de datos"}
    # Condición para saber si cargo el archivo
    if df_movies is not None:
        # Ciclo para recorrer
        for i in range(0, len(df_movies)):
            # Condición para saber si el titulo existe
            if df_movies['title'][i] == Titulo:
                Variable = {"La pelicula elegida no tiene mas de 2000 votaciones": "Por lo que no se muestra ningun valor"}
                # COndición para las peliculas que tienen mas de 2000
                if df_movies['vote_count'][i] >= 2000:
                    Variable = {"La pelicula": Titulo, "fue estrenada en el año": str(df_movies['release_year'][i]), "La misma cuenta con un total de": str(df_movies['vote_count'][i]), "valoraciones, con un promedio de": str(df_movies['vote_average'][i])}
    else:
      raise HTTPException(status_code=404, detail="No se ha cargado ningún archivo Parquet")
    return Variable

@app.get("/Datos del actor", tags=['Proyecto_01'])
# Creamos la función
async def actor(Actor: str):
    # Valor que toma la variable si no encuentra el dato
    Variable = {"El dato ingresado es incorrecto o no": "se encuentra en nuestra base de datos"}
    # Variables iniciadas en 0
    conteo = 0
    retorno = 0
    promedio = 0
    # Condición para que no puedan ingresar nulos
    if df_movies is not None:
        # Recorrido fila a fila
        for indice, fila in df_movies.iterrows():
           # Por medio de este ciclo puede recorrer a los 10 actores 
           for i in range(0, 9):
               # Condición si llega a encontrar al actor digitado
               if fila[i] == Actor:
                   # Se realiza las operaciones
                   conteo += 1
                   retorno += fila[20]
        promedio = retorno / conteo
        Variable = {"El actor": Actor, "ha participado de": str(conteo), "cantidad de filmaciones, el mismo ha conseguido un retorno de": str(retorno), "con un promedio de": str(promedio), "por": "filmacion"}
    else:
        raise HTTPException(status_code=404, detail="No se ha cargado ningún archivo Parquet")
    return Variable

@app.get("/Datos director", tags=['Proyecto_01'])
async def Director(Director: str):
    # Se inicializa una lista y una variable en 0
    Datos = []
    Retorno = 0
    # Condición para nulos
    if df_movies is not None:
        #Ciclo para recorrer la columna
        for i in range(0, len(df_movies)):
            # Condición para encontrar al director digitado
            if df_movies['crew_Director'][i] == Director:
                # Se guardan los datos de salida en la lista
                Datos.append({"Titulo": str(df_movies['title'][i]), "Fecha de lanzamiento": str(df_movies['release_date'][i]), "Costo": str(df_movies['budget'][i]), "Ganancia": str(df_movies['revenue'][i] - df_movies['budget'][i])})
                Retorno += df_movies['return'][i]
        Datos.append({"Exito segun retorno": str(Retorno)})
    else:
        raise HTTPException(status_code=404, detail="No se ha cargado ningún archivo Parquet")
    return Datos        

@app.get("/Recomendaciones de peliculas", tags=['Proyecto_01'])
async def Recomendaciones(Pelicula: str):
    # Convertimos los titulos de las peliculas en una matriz TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X_text = vectorizer.fit_transform(df_movies['title'])
    #Normalizacion de variables númericas
    scaler = StandardScaler()
    X_numeric = scaler.fit_transform(df_movies[['popularity', 'vote_count']])
    # Concatenamos las caracteristicas de texto y númericas
    X = hstack([X_text, X_numeric])

    # Definimos la cantidad de clusters
    num_clusters = 3
    #Aplicamos K-means
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    # Cremos una nueva columna para poder poner las etiquetas de los clusters
    df_movies['Clusters'] = kmeans.labels_

    # Obtenemos el indice de la pelicula solicitada
    idx = df_movies[df_movies['title'] == Pelicula].index[0]

    # Obtenemos el cluster de la pelicula solicitada
    movie_cluster = df_movies.loc[idx, 'Clusters']

    # Filtrar las peliculas que estan en el mismo cluster
    cluster_indices = df_movies[df_movies['Clusters'] == movie_cluster].index

    # Calculamos las similitud de coseno entre la pelicula solicitada y las peliculas que estan en el mismi cluster
    coseno_similares = cosine_similarity(X_text[idx], X_text[cluster_indices]).flatten()

    # Ordenar las peliculas por similitud
    similar_indices = coseno_similares.argsort()[-5-1:-1][::-1]

    # Oredenar los titulos de las peliculas recomendadas
    recommended_movies = df_movies.iloc[cluster_indices[similar_indices]]['title']


    return recommended_movies
    


