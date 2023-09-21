Indicateurs de consommation d'espace
=====================================

Présentation
------------

``apifoncier`` permet d'interroger librement les **données de consommation d'espace annuelles** produites par le Cerema 
et la DGALN. Plus de détails sur le `portail de l'artificialisation <https://artificialisation.developpement-durable.gouv.fr/>`_

Les données proposées sont disponibles à **deux échelles** : communes et départements.

Import
------

Pour importer le module correspondant :

.. code-block:: python

    import apifoncier.ind_conso_espace as conso_enaf 

Description des fonctions
-------------------------

Pour les communes
^^^^^^^^^^^^^^^^^

L'accès aux indicateurs annuels communaux s'effectue via les codes INSEE des communes, 
en limitant éventuellement la période :

.. autofunction:: apifoncier.ind_conso_espace.communes


Pour les départements
^^^^^^^^^^^^^^^^^^^^^

L'accès aux indicateurs annuels départementaux s'effectue via les codes INSEE des départements, 
en limitant éventuellement la période :

.. autofunction:: apifoncier.ind_conso_espace.departements

Exemples
--------

La rubriques Exemples présente des usages de ce module :
:ref:`Exemples sur Consommation d'espace`