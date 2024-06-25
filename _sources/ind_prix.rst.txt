Indicateurs de prix (déprécié) 
==============================

Présentation
------------

``apifoncier`` permet d'interroger librement les **indicateurs de prix annuels et tri-annuels** produites par le Cerema 
à partir de DV3F. Plus de détails sur `la rubrique Datafoncier <https://datafoncier.cerema.fr/donnees/autres-donnees-foncieres/indicateurs-prix/>`_

Les données proposées sont disponibles à **différentes échelles administratives** : communes, EPCI, départements, régions ainsi
qu'à l'échelle des aires d'attraction des villes (AAV).

Import
------

Pour importer le module correspondant :

.. code-block:: python

    import apifoncier.ind_prix as prix 

Description des fonctions
-------------------------

L'accès aux indicateurs annuels ou triennaux s'effectue via les codes INSEE ou code AAV, 
en précisant éventuellement une année particulière :

Pour les communes
^^^^^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_prix.communes

Pour les EPCI
^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_prix.epci

Pour les départements
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_prix.departements

Pour les régions
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_prix.regions

Pour les aires d'attraction de la ville (AAV)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: apifoncier.ind_prix.aav


Exemples
--------

La rubriques Exemples présente des usages de ce module :
:ref:`Exemples sur Indicateurs de prix`
