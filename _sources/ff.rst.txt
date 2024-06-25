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

    ## Configuration préalable du jeton API
    import apifoncier
    API_TOKEN = "<MON_TOKEN_API>"
    apifoncier.configure(TOKEN=API_TOKEN)

    import apifoncier.ff as ff

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
