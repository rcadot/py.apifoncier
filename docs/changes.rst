Changements
===========

0.1.0
-----

Sécurité

- Jeton transmis uniquement en HTTPS et vers l'hôte de ``BASE_URL`` ; lecture possible depuis ``APIFONCIER_TOKEN``.
- Liens de pagination vers un autre hôte refusés.
- Identifiants insérés dans les chemins d'URL contrôlés et encodés (protection contre la traversée de chemin).
- Publication de la documentation limitée à la branche ``main`` ; publication PyPI par Trusted Publishing.

Performances

- Session HTTP partagée et réutilisation des connexions.
- Nouvelles tentatives avec attente exponentielle (erreurs réseau, 429, 5xx, ``Retry-After``).
- Codes INSEE regroupés par lots de 10 par requête.
- Paramètres non dupliqués sur les pages suivantes ; assemblage des pages en une seule opération.

Nouveautés

- Fonction générique :func:`apifoncier.get`.
- Sortie polars optionnelle (``OUTPUT_FORMAT="polars"``, extra ``apifoncier[polars]``).
- Paramètres de configuration ``PAGE_SIZE``, ``BACKOFF_FACTOR``, ``OUTPUT_FORMAT`` ; :func:`apifoncier.get_config` masque le jeton.
- Filtre ``segmtab`` pour ``dvf_opendata`` et ``dv3f``.
- Exceptions ``ApiFoncierError``, ``ValidationError``, ``AuthenticationError``, ``InsecureTransportError``.
- Dictionnaire de données généré depuis le code.

Corrections

- ``ff.tup()`` interrogeait ``/ff/parcelles/`` au lieu de ``/ff/tups/``.
- ``ff.parcelles``/``geoparcelles`` : ``jannathmin_*`` renommés ``jannatmin_*`` (anciens noms dépréciés).
- Absence de paramètre de localisation : ``ValidationError`` explicite au lieu d'une ``UnboundLocalError``.
- Erreurs de l'API sans corps JSON correctement remontées.
- ``ind_marche`` : plus de paramètres parasites (``periode``, ``echelle``) dans la requête.
- ``GeoDataFrame`` toujours géoréférencés en EPSG:4326, y compris vides.

Maintenance

- ``pyproject.toml`` (hatchling) et ``uv`` remplacent ``setup.py`` et les fichiers ``requirements``.
- Annotations de type, docstrings Google, ``py.typed`` ; ruff, mypy, pre-commit.
- Tests hors ligne sur réponses simulées (y compris endpoints restreints), tests réseau optionnels.
- CI sur Python 3.9 à 3.13.

0.0.27
------
- Integration indicateurs de marché

0.0.17
------
- Reprise des modules
- Mise en place progressbar
- Reprise documentation

0.0.11
------
Ajout de dvf_opendata

0.0.9
-----

Ajout de la documentation pour les fonctions.

0.0.8
-----

Modularisation des fonctions.