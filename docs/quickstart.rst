Démarrage rapide
================

``apifoncier`` est un client Python pour `l'API Données foncières du Cerema <https://apidf-preprod.cerema.fr/swagger/>`_.
Il restitue les données sous forme de tableaux ``pandas`` (ou ``polars``) et de ``GeoDataFrame``
(``geopandas``), à partir des bases foncières produites par le Cerema et la DGALN.

.. note::

   Les flux Fichiers fonciers et DV3F sont à accès restreint. Ils exigent d'appartenir
   à une structure publique bénéficiaire des données foncières et de disposer d'un jeton,
   à demander sur `ConsultDF <https://consultdf.cerema.fr/consultdf/services/apidf>`_.

Installation
------------

.. code-block:: bash

   pip install apifoncier

Le format de sortie ``polars`` est facultatif et nécessite l'extra correspondant :

.. code-block:: bash

   pip install "apifoncier[polars]"

Le paquet requiert Python 3.9 ou une version ultérieure.

Accès libre
-----------

Il suffit d'importer le module thématique voulu et d'appeler la fonction adaptée.
Les fonctions dont le nom commence par ``geo`` renvoient un ``GeoDataFrame``.

.. code-block:: python

    ## Consommation d'espace sur une commune
    import apifoncier.ind_conso_espace as conso

    df = conso.communes(code_insee="59350")

.. code-block:: python

    ## Prix sur une commune
    import apifoncier.ind_prix as prix

    df = prix.communes(code_insee="59350")

.. code-block:: python

    ## Transactions issues de DVF+ sur une commune
    import apifoncier.dvf_opendata as dvf

    df = dvf.mutations(code_insee="59350")

    # avec les géométries
    gdf = dvf.geomutations(in_bbox=[3, 50, 3.01, 50.01])

.. code-block:: python

    ## Friches
    import apifoncier.cartofriches as cartofriches

    # sur un département
    df = cartofriches.friches(coddep="59")

    # sur plusieurs communes, avec les contours
    gdf = cartofriches.geofriches(code_insee=["59350", "59009"])

La localisation se précise par ``code_insee`` (une chaîne ou une liste), ``coddep``,
``in_bbox`` (emprise ``[lon_min, lat_min, lon_max, lat_max]``) ou ``lon_lat``
(point contenu dans l'entité). Si aucun de ces paramètres n'est fourni pour un endpoint
qui l'exige, une ``ValidationError`` est levée. Lorsque plusieurs sont fournis, seul le plus
prioritaire est utilisé et un avertissement est émis. Les codes INSEE sont regroupés
par lots de 10 dans une même requête.

L'emprise ``in_bbox`` est contrôlée avant l'envoi de la requête. Elle ne peut pas dépasser
0,02° x 0,02° pour les Fichiers fonciers, DVF+ et DV3F, ni 1° x 1° pour Cartofriches.

Accès restreint
---------------

Le jeton se fournit de préférence par la variable d'environnement ``APIFONCIER_TOKEN``,
que le module lit lorsque le paramètre ``TOKEN`` n'est pas configuré :

.. code-block:: bash

   export APIFONCIER_TOKEN="<jeton>"

Les fonctions des modules ``ff`` et ``dv3f`` sont alors directement utilisables :

.. code-block:: python

    ## Parcelles des Fichiers fonciers
    import apifoncier.ff as ff

    df = ff.parcelles(code_insee="59646")
    gdf = ff.geoparcelles(in_bbox=[3, 50, 3.01, 50.01])

.. code-block:: python

    ## Mutations de DV3F
    import apifoncier.dv3f as dv3f

    df = dv3f.mutations(code_insee="59646")
    gdf = dv3f.geomutations(in_bbox=[3, 50, 3.01, 50.01])

Le jeton peut aussi être transmis par ``apifoncier.configure(TOKEN=...)``, à condition de
le lire dans l'environnement ou de le saisir à l'exécution, et non de l'écrire dans le code :

.. code-block:: python

    import os
    import apifoncier

    apifoncier.configure(TOKEN=os.environ["MON_JETON"])

.. warning::

   Un jeton écrit en clair dans un script ou un notebook versionné finit tôt ou tard
   dans l'historique du dépôt et doit alors être considéré comme compromis.

Formats de sortie
-----------------

Les tableaux sont des ``DataFrame`` pandas par défaut. Pour obtenir des ``DataFrame``
polars, il faut installer l'extra ``polars`` puis modifier la configuration :

.. code-block:: python

    import apifoncier

    apifoncier.configure(OUTPUT_FORMAT="polars")

Les fonctions ``geo*`` renvoient toujours un ``GeoDataFrame`` en EPSG:4326, indexé par
l'identifiant des entités, y compris lorsque la réponse est vide.

Pour aller plus loin
--------------------

La page :doc:`configuration` détaille l'ensemble des paramètres, la gestion des erreurs,
la fonction générique :func:`apifoncier.get` et les garanties de sécurité du module.

Ressources
----------

Les informations sur les données foncières sont rassemblées sur
`datafoncier.cerema.fr <https://datafoncier.cerema.fr>`_, et le dictionnaire des variables
sur `doc-datafoncier.cerema.fr <https://doc-datafoncier.cerema.fr>`_. L'API elle-même est décrite
dans son `swagger <https://apidf-preprod.cerema.fr/swagger/>`_.
