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

    ## Le jeton est lu dans la variable d'environnement APIFONCIER_TOKEN
    import apifoncier.dv3f as dv3f

Le module lit par défaut la variable d'environnement ``APIFONCIER_TOKEN``, ce qui évite
d'écrire le jeton dans le code. À défaut, il peut être transmis explicitement, en le lisant
dans l'environnement ou en le saisissant à l'exécution, jamais en clair dans un script versionné :

.. code-block:: python

    import os
    from getpass import getpass
    import apifoncier

    apifoncier.configure(TOKEN=os.environ["MON_JETON"])
    # ou, de façon interactive
    apifoncier.configure(TOKEN=getpass("Jeton API : "))

Description des fonctions
-------------------------

.. autofunction:: apifoncier.dv3f.mutations

.. autofunction:: apifoncier.dv3f.geomutations

.. autofunction:: apifoncier.dv3f.mutation


