Configuration et usage avancé
=============================

Cette page décrit les paramètres de configuration globale, le comportement du client
face aux erreurs réseau, la fonction générique :func:`apifoncier.get`, les exceptions
du module, la journalisation et les garanties de sécurité.

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

.. code-block:: python

    apifoncier.configure(OUTPUT_FORMAT="polars")

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
dans le fichier ``SECURITY.md`` du dépôt.
