Fichiers fonciers
=================

Présentation
------------

``apifoncier`` permet d'interroger les **parcelles, tup, locaux, propriétaires issues des Fichiers fonciers**,
base de données enrichie par le Cerema. 
Plus de détails sur `Fichiers fonciers <https://datafoncier.cerema.fr/fichiers-fonciers>`_


Les données proposées sont disponibles sous forme de dataframe ou geodataframe, accessible soit via le
code insee de la commune, du département ou une emprise geographique.

.. note:: 
    
    L'accès aux données Fichiers fonciers nécessite d'appartenir à une structure publique bénéficiaire
    et d'avoir prélablement obtenu un jeton API.
    Rendez-vous sur `ConsultDF <https://consultdf.cerema.fr/consultdf/services/apidf>`_ pour
    plus d'informations.

Import
------

Pour importer le module correspondant :

.. code-block:: python

    ## Le jeton est lu dans la variable d'environnement APIFONCIER_TOKEN
    import apifoncier.ff as ff

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

Parcelles
^^^^^^^^^

.. autofunction:: apifoncier.ff.parcelles

.. autofunction:: apifoncier.ff.geoparcelles

.. autofunction:: apifoncier.ff.parcelle


TUP
^^^

.. autofunction:: apifoncier.ff.tups

.. autofunction:: apifoncier.ff.geotups

.. autofunction:: apifoncier.ff.tup


Locaux
^^^^^^

.. autofunction:: apifoncier.ff.locaux

.. autofunction:: apifoncier.ff.local


Propriétaires
^^^^^^^^^^^^^

.. autofunction:: apifoncier.ff.proprios

.. autofunction:: apifoncier.ff.proprio
