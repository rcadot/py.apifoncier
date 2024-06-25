Indicateurs de marché 
=====================

Présentation
------------

``apifoncier`` permet d'interroger librement les **indicateurs de marché** produites par le Cerema 
à partir de DV3F. Plus de détails sur `la rubrique Datafoncier <https://datafoncier.cerema.fr/donnees/autres-donnees-foncieres/indicateurs-prix/>`_

Les données proposées sont disponibles à **différentes échelles administratives** : communes, EPCI, départements, régions ainsi
qu'à l'échelle des aires d'attraction des villes (AAV).

Import
------

Pour importer le module correspondant :

.. code-block:: python

    import apifoncier.ind_marche as marche 

Description des fonctions
-------------------------

L'accès aux indicateurs de s'effectue via les codes INSEE des entités geographiques, 
en précisant éventuellement une année particulière :

Prix et volumes
^^^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_marche.prix_volume

Accessibilité
^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_marche.accessibilite

Activité de marché
^^^^^^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_marche.activite

Valorisation
^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_marche.valorisation

