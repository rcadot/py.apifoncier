from apifoncier.utils import _get_api_data_list, _get_api_data_list_param, _get_api_data_list_param_geo

# %%
def friches(
    code_insee,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    """Retourne les friches issues de Cartofriches pour la commune demandée

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)
        
        fields (str, optional): Retourne tous les champs associés si fields=all, sinon retourne uniquement une selection de champs. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results. Defaults to None.
        
        surface_max (int, optional): Surface maximale de l'unité foncière. Defaults to None.
        
        surface_min (int, optional): Surface minimale de l'unité foncière. Defaults to None.
        
        urba_zone_type (str, optional): Type de zone d'urbanisme. Defaults to None.

    Returns:
        dataframe: Retourne les friches issues de Cartofriches pour la commune demandée
    
    >>> apifoncier.cartofriches.friches([59350,59002])
    """
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


# %%
def friches_dep(
    coddep,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    """Retourne les friches issues de Cartofriches pour le département demandé

    Args:
        coddep (str): Code INSEE du département (possibilité de passer une liste de code insee sans limite maximum)
        
        fields (str, optional): Retourne tous les champs associés si fields=all, sinon retourne uniquement une selection de champs. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results. Defaults to None.
        
        surface_max (int, optional): Surface maximale de l'unité foncière. Defaults to None.
        
        surface_min (int, optional): Surface minimale de l'unité foncière. Defaults to None.
        
        urba_zone_type (str, optional): Type de zone d'urbanisme. Defaults to None.

    Returns:
        dataframe: Retourne les friches issues de Cartofriches pour le département demandé
    
    >>> apifoncier.cartofriches.friches_dep('59')
    """
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

# friches_dep([59,62])


# %%

def geofriches(
    code_insee,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    """Retourne les geodataframe des friches issues de Cartofriches pour la commune demandée

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)
        
        fields (str, optional): Retourne tous les champs associés si fields=all, sinon retourne uniquement une selection de champs. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results. Defaults to None.
        
        surface_max (int, optional): Surface maximale de l'unité foncière. Defaults to None.
        
        surface_min (int, optional): Surface minimale de l'unité foncière. Defaults to None.
        
        urba_zone_type (str, optional): Type de zone d'urbanisme. Defaults to None.

    Returns:
       geodataframe: Retourne les friches issues de Cartofriches pour la commune demandée
    
    >>> apifoncier.cartofriches.geofriches('59350')
    """
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

# geofriches(59350)
# %%

def geofriches_dep(
    coddep,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None
    ):
    """Retourne les geodataframe des friches issues de Cartofriches pour le département demandé

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)
        
        fields (str, optional): Retourne tous les champs associés si fields=all, sinon retourne uniquement une selection de champs. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results. Defaults to None.
        
        surface_max (int, optional): Surface maximale de l'unité foncière. Defaults to None.
        
        surface_min (int, optional): Surface minimale de l'unité foncière. Defaults to None.
        
        urba_zone_type (str, optional): Type de zone d'urbanisme. Defaults to None.

    Returns:
       geodataframe: Retourne les friches issues de Cartofriches pour le département demandé
    
    >>> apifoncier.cartofriches.geofriches_dep('59')
    """
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





# %%
def friches_site(
    site_id        
):
    """Retourne la friche pour l'identifiant de site demandé

    Args:
        site_id (str): A unique value identifying this cartofriches.

    Returns:
        dict: Retourne la friche pour l'identifiant de site demandé

    >>> friches_site(site_id = ['59002_10038','59002_3873'])
    """
    return get_api_data_list_dic(
        base_url='https://apidf-preprod.cerema.fr/cartofriches/friches/',
        id_peri_list=site_id,
        params={},
        debug=False
    )

