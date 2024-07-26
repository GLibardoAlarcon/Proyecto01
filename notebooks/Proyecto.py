# Librerias utililizadas para el proyecto 01, Modelo de recomendaciones de peliculas 
import pandas as pd
import numpy as np
import seaborn as sn
import json
from pandas import json_normalize
import re
import matplotlib.pyplot as plt
import requests
import ast
sn.set_theme()

# Cargamos el cvs 
df_movies = pd.read_csv('Archivos/movies_dataset.csv')

# Desempaquetamos las columnas de belongs_to_collection donde tomamos el id y el name las demas las podemos descartar
Datos = []
# Realizamos el recorrido fila a fila
for indice, fila in df_movies.iterrows():
    # Si el resultado es Nulo por defecto lo va a dejar como tal 
    collection_id = None
    collection_name = None
    # Sentencia para descartar los valores nulos en las filas de belongs_to_collection
    if pd.notna(fila['belongs_to_collection']):
        # se evalua y la pasamos a una nueva variable 
        collection_data = ast.literal_eval(fila['belongs_to_collection'])
        # Condición para evaluar valores flotantes y los concidere como nulo
        if isinstance(collection_data, float):
            collection_id = None
            collection_name = None
        else:
            # De no ser flotantes pasamos el valor contenido a estas variables
            collection_id = collection_data['id']
            collection_name = collection_data['name']
            #Guardamos los datos en cada una de estas variables y borramos belongs_to_collection
    Datos.append({'collection_id': collection_id,
                   'collection_name': collection_name,
                    **fila.drop(['belongs_to_collection'])
                    })
        

# Pasamos en nuevo dataframe desanidada la comulna belongs_to_collection
df_movies = pd.DataFrame(Datos)

# Desempaquetamos las columnas de genres donde tomamos el id y el name 
Datos1 = []
# Realizamos el recorrido fila a fila
for indice, fila in df_movies.iterrows():
    # Realizamos a condicion para que en cada fila no haya ningun nulo
    if pd.notna(fila['genres']):
        # Evalua y los datos se pasan a una nueva variable 
        genres_data = ast.literal_eval(fila['genres'])
        # Ciclo para poder acceder a cada uno de los datos de genres
        for i in range(0, len(genres_data)):
             if i == 0:
                 genres_id = genres_data[0]['id']
                 genres_name = genres_data[0]['name']
             if i == 1:
                 genres_id1 = genres_data[1]['id']
                 genres_name1 = genres_data[1]['name']
             if i == 2:
                 genres_id2 = genres_data[2]['id']
                 genres_name2 = genres_data[2]['name']
                 # Guardamos cada uno de los datos y borramos la columna genres
    Datos1.append({'genres_id': genres_id,
                    'genres_name': genres_name,
                    'genres_id1': genres_id1,
                    'genres_name1': genres_name1,
                    'genres_id2': genres_id2,
                    'genres_name2': genres_name2,
                    **fila.drop(['genres'])
                    })
    
# Pasamos la columna de gernes desanidada ya borrando esta 
df_movies = pd.DataFrame(Datos1)

# Desempaquetamos las columnas de production_companies donde tomamos el id y el name 
Datos2 = []
# Realizamos el recorrido fila a fila
for indice, fila in df_movies.iterrows():
    # Si el valor de la fila es None queda como tal
    companies_name = None
    companies_id = None
    booTrue = True
    booFalse = False
    # Condición para que las filas con valores None no sean tomadas en cuenta
    if pd.notna(fila['production_companies']):
        #Evalua y se pasan los datos a una nueva variable
        companies_data = ast.literal_eval(fila['production_companies'])
        # Condición que evalua si hay columnas con valores booleanos o que no tengan datos
        if  companies_data == booTrue or companies_data == booFalse or len(companies_data) < 1  :
           companies_name = None
           companies_id = None
        else:
            # Si no se cumple se desanidan los datos en las dos variables
            companies_name = companies_data[0]['name']
            companies_id = companies_data[0]['id']
    # Rellenamos el dataset con los valores resultantes 
    Datos2.append({ 'companies_name': companies_name,
                   'companies_id': companies_id,
                   **fila.drop(['production_companies'])

    })
           

df_movies =  pd.DataFrame(Datos2)

# Desempaquetamos la columna production_countries y tomamos iso_3166_1 y name
Datos3 = []
for index, fila in df_movies.iterrows():
    # Si hay valores nulos los va tomar como tal
    counttries_iso_3166_1 = None
    countries_name = None
    # Condicion para que no tome valores nulos
    if pd.notna(fila['production_countries']):
       countries_data = ast.literal_eval(fila['production_countries'])
       # Condición para valores vacios o valores flotantes
       if isinstance(countries_data, float) or len(countries_data) < 1 :
          counttries_iso_3166_1 = None
          countries_name = None
       else:
          # Si todo esta perfecto lo pasamos a nuestras variables 
          counttries_iso_3166_1 = countries_data[0]['iso_3166_1']
          countries_name = countries_data[0]['name']
          # Guardamos la información en el nuevo dataset donde queda desanidadas
    Datos3.append({ 'iso_3166_1': counttries_iso_3166_1,
                   'name': countries_name,
                   **fila.drop(['production_countries'])
       
    })

# Agregamos los cambios al dataset original
df_movies = pd.DataFrame(Datos3)

# Desempaquetamos la columna spoken_languages y tomamos iso_639_1 y name
Datos4 = []
# Realizamos el recorrido fila a fila
for indice, fila in df_movies.iterrows():
    # si hay valores Nulos queda como tal
    language_iso_639_1 = None
    language_name = None
    # Condición para valores no nulos
    if pd.notna(fila['spoken_languages']):
        languages_data = ast.literal_eval(fila['spoken_languages'])
        # Condición para valores vacios 
        if len(languages_data) < 1:
            language_iso_639_1 = None
            language_name = None
            # Si esta perfecto procede a dejar cada valor en las variables creadas
        else:
            language_iso_639_1 = languages_data[0]['iso_639_1']
            language_name = languages_data[0]['name']
        # se empiesa a desanidar nombrando dos nuevas columnas
    Datos4.append({'iso_639_1': language_iso_639_1,
                   'name': language_name,
                   **fila.drop(['spoken_languages'])
    })
   
#Pasamos los cambios a nuestro dataframe
df_movies = pd.DataFrame(Datos4)

# Validamos los valores que tiene nulos 
df_movies['revenue'].info()

# Realizamos el remplazo de los valores nulos por ceros a la columna revenue
# Por medio de este ciclo podemos hacer el recorrido a toda la columna del revenue
for i in range(0, df_movies['revenue'].size):
    # Si el valor no es nulo ingresa a esta condición que la deja tal cual
    if pd.notna(df_movies['revenue'][i]):
        df_movies['revenue'][i] = df_movies['revenue'][i]
        # De ser nulo realiza el cambio por 0
    else:
        df_movies['revenue'][i] = 0

# Para siguiente columna no tenemos valores nulos 
df_movies['budget'].info()

# Validamos si hay valores nulos 
df_movies['release_date'].info()

# Pasamos a eliminar los valores nulos de la columna release_date
df_movies = df_movies.dropna(subset=['release_date'])
# Reseteamos los indices para evitar que no exista angun indice
df_movies = df_movies.reset_index(drop= True)

# Creamos una funcion para detectar si el valor ingresado es de tipo fecha de lo contrario lo deja como nulo
def verificar_fecha(fecha):
    try:
        fecha_trasformada = pd.to_datetime(fecha, format='%Y-%m-%d')
        return fecha_trasformada
    except ValueError:
        return None


# Procedemos a aplicar la función anterior
df_movies['release_date'] = df_movies['release_date'].apply(verificar_fecha)

# Como al aplicar la función donde encontraba valores que tienen un formato muy difererente a de date los trasformaba en Nulos por lo que optubimos nuevos valores nulos
# Procedemos a borrarlos
df_movies = df_movies.dropna(subset=['release_date'])
# Reseteamos los indices para evitar que no exista angun indice
df_movies = df_movies.reset_index(drop= True)

# Extraemos el años de la columna release_year a una nueva columna
df_movies['release_year'] = df_movies['release_date'].dt.year 

# Cambiamos el tipo de dato a la columna budget en tipo int
df_movies['budget'] = df_movies['budget'].astype(int)

# Cambiamos el tipo de dato a la columna revenue en tipo int
df_movies['revenue'] = df_movies['revenue'].astype(int)

# Creamos una nueva columna con 0
df_movies['return'] = 0
# Ciclo para obtener el indice
for i in range(0, df_movies['revenue'].size):
    # Condicion donde si en alguna de las colubnas existe un 0 dejemos el valor como 0 ya que no tendria sentido realiar la operación de retorno de inverción si hay un cero que podria indicar que no se introdujo el valor
    if df_movies['revenue'][i] == 0 or df_movies['budget'][i] == 0:
        df_movies['return'][i] = 0
        # Se realiza la operación y se cambia el 0 por el valor corrrespondiente
    else:
        df_movies['return'][i] = df_movies['revenue'][i] / df_movies['budget'][i]

# Eliminamos las columnas que no vamos a utilizar 
df_movies = df_movies.drop(['video', 'imdb_id', 'adult', 'original_title', 'poster_path', 'homepage'], axis=1)

# Cargamos el cvs credits 
df_Credits = pd.read_csv('Archivos/credits.csv')

# Desempaquetamos la crew y tomamos solo la columna de Directores
Datos_cre = []
# Realizamos un ciclo para recorrer fila a fila
for indice, fila in df_Credits.iterrows():
    # Si la fila es nula o None la variable queda con este valor
    crew_Director = None
    # Condición para, donde no hacepta valores nulos
    if pd.notna(fila['crew']):
        # Evalua y pasa los valores a una nueva variable
        crew_data = ast.literal_eval(fila['crew'])
        # Condición para los filas que no tienen contenido
        if len(crew_data) > 0:
           # Ciclo poder recorrer cada uno de los diccionarios que contenga la fila
           for i in range(0, len(crew_data)):
               # Condición donde si encuentra un trabajo que sea Director tome el nombre 
               if crew_data[i]['job'] == 'Director':
                   crew_Director = crew_data[i]['name']
                   # Guardamos la información y borramos la columna crew
    Datos_cre.append({
            'crew_Director': crew_Director,
            **fila.drop(['crew'])
                })
                   

df_Credits = pd.DataFrame(Datos_cre)

# Pasamos los cambios a el dataframe principal 
df_Credits = pd.DataFrame(Datos_cre)

# Desempaquetamos la crew y tomamos solo la columna de Directores
Datos_cre = []
# Realizamos un ciclo para recorrer fila a fila
for indice, fila in df_Credits.iterrows():
    # Si la fila es nula o None la variable queda con este valor
    crew_Director = None
    # Condición para, donde no hacepta valores nulos
    if pd.notna(fila['crew']):
        # Evalua y pasa los valores a una nueva variable
        crew_data = ast.literal_eval(fila['crew'])
        # Condición para los filas que no tienen contenido
        if len(crew_data) > 0:
           # Ciclo poder recorrer cada uno de los diccionarios que contenga la fila
           for i in range(0, len(crew_data)):
               # Condición donde si encuentra un trabajo que sea Director tome el nombre 
               if crew_data[i]['job'] == 'Director':
                   crew_Director = crew_data[i]['name']
                   # Guardamos la información y borramos la columna crew
    Datos_cre.append({
            'crew_Director': crew_Director,
            **fila.drop(['crew'])
                })
                   
df_Credits = pd.DataFrame(Datos_cre)

# Pasamos los cambios a el dataframe principal 
df_Credits = pd.DataFrame(Datos_cre)

# Desempaquetamos la columna cast y tomamos los actores que protagonizarón la pelicula
Datos_cast = []
# Ciclo para sacar fila a fila
for indice, fila in df_Credits.iterrows():
    # si los valoes nulos quedan tal cual 
    cas_actor1 = None
    cas_actor2 = None
    cas_actor3 = None
    cas_actor4 = None
    cas_actor5 = None
    cas_actor6 = None
    cas_actor7 = None
    cas_actor8 = None
    cas_actor9 = None
    cas_actor10 = None
    # Condición donde no admite nulos
    if pd.notna(fila['cast']):
        # Transformación de cada fila para poder trabajarla
        cas_actorData = ast.literal_eval(fila['cast'])
        # Condición para los actores 
        if len(cas_actorData) > 0 and len(cas_actorData) <= 10:
                # Ciclo para pasar actor por actor y almacenarlo en su devida variable
                for i in range(0, len(cas_actorData)):
                      if i == 0:
                         cas_actor1 = cas_actorData[i]['name']
                      if i == 1:
                         cas_actor2 = cas_actorData[i]['name']
                      if i == 2:
                         cas_actor3 = cas_actorData[i]['name']
                      if i == 3:
                         cas_actor4 = cas_actorData[i]['name']
                      if i == 4:
                         cas_actor5 = cas_actorData[i]['name']
                      if i == 5:
                         cas_actor6 = cas_actorData[i]['name']
                      if i == 6:
                         cas_actor7 = cas_actorData[i]['name']
                      if i == 7:
                         cas_actor8 = cas_actorData[i]['name']
                      if i == 8:
                         cas_actor9 = cas_actorData[i]['name']
                      if i == 9:
                         cas_actor10 = cas_actorData[i]['name']
                         # Almacenamiento de la información 
    Datos_cast.append({
            'cas_actor1': cas_actor1,
            'cas_actor2': cas_actor2,
            'cas_actor3': cas_actor3,
            'cas_actor4': cas_actor4,
            'cas_actor5': cas_actor5,
            'cas_actor6': cas_actor6,
            'cas_actor7': cas_actor7,
            'cas_actor8': cas_actor8,
            'cas_actor9': cas_actor9,
            'cas_actor10': cas_actor10,
            **fila.drop(['cast'])
                    })
               
df_Credits = pd.DataFrame(Datos_cast)

# Guardamos los cambios en un nuevo cvs para obtener solo la información que necesitamos
df_Credits.to_csv('credits_final.csv', index=False)
