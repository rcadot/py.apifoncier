# %%
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


# %% [markdown]
# # Conso
# ## ind_conso_espace_communes

# %%
def ind_conso_espace_communes(
    code_insee,
    annee_min=None,
    annee_max=None
    ):
    return _get_api_data_list(
        base_url='https://apidf-preprod.cerema.fr/indicateurs/conso_espace/communes/',
        id_peri_list=code_insee,
        params={                
                'annee_min': annee_min,
                'annee_max': annee_max
            }
    )

# %%
# ind_conso_espace_communes(['97233','97234'])

# %%
# ind_conso_espace_communes('97233')

# %% [markdown]
# ## ind_conso_espace_communes_g

# %%
def ind_conso_espace_communes_g(
    code_insee,
    annee_min=None,
    annee_max=None,
    total=False
    ):

    data_api = _get_api_data_list(
        base_url='https://apidf-preprod.cerema.fr/indicateurs/conso_espace/communes/',
        id_peri_list=code_insee,
        params={                
                'annee_min': annee_min,
                'annee_max': annee_max
            }
    )

    data_api.rename(columns={
        'conso_act': 'Activité',
        'conso_hab': 'Habitat',
        'conso_mix': 'Mixte',
        'conso_inc': 'Inconnue'
    }, inplace=True)

    df_final=pd.melt(
            data_api,
            id_vars=['annee', 'idcom'],
            value_vars=['Activité' , 'Habitat' , 'Mixte' , 'Inconnue'],
            var_name='conso_type',
            value_name='conso_value'
        )
    
    if total:
         df_agg=df_final.groupby(['annee'])['conso_value'].sum().reset_index()
         df_agg=df_agg.assign(conso_type='Total')
    else :
         df_agg=df_final.groupby(['conso_type','annee'])['conso_value'].sum().reset_index()


    fig = px.bar(
        df_agg, 
        x='annee', 
        y='conso_value',
        color='conso_type',
        title="Consommation d'ENAF"
        )
    
    fig.update_layout(
        showlegend= not total,
        legend=dict(title="Types"),
        hovermode = "x unified",
        xaxis=dict(
            title='Années',
            tickmode='linear'
        ),
        yaxis=dict(
            title="Consommation d'ENAF en m²"
        )
    )
        
    return fig.show()


# ind_conso_espace_communes_g(['59002','59350'],total=False)




# %% [markdown]
# ## ind_conso_espace_dep

# %%
def ind_conso_espace_dep(
    coddep,
    annee_min=None,
    annee_max=None
    ):
    return _get_api_data_list(
        base_url='https://apidf-preprod.cerema.fr/indicateurs/conso_espace/departements/',
        id_peri_list=coddep,
        params={                
                'annee_min': annee_min,
                'annee_max': annee_max
            }
    )

# %%
# ind_conso_espace_dep([10,11,972],annee_min=2019)

# %% [markdown]
# ## ind_conso_espace_dep_g

# %%
def ind_conso_espace_dep_g(
    coddep,
    annee_min=None,
    annee_max=None,
    total=False
    ):

    data_api = _get_api_data_list(
        base_url='https://apidf-preprod.cerema.fr/indicateurs/conso_espace/departements/',
        id_peri_list=coddep,
        params={                
                'annee_min': annee_min,
                'annee_max': annee_max
            }
    )

    data_api.rename(columns={
        'conso_act': 'Activité',
        'conso_hab': 'Habitat',
        'conso_mix': 'Mixte',
        'conso_inc': 'Inconnue'
    }, inplace=True)

    # return data_api

    df_final=pd.melt(
            data_api,
            id_vars=['annee', 'iddep'],
            value_vars=['Activité' , 'Habitat' , 'Mixte' , 'Inconnue'],
            var_name='conso_type',
            value_name='conso_value'
        )
    
    # return df_final
    
    if total:
         df_agg=df_final.groupby(['annee'])['conso_value'].sum().reset_index()
         df_agg=df_agg.assign(conso_type='Total')
    else :
         df_agg=df_final.groupby(['conso_type','annee'])['conso_value'].sum().reset_index()


    fig = px.bar(
        df_agg, 
        x='annee', 
        y='conso_value',
        color='conso_type',
        title="Consommation d'ENAF"
        )
    
    fig.update_layout(
        showlegend= not total,
        legend=dict(title="Types"),
        hovermode = "x unified",
        xaxis=dict(
            title='Années',
            tickmode='linear'
        ),
        yaxis=dict(
            title="Consommation d'ENAF en m²"
        )
    )
        
    return fig.show()


# ind_conso_espace_dep_g(['59','62'],total=True)

# %% [markdown]
# # Indicateurs de prix
# ## ind_dv3f_aav_annuel

# %%
def ind_dv3f_aav_annuel(
    code_aav,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/aav/annuel/',
            id_peri_list=code_aav,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_aav_annuel(code_aav='004')

# %% [markdown]
# ## ind_dv3f_aav_triennal

# %%
def ind_dv3f_aav_triennal(
    code_aav,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/aav/triennal/',
            id_peri_list=code_aav,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_aav_triennal(code_aav='004')

# %% [markdown]
# ## ind_dv3f_com_annuel

# %%
def ind_dv3f_com_annuel(
    code_insee,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/communes/annuel/',
            id_peri_list=code_insee,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_com_annuel(code_insee='59350')

# %% [markdown]
# ## ind_dv3f_com_triennal

# %%
def ind_dv3f_com_triennal(
    code_insee,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/communes/triennal/',
            id_peri_list=code_insee,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_com_triennal(code_insee='59350')

# %% [markdown]
# ## ind_dv3f_dep_annuel

# %%
def ind_dv3f_dep_annuel(
    coddep,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/departements/annuel/',
            id_peri_list=coddep,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_dep_annuel(coddep='59')

# %% [markdown]
# ## ind_dv3f_dep_triennal

# %%
def ind_dv3f_dep_triennal(
    coddep,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/departements/triennal/',
            id_peri_list=coddep,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_dep_triennal(coddep='59')

# %% [markdown]
# ## ind_dv3f_epci_annuel

# %%
def ind_dv3f_epci_annuel(
    code_epci,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/epci/annuel/',
            id_peri_list=code_epci,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_epci_annuel(code_epci='200093201')

# %% [markdown]
# ## ind_dv3f_epci_triennal

# %%
def ind_dv3f_epci_triennal(
    code_epci,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/epci/triennal/',
            id_peri_list=code_epci,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_epci_triennal(code_epci='200093201')

# %% [markdown]
# ## ind_dv3f_reg_annuel

# %%
def ind_dv3f_reg_annuel(
    codreg,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/regions/annuel/',
            id_peri_list=codreg,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_reg_annuel(codreg='32')

# %% [markdown]
# ## ind_dv3f_reg_triennal

# %%
def ind_dv3f_reg_triennal(
    codreg,
    annee=None,
    ordering=None
    ):
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/regions/triennal/',
            id_peri_list=codreg,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# ind_dv3f_reg_triennal(codreg='32')

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
# ## cartofriches_friches

# %%
def cartofriches_friches(
    code_insee,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    return _get_api_data_list_param( 
        base_url='https://apidf-preprod.cerema.fr/cartofriches/friches/', 
        id_peri_list="code_insee", # juste "" 
        params={
            'code_insee':code_insee, # le code_insee dans les params
            'fields':fields,
            'ordering':ordering,
            'surface_max':surface_max,
            'surface_min':surface_min,
            'urba_zone_type':urba_zone_type
        }
    )

# cartofriches_friches([59350,59002])
# %% [markdown]
# ## cartofriches_friches_dep
# %%
def cartofriches_friches_dep(
    coddep,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    return _get_api_data_list_param( 
        base_url='https://apidf-preprod.cerema.fr/cartofriches/friches/', 
        id_peri_list="coddep", # juste "" 
        params={
            'coddep':coddep, # le code_insee dans les params
            'fields':fields,
            'ordering':ordering,
            'surface_max':surface_max,
            'surface_min':surface_min,
            'urba_zone_type':urba_zone_type
        }
    )

# cartofriches_friches_dep([59,62])

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

def cartofriches_geofriches(
    code_insee,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    return _get_api_data_list_param_geo( 
        debug=False,
        base_url='https://apidf-preprod.cerema.fr/cartofriches/geofriches/', 
        id_peri_list="code_insee", 
        params={
            'code_insee':code_insee,
            'fields':fields,
            'ordering':ordering,
            'surface_max':surface_max,
            'surface_min':surface_min,
            'urba_zone_type':urba_zone_type
        }
    )

# cartofriches_geofriches(59350)
# %%

def cartofriches_geofriches_dep(
    coddep,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    return _get_api_data_list_param_geo( 
        debug=False,
        base_url='https://apidf-preprod.cerema.fr/cartofriches/geofriches/', 
        id_peri_list="coddep", 
        params={
            'coddep':coddep,
            'fields':fields,
            'ordering':ordering,
            'surface_max':surface_max,
            'surface_min':surface_min,
            'urba_zone_type':urba_zone_type
        }
    )

# cartofriches_geofriches_dep(['59','02'])


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


# %%
def cartofriches_friches_site(
    site_id        
):
    return get_api_data_list_dic(
        base_url='https://apidf-preprod.cerema.fr/cartofriches/friches/',
        id_peri_list=site_id,
        params={},
        debug=False
    )

# cartofriches_friches_site(site_id = ['59002_10038','59002_3873'])
# %%
