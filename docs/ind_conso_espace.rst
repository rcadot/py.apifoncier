Consommation ENAF
=================


Les données sont disponibles à deux échelles : communes et départements.

En indiquant le code INSEE d'une commune au format ``string``, on obtient un dataframe des consommations.


La fonction ``apifoncier.ind_conso_espace.communes_g()`` permet de générer un graphique ``plotly``` de la consommation sur la commune de son choix.

.. code-block:: python
    
    apifoncier.ind_conso_espace.communes_g(['97233','97234'],total=False)

Par défaut, les consommations sont affichées en hectares, mais on peut les indiquer en m² en choisissant ``hectare=FALSE``.



Retrouvez toutes les fonctions liées aux données de consommation d'ENAF :


.. autofunction:: apifoncier.ind_conso_espace.communes

.. autofonction:: apifoncier.ind_conso_espace.communes_g

.. autofunction:: apifoncier.ind_conso_espace.dep

.. autofonction:: apifoncier.ind_conso_espace.dep_g