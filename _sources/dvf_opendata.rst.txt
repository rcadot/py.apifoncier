DVF+ open-data
===============

Présentation
------------

``apifoncier`` permet d'interroger librement les **mutations issues de DVF** selon le modèle de données du Cerema. 
Plus de détails sur `DVF+ <https://datafoncier.cerema.fr/donnees/autres-donnees-foncieres/dvfplus-open-data>`_

Les données proposées sont disponibles sous forme de dataframe ou geodataframe, accessible soit via le
code insee de la commune ou une emprise geographique.

Import
------

Pour importer le module correspondant :

.. code-block:: python

    import apifoncier.dvf_opendata as dvf

Description des fonctions
-------------------------

.. autofunction:: apifoncier.dvf_opendata.mutations

.. autofunction:: apifoncier.dvf_opendata.geomutations

.. autofunction:: apifoncier.dvf_opendata.mutation


Exemples
--------

La rubriques Exemples présente des usages de ce module :
:ref:`Exemples sur DVF+ open-data`
