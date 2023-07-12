Indicateurs de prix
===================


On peut extraire les données prix pour le périmètre de son choix tel que la commune ou l'epci comme dans les exemples ci-dessous.


.. code-block:: python
    apifoncier.ind_dv3f.com_annuel(code_insee='59350')


L'ensemble des fonctions liées aux indicateurs de prix présentées ci-dessous commencent par le 
préfixe `PERI_FREQ` où ``PERI`` et ``FREQ`` désigne les périmètres et fréquences des données comme indiqué dans  le `chapitre dédié <https://>`_.

.. autofunction:: apifoncier.ind_dv3f.aav_annuel

.. autofunction:: apifoncier.ind_dv3f.aav_triennal

.. autofunction:: apifoncier.ind_dv3f.com_annuel

.. autofunction:: apifoncier.ind_dv3f.com_triennal

.. autofunction:: apifoncier.ind_dv3f.dep_annuel

.. autofunction:: apifoncier.ind_dv3f.dep_triennal
    
.. autofunction:: apifoncier.ind_dv3f.epci_annuel

.. autofunction:: apifoncier.ind_dv3f.epci_triennal

.. autofunction:: apifoncier.ind_dv3f.reg_annuel

.. autofunction:: apifoncier.ind_dv3f.reg_triennal