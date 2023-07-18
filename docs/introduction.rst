
Présentation du package
=======================

Grâce au package ``apifoncier``, vous pouvez interroger les
différentes bases de données foncières produites par le Cerema et la
DGALN à l'aide de ``python``. Une partie des données est interrogeable
uniquement avec un accès restreint lié à vos droits. Pensez à vous
rendre sur 
`ConsultDF <https://consultdf.cerema.fr/consultdf/services/apidf>`_ 
pour obtenir un jeton d'accès.

Installation
============

Vous pouvez installer ``apifoncier`` via pip :

.. code-block:: python
    pip install apifoncier


Quickstart
================================


Indicateurs de consommation d’espace (accès libre)
--------------------------------------------------

.. code-block:: python
    import apifoncier.ind_conso_espace as conso
    df = conso.communes(code_insee=['59350'])

Indicateurs de prix (accès libre)
----------------------------------


Cartofriches (accès libre)
-------------------------------


DVF+ (accès libre)
---------------------


DV3F (accès restreint)
-------------------------


Fichiers fonciers (accès restreint)
--------------------------------------


Ressources
============

Pour retrouver toutes les informations sur les données foncières :
`datafoncier.cerema.fr <https://datafoncier.cerema.fr>`_

Dictionnaire et documentation sur toutes les variables :
`doc-datafoncier.cerema.fr <https://doc-datafoncier.cerema.fr>`_

`Pour en savoir plus sur l’API données foncières du
cerema. <https://apidf-preprod.cerema.fr/swagger/>`_