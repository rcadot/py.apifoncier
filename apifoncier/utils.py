import requests
import pandas as pd
import plotly.express as px
import geopandas as gpd
from urllib.parse import urlencode

# %%
def _get_api_data_list(base_url, id_peri_list, params=None, debug=False):
    df_list = []  # Liste pour stocker les DataFrames de chaque page de résultats
    
    if isinstance(id_peri_list, str):
        id_peri_list=[id_peri_list] # Convertir en liste si c'est une chaîne de caractères

    for id_peri in id_peri_list:
        url = f"{base_url}{id_peri}/"  # Construire l'URL complète en ajoutant l'id_peri
        dfs = []  # Liste pour stocker les DataFrames de chaque page de résultats
        page = 1
        params['page'] = 1
        has_more_pages = True

        if debug:
            print("id_peri:", id_peri)
            print("url:", url)

        while has_more_pages:
            response = requests.get(url, params=params)

            if debug:
                print("response status code:", response.status_code)

            if response.status_code == 200:
                data = response.json()['results']
                df = pd.DataFrame(data)
                dfs.append(df)

                # Vérifier si d'autres pages de résultats existent
                has_more_pages = response.json()['next'] is not None

                if debug:
                    print("has_more_pages:", has_more_pages)
                    print("page:", page)

                page += 1

                # Mettre à jour les paramètres de requête avec la page suivante
                params['page'] = page
            else:
                # La requête a échoué, vous pouvez gérer l'erreur en conséquence
                print("Erreur lors de la requête :", response.status_code)
                return None

        if dfs:
            df_i = pd.concat(dfs, ignore_index=True)

            if debug:
                print("df_i shape:", df_i.shape)

            df_list.append(df_i)  # Ajouter df_i à la liste df_list

    if df_list:
        df_final = pd.concat(df_list, ignore_index=True)

        if debug:
            print("df_final shape:", df_final.shape)

        return df_final
    else:
        return None


# %%
# fonction quand on doit boucler sur une valeur de param et pas dans l'url

def _get_api_data_list_param(base_url, id_peri_list, params=None, debug=False):
    df_list = []  # Liste pour stocker les DataFrames de chaque page de résultats
    
    if debug:
        print("pas_liste_avant :",not isinstance( params[id_peri_list], list))
    
    if not isinstance( params[id_peri_list], list):
        params[id_peri_list] = [params[id_peri_list]]  # Convertir en liste si c'est pas une liste

    if debug:
        print("pas_liste_apres :",not isinstance( params[id_peri_list], list))
    
    if debug:
        print(params[id_peri_list])
    
    
    
    for id_peri in params[id_peri_list]:
        url = f"{base_url}"  # Construire l'URL complète en ajoutant l'id_peri
        dfs = []  # Liste pour stocker les DataFrames de chaque page de résultats
        page = 1
        params['page'] = 1
        params[id_peri_list]=id_peri
        has_more_pages = True

        if debug:
            print("id_peri:", id_peri)
            print("url:", url)

        while has_more_pages:
            response = requests.get(url, params=params)

            if debug:
                print("response status code:", response.status_code)

            if response.status_code == 200:
                data = response.json()['results']
                df = pd.DataFrame(data)
                dfs.append(df)

                # Vérifier si d'autres pages de résultats existent
                has_more_pages = response.json()['next'] is not None

                if debug:
                    print("has_more_pages:", has_more_pages)
                    print("page:", page)

                page += 1

                # Mettre à jour les paramètres de requête avec la page suivante
                params['page'] = page
            else:
                # La requête a échoué, vous pouvez gérer l'erreur en conséquence
                print("Erreur lors de la requête :", response.status_code)
                return None

        if dfs:
            df_i = pd.concat(dfs, ignore_index=True)

            if debug:
                print("df_i shape:", df_i.shape)

            df_list.append(df_i)  # Ajouter df_i à la liste df_list

    if df_list:
        df_final = pd.concat(df_list, ignore_index=True)

        if debug:
            print("df_final shape:", df_final.shape)

        return df_final
    else:
        return None


# %% [markdown]
# ## fonction pour récupérer les données geo

# %%
def _get_api_data_list_param_geo(base_url, id_peri_list, params=None, debug=False):
    df_list = []  # Liste pour stocker les DataFrames de chaque page de résultats
    
    if debug:
        print("pas_liste_avant :",not isinstance( params[id_peri_list], list))
    
    if not isinstance( params[id_peri_list], list):
        params[id_peri_list] = [params[id_peri_list]]  # Convertir en liste si c'est pas une liste

    if debug:
        print("pas_liste_apres :",not isinstance( params[id_peri_list], list))
    
    if debug:
        print(params[id_peri_list])
    
    
    
    for id_peri in params[id_peri_list]:
        url = f"{base_url}"  # Construire l'URL complète en ajoutant l'id_peri
        dfs = []  # Liste pour stocker les DataFrames de chaque page de résultats
        page = 1
        params['page'] = 1
        params[id_peri_list]=id_peri
        has_more_pages = True

        if debug:
            print("id_peri:", id_peri)
            print("url:", url)

        while has_more_pages:
            response = requests.get(url, params=params)

            if debug:
                print("response status code:", response.status_code)

            if response.status_code == 200:
                # Filtrer les clés ayant des valeurs non nulles
                filtered_params = {key: value for key, value in params.items() if value is not None}
                
                # Générer les paramètres de la requête dans l'URL
                query_string = urlencode(filtered_params)
                
                # Concaténer l'URL de base avec les paramètres de la requête
                full_url = f"{url}?{query_string}"

                
                if debug:
                    print(full_url)
                
                df=gpd.read_file(full_url)
                # data = response.json()['results']
                # df = pd.DataFrame(data)
                dfs.append(df)

                # Vérifier si d'autres pages de résultats existent
                has_more_pages = response.json()['next'] is not None

                if debug:
                    print("has_more_pages:", has_more_pages)
                    print("page:", page)

                page += 1

                # Mettre à jour les paramètres de requête avec la page suivante
                params['page'] = page
            else:
                # La requête a échoué, vous pouvez gérer l'erreur en conséquence
                print("Erreur lors de la requête :", response.status_code)
                return None

        if dfs:
            df_i = pd.concat(dfs, ignore_index=True)

            if debug:
                print("df_i shape:", df_i.shape)

            df_list.append(df_i)  # Ajouter df_i à la liste df_list

    if df_list:
        df_final = pd.concat(df_list, ignore_index=True)

        if debug:
            print("df_final shape:", df_final.shape)

        return df_final
    else:
        return None
    
# %% [markdown]
# ## _get_api_data_list_param_geo



# %%
# on a quelques fois des résultats sous forme de dictionnaires non dataframable
# fonction spéciale :

def get_api_data_list_dic(base_url, id_peri_list, params=None, debug=False):
    df_list = []  # Liste pour stocker les dict de chaque page de résultats

    if isinstance(id_peri_list, str):
        id_peri_list = [id_peri_list]  # Convertir en liste si c'est une chaîne de caractères

    for id_peri in id_peri_list:
        url = f"{base_url}{id_peri}/"  # Construire l'URL complète en ajoutant l'id_peri
        dfs = []  # Liste pour stocker les DataFrames de chaque page de résultats
        page = 1
        params['page'] = 1
        has_more_pages = True

        if debug:
            print("id_peri:", id_peri)
            print("url:", url)

        while has_more_pages:
            response = requests.get(url, params=params)

            if debug:
                print("response status code:", response.status_code)

            if response.status_code == 200:
                data = response.json()
                dfs.append(data)

                # Vérifier si d'autres pages de résultats existent
                has_more_pages = False

                if debug:
                    print("has_more_pages:", has_more_pages)
                    print("page:", page)

                page += 1

                # Mettre à jour les paramètres de requête avec la page suivante
                params['page'] = page
            else:
                # La requête a échoué, vous pouvez gérer l'erreur en conséquence
                print("Erreur lors de la requête :", response.status_code)
                return None

        if dfs:
            df_list.extend(dfs)

    if df_list:
        return df_list
    else:
        return None
