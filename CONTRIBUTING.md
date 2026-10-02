# Contribuer à apifoncier

## Mise en place

Le projet utilise [uv](https://docs.astral.sh/uv/) pour gérer l'environnement. Après avoir cloné le dépôt, l'installation des dépendances de développement tient en une commande :

```bash
uv sync --group dev
```

Le paquet requiert Python 3.9 ou une version ultérieure. Un fichier `.pre-commit-config.yaml` est fourni pour exécuter ruff et quelques contrôles de base avant chaque commit :

```bash
uv tool install pre-commit
pre-commit install
```

## Commandes courantes

```bash
uv run pytest                   # tests hors ligne
uv run ruff check .             # analyse statique
uv run ruff format .            # mise en forme
uv run mypy                     # vérification des types
```

La documentation se construit avec le groupe de dépendances dédié. Pandoc doit être installé sur le système pour convertir les notebooks.

```bash
uv sync --group docs
uv run sphinx-build -b html docs docs/_build/html
```

## Tests

Par défaut, la suite de tests s'exécute entièrement hors ligne : les réponses de l'API sont simulées avec la bibliothèque `responses`. Les endpoints à accès restreint (Fichiers fonciers, DV3F) sont eux aussi testés de cette manière, avec un jeton fictif. Il est donc possible de contribuer sans disposer d'un jeton réel.

Les tests d'intégration contre l'API réelle ne s'exécutent qu'avec l'option `--run-network` :

```bash
uv run pytest --run-network
```

Ceux qui exigent un jeton sont ignorés si la variable d'environnement `APIFONCIER_TOKEN` n'est pas définie.

## Conventions

Les docstrings suivent le style Google et sont rédigées en français, avec les sections `Args`, `Returns`, `Raises` et, le cas échéant, `Examples`. Les signatures portent des annotations de type, vérifiées par mypy. Le code est mis en forme par ruff.

Les messages de commit respectent la convention des [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/), rédigés en français, par exemple `fix(ff): corriger l'endpoint de tup` ou `docs: réécrire le guide de démarrage`.

## Ajouter un endpoint

L'ajout d'un endpoint se déroule en quatre temps.

1. Écrire la fonction dans le module thématique concerné (`ff.py`, `dv3f.py`, `dvf_opendata.py`, `cartofriches.py`, `ind_conso_espace.py`, `ind_prix.py` ou `ind_marche.py`). Elle construit ses paramètres puis appelle `_query.fetch`, qui se charge de la localisation, de la pagination et de l'assemblage du résultat. Les identifiants destinés à un chemin d'URL passent par `_query.path_segment`, et les endpoints à accès restreint par `use_token=True`.
2. Ajouter un cas paramétré dans `tests/test_endpoints.py`, qui vérifie le chemin interrogé, les paramètres émis et la forme du résultat sur une réponse simulée.
3. Inscrire la fonction et son endpoint dans la liste `CATALOGUE` de `scripts/generer_dictionnaire.py`, puis régénérer `docs/dictionnaire_donnees.rst` avec `uv run python scripts/generer_dictionnaire.py`. Le fichier est produit à partir des signatures et des docstrings, et un test échoue s'il n'est plus à jour.
4. Référencer la fonction dans le fichier `.rst` du module (par exemple `docs/ff.rst`) à l'aide d'une directive `autofunction`.

Pour interroger rapidement un endpoint qui n'a pas encore de fonction dédiée, `apifoncier.get` peut servir de première étape.

## Proposer une modification

Les modifications passent par une pull request. L'intégration continue (GitHub Actions) exécute l'analyse statique, mypy, les tests sur Python 3.9 à 3.13 et la construction du paquet, et construit la documentation. La publication de la documentation sur GitHub Pages n'a lieu que depuis la branche `main`.

Les vulnérabilités ne se signalent pas dans une issue publique : voir [SECURITY.md](SECURITY.md).
