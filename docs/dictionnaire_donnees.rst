.. Fichier généré par scripts/generer_dictionnaire.py : ne pas modifier à la main.

Dictionnaire de données
=======================

Ce dictionnaire recense, pour chaque fonction publique du paquet, l'endpoint de l'API interrogé, le mode d'accès, l'objet renvoyé et les paramètres acceptés. La signification des champs renvoyés par l'API est documentée sur `doc-datafoncier.cerema.fr <https://doc-datafoncier.cerema.fr>`_.

Conventions communes aux endpoints de liste :

* un paramètre de localisation au moins est requis ; par ordre de priorité ``lon_lat``, ``in_bbox``, ``code_insee``, ``code``, ``coddep`` ;
* les listes de valeurs sont transmises séparées par des virgules ;
* ``page_size`` est fixé par la configuration ``PAGE_SIZE`` et la pagination est parcourue intégralement.

Module ``apifoncier.cartofriches``
----------------------------------

Accès : libre.

``friches``
^^^^^^^^^^^

* Endpoint : ``GET /cartofriches/friches/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``coddep``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE des départements.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 1° x 1° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les friches renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``surface_max``
     - float
     - ``None``
     - Surface maximale de l'unité foncière (m²).
   * - ``surface_min``
     - float
     - ``None``
     - Surface minimale de l'unité foncière (m²).
   * - ``urba_zone_type``
     - str
     - ``None``
     - Type de zone d'urbanisme.

``geofriches``
^^^^^^^^^^^^^^

* Endpoint : ``GET /cartofriches/geofriches/``
* Renvoie : GeoDataFrame (EPSG:4326), index = identifiant

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``coddep``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE des départements.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 1° x 1° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les friches renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``surface_max``
     - float
     - ``None``
     - Surface maximale de l'unité foncière (m²).
   * - ``surface_min``
     - float
     - ``None``
     - Surface minimale de l'unité foncière (m²).
   * - ``urba_zone_type``
     - str
     - ``None``
     - Type de zone d'urbanisme.

``friche``
^^^^^^^^^^

* Endpoint : ``GET /cartofriches/friches/{site_id}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``site_id``
     - str
     - ``requis``
     - Identifiant du site Cartofriches.

Module ``apifoncier.dvf_opendata``
----------------------------------

Accès : libre.

``mutations``
^^^^^^^^^^^^^

* Endpoint : ``GET /dvf_opendata/mutations/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les mutations renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``anneemut_min``
     - int \| str
     - ``None``
     - Année de mutation minimale.
   * - ``anneemut_max``
     - int \| str
     - ``None``
     - Année de mutation maximale.
   * - ``anneemut``
     - int \| str
     - ``None``
     - Année de mutation.
   * - ``codtypbien``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie de bien ; les premiers niveaux suffisent (liste ou chaîne séparée par des virgules).
   * - ``idnatmut``
     - str \| liste de str
     - ``None``
     - Code(s) de nature de mutation (liste ou chaîne séparée par des virgules).
   * - ``sbati_min``
     - float
     - ``None``
     - Surface bâtie minimale (m²).
   * - ``sbati_max``
     - float
     - ``None``
     - Surface bâtie maximale (m²).
   * - ``sterr_min``
     - float
     - ``None``
     - Surface de terrain minimale (m²).
   * - ``sterr_max``
     - float
     - ``None``
     - Surface de terrain maximale (m²).
   * - ``valeurfonc_min``
     - float
     - ``None``
     - Valeur foncière minimale (€).
   * - ``valeurfonc_max``
     - float
     - ``None``
     - Valeur foncière maximale (€).
   * - ``vefa``
     - bool \| str
     - ``None``
     - Vente en l'état futur d'achèvement.
   * - ``segmtab``
     - str \| liste de str
     - ``None``
     - Note(s) de segment du terrain à bâtir.

``geomutations``
^^^^^^^^^^^^^^^^

* Endpoint : ``GET /dvf_opendata/geomutations/``
* Renvoie : GeoDataFrame (EPSG:4326), index = identifiant

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les mutations renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``anneemut_min``
     - int \| str
     - ``None``
     - Année de mutation minimale.
   * - ``anneemut_max``
     - int \| str
     - ``None``
     - Année de mutation maximale.
   * - ``anneemut``
     - int \| str
     - ``None``
     - Année de mutation.
   * - ``codtypbien``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie de bien ; les premiers niveaux suffisent (liste ou chaîne séparée par des virgules).
   * - ``idnatmut``
     - str \| liste de str
     - ``None``
     - Code(s) de nature de mutation (liste ou chaîne séparée par des virgules).
   * - ``sbati_min``
     - float
     - ``None``
     - Surface bâtie minimale (m²).
   * - ``sbati_max``
     - float
     - ``None``
     - Surface bâtie maximale (m²).
   * - ``sterr_min``
     - float
     - ``None``
     - Surface de terrain minimale (m²).
   * - ``sterr_max``
     - float
     - ``None``
     - Surface de terrain maximale (m²).
   * - ``valeurfonc_min``
     - float
     - ``None``
     - Valeur foncière minimale (€).
   * - ``valeurfonc_max``
     - float
     - ``None``
     - Valeur foncière maximale (€).
   * - ``vefa``
     - bool \| str
     - ``None``
     - Vente en l'état futur d'achèvement.
   * - ``segmtab``
     - str \| liste de str
     - ``None``
     - Note(s) de segment du terrain à bâtir.

``mutation``
^^^^^^^^^^^^

* Endpoint : ``GET /dvf_opendata/mutations/{idmutation}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``idmutation``
     - int \| str
     - ``requis``
     - Identifiant de la mutation.

Module ``apifoncier.dv3f``
--------------------------

Accès : restreint (jeton).

``mutations``
^^^^^^^^^^^^^

* Endpoint : ``GET /dv3f/mutations/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les mutations renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``anneemut_min``
     - int \| str
     - ``None``
     - Année de mutation minimale.
   * - ``anneemut_max``
     - int \| str
     - ``None``
     - Année de mutation maximale.
   * - ``anneemut``
     - int \| str
     - ``None``
     - Année de mutation.
   * - ``codtypbien``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie de bien ; les premiers niveaux suffisent (liste ou chaîne séparée par des virgules).
   * - ``idnatmut``
     - str \| liste de str
     - ``None``
     - Code(s) de nature de mutation (liste ou chaîne séparée par des virgules).
   * - ``sbati_min``
     - float
     - ``None``
     - Surface bâtie minimale (m²).
   * - ``sbati_max``
     - float
     - ``None``
     - Surface bâtie maximale (m²).
   * - ``sterr_min``
     - float
     - ``None``
     - Surface de terrain minimale (m²).
   * - ``sterr_max``
     - float
     - ``None``
     - Surface de terrain maximale (m²).
   * - ``valeurfonc_min``
     - float
     - ``None``
     - Valeur foncière minimale (€).
   * - ``valeurfonc_max``
     - float
     - ``None``
     - Valeur foncière maximale (€).
   * - ``vefa``
     - bool \| str
     - ``None``
     - Vente en l'état futur d'achèvement.
   * - ``codtypprov``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie du vendeur ; les premiers niveaux suffisent.
   * - ``codtypproa``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie de l'acheteur ; les premiers niveaux suffisent.
   * - ``filtre``
     - str
     - ``None``
     - Code alphanumérique permettant d'exclure des transactions particulières.
   * - ``segmtab``
     - str \| liste de str
     - ``None``
     - Note(s) de segment du terrain à bâtir.

``geomutations``
^^^^^^^^^^^^^^^^

* Endpoint : ``GET /dv3f/geomutations/``
* Renvoie : GeoDataFrame (EPSG:4326), index = identifiant

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les mutations renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``anneemut_min``
     - int \| str
     - ``None``
     - Année de mutation minimale.
   * - ``anneemut_max``
     - int \| str
     - ``None``
     - Année de mutation maximale.
   * - ``anneemut``
     - int \| str
     - ``None``
     - Année de mutation.
   * - ``codtypbien``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie de bien ; les premiers niveaux suffisent (liste ou chaîne séparée par des virgules).
   * - ``idnatmut``
     - str \| liste de str
     - ``None``
     - Code(s) de nature de mutation (liste ou chaîne séparée par des virgules).
   * - ``sbati_min``
     - float
     - ``None``
     - Surface bâtie minimale (m²).
   * - ``sbati_max``
     - float
     - ``None``
     - Surface bâtie maximale (m²).
   * - ``sterr_min``
     - float
     - ``None``
     - Surface de terrain minimale (m²).
   * - ``sterr_max``
     - float
     - ``None``
     - Surface de terrain maximale (m²).
   * - ``valeurfonc_min``
     - float
     - ``None``
     - Valeur foncière minimale (€).
   * - ``valeurfonc_max``
     - float
     - ``None``
     - Valeur foncière maximale (€).
   * - ``vefa``
     - bool \| str
     - ``None``
     - Vente en l'état futur d'achèvement.
   * - ``codtypprov``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie du vendeur ; les premiers niveaux suffisent.
   * - ``codtypproa``
     - str \| liste de str
     - ``None``
     - Code(s) de typologie de l'acheteur ; les premiers niveaux suffisent.
   * - ``filtre``
     - str
     - ``None``
     - Code alphanumérique permettant d'exclure des transactions particulières.
   * - ``segmtab``
     - str \| liste de str
     - ``None``
     - Note(s) de segment du terrain à bâtir.

``mutation``
^^^^^^^^^^^^

* Endpoint : ``GET /dv3f/mutations/{idmutation}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``idmutation``
     - int \| str
     - ``requis``
     - Identifiant de la mutation.

Module ``apifoncier.ff``
------------------------

Accès : restreint (jeton).

``parcelles``
^^^^^^^^^^^^^

* Endpoint : ``GET /ff/parcelles/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les parcelles renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``catpro3``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
   * - ``ctpdl``
     - str
     - ``None``
     - Type de propriété divisée en lots (type de copropriété).
   * - ``dcntarti_min``
     - float
     - ``None``
     - Surface artificialisée minimale de la parcelle (m²).
   * - ``dcntarti_max``
     - float
     - ``None``
     - Surface artificialisée maximale de la parcelle (m²).
   * - ``dcntnaf_min``
     - float
     - ``None``
     - Surface NAF minimale de la parcelle (m²).
   * - ``dcntnaf_max``
     - float
     - ``None``
     - Surface NAF maximale de la parcelle (m²).
   * - ``dcntpa_min``
     - float
     - ``None``
     - Surface minimale de la parcelle (m²).
   * - ``dcntpa_max``
     - float
     - ``None``
     - Surface maximale de la parcelle (m²).
   * - ``idcomtxt``
     - str
     - ``None``
     - Chaîne contenue dans le libellé de la commune.
   * - ``idpar``
     - str \| liste de str
     - ``None``
     - Identifiant(s) de parcelle (liste ou chaîne séparée par des virgules).
   * - ``jannatmin_min``
     - int
     - ``None``
     - Année minimale de construction du local le plus ancien.
   * - ``jannatmin_max``
     - int
     - ``None``
     - Année maximale de construction du local le plus ancien.
   * - ``nlocal_min``
     - int
     - ``None``
     - Nombre minimal de locaux sur la parcelle.
   * - ``nlocal_max``
     - int
     - ``None``
     - Nombre maximal de locaux sur la parcelle.
   * - ``nlogh_min``
     - int
     - ``None``
     - Nombre minimal de logements sur la parcelle.
   * - ``nlogh_max``
     - int
     - ``None``
     - Nombre maximal de logements sur la parcelle.
   * - ``slocal_min``
     - float
     - ``None``
     - Surface minimale des parties d'évaluation (m²).
   * - ``slocal_max``
     - float
     - ``None``
     - Surface maximale des parties d'évaluation (m²).
   * - ``sprincp_min``
     - float
     - ``None``
     - Surface minimale des pièces principales professionnelles (m²).
   * - ``sprincp_max``
     - float
     - ``None``
     - Surface maximale des pièces principales professionnelles (m²).
   * - ``stoth_min``
     - float
     - ``None``
     - Surface minimale des pièces d'habitation (m²).
   * - ``stoth_max``
     - float
     - ``None``
     - Surface maximale des pièces d'habitation (m²).
   * - ``jannathmin_min``
     - int
     - ``None``
     - Obsolète, remplacé par ``jannatmin_min``.
   * - ``jannathmin_max``
     - int
     - ``None``
     - Obsolète, remplacé par ``jannatmin_max``.

``geoparcelles``
^^^^^^^^^^^^^^^^

* Endpoint : ``GET /ff/geoparcelles/``
* Renvoie : GeoDataFrame (EPSG:4326), index = identifiant

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les parcelles renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``catpro3``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
   * - ``ctpdl``
     - str
     - ``None``
     - Type de propriété divisée en lots (type de copropriété).
   * - ``dcntarti_min``
     - float
     - ``None``
     - Surface artificialisée minimale de la parcelle (m²).
   * - ``dcntarti_max``
     - float
     - ``None``
     - Surface artificialisée maximale de la parcelle (m²).
   * - ``dcntnaf_min``
     - float
     - ``None``
     - Surface NAF minimale de la parcelle (m²).
   * - ``dcntnaf_max``
     - float
     - ``None``
     - Surface NAF maximale de la parcelle (m²).
   * - ``dcntpa_min``
     - float
     - ``None``
     - Surface minimale de la parcelle (m²).
   * - ``dcntpa_max``
     - float
     - ``None``
     - Surface maximale de la parcelle (m²).
   * - ``idcomtxt``
     - str
     - ``None``
     - Chaîne contenue dans le libellé de la commune.
   * - ``idpar``
     - str \| liste de str
     - ``None``
     - Identifiant(s) de parcelle (liste ou chaîne séparée par des virgules).
   * - ``jannatmin_min``
     - int
     - ``None``
     - Année minimale de construction du local le plus ancien.
   * - ``jannatmin_max``
     - int
     - ``None``
     - Année maximale de construction du local le plus ancien.
   * - ``nlocal_min``
     - int
     - ``None``
     - Nombre minimal de locaux sur la parcelle.
   * - ``nlocal_max``
     - int
     - ``None``
     - Nombre maximal de locaux sur la parcelle.
   * - ``nlogh_min``
     - int
     - ``None``
     - Nombre minimal de logements sur la parcelle.
   * - ``nlogh_max``
     - int
     - ``None``
     - Nombre maximal de logements sur la parcelle.
   * - ``slocal_min``
     - float
     - ``None``
     - Surface minimale des parties d'évaluation (m²).
   * - ``slocal_max``
     - float
     - ``None``
     - Surface maximale des parties d'évaluation (m²).
   * - ``sprincp_min``
     - float
     - ``None``
     - Surface minimale des pièces principales professionnelles (m²).
   * - ``sprincp_max``
     - float
     - ``None``
     - Surface maximale des pièces principales professionnelles (m²).
   * - ``stoth_min``
     - float
     - ``None``
     - Surface minimale des pièces d'habitation (m²).
   * - ``stoth_max``
     - float
     - ``None``
     - Surface maximale des pièces d'habitation (m²).
   * - ``jannathmin_min``
     - int
     - ``None``
     - Obsolète, remplacé par ``jannatmin_min``.
   * - ``jannathmin_max``
     - int
     - ``None``
     - Obsolète, remplacé par ``jannatmin_max``.

``parcelle``
^^^^^^^^^^^^

* Endpoint : ``GET /ff/parcelles/{idpar}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``idpar``
     - str
     - ``requis``
     - Identifiant de la parcelle.

``tups``
^^^^^^^^

* Endpoint : ``GET /ff/tups/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les TUP renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``catpro3``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
   * - ``idtup``
     - str \| liste de str
     - ``None``
     - Identifiant(s) de TUP (liste ou chaîne séparée par des virgules).
   * - ``typetup``
     - str
     - ``None``
     - Type de TUP (``SIMPLE``, ``PDLMP`` ou ``UF``).

``geotups``
^^^^^^^^^^^

* Endpoint : ``GET /ff/geotups/``
* Renvoie : GeoDataFrame (EPSG:4326), index = identifiant

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux.
   * - ``in_bbox``
     - liste de 4 float
     - ``None``
     - Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 0,02° x 0,02° au plus.
   * - ``lon_lat``
     - liste de 2 float
     - ``None``
     - Point ``[longitude, latitude]`` contenu dans les TUP renvoyées.
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``catpro3``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
   * - ``idtup``
     - str \| liste de str
     - ``None``
     - Identifiant(s) de TUP (liste ou chaîne séparée par des virgules).
   * - ``typetup``
     - str
     - ``None``
     - Type de TUP (``SIMPLE``, ``PDLMP`` ou ``UF``).

``tup``
^^^^^^^

* Endpoint : ``GET /ff/tups/{idtup}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``idtup``
     - str
     - ``requis``
     - Identifiant de la TUP.

``locaux``
^^^^^^^^^^

* Endpoint : ``GET /ff/locaux/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``catpro3``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
   * - ``dteloc``
     - str \| liste de str
     - ``None``
     - Type(s) de local.
   * - ``idpar``
     - str
     - ``None``
     - Identifiant de parcelle.
   * - ``idprocpte``
     - str
     - ``None``
     - Identifiant de compte communal.
   * - ``idsec``
     - str
     - ``None``
     - Identifiant de section cadastrale.
   * - ``locprop``
     - str \| liste de str
     - ``None``
     - Localisation(s) généralisée(s) du propriétaire.
   * - ``loghlls``
     - str
     - ``None``
     - Logement social repéré par exonération.
   * - ``proba_rprs``
     - str \| liste de str
     - ``None``
     - Probabilité(s) de résidence principale ou secondaire.
   * - ``slocal_min``
     - float
     - ``None``
     - Surface minimale des parties d'évaluation (m²).
   * - ``slocal_max``
     - float
     - ``None``
     - Surface maximale des parties d'évaluation (m²).
   * - ``typeact``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de local d'activité ; les premiers niveaux suffisent.

``local``
^^^^^^^^^

* Endpoint : ``GET /ff/locaux/{idlocal}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``idlocal``
     - str
     - ``requis``
     - Identifiant fiscal du local.

``proprios``
^^^^^^^^^^^^

* Endpoint : ``GET /ff/proprios/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
   * - ``fields``
     - str
     - ``None``
     - ``"all"`` pour obtenir tous les champs.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``catpro3``
     - str \| liste de str
     - ``None``
     - Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
   * - ``ccodro``
     - str \| liste de str
     - ``None``
     - Code(s) du droit réel ou particulier.
   * - ``gtoper``
     - str
     - ``None``
     - Indicateur de personne physique ou morale.
   * - ``idprocpte``
     - str
     - ``None``
     - Identifiant de compte communal.
   * - ``locprop``
     - str \| liste de str
     - ``None``
     - Localisation(s) généralisée(s) du propriétaire.
   * - ``typedroit``
     - str
     - ``None``
     - Type de droit : propriétaire ou gestionnaire.

``proprio``
^^^^^^^^^^^

* Endpoint : ``GET /ff/proprios/{idprodroit}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``idprodroit``
     - str
     - ``requis``
     - Identifiant du droit de propriété.

Module ``apifoncier.ind_conso_espace``
--------------------------------------

Accès : libre.

``communes``
^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/conso_espace/communes/{code_insee}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``annee_min``
     - int \| str
     - ``None``
     - Année minimale (incluse).
   * - ``annee_max``
     - int \| str
     - ``None``
     - Année maximale (incluse).

``departements``
^^^^^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/conso_espace/departements/{coddep}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``coddep``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE départementaux (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``annee_min``
     - int \| str
     - ``None``
     - Année minimale (incluse).
   * - ``annee_max``
     - int \| str
     - ``None``
     - Année maximale (incluse).

Module ``apifoncier.ind_prix``
------------------------------

Accès : libre.

``aav``
^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/aav/{periode}/{code_insee}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE des AAV (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``periode``
     - str
     - ``'annuel'``
     - ``"annuel"`` (par défaut) ou ``"triennal"``.

``communes``
^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/communes/{periode}/{code_insee}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``periode``
     - str
     - ``'annuel'``
     - ``"annuel"`` (par défaut) ou ``"triennal"``.

``departements``
^^^^^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/departements/{periode}/{coddep}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``coddep``
     - str \| liste de str
     - ``None``
     - Code(s) des départements (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``periode``
     - str
     - ``'annuel'``
     - ``"annuel"`` (par défaut) ou ``"triennal"``.

``epci``
^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/epci/{periode}/{code_insee}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) SIREN des EPCI (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``periode``
     - str
     - ``'annuel'``
     - ``"annuel"`` (par défaut) ou ``"triennal"``.

``regions``
^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/regions/{periode}/{code_insee}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE des régions (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.
   * - ``periode``
     - str
     - ``'annuel'``
     - ``"annuel"`` (par défaut) ou ``"triennal"``.

Module ``apifoncier.ind_marche``
--------------------------------

Accès : libre.

``prix_volume``
^^^^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/prix/{periode}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``echelle``
     - str
     - ``None``
     - Échelle géographique parmi ``communes``, ``epci``, ``aav``, ``departements``, ``regions`` et ``france`` (requis).
   * - ``code``
     - str \| liste de str
     - ``None``
     - Code(s) des entités géographiques (requis), regroupés par lots de 10 par requête.
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année (année centrale pour la période triennale).
   * - ``periode``
     - str
     - ``'annuel'``
     - ``"annuel"`` (par défaut) ou ``"triennal"``.

``activite``
^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/activite/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``echelle``
     - str
     - ``None``
     - Échelle géographique parmi ``communes``, ``epci``, ``aav``, ``departements``, ``regions`` et ``france`` (requis).
   * - ``code``
     - str \| liste de str
     - ``None``
     - Code(s) des entités géographiques (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année centrale de la période de trois ans.

``accessibilite``
^^^^^^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/accessibilite/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``code``
     - str \| liste de str
     - ``None``
     - Code(s) INSEE des aires d'attraction des villes (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année.

``valorisation``
^^^^^^^^^^^^^^^^

* Endpoint : ``GET /indicateurs/dv3f/valorisation/{echelle}/{code_insee}/``
* Renvoie : DataFrame pandas (ou polars si OUTPUT_FORMAT='polars')

.. list-table::
   :header-rows: 1
   :widths: 20 20 15 45

   * - Paramètre
     - Type
     - Défaut
     - Description
   * - ``echelle``
     - str
     - ``None``
     - ``"aav"`` ou ``"epci"`` (requis).
   * - ``code_insee``
     - str \| liste de str
     - ``None``
     - Code(s) des AAV ou des EPCI (requis).
   * - ``ordering``
     - str
     - ``None``
     - Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
   * - ``annee``
     - int \| str
     - ``None``
     - Année centrale de la période de trois ans.

Configuration
-------------

Paramètres modifiables par :func:`apifoncier.configure` (clés insensibles à la casse).

.. list-table::
   :header-rows: 1

   * - Clé
     - Valeur par défaut
   * - ``BASE_URL``
     - ``'https://apidf-preprod.cerema.fr'``
   * - ``TOKEN``
     - ``None``
   * - ``PROXY``
     - ``None``
   * - ``PROGRESS_BAR``
     - ``True``
   * - ``MAX_ATTEMPTS``
     - ``3``
   * - ``BACKOFF_FACTOR``
     - ``0.5``
   * - ``TIMEOUT``
     - ``15``
   * - ``PAGE_SIZE``
     - ``500``
   * - ``OUTPUT_FORMAT``
     - ``'pandas'``

Variables d'environnement : ``APIFONCIER_TOKEN`` (jeton, utilisé si ``TOKEN`` n'est pas configuré) et ``APIFONCIER_BASE_URL``.

Exceptions
----------

.. list-table::
   :header-rows: 1

   * - Exception
     - Hérite de
     - Signification
   * - ``ApiFoncierError``
     - ``Exception``
     - Exception de base du module ``apifoncier``.
   * - ``ValidationError``
     - ``ApiFoncierError, ValueError``
     - Paramètre d'appel invalide, détecté avant toute requête réseau.
   * - ``ApiDFError``
     - ``ApiFoncierError``
     - Erreur renvoyée par l'API Données foncières (code HTTP différent de 200).
   * - ``AuthenticationError``
     - ``ApiDFError``
     - Jeton absent, invalide ou insuffisant pour la ressource demandée (401/403).
   * - ``TokenNotConfigured``
     - ``ApiFoncierError``
     - Un endpoint à accès restreint est appelé sans jeton configuré.
   * - ``InsecureTransportError``
     - ``ApiFoncierError``
     - Refus d'envoyer le jeton d'authentification sur une connexion non chiffrée.
