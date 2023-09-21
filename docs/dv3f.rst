DV3F
==========

Présentation
------------

``apifoncier`` permet d'interroger les **mutations issues de DV3F**, base de données enrichie 
sur les marchés fonciers et immobiliers du Cerema. 
Plus de détails sur `DV3F <https://datafoncier.cerema.fr/dv3f>`_

Les données proposées sont disponibles sous forme de dataframe ou geodataframe, accessible soit via le
code insee de la commune ou une emprise geographique.

.. note:: 
    
    L'accès aux données DV3F nécessite d'appartenir à une structure publique bénéficiaire
    et d'avoir prélablement obtenu un jeton API.
    Rendez-vous sur `ConsultDF <https://consultdf.cerema.fr/consultdf/services/apidf>`_ pour
    plus d'informations.

Import
------

Pour importer le module correspondant :

.. code-block:: python

    ## Configuration préalable du jeton API
    import apifoncier
    API_TOKEN = "<MON_TOKEN_API>"
    apifoncier.configure(TOKEN=API_TOKEN)

    import apifoncier.dv3f as dv3f

Description des fonctions
-------------------------

.. autofunction:: apifoncier.dv3f.mutations

.. autofunction:: apifoncier.dv3f.geomutations

.. autofunction:: apifoncier.dv3f.mutation


