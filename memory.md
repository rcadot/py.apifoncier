# memory.md : points à retenir pour reprendre le travail

Dernière mise à jour : 2026-10-01 (refonte 0.1.0, branche `claude/wonderful-tesla-879wks`).

## Architecture

- `apifoncier/_http.py` : session `requests` partagée (reconstruite quand `config.generation()` change),
  `Retry` urllib3 (`MAX_ATTEMPTS - 1` nouvelles tentatives, 429/5xx, `BACKOFF_FACTOR`),
  contrôles du jeton (`_auth_headers`), conversion des erreurs, `iter_pages`.
- `apifoncier/_query.py` : `build_requests` (localisation, lots de 10 codes, `path_code`),
  `collect` (pages + barre tqdm), `to_table` (pandas/polars), `to_geodataframe` (EPSG:4326), `fetch`, `fetch_one`.
- Modules thématiques : simples fonctions typées qui appellent `fetch(endpoint, dict(locals()), ...)`.
  Attention : `params = dict(locals())` doit rester la PREMIÈRE instruction de la fonction.
- `apifoncier/utils.py` : façade de compatibilité (`Resultat`, `get_all_data`, `get_all_geodata`,
  `get_api_response`, `is_num`). Ne pas supprimer sans version majeure.
- `scripts/generer_dictionnaire.py` génère `docs/dictionnaire_donnees.rst` ; un test échoue s'il est obsolète.

## Contraintes d'environnement rencontrées

- Le proxy de l'environnement cloud bloque `apidf-preprod.cerema.fr` et `apidf.cerema.fr` (403 CONNECT) :
  aucun appel réel n'a pu être fait ; le schéma OpenAPI (`/swagger/`) n'a pas pu être lu.
- Pas de jeton : les endpoints restreints (FF, DV3F) sont testés uniquement sur réponses simulées
  (`responses`) avec un jeton fictif. Tests réels : `uv run pytest --run-network` (+ `APIFONCIER_TOKEN`).

## Sources utilisées pour les noms d'endpoints et de paramètres

- Client officiel CEREMA/apifoncier (github.com/CEREMA/apifoncier, commit b7c83ba, 2025-11-19).
- Paquet R rcadot/r.apifoncier.
- Ces deux sources concordent sur : `jannatmin_min/max` (et non `jannathmin`), `segmtab` (DV3F ;
  DVF+ seulement dans le paquet R), `/ff/tups/{idtup}`, `code_insee` multiple (max 10, séparés par virgule),
  emprise max 0,02° (FF, DVF+, DV3F) et 1° (Cartofriches).

## Hypothèses à vérifier sur l'API réelle (quand l'accès sera possible)

1. `code_insee=a,b,c` accepté par tous les endpoints de liste (lots de 10). Si faux : remettre
   une requête par code dans `build_requests` (branche `coddep`).
2. `segmtab` réellement filtrant sur `/dvf_opendata/`.
3. Les liens `next` sont parfois en `http://` derrière le mandataire : on force le schéma initial.
4. `page_size=500` accepté sur les endpoints à code dans le chemin (indicateurs).
5. Valeurs exactes d'`echelle` (`france` : quel `code` ?).

## Conventions

- Commits : conventional commits en français, sans mention de l'outil.
- Docstrings Google en français, annotations de type, Python >= 3.9.
- `uv sync --group dev` ; `uv run ruff check . && uv run ruff format --check . && uv run mypy && uv run pytest`.
