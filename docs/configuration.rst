Configuration et usage avancé
=============================

Cette page décrit les paramètres de configuration globale, le comportement du client
face aux erreurs réseau, la fonction générique :func:`apifoncier.get`, les exceptions
du module, le découpage des grandes emprises, les requêtes parallèles, le cache local, la
journalisation et les garanties de sécurité.

Paramètres
----------

La configuration est partagée par toutes les fonctions du module. Elle se modifie par
:func:`apifoncier.configure`, dont les clés sont insensibles à la casse. Une clé inconnue
ou une valeur invalide lève une :class:`~apifoncier.exceptions.ValidationError`, sous-classe
de ``ValueError``.

.. code-block:: python

    import apifoncier

    apifoncier.configure(timeout=30, page_size=200, progress_bar=False)

    apifoncier.get_config()      # copie de la configuration, jeton masqué
    apifoncier.reset()           # retour aux valeurs par défaut
    apifoncier.close_session()   # fermeture de la session HTTP partagée
    apifoncier.clear_cache()     # vidage du cache HTTP local, s'il est activé

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Clé
     - Rôle
     - Valeur par défaut
   * - ``BASE_URL``
     - URL racine de l'API
     - ``https://apidf-preprod.cerema.fr``
   * - ``TOKEN``
     - Jeton d'accès aux données restreintes
     - ``None``
   * - ``PROXY``
     - URL du proxy HTTP(S)
     - ``None``
   * - ``PROGRESS_BAR``
     - Affichage d'une barre de progression
     - ``True``
   * - ``MAX_ATTEMPTS``
     - Nombre maximal de tentatives par requête
     - ``3``
   * - ``BACKOFF_FACTOR``
     - Facteur de l'attente exponentielle, en secondes
     - ``0.5``
   * - ``TIMEOUT``
     - Délai maximal d'attente d'une réponse, en secondes
     - ``15``
   * - ``PAGE_SIZE``
     - Nombre d'enregistrements demandés par page
     - ``500``
   * - ``OUTPUT_FORMAT``
     - Format des tableaux, ``"pandas"`` ou ``"polars"``
     - ``"pandas"``
   * - ``MAX_TILES``
     - Nombre maximal de tuiles par emprise ``in_bbox``
     - ``100``
   * - ``MAX_WORKERS``
     - Nombre de requêtes exécutées en parallèle
     - ``4``
   * - ``CACHE``
     - Activation du cache HTTP local (extra ``cache``)
     - ``False``
   * - ``CACHE_EXPIRE``
     - Durée de validité des réponses en cache, en secondes
     - ``86400``
   * - ``CACHE_PATH``
     - Fichier SQLite du cache
     - ``None`` (dossier de cache de l'utilisateur)

Variables d'environnement
-------------------------

Deux variables d'environnement sont lues par le module. ``APIFONCIER_TOKEN`` fournit le jeton
lorsque ``TOKEN`` n'a pas été configuré, et ``APIFONCIER_BASE_URL`` remplace l'URL
par défaut de l'API. Un jeton configuré explicitement par ``configure(TOKEN=...)`` l'emporte
sur la variable d'environnement.

.. code-block:: bash

   export APIFONCIER_TOKEN="<jeton>"
   export APIFONCIER_BASE_URL="https://apidf-preprod.cerema.fr"

Il est recommandé de ne jamais écrire le jeton en clair dans un script ou un notebook versionné.
La variable d'environnement évite cet écueil. À défaut, on peut le saisir à l'exécution :

.. code-block:: python

    from getpass import getpass
    import apifoncier

    apifoncier.configure(TOKEN=getpass("Jeton API : "))

Proxy
-----

Le paramètre ``PROXY`` attend une URL HTTP(S) absolue et s'applique aux connexions
``http`` et ``https`` de la session partagée.

.. code-block:: python

    apifoncier.configure(PROXY="http://proxy.exemple.fr:3128")

Nouvelles tentatives
--------------------

Les requêtes partagent une même session HTTP, ce qui permet de réutiliser les connexions.
Les erreurs réseau et les réponses de code 429, 500, 502, 503 et 504 déclenchent de nouvelles
tentatives, séparées par une attente exponentielle réglée par ``BACKOFF_FACTOR``. L'en-tête
``Retry-After`` est respecté lorsque l'API le fournit. ``MAX_ATTEMPTS`` borne le nombre total
de tentatives par requête, la première comprise. Toute modification de la configuration
entraîne la reconstruction de la session à la requête suivante.

.. code-block:: python

    apifoncier.configure(MAX_ATTEMPTS=5, BACKOFF_FACTOR=1.0, TIMEOUT=30)

Format polars
-------------

Avec ``OUTPUT_FORMAT="polars"``, les fonctions renvoient des ``DataFrame`` polars au lieu
de ``DataFrame`` pandas. Le paquet polars doit être installé, par exemple avec
``pip install "apifoncier[polars]"``. Dans le cas contraire, une ``ImportError`` indique
la commande à exécuter. Les fonctions ``geo*`` ne sont pas concernées : elles renvoient toujours
un ``GeoDataFrame`` en EPSG:4326, indexé par l'identifiant des entités, y compris lorsqu'il est vide.
Le format peut aussi être choisi appel par appel (voir plus bas).

.. code-block:: python

    apifoncier.configure(OUTPUT_FORMAT="polars")

Grandes emprises
----------------

L'API limite la taille de l'emprise ``in_bbox`` d'une requête : 0,02° de côté pour les Fichiers
fonciers, DVF+ et DV3F, 1° pour Cartofriches. Une emprise plus grande est découpée
automatiquement en tuiles de cette taille maximale. Chaque tuile fait l'objet d'une requête, puis
les enregistrements strictement identiques renvoyés par plusieurs tuiles sont dédoublonnés. Le nombre
de tuiles est plafonné par ``MAX_TILES`` : au-delà, une
:class:`~apifoncier.exceptions.ValidationError` invite à réduire l'emprise ou à relever ce
plafond. Avec :func:`apifoncier.get`, le paramètre ``max_bbox=None`` supprime tout découpage.

.. code-block:: python

    import apifoncier
    import apifoncier.dvf_opendata as dvf

    # 0,06° x 0,04° : six tuiles de 0,02° au plus
    gdf = dvf.geomutations(in_bbox=[3.04, 50.62, 3.10, 50.66], anneemut=2022)

    apifoncier.configure(MAX_TILES=400)  # relève le plafond de tuiles

Requêtes parallèles
-------------------

Lorsqu'un appel produit plusieurs requêtes (plusieurs départements, codes INSEE répartis en lots de 10,
codes insérés dans le chemin, tuiles d'une emprise), celles-ci s'exécutent en parallèle sur
``MAX_WORKERS`` threads. Les résultats sont assemblés dans l'ordre du plan de requêtes, quel que soit l'ordre
d'arrivée des réponses. ``MAX_WORKERS=1`` rétablit un fonctionnement en série. Pour un appel à plusieurs requêtes,
la barre de progression compte les requêtes terminées, alors qu'une requête unique affiche la progression par enregistrement.

.. code-block:: python

    apifoncier.configure(MAX_WORKERS=8)   # davantage de requêtes simultanées
    apifoncier.configure(MAX_WORKERS=1)   # exécution en série

Cache local
-----------

Un cache HTTP local, facultatif, évite de répéter des requêtes identiques. Il repose sur le paquet
``requests-cache``, installé avec ``pip install "apifoncier[cache]"``. Sans ce paquet, l'activation du
cache lève une ``ImportError`` qui indique la commande à exécuter. Les réponses sont stockées dans une base SQLite,
placée dans le dossier de cache de l'utilisateur ou à l'emplacement donné par ``CACHE_PATH``, et restent
valides ``CACHE_EXPIRE`` secondes (24 heures par défaut). Seules les réponses de code 200 aux requêtes GET sont conservées.
:func:`apifoncier.clear_cache` vide le cache.

.. code-block:: python

    apifoncier.configure(CACHE=True, CACHE_EXPIRE=3600)

    df = dvf.mutations(code_insee="59350")   # interroge l'API
    df = dvf.mutations(code_insee="59350")   # relu depuis le cache

    apifoncier.clear_cache()

L'en-tête ``Authorization`` est exclu de la clé de cache et des réponses stockées : le jeton n'est
jamais écrit sur disque. Les données à accès restreint mises en cache le sont en revanche en clair.
Le cache ne doit donc être activé que sur un poste maîtrisé, et vidé après usage.

Pagination et format par appel
------------------------------

Toutes les fonctions de liste acceptent deux options propres au module, qui ne sont pas transmises à l'API.
``paginate=False`` ne récupère que la première page, soit ``PAGE_SIZE`` enregistrements au plus, ce qui
suffit pour un aperçu. ``output`` prend la valeur ``"pandas"``, ``"polars"`` ou ``"dict"`` (liste brute des
enregistrements) et l'emporte sur ``OUTPUT_FORMAT`` pour l'appel considéré. Pour les fonctions ``geo*``,
``output="dict"`` renvoie une FeatureCollection GeoJSON, de la forme
``{"type": "FeatureCollection", "features": [...]}``, et ``output="polars"`` lève une
:class:`~apifoncier.exceptions.ValidationError`. Ces deux options s'appliquent aussi à
:func:`apifoncier.get`.

.. code-block:: python

    apercu = dvf.mutations(code_insee="59350", paginate=False)
    df = dvf.mutations(code_insee="59350", output="polars")
    lignes = dvf.mutations(code_insee="59350", output="dict")
    geojson = dvf.geomutations(in_bbox=[3.04, 50.62, 3.06, 50.64], output="dict")

Fonction générique ``get``
--------------------------

Pour un endpoint qui ne dispose pas encore de fonction dédiée, :func:`apifoncier.get`
applique les mêmes mécanismes que les fonctions thématiques : pagination, nouvelles tentatives,
regroupement des codes INSEE par lots de 10 et contrôle des paramètres de localisation.

.. code-block:: python

    import apifoncier

    df = apifoncier.get("/cartofriches/friches/", code_insee="59350")
    gdf = apifoncier.get("/ff/geotups/", geo=True, use_token=True, code_insee="59350")

.. autofunction:: apifoncier.get

Gestion des erreurs
-------------------

Toutes les exceptions propres au module héritent de ``ApiFoncierError`` et sont importables
depuis ``apifoncier``. Un seul bloc ``except`` suffit donc pour les intercepter, et les sous-classes
permettent de distinguer les cas. ``AuthenticationError`` correspond aux codes HTTP 401 et 403,
et ``ApiDFError`` porte les attributs ``status_code`` et ``detail``.

.. code-block:: python

    import apifoncier
    import apifoncier.ff as ff

    try:
        df = ff.parcelles(code_insee="59646")
    except apifoncier.TokenNotConfigured:
        print("Aucun jeton n'est configuré.")
    except apifoncier.AuthenticationError as exc:
        print(f"Jeton refusé ({exc.status_code}) : {exc.detail}")
    except apifoncier.ApiDFError as exc:
        print(f"Erreur de l'API ({exc.status_code}) : {exc.detail}")
    except apifoncier.ValidationError as exc:
        print(f"Paramètre invalide : {exc}")

Les erreurs réseau persistantes, une fois les tentatives épuisées, remontent sous la forme
d'exceptions de la bibliothèque ``requests``.

.. automodule:: apifoncier.exceptions
   :members:

Journalisation
--------------

Le module journalise ses requêtes avec le logger nommé ``"apifoncier"``. Au niveau ``DEBUG``,
chaque requête GET est tracée avec son URL et ses paramètres. Le jeton n'y figure pas, puisqu'il
voyage dans un en-tête.

.. code-block:: python

    import logging

    logging.basicConfig()
    logging.getLogger("apifoncier").setLevel(logging.DEBUG)

Sécurité
--------

Le jeton n'est transmis qu'aux endpoints à accès restreint (Fichiers fonciers et DV3F). Il
ne part qu'en HTTPS et qu'à destination de l'hôte de ``BASE_URL``, sans quoi une
``InsecureTransportError`` est levée avant tout envoi. Un jeton absent lève ``TokenNotConfigured``.

Les liens de pagination ``next`` renvoyés par l'API sont suivis uniquement s'ils désignent
le même hôte que la requête initiale. Les identifiants insérés dans les chemins d'URL
(``idpar``, ``idmutation``, ``site_id``, codes des indicateurs, etc.) sont limités aux lettres,
chiffres et aux caractères ``+ * _ -``, puis encodés, ce qui exclut la traversée de chemin.
:func:`apifoncier.get_config` masque le jeton. La marche à suivre pour signaler une vulnérabilité figure
dans le fichier ``SECURITY.md`` du dépôt. Le cache local, s'il est activé, ne contient jamais le jeton,
mais il conserve en clair les données à accès restreint déjà téléchargées (voir la section « Cache local »).
