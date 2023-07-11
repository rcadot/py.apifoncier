from apifoncier.utils import _get_api_data_list, _get_api_data_list_param, _get_api_data_list_param_geo

# ## friches

# %%
def friches(
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

# friches([59350,59002])
# %% [markdown]
# ## friches_dep
# %%
def friches_dep(
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

# geofriches_dep(['59','02'])



# %%
def friches_site(
    site_id        
):
    return get_api_data_list_dic(
        base_url='https://apidf-preprod.cerema.fr/cartofriches/friches/',
        id_peri_list=site_id,
        params={},
        debug=False
    )

# friches_site(site_id = ['59002_10038','59002_3873'])
# %%
