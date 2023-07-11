from apifoncier.utils import _get_api_data_list, _get_api_data_list_param, _get_api_data_list_param_geo


def aav_annuel(
    code_aav,
    annee=None,
    ordering=None
    ):
    """
    Indicateurs annuels DV3F à l'échelle AAV

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

# apifoncier.ind_dv3f.aav_annuel(code_aav='004')

# %% [markdown]
# ## aav_triennal

# %%
def aav_triennal(
    code_aav,
    annee=None,
    ordering=None
    ):
    """
    Indicateurs triennaux DV3F à l'échelle AAV
    
    Args:
    	code_aav(str): Code AAV de l'aire INSEE
    	
        annee(int): Année de mutation centrale de la période triennale (par exemple, 2011 pour la période 2010-2012)
    	
        ordering(str,optional): Which field to use when ordering the results.
    
    Returns: 
    	Renvoie les indicateurs triennaux DV3F à l'échelle AAV
    
    >>> apifoncier.ind_dv3f.aav_triennal('004')

    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/aav/triennal/',
            id_peri_list=code_aav,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# %%
def com_annuel(
    code_insee,
    annee=None,
    ordering=None
    ):
    """
    Indicateurs annuels DV3F à l'échelle de la commune

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs annuels DV3F à l'échelle communale

    >>> apifoncier.ind_dv3f.com_annuel(code_insee='59350')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/communes/annuel/',
            id_peri_list=code_insee,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# apifoncier.ind_dv3f.com_annuel(code_insee='59350')

# %% [markdown]
# ## com_triennal

# %%
def com_triennal(
    code_insee,
    annee=None,
    ordering=None
    ):
    """
    Indicateurs triennaux DV3F à l'échelle de la commune

    Parameters:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation centrale de la période triennale (par exemple, 2011 pour la période 2010-2012). Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs annuels DV3F à l'échelle communale

    >>> apifoncier.ind_dv3f.com_triennal(code_insee='59350')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/communes/triennal/',
            id_peri_list=code_insee,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )


# %%
def dep_annuel(
    coddep,
    annee=None,
    ordering=None
    ):
    """Indicateurs annuels DV3F à l'échelle du département

    Args:
        coddep (str): Code INSEE départemental (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs annuels DV3F à l'échelle départementale

    >>> apifoncier.ind_dv3f.dep_annuel(coddep='59')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/departements/annuel/',
            id_peri_list=coddep,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

# %%
def dep_triennal(
    coddep,
    annee=None,
    ordering=None
    ):
    """Indicateurs triennaux DV3F à l'échelle du département

    Args:
        coddep (str): Code INSEE départemental (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation centrale de la période triennale (par exemple, 2011 pour la période 2010-2012). Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs triennaux DV3F à l'échelle départementale

    >>> apifoncier.ind_dv3f.dep_triennal(coddep='59')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/departements/triennal/',
            id_peri_list=coddep,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )


# %%
def epci_annuel(
    code_epci,
    annee=None,
    ordering=None
    ):
    """Indicateurs annuels DV3F à l'échelle de l'epci

    Args:
        code_epci (str): Code INSEE de l'epci (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs annuels DV3F à l'échelle de l'epci

    >>> apifoncier.ind_dv3f.epci_annuel(code_epci='200093201')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/epci/annuel/',
            id_peri_list=code_epci,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )


# %%
def epci_triennal(
    code_epci,
    annee=None,
    ordering=None
    ):
    """Indicateurs triennaux DV3F à l'échelle de l'epci

    Args:
        code_epci (str): Code INSEE de l'epci (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation centrale de la période triennale (par exemple, 2011 pour la période 2010-2012)
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs triennaux DV3F à l'échelle de l'epci

    >>> apifoncier.ind_dv3f.epci_triennal(code_epci='200093201')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/epci/triennal/',
            id_peri_list=code_epci,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )


# %%
def reg_annuel(
    codreg,
    annee=None,
    ordering=None
    ):
    """
    Indicateurs annuels DV3F à l'échelle de la région

    Args:
        codreg (str): Code INSEE de la région (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation. Defaults to None.
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs annuels DV3F à l'échelle de la région

    >>> apifoncier.ind_dv3f.reg_annuel(codreg='32')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/regions/annuel/',
            id_peri_list=codreg,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )


# %% [markdown]
# ## reg_triennal

# %%
def reg_triennal(
    codreg,
    annee=None,
    ordering=None
    ):
    """
    Indicateurs triennaux DV3F à l'échelle de la région

    Args:
        codreg (str): Code INSEE de la région (possibilité de passer une liste de code insee sans limite maximum)
        
        annee (int, optional): Année de mutation centrale de la période triennale (par exemple, 2011 pour la période 2010-2012)
        
        ordering (str, optional): Which field to use when ordering the results.. Defaults to None.

    Returns:
        dataframe: Renvoie les indicateurs triennaux DV3F à l'échelle de la région

    >>> apifoncier.ind_dv3f.reg_triennal(codreg='32')
    """
    return _get_api_data_list(
            base_url='https://apidf-preprod.cerema.fr/indicateurs/dv3f/regions/triennal/',
            id_peri_list=codreg,
            #debug=True,
            params={                
                    'annee': annee,
                    'ordering': ordering
                }
        )

