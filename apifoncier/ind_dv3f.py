from apifoncier.utils import _get_api_data_list, _get_api_data_list_param, _get_api_data_list_param_geo


def aav_annuel(
    code_aav,
    annee=None,
    ordering=None
    ):
    """Indicateurs annuels DV3F à l'échelle AAV
    Args:
        code_aav (str): Code AAV de l'aire INSEE ou liste de codes
        annee (int, optional): Année de mutation. Defaults to None.
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs annuels DV3F à l'échelle AAV
        """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/aav/annuel/',
            id_peri_list=code_aav,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# aav_annuel(code_aav='004')

# %% [markdown]
# ## aav_triennal

# %%
def aav_triennal(
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

# aav_triennal(code_aav='004')

# %% [markdown]
# ## com_annuel

# %%
def com_annuel(
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

# com_annuel(code_insee='59350')

# %% [markdown]
# ## com_triennal

# %%
def com_triennal(
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

# com_triennal(code_insee='59350')

# %% [markdown]
# ## dep_annuel

# %%
def dep_annuel(
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

# dep_annuel(coddep='59')

# %% [markdown]
# ## dep_triennal

# %%
def dep_triennal(
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

# dep_triennal(coddep='59')

# %% [markdown]
# ## epci_annuel

# %%
def epci_annuel(
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

# epci_annuel(code_epci='200093201')

# %% [markdown]
# ## epci_triennal

# %%
def epci_triennal(
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

# epci_triennal(code_epci='200093201')

# %% [markdown]
# ## reg_annuel

# %%
def reg_annuel(
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

# reg_annuel(codreg='32')

# %% [markdown]
# ## reg_triennal

# %%
def reg_triennal(
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

# reg_triennal(codreg='32')
