Cartofriches
===================


On peut accéder aux friches, soit par département, commune.

Pour un ou plusieurs département :

.. code-block:: python

    apifoncier.cartofriches.friches_dep(['62','59'])


Pour une ou plusieurs communes :

.. code-block:: python

    apifoncier.cartofriches.friches(code_insee = ['59002','59008'])

 
On peut également accéder aux objets géographiques associés.

.. code-block:: python
    
    apifoncier.cartofriches.geofriches('59350')

Retrouvez toutes les fonctions liées aux données de 
cartofriches :

.. autofunction:: apifoncier.cartofriches.friches

.. autofunction:: apifoncier.cartofriches.friches_dep

.. autofunction:: apifoncier.cartofriches.geofriches

.. autofunction:: apifoncier.cartofriches.geofriches_dep

.. autofunction:: apifoncier.cartofriches.friches_site