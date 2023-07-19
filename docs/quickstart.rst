
Description
===========

``apifoncier`` est un module ``python`` qui propose 
une boîte à outils pour interagir plus facilement avec `l'API
Données foncières du Cerema <https://apidf-preprod.cerema.fr/>`_.

Il permet d'interroger facilement les différentes bases de données 
foncières produites par le Cerema et la DGALN directement via ``python``. 

.. note::
   
   Certains flux de l'API sont à accès restreint et nécessitent 
   d'appartenir à une structure publique bénéficiaire des données foncières.
   Rendez-vous sur `ConsultDF <https://consultdf.cerema.fr/consultdf/services/apidf>`_ 
   pour obtenir un jeton d'accès.

Installation
============

``apifoncier`` peut être installé via pip. Ouvrez votre terminal et taper la cammande suivante :

.. code-block:: bash

   $ pip install apifoncier


Usage
=====

Accès ouvert
------------

Pour démarrer, il suffit d'importer le module souhaité et de récupérer les données dans un dataframe (``pandas``)
ou un geodataframe (``geopandas``) via la fonction adéquate :

.. code-block:: python

    ## Récupérer des données de consommation d'espace sur une commune
    import apifoncier.ind_conso_espace as conso

    df = conso.communes(code_insee='59350')

.. code-block:: python

    ## Récupérer des données de prix sur une commune
    import apifoncier.ind_prix as prix
    
    df = prix.communes(code_insee='59350')

.. code-block:: python

    ## Récupérer des transactions issues de DVF+ sur une commune
    import apifoncier.dvf_opendata as dvf
    
    df = dvf.mutations(code_insee='59350')
    
    # avec les geometries
    gdf = dvf.geomutations(in_bbox=[])

.. code-block:: python

    ## Récupérer les friches
    import apifoncier.cartofriches as cartofriches

    # sur un département
    df = cartofriches.friches(coddep='59')

    # sur une commune avec les contours géométriques
    gdf = cartofriches.geofriches(code_insee=["59350", "59009"])

Accès restreint
---------------

Pour les données Fichiers fonciers et DV3F, il faut disposer d'un **jeton d'accès API** pour
s'authentifier et récupérer les données correspondantes. 
Le jeton est fourni au module via la méthode ``.configure()``

.. code-block:: python

    ## Import du module
    import apifoncier

    ## Configuration préalable du jeton API
    API_TOKEN = "<MON_TOKEN_API>"
    apifoncier.configure(TOKEN=API_TOKEN)

Une fois, le jeton configuré, les fonctions accessibles via le token sont désormais utilisables.

.. code-block:: python
    
    ## Récupérer les parcelles
    import apifoncier.ff as ff
    
    # sur une commune
    df = ff.parcelles(code_insee='59646')
    
    # sur une commune avec les contours géométriques
    gdf = ff.geoparcelles(in_bbox=[])


.. code-block:: python

    # Récupérer les mutations de DV3F
    import apifoncier.dv3f as dv3f
    
    # sur une commune
    df = dv3f.mutations(code_insee='59646')
    
    # sur une commune avec les contours géométriques
    gdf = dv3f.geomutations(in_bbox=[])

Ressources
============

Pour retrouver toutes les informations sur les données foncières :
`datafoncier.cerema.fr <https://datafoncier.cerema.fr>`_

Dictionnaire et documentation sur toutes les variables :
`doc-datafoncier.cerema.fr <https://doc-datafoncier.cerema.fr>`_

