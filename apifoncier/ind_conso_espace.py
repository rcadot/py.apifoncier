from apifoncier.utils import _get_api_data_list, _get_api_data_list_param, _get_api_data_list_param_geo

def communes(
    code_insee,
    annee_min=None,
    annee_max=None
    ):
    """
    Consommation d'espace par commune

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer un vecteur de code insee sans limite maximum)
        
        annee_min (int, optional): Année jusqu'à laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.
        
        annee_max (int, optional): Année à partir de laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs de consommation d'espace pour la période comprise entre annee_min et annee_max, bornes incluses, à l'échelle communale

    >>> apifoncier.conso_espace.communes(['97233','97234'])
    """
    return _get_api_data_list(
        base_url='https://apidf-preprod.cerema.fr/indicateurs/conso_espace/communes/',
        id_peri_list=code_insee,
        params={                
                'annee_min': annee_min,
                'annee_max': annee_max
            }
    )

# %%
def communes_g(
    code_insee,
    annee_min=None,
    annee_max=None,
    total=False
    ):
    """
    Consommation d'espace par commune (graphique)

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer un vecteur de code insee sans limite maximum)
        
        annee_min (int, optional): Année jusqu'à laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.
        
        annee_max (int, optional): Année à partir de laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.

        total(bool, optional): True pour afficher le total agrégé, False pour avoir par typologie

    Returns:
        graphique plotly: Renvoie les indicateurs de consommation d'espace pour la période comprise entre annee_min et annee_max, bornes incluses, à l'échelle communale

    >>> apifoncier.conso_espace.communes_g(['97233','97234'],total=False)
    """

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


# %%
def dep(
    coddep,
    annee_min=None,
    annee_max=None
    ):
    """Consommation d'espace par département

    Args:
        coddep (str): Code INSEE du département (possibilité de passer un vecteur de code insee sans limite maximum)
        
        annee_min (int, optional): Année jusqu'à laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.
        
        annee_max (int, optional): Année à partir de laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs de consommation d'espace pour la période comprise entre annee_min et annee_max, bornes incluses, à l'échelle départementale

    >>> apifoncier.conso_espace.dep(['972','971'])
    """
    return _get_api_data_list(
        base_url='https://apidf-preprod.cerema.fr/indicateurs/conso_espace/departements/',
        id_peri_list=coddep,
        params={                
                'annee_min': annee_min,
                'annee_max': annee_max
            }
    )


# %%
def dep_g(
    coddep,
    annee_min=None,
    annee_max=None,
    total=False
    ):
    """
    Consommation d'espace par département (graphique)

    Args:
        coddep (str): Code INSEE u département (possibilité de passer un vecteur de code insee sans limite maximum)
        
        annee_min (int, optional): Année jusqu'à laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.
        
        annee_max (int, optional): Année à partir de laquelle renvoyer les indicateurs d'artificialisation (incluse). Defaults to None.

        total(bool, optional): True pour afficher le total agrégé, False pour avoir par typologie

    Returns:
        graphique plotly: Renvoie les indicateurs de consommation d'espace pour la période comprise entre annee_min et annee_max, bornes incluses, à l'échelle départementale

    >>> apifoncier.conso_espace.dep_g(['59','62'],total=True)
    """
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

